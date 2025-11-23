"""
Service pour la logique metier des missions
"""

from typing import Optional, List, Tuple
from models.mission_model import MissionModel
from repositories.mission_repository import MissionRepository
from dto.mission import (
    MissionCreateDto,
    MissionDisplayDto,
    MissionFilterDto,
    MissionTypeDto
)


# Types de missions disponibles
MISSION_TYPES = {
    "CLEANING": MissionTypeDto(
        code="CLEANING",
        name="Nettoyage",
        description="Services de nettoyage et entretien"
    ),
    "DELIVERY": MissionTypeDto(
        code="DELIVERY",
        name="Livraison",
        description="Services de livraison et transport"
    ),
    "HANDYMAN": MissionTypeDto(
        code="HANDYMAN",
        name="Bricolage",
        description="Travaux de bricolage et reparations"
    ),
    "GARDENING": MissionTypeDto(
        code="GARDENING",
        name="Jardinage",
        description="Services de jardinage et espaces verts"
    ),
    "TUTORING": MissionTypeDto(
        code="TUTORING",
        name="Cours particuliers",
        description="Enseignement et soutien scolaire"
    ),
    "OTHER": MissionTypeDto(
        code="OTHER",
        name="Autre",
        description="Autres types de missions"
    )
}


class MissionService:
    """Service pour la gestion des missions"""

    def __init__(self, repository: MissionRepository):
        self.repository = repository

    def _get_mission_type(self, type_code: str) -> MissionTypeDto:
        """Recupere le type de mission depuis le code"""
        return MISSION_TYPES.get(type_code, MISSION_TYPES["OTHER"])

    def create_mission(self, data: dict) -> Tuple[bool, str, Optional[MissionDisplayDto]]:
        """
        Cree une nouvelle mission
        Returns: (success, message, mission_display_dto)
        """
        try:
            # Convertir en DTO et valider
            create_dto = MissionCreateDto.from_dict(data)
            is_valid, error_message = create_dto.validate()

            if not is_valid:
                return False, error_message, None

            # Verifier que le type de mission existe
            if create_dto.type_code not in MISSION_TYPES:
                return False, f"Type de mission invalide: {create_dto.type_code}", None

            # Creer le modele
            mission = MissionModel(
                title=create_dto.title,
                description=create_dto.description,
                type_code=create_dto.type_code,
                location=create_dto.location,
                budget=create_dto.budget,
                publisher_id=create_dto.publisher_id,
                work_days=create_dto.work_days,
                status="PUBLISHED" if create_dto.publish else "DRAFT"
            )

            # Sauvegarder
            created_mission = self.repository.create(mission)

            # Creer le DTO de reponse
            mission_type = self._get_mission_type(created_mission.type_code)
            display_dto = MissionDisplayDto(
                id=created_mission.id,
                title=created_mission.title,
                description=created_mission.description,
                type=mission_type,
                location=created_mission.location,
                budget=str(created_mission.budget),
                publisher_id=created_mission.publisher_id,
                status=created_mission.status,
                work_days=created_mission.work_days
            )

            status_msg = "publiee" if create_dto.publish else "creee en brouillon"
            return True, f"Mission {status_msg} avec succes", display_dto

        except Exception as e:
            return False, f"Erreur lors de la creation: {str(e)}", None

    def get_all_missions(self) -> List[MissionDisplayDto]:
        """Recupere toutes les missions"""
        missions = self.repository.find_all()
        display_dtos = []

        for mission in missions:
            mission_type = self._get_mission_type(mission.type_code)
            display_dto = MissionDisplayDto(
                id=mission.id,
                title=mission.title,
                description=mission.description,
                type=mission_type,
                location=mission.location,
                budget=str(mission.budget),
                publisher_id=mission.publisher_id,
                status=mission.status,
                work_days=mission.work_days
            )
            display_dtos.append(display_dto)

        return display_dtos

    def get_mission_by_id(self, mission_id: str) -> Optional[MissionDisplayDto]:
        """Recupere une mission par son ID"""
        mission = self.repository.find_by_id(mission_id)

        if not mission:
            return None

        mission_type = self._get_mission_type(mission.type_code)
        return MissionDisplayDto(
            id=mission.id,
            title=mission.title,
            description=mission.description,
            type=mission_type,
            location=mission.location,
            budget=str(mission.budget),
            publisher_id=mission.publisher_id,
            status=mission.status,
            work_days=mission.work_days
        )

    def get_missions_by_filters(self, filters_data: dict) -> List[MissionDisplayDto]:
        """Recherche des missions avec des filtres"""
        filter_dto = MissionFilterDto.from_dict(filters_data)
        missions = self.repository.find_by_filters(filter_dto)

        display_dtos = []
        for mission in missions:
            mission_type = self._get_mission_type(mission.type_code)
            display_dto = MissionDisplayDto(
                id=mission.id,
                title=mission.title,
                description=mission.description,
                type=mission_type,
                location=mission.location,
                budget=str(mission.budget),
                publisher_id=mission.publisher_id,
                status=mission.status,
                work_days=mission.work_days
            )
            display_dtos.append(display_dto)

        return display_dtos

    def publish_mission(self, mission_id: str, user_id: str) -> Tuple[bool, str, Optional[MissionDisplayDto]]:
        """
        Publie une mission (passe de DRAFT a PUBLISHED)
        Returns: (success, message, mission_display_dto)
        """
        try:
            # Recuperer la mission
            mission = self.repository.find_by_id(mission_id)

            if not mission:
                return False, "Mission non trouvee", None

            # Verifier que l'utilisateur est le proprietaire
            if not mission.is_owner(user_id):
                return False, "Vous n'etes pas autorise a publier cette mission", None

            # Verifier le statut
            if mission.status == "PUBLISHED":
                return False, "Cette mission est deja publiee", None

            if mission.status != "DRAFT":
                return False, f"Impossible de publier une mission avec le statut {mission.status}", None

            # Publier la mission
            mission.publish()

            # Sauvegarder
            updated_mission = self.repository.update(mission)

            # Creer le DTO de reponse
            mission_type = self._get_mission_type(updated_mission.type_code)
            display_dto = MissionDisplayDto(
                id=updated_mission.id,
                title=updated_mission.title,
                description=updated_mission.description,
                type=mission_type,
                location=updated_mission.location,
                budget=str(updated_mission.budget),
                publisher_id=updated_mission.publisher_id,
                status=updated_mission.status,
                work_days=updated_mission.work_days
            )

            return True, "Mission publiee avec succes", display_dto

        except Exception as e:
            return False, f"Erreur lors de la publication: {str(e)}", None

    def accept_mission(self, mission_id: str, user_id: str) -> Tuple[bool, str, Optional[MissionDisplayDto]]:
        """
        Accepte une mission - Un utilisateur devient le travailleur de la mission
        Returns: (success, message, mission_display_dto)
        """
        try:
            # Recuperer la mission
            mission = self.repository.find_by_id(mission_id)

            if not mission:
                return False, "Mission non trouvee", None

            # Verifier que l'utilisateur n'est pas le proprietaire
            if mission.is_owner(user_id):
                return False, "Vous ne pouvez pas accepter votre propre mission", None

            # Verifier le statut - seules les missions PUBLISHED peuvent etre acceptees
            if mission.status != "PUBLISHED":
                return False, f"Cette mission ne peut pas etre acceptee (statut: {mission.status})", None

            # Accepter la mission
            mission.accept(user_id)

            # Sauvegarder
            updated_mission = self.repository.update(mission)

            # Creer le DTO de reponse
            mission_type = self._get_mission_type(updated_mission.type_code)
            display_dto = MissionDisplayDto(
                id=updated_mission.id,
                title=updated_mission.title,
                description=updated_mission.description,
                type=mission_type,
                location=updated_mission.location,
                budget=str(updated_mission.budget),
                publisher_id=updated_mission.publisher_id,
                status=updated_mission.status,
                work_days=updated_mission.work_days
            )

            return True, "Mission acceptee avec succes", display_dto

        except Exception as e:
            return False, f"Erreur lors de l'acceptation: {str(e)}", None

    def complete_mission(self, mission_id: str, user_id: str) -> Tuple[bool, str, Optional[MissionDisplayDto]]:
        """
        Termine une mission - Peut etre fait par le proprietaire ou le travailleur
        Returns: (success, message, mission_display_dto)
        """
        try:
            # Recuperer la mission
            mission = self.repository.find_by_id(mission_id)

            if not mission:
                return False, "Mission non trouvee", None

            # Verifier que l'utilisateur est autorise (proprietaire ou travailleur)
            is_owner = mission.is_owner(user_id)
            is_worker = mission.is_worker(user_id)

            if not is_owner and not is_worker:
                return False, "Vous n'etes pas autorise a terminer cette mission", None

            # Verifier le statut - seules les missions ASSIGNED peuvent etre terminees
            if mission.status != "ASSIGNED":
                return False, f"Cette mission ne peut pas etre terminee (statut: {mission.status})", None

            # Terminer la mission
            mission.complete()

            # Sauvegarder
            updated_mission = self.repository.update(mission)

            # Creer le DTO de reponse
            mission_type = self._get_mission_type(updated_mission.type_code)
            display_dto = MissionDisplayDto(
                id=updated_mission.id,
                title=updated_mission.title,
                description=updated_mission.description,
                type=mission_type,
                location=updated_mission.location,
                budget=str(updated_mission.budget),
                publisher_id=updated_mission.publisher_id,
                status=updated_mission.status,
                work_days=updated_mission.work_days
            )

            return True, "Mission terminee avec succes", display_dto

        except Exception as e:
            return False, f"Erreur lors de la completion: {str(e)}", None
