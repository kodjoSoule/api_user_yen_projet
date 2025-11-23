from datetime import datetime
from typing import Optional
from enum import Enum


class UserType(str, Enum):
    """Type d'utilisateur"""
    PARTICULIER = "PARTICULIER"
    ENTREPRISE = "ENTREPRISE"


class UserModel:
    """Modèle représentant un utilisateur"""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: str,
        email: str,
        phone_number: str,
        password: str,
        user_type: str,
        country: str,
        address: str,
        user_id: Optional[str] = None,
        photo_url: Optional[str] = None,
        is_active: bool = False,
        is_verified: bool = False,
        is_completed: bool = False,
        is_deleted: bool = False,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        last_login: Optional[str] = None,
        last_password_change: Optional[str] = None
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.user_type = user_type
        self.country = country
        self.address = address
        self.photo_url = photo_url
        self.is_active = is_active
        self.is_verified = is_verified
        self.is_completed = is_completed
        self.is_deleted = is_deleted
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at
        self.last_login = last_login
        self.last_password_change = last_password_change

    def to_dict(self, exclude_password: bool = True):
        """Convertit l'utilisateur en dictionnaire"""
        user_dict = {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "email": self.email,
            "phone_number": self.phone_number,
            "user_type": self.user_type,
            "country": self.country,
            "address": self.address,
            "photo_url": self.photo_url,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_completed": self.is_completed,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_login": self.last_login,
            "last_password_change": self.last_password_change
        }

        if not exclude_password:
            user_dict["password"] = self.password

        return user_dict

    @staticmethod
    def from_dict(data: dict):
        """Crée un UserModel à partir d'un dictionnaire"""
        return UserModel(**data)


class LoginModel:
    """Modèle pour la connexion"""

    def __init__(
        self,
        password: str,
        email: Optional[str] = None,
        phone_number: Optional[str] = None
    ):
        self.email = email
        self.phone_number = phone_number
        self.password = password

    def to_dict(self):
        """Convertit le modèle de connexion en dictionnaire"""
        return {
            "email": self.email,
            "phone_number": self.phone_number,
            "password": self.password
        }

    @staticmethod
    def from_dict(data: dict):
        """Crée un LoginModel à partir d'un dictionnaire"""
        return LoginModel(**data)
