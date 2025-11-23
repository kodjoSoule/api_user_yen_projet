"""DTOs pour les réponses (Response DTOs)"""
from typing import Optional, Any
from dataclasses import dataclass, field


@dataclass
class ApiResponse:
    """DTO de base pour toutes les réponses de l'API"""
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    errors: Optional[list] = None

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        result = {'success': self.success}
        if self.message is not None:
            result['message'] = self.message
        if self.data is not None:
            result['data'] = self.data
        if self.errors is not None:
            result['errors'] = self.errors
        return result


@dataclass
class UserResponse:
    """DTO pour la réponse utilisateur"""
    user_id: str
    first_name: str
    last_name: str
    birth_date: str
    email: str
    phone_number: str
    user_type: str
    country: str
    address: str
    photo_url: Optional[str] = None
    is_active: bool = False
    is_verified: bool = False
    is_completed: bool = False
    is_deleted: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    last_login: Optional[str] = None
    last_password_change: Optional[str] = None

    @staticmethod
    def from_model(user_model) -> 'UserResponse':
        """Crée un DTO depuis un UserModel"""
        return UserResponse(
            user_id=user_model.user_id,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            birth_date=user_model.birth_date,
            email=user_model.email,
            phone_number=user_model.phone_number,
            user_type=user_model.user_type,
            country=user_model.country,
            address=user_model.address,
            photo_url=user_model.photo_url,
            is_active=user_model.is_active,
            is_verified=user_model.is_verified,
            is_completed=user_model.is_completed,
            is_deleted=user_model.is_deleted,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            last_login=user_model.last_login,
            last_password_change=user_model.last_password_change
        )

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'email': self.email,
            'phone_number': self.phone_number,
            'user_type': self.user_type,
            'country': self.country,
            'address': self.address,
            'photo_url': self.photo_url,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'is_completed': self.is_completed,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_login': self.last_login,
            'last_password_change': self.last_password_change
        }


@dataclass
class LoginResponse:
    """DTO pour la réponse de connexion"""
    token: str
    user: UserResponse

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'token': self.token,
            'user': self.user.to_dict()
        }


@dataclass
class UserListResponse:
    """DTO pour la liste des utilisateurs"""
    users: list[UserResponse] = field(default_factory=list)
    total: int = 0

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'users': [user.to_dict() for user in self.users],
            'total': self.total
        }


@dataclass
class PhotoUploadResponse:
    """DTO pour la réponse d'upload de photo"""
    photo_url: str

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'photo_url': self.photo_url
        }


@dataclass
class ValidationError:
    """DTO pour les erreurs de validation"""
    field: str
    message: str

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'field': self.field,
            'message': self.message
        }
