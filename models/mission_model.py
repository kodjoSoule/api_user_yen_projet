"""
Modele de donnees pour les missions
"""

import uuid
from datetime import datetime
from typing import List
from dto.mission import AddressDto, WorkDayDto, MissionTypeDto


class MissionModel:
    """Modele representant une mission"""

    def __init__(
        self,
        title: str,
        description: str,
        type_code: str,
        location: AddressDto,
        budget: float,
        publisher_id: str,
        work_days: List[WorkDayDto],
        mission_id: str = None,
        status: str = "DRAFT",
        worker_id: str = None,
        created_at: str = None,
        updated_at: str = None
    ):
        self.id = mission_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.type_code = type_code
        self.location = location
        self.budget = budget
        self.publisher_id = publisher_id
        self.worker_id = worker_id
        self.status = status
        self.work_days = work_days
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at

    def to_dict(self):
        """Convertit le modele en dictionnaire"""
        result = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type_code": self.type_code,
            "location": self.location.to_dict() if isinstance(self.location, AddressDto) else self.location,
            "budget": float(self.budget),
            "publisher_id": self.publisher_id,
            "status": self.status,
            "work_days": [wd.to_dict() if isinstance(wd, WorkDayDto) else wd for wd in self.work_days],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if self.worker_id:
            result["worker_id"] = self.worker_id
        return result

    @staticmethod
    def from_dict(data: dict) -> 'MissionModel':
        """Cree un modele a partir d'un dictionnaire"""
        location_data = data.get('location', {})
        work_days_data = data.get('work_days', [])

        return MissionModel(
            mission_id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            type_code=data.get('type_code', ''),
            location=AddressDto.from_dict(location_data) if isinstance(location_data, dict) else location_data,
            budget=float(data.get('budget', 0)),
            publisher_id=data.get('publisher_id', ''),
            worker_id=data.get('worker_id'),
            status=data.get('status', 'DRAFT'),
            work_days=[WorkDayDto.from_dict(wd) if isinstance(wd, dict) else wd for wd in work_days_data],
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def publish(self):
        """Passe la mission en statut PUBLISHED"""
        self.status = "PUBLISHED"
        self.updated_at = datetime.utcnow().isoformat()

    def accept(self, user_id: str):
        """Accepte la mission et assigne un travailleur"""
        self.status = "ASSIGNED"
        self.worker_id = user_id
        self.updated_at = datetime.utcnow().isoformat()

    def complete(self):
        """Termine la mission"""
        self.status = "COMPLETED"
        self.updated_at = datetime.utcnow().isoformat()

    def is_owner(self, user_id: str) -> bool:
        """Verifie si l'utilisateur est le proprietaire de la mission"""
        return self.publisher_id == user_id

    def is_worker(self, user_id: str) -> bool:
        """Verifie si l'utilisateur est le travailleur assigne"""
        return hasattr(self, 'worker_id') and self.worker_id == user_id
