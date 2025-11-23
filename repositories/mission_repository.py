"""
Repository pour la gestion de la persistance des missions
"""

import json
import os
from typing import List, Optional
from models.mission_model import MissionModel
from dto.mission import MissionFilterDto


class MissionRepository:
    """Repository pour les operations CRUD sur les missions"""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Cree le fichier de donnees s'il n'existe pas"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_missions(self) -> List[dict]:
        """Lit toutes les missions depuis le fichier"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_missions(self, missions: List[dict]):
        """Ecrit les missions dans le fichier"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(missions, f, ensure_ascii=False, indent=2)

    def create(self, mission: MissionModel) -> MissionModel:
        """Cree une nouvelle mission"""
        missions = self._read_missions()
        missions.append(mission.to_dict())
        self._write_missions(missions)
        return mission

    def find_all(self) -> List[MissionModel]:
        """Recupere toutes les missions"""
        missions_data = self._read_missions()
        return [MissionModel.from_dict(m) for m in missions_data]

    def find_by_id(self, mission_id: str) -> Optional[MissionModel]:
        """Trouve une mission par son ID"""
        missions = self._read_missions()
        for mission_data in missions:
            if mission_data.get('id') == mission_id:
                return MissionModel.from_dict(mission_data)
        return None

    def update(self, mission: MissionModel) -> MissionModel:
        """Met a jour une mission existante"""
        missions = self._read_missions()
        for i, m in enumerate(missions):
            if m.get('id') == mission.id:
                missions[i] = mission.to_dict()
                self._write_missions(missions)
                return mission
        raise ValueError(f"Mission avec l'ID {mission.id} non trouvee")

    def find_by_filters(self, filters: MissionFilterDto) -> List[MissionModel]:
        """Trouve des missions selon des filtres"""
        all_missions = self.find_all()
        filtered_missions = []

        for mission in all_missions:
            # Filtre par titre
            if filters.title and filters.title.lower() not in mission.title.lower():
                continue

            # Filtre par type
            if filters.type_code and mission.type_code != filters.type_code:
                continue

            # Filtre par localisation
            if filters.country and mission.location.country != filters.country:
                continue
            if filters.city and mission.location.city != filters.city:
                continue
            if filters.neighborhood and mission.location.neighborhood != filters.neighborhood:
                continue

            # Filtre par budget
            if filters.budget_min is not None and mission.budget < filters.budget_min:
                continue
            if filters.budget_max is not None and mission.budget > filters.budget_max:
                continue

            # Filtre par publisher
            if filters.publisher_id and mission.publisher_id != filters.publisher_id:
                continue

            # Filtre par statut
            if filters.status and mission.status != filters.status:
                continue

            filtered_missions.append(mission)

        return filtered_missions

    def find_by_publisher(self, publisher_id: str) -> List[MissionModel]:
        """Trouve toutes les missions d'un publisher"""
        all_missions = self.find_all()
        return [m for m in all_missions if m.publisher_id == publisher_id]

    def find_by_status(self, status: str) -> List[MissionModel]:
        """Trouve toutes les missions avec un statut donne"""
        all_missions = self.find_all()
        return [m for m in all_missions if m.status == status]
