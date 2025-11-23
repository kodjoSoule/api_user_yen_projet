"""DTOs de requête pour le domaine User"""
from typing import Optional
from dataclasses import dataclass


@dataclass
class CreateUserRequest:
    """DTO pour la création d'un utilisateur"""
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
    def from_dict(data: dict) -> 'CreateUserRequest':
        """Crée un DTO depuis un dictionnaire"""
        return CreateUserRequest(
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


@dataclass
class UpdateUserRequest:
    """DTO pour la mise à jour d'un utilisateur"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    user_type: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    photo_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_completed: Optional[bool] = None

    @staticmethod
    def from_dict(data: dict) -> 'UpdateUserRequest':
        """Crée un DTO depuis un dictionnaire"""
        return UpdateUserRequest(
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
            is_active=data.get('is_active'),
            is_verified=data.get('is_verified'),
            is_completed=data.get('is_completed')
        )

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire (seulement les champs non None)"""
        result = {}
        if self.first_name is not None:
            result['first_name'] = self.first_name
        if self.last_name is not None:
            result['last_name'] = self.last_name
        if self.birth_date is not None:
            result['birth_date'] = self.birth_date
        if self.email is not None:
            result['email'] = self.email
        if self.phone_number is not None:
            result['phone_number'] = self.phone_number
        if self.password is not None:
            result['password'] = self.password
        if self.user_type is not None:
            result['user_type'] = self.user_type
        if self.country is not None:
            result['country'] = self.country
        if self.address is not None:
            result['address'] = self.address
        if self.photo_url is not None:
            result['photo_url'] = self.photo_url
        if self.is_active is not None:
            result['is_active'] = self.is_active
        if self.is_verified is not None:
            result['is_verified'] = self.is_verified
        if self.is_completed is not None:
            result['is_completed'] = self.is_completed
        return result

    def validate(self) -> tuple[bool, Optional[str]]:
        """Valide les données du DTO"""
        if self.user_type is not None and self.user_type not in ['PARTICULIER', 'ENTREPRISE']:
            return False, "Le type d'utilisateur doit être PARTICULIER ou ENTREPRISE"
        return True, None


@dataclass
class UploadPhotoRequest:
    """DTO pour l'upload de photo"""
    user_id: str

    @staticmethod
    def from_form(form_data) -> 'UploadPhotoRequest':
        """Crée un DTO depuis les données de formulaire"""
        return UploadPhotoRequest(
            user_id=form_data.get('user_id')
        )

    def validate(self) -> tuple[bool, Optional[str]]:
        """Valide les données du DTO"""
        if not self.user_id or not self.user_id.strip():
            return False, "L'ID utilisateur est requis"
        return True, None
