import json
import os
from typing import List, Optional
from models.user_model import UserModel
from config.settings import DATA_FILE


class UserRepository:
    """Repository pour gérer la persistance des utilisateurs"""

    def __init__(self):
        self.data_file = DATA_FILE
        self._ensure_data_file()

    def _ensure_data_file(self):
        """Crée le fichier de données s'il n'existe pas"""
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _read_data(self) -> List[dict]:
        """Lit les données du fichier JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[dict]):
        """Écrit les données dans le fichier JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def create(self, user: UserModel) -> UserModel:
        """Crée un nouvel utilisateur"""
        users = self._read_data()

        # Génère un ID unique
        import uuid
        user.user_id = str(uuid.uuid4())

        user_dict = user.to_dict(exclude_password=False)
        users.append(user_dict)
        self._write_data(users)

        return user

    def find_all(self) -> List[UserModel]:
        """Récupère tous les utilisateurs"""
        users_data = self._read_data()
        return [UserModel.from_dict(user) for user in users_data]

    def find_by_id(self, user_id: str) -> Optional[UserModel]:
        """Trouve un utilisateur par son ID"""
        users = self._read_data()
        for user_data in users:
            if user_data.get('user_id') == user_id:
                return UserModel.from_dict(user_data)
        return None

    def find_by_email(self, email: str) -> Optional[UserModel]:
        """Trouve un utilisateur par son email"""
        users = self._read_data()
        for user_data in users:
            if user_data.get('email') == email:
                return UserModel.from_dict(user_data)
        return None

    def find_by_phone(self, phone_number: str) -> Optional[UserModel]:
        """Trouve un utilisateur par son numéro de téléphone"""
        users = self._read_data()
        for user_data in users:
            if user_data.get('phone_number') == phone_number:
                return UserModel.from_dict(user_data)
        return None

    def update(self, user_id: str, user: UserModel) -> Optional[UserModel]:
        """Met à jour un utilisateur"""
        users = self._read_data()

        for i, user_data in enumerate(users):
            if user_data.get('user_id') == user_id:
                # Conserve l'ID original
                user.user_id = user_id
                # Met à jour la date de modification
                from datetime import datetime
                user.updated_at = datetime.utcnow().isoformat()

                users[i] = user.to_dict(exclude_password=False)
                self._write_data(users)
                return user

        return None

    def delete(self, user_id: str) -> bool:
        """Supprime un utilisateur (soft delete)"""
        users = self._read_data()

        for i, user_data in enumerate(users):
            if user_data.get('user_id') == user_id:
                users[i]['is_deleted'] = True
                from datetime import datetime
                users[i]['updated_at'] = datetime.utcnow().isoformat()
                self._write_data(users)
                return True

        return False

    def update_photo_url(self, user_id: str, photo_url: str) -> bool:
        """Met à jour l'URL de la photo de profil"""
        users = self._read_data()

        for i, user_data in enumerate(users):
            if user_data.get('user_id') == user_id:
                users[i]['photo_url'] = photo_url
                from datetime import datetime
                users[i]['updated_at'] = datetime.utcnow().isoformat()
                self._write_data(users)
                return True

        return False
