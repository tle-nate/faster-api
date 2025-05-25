"""Authentication Exceptions"""
from fastapi import HTTPException, status


class InvalidTokenPayloadException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(status_code=status_code, detail=detail)
