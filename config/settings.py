import os

# Chemins de base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "users.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Crée les dossiers nécessaires
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuration JWT
SECRET_KEY = "dev-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_IN_MINUTES = 60

# Configuration Swagger
SWAGGER_INFO = {
    "title": "Users Microservice",
    "version": "0.1.0",
    "description": "EQOS : Gestion des utilisateurs"
}
