# type: ignore
import argparse
import getpass
import os
import subprocess
import sys
import uuid
from pathlib import Path

from pydantic import ValidationError as PydanticValidationError
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

import faster_api.messages as messages

console = Console()

sys.path.insert(0, os.getcwd())


def main():
    parser = argparse.ArgumentParser(prog="fasterapi")
    subparsers = parser.add_subparsers(dest="command")

    # Start a new Project
    project_parser = subparsers.add_parser(
        "startproject", help="Start a new project in the current directory")
    project_parser.add_argument("name", help="Project name")
    project_parser.add_argument("--db_port", type=int, default=5432,
                                help="The port to run the (optional) local PostgreSQL server on.")

    # Start a new App
    app_parser = subparsers.add_parser(
        "startapp", help="Start a new app in the current directory")
    app_parser.add_argument("name", help="App name")

    # Run the local development server
    runserver_parser = subparsers.add_parser(
        "runserver", help="Run the local development server")
    runserver_parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    runserver_parser.add_argument(
        "--port", type=int, default=8080, help="Port to bind (default: 8080)")

    # Database migrations
    makemigrations_parser = subparsers.add_parser(
        "makemigrations", help="Create new alembic migration")
    migrate_parser = subparsers.add_parser(
        "migrate", help="Apply alembic migrations")

    # Local Development DB Controls
    dbup_parser = subparsers.add_parser(
        "dbup", help="Start the optional local development database container")
    dbdown_parser = subparsers.add_parser(
        "dbdown", help="Stop the database container")
    dbreset_parser = subparsers.add_parser(
        "dbreset", help="Deletes the local development database container and volume from docker")

    createsuperuser_parser = subparsers.add_parser(
        "createsuperuser", help="Interactive command to create a new superuser in the database.")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return
    if args.command == "startproject":
        console.print(
            f"[bold green]Setting up your FastAPI project...[/bold green]")
        copy_template(Path(__file__).parent / "templates/project", ".", args.name, {
            "<<PROJECT_NAME>>": args.name,
            "<<DB_PORT>>": args.db_port
        })
        console.print(Panel(messages.SUCCESSFUL_PROJECT_CREATION.format(
            project_name=args.name), title="[bold green]Success[/bold green]"))

    elif args.command == "startapp":
        console.print(
            f"[bold green]Creating new app:[/bold green] {args.name}")
        copy_template(Path(__file__).parent / "templates/app",
                      "app", args.name, {"<<APP_NAME>>": args.name})
        console.print(Panel(messages.SUCCESSFUL_APP_CREATION.format(
            app_name=args.name), title="[bold green]Success[/bold green]"))

    elif args.command == "runserver":
        cmd = [
            "uvicorn",
            "app.main:app",
            "--host", args.host,
            "--port", str(args.port),
            "--reload",
        ]
        console.print(
            f"[bold cyan]Running server:[/bold cyan] {' '.join(cmd)}")
        subprocess.run(cmd, cwd=os.getcwd(), check=True)

    elif args.command == "makemigrations":
        cmd = ["alembic", "revision",
               "--autogenerate", "-m", str(uuid.uuid4())]
        console.print(
            f"[bold cyan]Creating migration:[/bold cyan] {' '.join(cmd)}")
        subprocess.run(cmd, cwd=os.getcwd(), check=True)

    elif args.command == "migrate":
        cmd = ["alembic", "upgrade", "head"]
        console.print(
            f"[bold cyan]Applying migrations:[/bold cyan] {' '.join(cmd)}")
        subprocess.run(cmd, cwd=os.getcwd(), check=True)

    elif args.command == "dbup":
        console.print(
            "[bold cyan]Starting database with docker-compose up -d[/bold cyan]")
        subprocess.run(["docker-compose", "up", "-d"],
                       cwd=os.getcwd(), check=True)

    elif args.command == "dbdown":
        console.print(
            "[bold cyan]Stopping database with docker-compose down[/bold cyan]")
        subprocess.run(["docker-compose", "down"], cwd=os.getcwd(), check=True)

    elif args.command == "dbreset":
        confirm = Confirm.ask(
            "[bold red]Are you sure you want to completely remove all database containers and volumes? This cannot be undone![/bold red]")
        if confirm:
            console.print(
                "[bold red]Stopping and removing database containers and volumes[/bold red]")
            subprocess.run(["docker-compose", "down", "-v"],
                           cwd=os.getcwd(), check=True)
        else:
            console.print("[bold yellow]Aborted dbreset.[/bold yellow]")

    elif args.command == "createsuperuser":
        console.print("[bold green]Creating superuser...[/bold green]")
        handle_createsuperuser()


def copy_template(template_dir, dest_root, name, text_replacements=None):
    if text_replacements is None:
        text_replacements = {"<<PROJECT_NAME>>": name}

    root_target = Path(dest_root) / name

    for root, dirs, files in os.walk(template_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        rel_path = Path(root).relative_to(template_dir)
        target_root = Path(dest_root) / name / rel_path
        target_root.mkdir(parents=True, exist_ok=True)

        for file in files:
            src_file = Path(root) / file
            dst_file = target_root / file

            try:
                with open(src_file, "r", encoding="utf-8") as f:
                    content = f.read()
                for placeholder, replacement_text in text_replacements.items():
                    content = content.replace(
                        placeholder, str(replacement_text))
                with open(dst_file, "w", encoding="utf-8") as f:
                    f.write(content)
            except UnicodeDecodeError:
                console.print(
                    f"[yellow]Skipping binary file:[/yellow] {src_file}")


"""These functions only work after a project has been started in the current directory. """
try:
    from app.auth.crud import create_superuser
    from app.core.db.session import SessionLocal

    def handle_createsuperuser():
        db = SessionLocal()

        try:
            email = Prompt.ask("Email").strip()
            name = Prompt.ask("Name").strip()
            while True:
                password = getpass.getpass("Password: ")
                password_confirm = getpass.getpass("Confirm Password: ")
                if password == password_confirm:
                    break
                console.print(
                    "[red]Passwords do not match. Please try again.[/red]")

            user = create_superuser(
                db, name=name, email=email, password=password)
            console.print(
                f"[bold green]Superuser {user.email} created successfully.[/bold green]")
        finally:
            db.close()

except PydanticValidationError as e:
    if (
        len(e.errors()) == 1 and
        e.errors()[0].get("loc") == ("database_url",)
    ):
        console.print(
            "[red]Failed: DATABASE_URL is missing from FastAPI app.core.config.settings[/red]")
        console.print(
            "[yellow bold]Reminder: Configure your .env file or set the DATABASE_URL environment variable.[/yellow bold]")
        exit()
    raise
except ModuleNotFoundError:
    def handle_createsuperuser():
        console.print(
            "[red]Superuser creation requires a project context.[/red]")
        pass


if __name__ == "__main__":
    main()
