"""DTOs de réponse pour le domaine Auth"""
from typing import Optional
from dataclasses import dataclass


@dataclass
class LoginResponse:
    """DTO pour la réponse de connexion"""
    token: str
    user: 'UserResponse'  # Forward reference

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'token': self.token,
            'user': self.user.to_dict()
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
