"""DTOs de requête pour le domaine Auth"""
from typing import Optional
from dataclasses import dataclass


@dataclass
class LoginRequest:
    """DTO pour la connexion"""
    password: str
    email: Optional[str] = None
    phone_number: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> 'LoginRequest':
        """Crée un DTO depuis un dictionnaire"""
        return LoginRequest(
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            password=data.get('password')
        )

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'email': self.email,
            'phone_number': self.phone_number,
            'password': self.password
        }

    def validate(self) -> tuple[bool, Optional[str]]:
        """Valide les données du DTO"""
        if not self.password or not self.password.strip():
            return False, "Le mot de passe est requis"
        if not self.email and not self.phone_number:
            return False, "L'email ou le numéro de téléphone est requis"
        return True, None


@dataclass
class RegisterRequest:
    """DTO pour l'enregistrement (alias de CreateUserRequest)"""
    first_name: str
    last_name: str
    birth_date: str
    email: str
    phone_number: str
    password: str
    user_type: str
    country: str
    address: str
    photo_url: Optional[str] = None
    is_active: Optional[bool] = False
    is_verified: Optional[bool] = False
    is_completed: Optional[bool] = False

    @staticmethod
    def from_dict(data: dict) -> 'RegisterRequest':
        """Crée un DTO depuis un dictionnaire"""
        return RegisterRequest(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            birth_date=data.get('birth_date'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            password=data.get('password'),
            user_type=data.get('user_type'),
            country=data.get('country'),
            address=data.get('address'),
            photo_url=data.get('photo_url'),
            is_active=data.get('is_active', False),
            is_verified=data.get('is_verified', False),
            is_completed=data.get('is_completed', False)
        )

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'email': self.email,
            'phone_number': self.phone_number,
            'password': self.password,
            'user_type': self.user_type,
            'country': self.country,
            'address': self.address,
            'photo_url': self.photo_url,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'is_completed': self.is_completed
        }

    def validate(self) -> tuple[bool, Optional[str]]:
        """Valide les données du DTO"""
        if not self.first_name or not self.first_name.strip():
            return False, "Le prénom est requis"
        if not self.last_name or not self.last_name.strip():
            return False, "Le nom est requis"
        if not self.birth_date or not self.birth_date.strip():
            return False, "La date de naissance est requise"
        if not self.email or not self.email.strip():
            return False, "L'email est requis"
        if not self.phone_number or not self.phone_number.strip():
            return False, "Le numéro de téléphone est requis"
        if not self.password or not self.password.strip():
            return False, "Le mot de passe est requis"
        if not self.user_type or self.user_type not in ['PARTICULIER', 'ENTREPRISE']:
            return False, "Le type d'utilisateur doit être PARTICULIER ou ENTREPRISE"
        if not self.country or not self.country.strip():
            return False, "Le pays est requis"
        if not self.address or not self.address.strip():
            return False, "L'adresse est requise"
        return True, None
