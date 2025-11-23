from flask import Blueprint, request, jsonify
from services.user_service import UserService
from utils.file_upload import save_uploaded_file, get_file_url
from dto.common import ApiResponse
from dto.user import CreateUserRequest, UpdateUserRequest, UploadPhotoRequest, PhotoUploadResponse
from dto.auth import LoginRequest


user_bp = Blueprint("users", __name__)
_service: UserService = None


def inject(service: UserService):
    global _service
    _service = service


@user_bp.route("/", methods=["POST"])
def create_user():
    """Crée un nouvel utilisateur
    ---
    tags:
      - EQOS : Gestion des utilisateurs
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
            is_active:
              type: boolean
              default: false
            is_verified:
              type: boolean
              default: false
            is_completed:
              type: boolean
              default: false
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


@user_bp.route("/all", methods=["GET"])
def get_all_users():
    """Récupère tous les utilisateurs
    ---
    tags:
      - EQOS : Gestion des utilisateurs
    responses:
      200:
        description: Successful Response
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                users:
                  type: array
                  items:
                    type: object
                total:
                  type: integer
    """
    try:
        # Appel au service
        user_list_response = _service.get_all_users()

        response = ApiResponse(
            success=True,
            data=user_list_response.to_dict()
        )
        return jsonify(response.to_dict()), 200
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@user_bp.route("/<id>", methods=["GET"])
def get_user_by_id(id):
    """Récupère un utilisateur par son ID
    ---
    tags:
      - EQOS : Gestion des utilisateurs
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
        description: L'ID de l'utilisateur
    responses:
      200:
        description: Successful Response
      404:
        description: Utilisateur non trouvé
      422:
        description: Validation Error
    """
    try:
        # Appel au service
        user_response = _service.get_user_by_id(id)

        if user_response:
            response = ApiResponse(
                success=True,
                data=user_response.to_dict()
            )
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message="Utilisateur non trouvé")
        return jsonify(response.to_dict()), 404
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@user_bp.route("/email/<email>", methods=["GET"])
def get_user_by_email(email):
    """Récupère un utilisateur par son email
    ---
    tags:
      - EQOS : Gestion des utilisateurs
    parameters:
      - in: path
        name: email
        required: true
        schema:
          type: string
          format: email
        description: L'email de l'utilisateur
    responses:
      200:
        description: Successful Response
      404:
        description: Utilisateur non trouvé
      422:
        description: Validation Error
    """
    try:
        # Appel au service
        user_response = _service.get_user_by_email(email)

        if user_response:
            response = ApiResponse(
                success=True,
                data=user_response.to_dict()
            )
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message="Utilisateur non trouvé")
        return jsonify(response.to_dict()), 404
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@user_bp.route("/phone_number/<phone_num>", methods=["GET"])
def get_user_by_phone(phone_num):
    """Récupère un utilisateur par son numéro de téléphone
    ---
    tags:
      - EQOS : Gestion des utilisateurs
    parameters:
      - in: path
        name: phone_num
        required: true
        schema:
          type: string
        description: Le numéro de téléphone de l'utilisateur
    responses:
      200:
        description: Successful Response
      404:
        description: Utilisateur non trouvé
      422:
        description: Validation Error
    """
    try:
        # Appel au service
        user_response = _service.get_user_by_phone(phone_num)

        if user_response:
            response = ApiResponse(
                success=True,
                data=user_response.to_dict()
            )
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message="Utilisateur non trouvé")
        return jsonify(response.to_dict()), 404
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@user_bp.route("/<id>", methods=["PUT"])
def update_user(id):
    """Met à jour un utilisateur
    ---
    tags:
      - EQOS : Gestion des utilisateurs
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
        description: L'ID de l'utilisateur
      - in: body
        name: body
        required: true
        schema:
          type: object
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
            country:
              type: string
            address:
              type: string
            photo_url:
              type: string
            is_active:
              type: boolean
            is_verified:
              type: boolean
            is_completed:
              type: boolean
    responses:
      200:
        description: Successful Response
      404:
        description: Utilisateur non trouvé
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
        update_user_request = UpdateUserRequest.from_dict(data)

        # Appel au service
        success, message, user_response = _service.update_user(id, update_user_request)

        if success:
            response = ApiResponse(
                success=True,
                message=message,
                data=user_response.to_dict()
            )
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), 400
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@user_bp.route("/<id>", methods=["DELETE"])
def delete_user(id):
    """Supprime un utilisateur (soft delete)
    ---
    tags:
      - EQOS : Gestion des utilisateurs
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
        description: L'ID de l'utilisateur
    responses:
      200:
        description: Successful Response
      404:
        description: Utilisateur non trouvé
      422:
        description: Validation Error
    """
    try:
        # Appel au service
        success, message = _service.delete_user(id)

        if success:
            response = ApiResponse(success=True, message=message)
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), 404
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@user_bp.route("/verify-users-creds", methods=["POST"])
def verify_users_credentials():
    """Vérifie les identifiants de l'utilisateur et retourne un token JWT
    ---
    tags:
      - EQOS : Gestion des utilisateurs
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


@user_bp.route("/upload-profile-photo", methods=["POST"])
def upload_photo():
    """Upload une photo de profil pour un utilisateur
    ---
    tags:
      - EQOS : Gestion des utilisateurs
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: photo
        type: file
        required: true
        description: Fichier photo (PNG, JPG, JPEG, GIF, WEBP)
      - in: formData
        name: user_id
        type: string
        required: true
        description: ID de l'utilisateur
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
                photo_url:
                  type: string
      400:
        description: Fichier manquant ou invalide
      404:
        description: Utilisateur non trouvé
      422:
        description: Validation Error
    """
    try:
        # Validation de la présence du fichier
        if 'photo' not in request.files:
            response = ApiResponse(success=False, message='Fichier photo manquant')
            return jsonify(response.to_dict()), 400

        # Création du DTO de requête depuis les données du formulaire
        upload_request = UploadPhotoRequest.from_form(request.form)

        # Validation du DTO
        is_valid, error_message = upload_request.validate()
        if not is_valid:
            response = ApiResponse(success=False, message=error_message)
            return jsonify(response.to_dict()), 400

        # Vérification de l'existence de l'utilisateur
        user_response = _service.get_user_by_id(upload_request.user_id)
        if not user_response:
            response = ApiResponse(success=False, message='Utilisateur non trouvé')
            return jsonify(response.to_dict()), 404

        # Sauvegarde du fichier
        file = request.files['photo']
        file_success, result = save_uploaded_file(file)
        if not file_success:
            response = ApiResponse(success=False, message=result)
            return jsonify(response.to_dict()), 400

        # Génération de l'URL de la photo
        photo_url = get_file_url(result, request.host_url.rstrip('/'))

        # Mise à jour de la photo de profil
        success, message = _service.update_profile_photo(upload_request.user_id, photo_url)

        if success:
            photo_response = PhotoUploadResponse(photo_url=photo_url)
            response = ApiResponse(
                success=True,
                message=message,
                data=photo_response.to_dict()
            )
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), 500
    except Exception as e:
        response = ApiResponse(success=False, message=f'Erreur: {str(e)}')
        return jsonify(response.to_dict()), 500
