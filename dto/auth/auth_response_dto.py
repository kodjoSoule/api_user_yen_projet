"""DTOs de réponse pour le domaine Auth"""
from typing import Optional
from dataclasses import dataclass


@dataclass
class LoginResponse:
    """DTO pour la réponse de connexion avec access et refresh tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600  # en secondes (60 minutes par défaut)
    user: Optional['UserResponse'] = None  # Forward reference

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        result = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'token_type': self.token_type,
            'expires_in': self.expires_in
        }
        if self.user:
            result['user'] = self.user.to_dict()
        return result


@dataclass
class RefreshTokenResponse:
    """DTO pour la réponse de rafraîchissement de token"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'access_token': self.access_token,
            'token_type': self.token_type,
            'expires_in': self.expires_in
        }


@dataclass
class RegisterResponse:
    """DTO pour la réponse d'enregistrement"""
    user: 'UserResponse'  # Forward reference
    message: Optional[str] = "Utilisateur créé avec succès"

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        result = {
            'user': self.user.to_dict()
        }
        if self.message:
            result['message'] = self.message
        return result


# Import pour résoudre les forward references
from dto.user.user_response_dto import UserResponse
