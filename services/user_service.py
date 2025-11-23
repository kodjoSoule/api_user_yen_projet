from typing import Optional, List
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import UserModel, LoginModel
from repositories.user_repository import UserRepository
from utils.jwt_utils import generate_token
from dto.user import CreateUserRequest, UpdateUserRequest, UserResponse, UserListResponse
from dto.auth import LoginRequest, LoginResponse


class UserService:
    """Service pour la logique métier des utilisateurs"""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, request_dto: CreateUserRequest) -> tuple[bool, str, Optional[UserResponse]]:
        """
        Crée un nouvel utilisateur
        Returns: (success, message, user_response)
        """
        # Validation du DTO
        is_valid, error_message = request_dto.validate()
        if not is_valid:
            return False, error_message, None

        # Vérifie si l'email existe déjà
        existing_user = self.repository.find_by_email(request_dto.email)
        if existing_user:
            return False, "Un utilisateur avec cet email existe déjà", None

        # Vérifie si le téléphone existe déjà
        existing_phone = self.repository.find_by_phone(request_dto.phone_number)
        if existing_phone:
            return False, "Un utilisateur avec ce numéro de téléphone existe déjà", None

        # Prépare les données utilisateur
        user_data = request_dto.to_dict()
        user_data['password'] = generate_password_hash(user_data['password'])
        user_data['last_password_change'] = datetime.utcnow().isoformat()

        # Crée l'utilisateur
        user = UserModel.from_dict(user_data)
        created_user = self.repository.create(user)

        # Convertit en DTO de réponse
        user_response = UserResponse.from_model(created_user)
        return True, "Utilisateur créé avec succès", user_response

    def get_all_users(self) -> UserListResponse:
        """Récupère tous les utilisateurs non supprimés"""
        all_users = self.repository.find_all()
        active_users = [user for user in all_users if not user.is_deleted]
        user_responses = [UserResponse.from_model(user) for user in active_users]
        return UserListResponse(users=user_responses, total=len(user_responses))

    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Récupère un utilisateur par son ID"""
        user = self.repository.find_by_id(user_id)
        if user and not user.is_deleted:
            return UserResponse.from_model(user)
        return None

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Récupère un utilisateur par son email"""
        user = self.repository.find_by_email(email)
        if user and not user.is_deleted:
            return UserResponse.from_model(user)
        return None

    def get_user_by_phone(self, phone_number: str) -> Optional[UserResponse]:
        """Récupère un utilisateur par son numéro de téléphone"""
        user = self.repository.find_by_phone(phone_number)
        if user and not user.is_deleted:
            return UserResponse.from_model(user)
        return None

    def update_user(self, user_id: str, request_dto: UpdateUserRequest) -> tuple[bool, str, Optional[UserResponse]]:
        """
        Met à jour un utilisateur
        Returns: (success, message, user_response)
        """
        # Validation du DTO
        is_valid, error_message = request_dto.validate()
        if not is_valid:
            return False, error_message, None

        existing_user = self.repository.find_by_id(user_id)
        if not existing_user or existing_user.is_deleted:
            return False, "Utilisateur non trouvé", None

        # Prépare les données à mettre à jour
        user_data = request_dto.to_dict()

        # Si le mot de passe est fourni, le hasher
        if 'password' in user_data and user_data['password']:
            user_data['password'] = generate_password_hash(user_data['password'])
            user_data['last_password_change'] = datetime.utcnow().isoformat()
        else:
            # Conserve le mot de passe actuel
            user_data['password'] = existing_user.password

        # Vérifie l'unicité de l'email si modifié
        if 'email' in user_data and user_data['email'] != existing_user.email:
            email_exists = self.repository.find_by_email(user_data['email'])
            if email_exists:
                return False, "Cet email est déjà utilisé", None

        # Vérifie l'unicité du téléphone si modifié
        if 'phone_number' in user_data and user_data['phone_number'] != existing_user.phone_number:
            phone_exists = self.repository.find_by_phone(user_data['phone_number'])
            if phone_exists:
                return False, "Ce numéro de téléphone est déjà utilisé", None

        user = UserModel.from_dict(user_data)
        updated_user = self.repository.update(user_id, user)

        if updated_user:
            user_response = UserResponse.from_model(updated_user)
            return True, "Utilisateur mis à jour avec succès", user_response
        return False, "Erreur lors de la mise à jour", None

    def delete_user(self, user_id: str) -> tuple[bool, str]:
        """
        Supprime un utilisateur (soft delete)
        Returns: (success, message)
        """
        user = self.repository.find_by_id(user_id)
        if not user or user.is_deleted:
            return False, "Utilisateur non trouvé"

        success = self.repository.delete(user_id)
        if success:
            return True, "Utilisateur supprimé avec succès"
        return False, "Erreur lors de la suppression"

    def verify_credentials(self, request_dto: LoginRequest) -> tuple[bool, str, Optional[LoginResponse]]:
        """
        Vérifie les identifiants d'un utilisateur
        Returns: (success, message, login_response)
        """
        # Validation du DTO
        is_valid, error_message = request_dto.validate()
        if not is_valid:
            return False, error_message, None

        # Recherche l'utilisateur
        user = None
        if request_dto.email:
            user = self.repository.find_by_email(request_dto.email)
        elif request_dto.phone_number:
            user = self.repository.find_by_phone(request_dto.phone_number)

        if not user or user.is_deleted:
            return False, "Identifiants incorrects", None

        # Vérifie le mot de passe
        if not check_password_hash(user.password, request_dto.password):
            return False, "Identifiants incorrects", None

        # Met à jour la date de dernière connexion
        user.last_login = datetime.utcnow().isoformat()
        self.repository.update(user.user_id, user)

        # Génère un token JWT
        token = generate_token(user.user_id, user.email)

        # Crée la réponse
        user_response = UserResponse.from_model(user)
        login_response = LoginResponse(token=token, user=user_response)

        return True, "Connexion réussie", login_response

    def update_profile_photo(self, user_id: str, photo_url: str) -> tuple[bool, str]:
        """
        Met à jour l'URL de la photo de profil
        Returns: (success, message)
        """
        user = self.repository.find_by_id(user_id)
        if not user or user.is_deleted:
            return False, "Utilisateur non trouvé"

        success = self.repository.update_photo_url(user_id, photo_url)
        if success:
            return True, "Photo de profil mise à jour avec succès"
        return False, "Erreur lors de la mise à jour de la photo"
