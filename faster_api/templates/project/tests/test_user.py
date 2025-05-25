"""Tests for user endpoints."""
import pytest
from typing import Any, Dict
from fastapi.testclient import TestClient

def test_my_account_unauthorized(client: TestClient) -> None:
    # Accessing protected endpoint without token should fail
    response = client.get("/api/v1/user/")
    assert response.status_code == 401

def test_my_account_and_user_endpoints(client: TestClient, new_user_data: Dict[str, Any]) -> None:
    # Register user
    client.post("/api/v1/auth/join", json=new_user_data)
    # Login to get access token
    login_resp = client.post(
        "/api/v1/auth/login",
        data={
            "username": new_user_data["email"],
            "password": new_user_data["password"],
        },
    )
    access_token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Get current user info
    me_resp = client.get("/api/v1/user/", headers=headers)
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == new_user_data["email"]
    assert me_data["name"] == new_user_data["name"]

    # Test reading preferences
    prefs_resp = client.get("/api/v1/user/preferences", headers=headers)
    assert prefs_resp.status_code == 200
    prefs_data = prefs_resp.json()
    assert prefs_data.get("user_id") == me_data.get("id")

    # Test reading profile
    profile_resp = client.get("/api/v1/user/profile", headers=headers)
    assert profile_resp.status_code == 200
    profile_data = profile_resp.json()
    assert profile_data.get("user_id") == me_data.get("id")
