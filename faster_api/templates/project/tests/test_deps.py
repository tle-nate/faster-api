# type: ignore[reportUnknownVariableType]
"""Tests for dependency functions."""
from types import SimpleNamespace

import app.core.deps as deps
import pytest
from fastapi import HTTPException


def test_get_current_user_invalid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    # verify_token raises HTTPException
    monkeypatch.setattr(deps, 'verify_token', lambda token,
                        exc, token_type: (_ for _ in ()).throw(exc))
    with pytest.raises(HTTPException):
        deps.get_current_user(db=None, token='bad')


def test_get_current_user_missing_sub(monkeypatch: pytest.MonkeyPatch) -> None:
    # verify_token returns no 'sub'
    monkeypatch.setattr(deps, 'verify_token',
                        lambda token, exc, token_type: {})
    with pytest.raises(HTTPException):
        deps.get_current_user(db=None, token='tok')


def test_get_current_user_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    # valid payload but get_user returns None
    payload = {'sub': 'user1'}
    monkeypatch.setattr(deps, 'verify_token', lambda token,
                        exc, token_type: payload)
    monkeypatch.setattr(deps, 'get_user', lambda db, uid: None)
    with pytest.raises(HTTPException):
        deps.get_current_user(db=object(), token='tok')


def test_get_current_user_success(monkeypatch: pytest.MonkeyPatch) -> None:
    # valid payload and get_user returns a user
    user_obj = SimpleNamespace(id='u1')
    payload = {'sub': 'u1'}
    monkeypatch.setattr(deps, 'verify_token', lambda token,
                        exc, token_type: payload)
    monkeypatch.setattr(deps, 'get_user', lambda db, uid: user_obj)
    result = deps.get_current_user(db=object(), token='tok')
    assert result is user_obj
