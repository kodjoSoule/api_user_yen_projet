"""DTOs (Data Transfer Objects) pour l'API - Organisation par domaine"""
from .common import ApiResponse, ValidationError
from .user import (
    CreateUserRequest,
    UpdateUserRequest,
    UploadPhotoRequest,
    UserResponse,
    UserListResponse,
    PhotoUploadResponse
)
from .auth import (
    LoginRequest,
    RegisterRequest,
    LoginResponse,
    RegisterResponse
)

__all__ = [
    # Common
    'ApiResponse',
    'ValidationError',
    # User
    'CreateUserRequest',
    'UpdateUserRequest',
    'UploadPhotoRequest',
    'UserResponse',
    'UserListResponse',
    'PhotoUploadResponse',
    # Auth
    'LoginRequest',
    'RegisterRequest',
    'LoginResponse',
    'RegisterResponse'
]
