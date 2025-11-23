from flask import Flask, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
from controllers.user_controller import user_bp, inject as inject_user
from controllers.auth_controller import auth_bp, inject as inject_auth
from controllers.mission_controller import mission_bp, inject as inject_mission
from repositories.user_repository import UserRepository
from repositories.mission_repository import MissionRepository
from services.user_service import UserService
from services.mission_service import MissionService
from config.settings import SWAGGER_INFO, UPLOAD_FOLDER, MISSIONS_DATA_FILE

app = Flask(__name__)
CORS(app)

# Configuration Swagger
swagger_template = {
    "swagger": "2.0",
    "info": SWAGGER_INFO,
    "basePath": "/",
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}

swagger_config = {
    "specs": [{
        "endpoint": "apispec",
        "route": "/apispec.json"
    }],
    "swagger_ui": True,
    "specs_route": "/docs/",
    "headers": [],
    "static_url_path": "/flasgger_static",
    "swagger_ui_bundle_js": "//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js",
    "swagger_ui_standalone_preset_js": "//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js",
    "swagger_ui_css": "//unpkg.com/swagger-ui-dist@3/swagger-ui.css"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Injection de dépendances
user_repo = UserRepository()
user_service = UserService(user_repo)
inject_user(user_service)
inject_auth(user_service)

mission_repo = MissionRepository(MISSIONS_DATA_FILE)
mission_service = MissionService(mission_repo)
inject_mission(mission_service)

# Enregistrement des blueprints
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(auth_bp, url_prefix="/auth")

# Enregistrer le blueprint missions avec deux préfixes pour compatibilité
app.register_blueprint(mission_bp, url_prefix="/api/missions")

# Créer un blueprint alias pour /missions (sans /api)
from controllers.mission_controller import create_mission_blueprint_alias
mission_alias_bp = create_mission_blueprint_alias(mission_service)
app.register_blueprint(mission_alias_bp, url_prefix="/missions")


# Route pour servir les fichiers uploadés
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Sert les fichiers uploadés"""
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/')
def index():
    """Page d'accueil de l'API"""
    return {
        "message": "EQOS Microservices API",
        "version": "0.1.0",
        "services": {
            "users": "/users",
            "auth": "/auth",
            "missions": "/api/missions"
        },
        "documentation": "/docs/"
    }


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
