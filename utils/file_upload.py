import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from config.settings import UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename: str) -> bool:
    """Vérifie si le fichier a une extension autorisée"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file: FileStorage) -> tuple[bool, str]:
    """
    Sauvegarde un fichier uploadé
    Returns: (success, filename_or_error_message)
    """
    if not file:
        return False, "Aucun fichier fourni"

    if file.filename == '':
        return False, "Nom de fichier vide"

    if not allowed_file(file.filename):
        return False, f"Extension non autorisée. Utilisez: {', '.join(ALLOWED_EXTENSIONS)}"

    # Génère un nom unique pour le fichier
    original_filename = secure_filename(file.filename)
    file_extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    # Chemin complet du fichier
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        file.save(file_path)
        return True, unique_filename
    except Exception as e:
        return False, f"Erreur lors de la sauvegarde: {str(e)}"


def delete_uploaded_file(filename: str) -> bool:
    """Supprime un fichier uploadé"""
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


def get_file_url(filename: str, base_url: str = "") -> str:
    """Génère l'URL d'accès au fichier"""
    if not filename:
        return None
    return f"{base_url}/uploads/{filename}"
