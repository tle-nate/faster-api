"""User endpoints."""
from app.auth.models import User as UserModel
from app.core import deps
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .crud import (get_preferences, get_profile, update_preferences,
                   update_profile)
from .schemas import Preferences, PreferencesCreate, Profile, ProfileCreate
from .schemas import User as UserSchema

router = APIRouter()


# Get User
@router.get("/", response_model=UserSchema)
def my_account(current_user: UserModel = Depends(deps.get_current_user)) -> UserSchema:
    """Get current authenticated user."""
    return current_user


# User Preferences
@router.get("/preferences", response_model=Preferences)
def read_preferences(db: Session = Depends(deps.get_db), current_user: UserModel = Depends(deps.get_current_user)) -> Preferences:
    """Get preferences for the current user."""
    db_prefs = get_preferences(db, user_id=current_user.id)
    if not db_prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return db_prefs


@router.patch("/preferences", response_model=Preferences)
def patch_preferences(prefs_in: PreferencesCreate, db: Session = Depends(deps.get_db), current_user: UserModel = Depends(deps.get_current_user)) -> Preferences:
    """Update preferences for the current user."""
    db_prefs = update_preferences(
        db, user_id=current_user.id, updates=prefs_in.model_dump(exclude_unset=True))
    if not db_prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return db_prefs


# User Profile
@router.get("/profile", response_model=Profile)
def read_profile(db: Session = Depends(deps.get_db), current_user: UserModel = Depends(deps.get_current_user)) -> Profile:
    """Get profile for the current user."""
    db_profile = get_profile(db, user_id=current_user.id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@router.patch("/profile", response_model=Profile)
def patch_profile(profile_in: ProfileCreate, db: Session = Depends(deps.get_db), current_user: UserModel = Depends(deps.get_current_user)) -> Profile:
    """Update profile for the current user."""
    db_profile = update_profile(
        db, user_id=current_user.id, updates=profile_in.model_dump(exclude_unset=True))
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile
