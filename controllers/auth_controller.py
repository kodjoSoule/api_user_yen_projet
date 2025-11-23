from flask import Blueprint, request, jsonify
from services.user_service import UserService
from dto.common import ApiResponse
from dto.auth import LoginRequest, RegisterRequest
from dto.user import CreateUserRequest


auth_bp = Blueprint("auth", __name__)
_service: UserService = None


def inject(service: UserService):
    global _service
    _service = service


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authentifie un utilisateur et retourne un token JWT
    ---
    tags:
      - EQOS : Authentification
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - password
          properties:
            email:
              type: string
              description: Email de l'utilisateur
            phone_number:
              type: string
              description: Numéro de téléphone de l'utilisateur
            password:
              type: string
              description: Mot de passe en clair saisi par l'utilisateur
    responses:
      200:
        description: Successful Response
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              type: object
              properties:
                token:
                  type: string
                user:
                  type: object
      401:
        description: Identifiants invalides
      422:
        description: Validation Error
    """
    try:
        # Validation des données de la requête
        data = request.get_json()
        if not data:
            response = ApiResponse(success=False, message="Corps de la requête vide")
            return jsonify(response.to_dict()), 400

        # Création du DTO de requête
        login_request = LoginRequest.from_dict(data)

        # Appel au service
        success, message, login_response = _service.verify_credentials(login_request)

        if success:
            response = ApiResponse(
                success=True,
                message=message,
                data=login_response.to_dict()
            )
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), 401
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@auth_bp.route("/register", methods=["POST"])
def register():
    """Enregistre un nouvel utilisateur
    ---
    tags:
      - EQOS : Authentification
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - first_name
            - last_name
            - birth_date
            - email
            - phone_number
            - password
            - user_type
            - country
            - address
          properties:
            first_name:
              type: string
            last_name:
              type: string
            birth_date:
              type: string
              description: Date de naissance au format AAAA-MM-JJ ou JJ/MM/AAAA
            email:
              type: string
            phone_number:
              type: string
            password:
              type: string
            user_type:
              type: string
              enum: [PARTICULIER, ENTREPRISE]
              description: Rôle de l'utilisateur (ENTREPRISE, PARTICULIER)
            country:
              type: string
            address:
              type: string
            photo_url:
              type: string
              description: URL de la photo de profil
    responses:
      201:
        description: Utilisateur créé avec succès
      400:
        description: Données invalides
      422:
        description: Validation Error
    """
    try:
        # Validation des données de la requête
        data = request.get_json()
        if not data:
            response = ApiResponse(success=False, message="Corps de la requête vide")
            return jsonify(response.to_dict()), 400

        # Création du DTO de requête
        create_user_request = CreateUserRequest.from_dict(data)

        # Appel au service
        success, message, user_response = _service.create_user(create_user_request)

        if success:
            response = ApiResponse(
                success=True,
                message=message,
                data=user_response.to_dict()
            )
            return jsonify(response.to_dict()), 201

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), 400
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@auth_bp.route("/verify-credentials", methods=["POST"])
def verify_credentials():
    """Vérifie les identifiants de l'utilisateur (alias de /login)
    ---
    tags:
      - EQOS : Authentification
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - password
          properties:
            email:
              type: string
              description: Email de l'utilisateur
            phone_number:
              type: string
              description: Numéro de téléphone de l'utilisateur
            password:
              type: string
              description: Mot de passe en clair saisi par l'utilisateur
    responses:
      200:
        description: Successful Response
      401:
        description: Identifiants invalides
      422:
        description: Validation Error
    """
    try:
        # Validation des données de la requête
        data = request.get_json()
        if not data:
            response = ApiResponse(success=False, message="Corps de la requête vide")
            return jsonify(response.to_dict()), 400

        # Création du DTO de requête
        login_request = LoginRequest.from_dict(data)

        # Appel au service
        success, message, login_response = _service.verify_credentials(login_request)

        if success:
            response = ApiResponse(
                success=True,
                message=message,
                data=login_response.to_dict()
            )
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), 401
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500
