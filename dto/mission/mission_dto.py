"""
DTOs pour les missions
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import date, time


@dataclass
class AddressDto:
    """DTO pour l'adresse d'une mission"""
    country: str
    city: str
    neighborhood: str

    def to_dict(self):
        return {
            "country": self.country,
            "city": self.city,
            "neighborhood": self.neighborhood
        }

    @staticmethod
    def from_dict(data: dict) -> 'AddressDto':
        return AddressDto(
            country=data.get('country', ''),
            city=data.get('city', ''),
            neighborhood=data.get('neighborhood', '')
        )

    def validate(self) -> tuple[bool, str]:
        if not self.country or not self.country.strip():
            return False, "Le pays est requis"
        if not self.city or not self.city.strip():
            return False, "La ville est requise"
        if not self.neighborhood or not self.neighborhood.strip():
            return False, "Le quartier est requis"
        return True, ""


@dataclass
class WorkDayDto:
    """DTO pour un jour de travail"""
    day: str  # Format: YYYY-MM-DD
    start_time: str  # Format: HH:MM:SS
    end_time: str  # Format: HH:MM:SS

    def to_dict(self):
        return {
            "day": self.day,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @staticmethod
    def from_dict(data: dict) -> 'WorkDayDto':
        return WorkDayDto(
            day=data.get('day', ''),
            start_time=data.get('start_time', ''),
            end_time=data.get('end_time', '')
        )

    def validate(self) -> tuple[bool, str]:
        if not self.day:
            return False, "La date du jour est requise"
        if not self.start_time:
            return False, "L'heure de debut est requise"
        if not self.end_time:
            return False, "L'heure de fin est requise"

        # Validation du format de date
        try:
            from datetime import datetime
            datetime.strptime(self.day, '%Y-%m-%d')
        except ValueError:
            return False, "Format de date invalide (attendu: YYYY-MM-DD)"

        # Validation du format de temps
        try:
            datetime.strptime(self.start_time, '%H:%M:%S')
            datetime.strptime(self.end_time, '%H:%M:%S')
        except ValueError:
            return False, "Format d'heure invalide (attendu: HH:MM:SS)"

        return True, ""


@dataclass
class MissionTypeDto:
    """DTO pour le type de mission"""
    code: str
    name: str
    description: str

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description
        }

    @staticmethod
    def from_dict(data: dict) -> 'MissionTypeDto':
        return MissionTypeDto(
            code=data.get('code', ''),
            name=data.get('name', ''),
            description=data.get('description', '')
        )


@dataclass
class MissionCreateDto:
    """DTO pour la creation d'une mission"""
    title: str
    description: str
    type_code: str
    location: AddressDto
    budget: float
    publisher_id: str
    work_days: List[WorkDayDto]
    publish: bool = False

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "type_code": self.type_code,
            "location": self.location.to_dict(),
            "budget": str(self.budget),
            "publisher_id": self.publisher_id,
            "publish": self.publish,
            "work_days": [wd.to_dict() for wd in self.work_days]
        }

    @staticmethod
    def from_dict(data: dict) -> 'MissionCreateDto':
        location_data = data.get('location', {})
        work_days_data = data.get('work_days', [])

        return MissionCreateDto(
            title=data.get('title', ''),
            description=data.get('description', ''),
            type_code=data.get('type_code', ''),
            location=AddressDto.from_dict(location_data),
            budget=float(data.get('budget', 0)),
            publisher_id=data.get('publisher_id', ''),
            publish=data.get('publish', False),
            work_days=[WorkDayDto.from_dict(wd) for wd in work_days_data]
        )

    def validate(self) -> tuple[bool, str]:
        if not self.title or not self.title.strip():
            return False, "Le titre est requis"
        if not self.description or not self.description.strip():
            return False, "La description est requise"
        if not self.type_code or not self.type_code.strip():
            return False, "Le code du type de mission est requis"
        if not self.publisher_id or not self.publisher_id.strip():
            return False, "L'ID du publisher est requis"
        if self.budget <= 0:
            return False, "Le budget doit etre superieur a 0"

        # Valider l'adresse
        is_valid, error_msg = self.location.validate()
        if not is_valid:
            return False, error_msg

        # Valider les jours de travail
        if not self.work_days:
            return False, "Au moins un jour de travail est requis"

        for work_day in self.work_days:
            is_valid, error_msg = work_day.validate()
            if not is_valid:
                return False, error_msg

        return True, ""


@dataclass
class MissionDisplayDto:
    """DTO pour l'affichage d'une mission"""
    id: str
    title: str
    description: str
    type: MissionTypeDto
    location: AddressDto
    budget: str
    publisher_id: str
    status: str
    work_days: List[WorkDayDto]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type.to_dict(),
            "location": self.location.to_dict(),
            "budget": self.budget,
            "publisher_id": self.publisher_id,
            "status": self.status,
            "work_days": [wd.to_dict() for wd in self.work_days]
        }

    @staticmethod
    def from_model(model) -> 'MissionDisplayDto':
        """Convertit un modele Mission en DTO"""
        return MissionDisplayDto(
            id=model.id,
            title=model.title,
            description=model.description,
            type=model.type,
            location=model.location,
            budget=str(model.budget),
            publisher_id=model.publisher_id,
            status=model.status,
            work_days=model.work_days
        )


@dataclass
class MissionFilterDto:
    """DTO pour filtrer les missions"""
    title: Optional[str] = None
    type_code: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    publisher_id: Optional[str] = None
    status: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> 'MissionFilterDto':
        return MissionFilterDto(
            title=data.get('title'),
            type_code=data.get('type_code'),
            country=data.get('country'),
            city=data.get('city'),
            neighborhood=data.get('neighborhood'),
            budget_min=float(data['budget_min']) if data.get('budget_min') else None,
            budget_max=float(data['budget_max']) if data.get('budget_max') else None,
            publisher_id=data.get('publisher_id'),
            status=data.get('status')
        )
