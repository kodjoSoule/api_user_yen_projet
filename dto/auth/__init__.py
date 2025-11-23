"""DTOs pour le domaine Auth"""
from .auth_request_dto import LoginRequest, RegisterRequest
from .auth_response_dto import LoginResponse, RegisterResponse

__all__ = [
    'LoginRequest',
    'RegisterRequest',
    'LoginResponse',
    'RegisterResponse'
]
