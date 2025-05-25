from rich.markdown import Markdown

SUCCESSFUL_PROJECT_CREATION = """
# Your project was [bold green]successfully created[/bold green]! 

Next steps:

    1. Navigate to the project root:

        [bold cyan]> cd {project_name}[/bold cyan]
    
    2. Configure your .env file:

        [bold cyan]> cp .env.example .env[/bold cyan]

    3. (Optional) Start the development PostgreSQL server:

        [bold cyan]> fasterapi dbup[/bold cyan]    

    4. Run the database migrations:

        [bold cyan]> fasterapi makemigrations; fasterapi migrate[/bold cyan]

    5. Start the app:

        [bold cyan]> fasterapi runserver[/bold cyan]
"""

SUCCESSFUL_APP_CREATION = """
# Your app was [bold green]successfully created[/bold green]! Next steps:

1. Add your models file to ensure they're picked up for migrations:

   `/alembic/env.py`  
   [bold yellow]+ import app.{app_name}.models[/bold yellow]

2. Add your views to the router:

   `/app/core/routers/v1.py`  
   [bold yellow]+ from app.{app_name} import views as {app_name}_views[/bold yellow]  
   ...  
   [bold yellow]+ api_router.include_router({app_name}_views.router, prefix="/{app_name}", tags=["{app_name}"])[/bold yellow]
"""
