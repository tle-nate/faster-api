"""Tests for user CRUD operations."""
from typing import Any

import pytest
from app.user.crud import (create_preferences, create_profile, get_preferences,
                           get_profile, update_preferences, update_profile)
from sqlalchemy.orm import Session


def test_preferences_crud(db_session: Session, test_user: Any) -> None:
    # Initially no preferences exist for the user
    assert get_preferences(db_session, test_user.id) is None
    # Create preferences
    prefs = create_preferences(db_session, {"user_id": test_user.id})
    assert prefs.user_id == test_user.id
    # Retrieve preferences
    fetched = get_preferences(db_session, test_user.id)
    assert fetched
    assert fetched.id == prefs.id
    # Update preferences with empty data (no-op)
    updated = update_preferences(db_session, test_user.id, {})
    assert updated
    assert updated.id == prefs.id
    # Updating non-existent preferences returns None
    assert update_preferences(db_session, "no-such-user", {}) is None


def test_profile_crud(db_session: Session, test_user: Any) -> None:
    # Initially no profile exists for the user
    assert get_profile(db_session, test_user.id) is None
    # Create profile
    profile = create_profile(db_session, {"user_id": test_user.id})
    assert profile.user_id == test_user.id
    # Retrieve profile
    fetched = get_profile(db_session, test_user.id)
    assert fetched
    assert fetched.id == profile.id
    # Update profile field
    updated = update_profile(db_session, test_user.id, {"timezone": "UTC"})
    assert updated
    assert updated.timezone == "UTC"
    # Updating non-existent profile returns None
    assert update_profile(db_session, "no-user", {"timezone": "UTC"}) is None
