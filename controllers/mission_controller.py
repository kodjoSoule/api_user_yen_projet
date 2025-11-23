from flask import Blueprint, request, jsonify
from services.mission_service import MissionService
from dto.common import ApiResponse
from utils.auth_decorators import token_required, optional_token


mission_bp = Blueprint("mission", __name__)
_service: MissionService = None


def inject(service: MissionService):
    """Injecte le service de missions"""
    global _service
    _service = service


@mission_bp.route("/", methods=["GET"])
@optional_token
def get_all_missions():
    """Recupere toutes les missions
    ---
    tags:
      - EQOS : Missions
    responses:
      200:
        description: Liste de toutes les missions
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              title:
                type: string
              description:
                type: string
              type:
                type: object
                properties:
                  code:
                    type: string
                  name:
                    type: string
                  description:
                    type: string
              location:
                type: object
                properties:
                  country:
                    type: string
                  city:
                    type: string
                  neighborhood:
                    type: string
              budget:
                type: string
              publisher_id:
                type: string
              status:
                type: string
              work_days:
                type: array
                items:
                  type: object
                  properties:
                    day:
                      type: string
                      format: date
                    start_time:
                      type: string
                      format: time
                    end_time:
                      type: string
                      format: time
      500:
        description: Erreur serveur
    """
    try:
        missions = _service.get_all_missions()
        response = ApiResponse(success=True, message="Missions recuperees avec succes", data=[m.to_dict() for m in missions])
        return jsonify(response.to_dict()), 200
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@mission_bp.route("/", methods=["POST"])
@token_required
def create_mission():
    """Cree une nouvelle mission
    ---
    tags:
      - EQOS : Missions
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer token JWT
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
            - description
            - type_code
            - location
            - budget
            - publisher_id
            - work_days
          properties:
            title:
              type: string
              description: Titre de la mission
            description:
              type: string
              description: Description de la mission
            type_code:
              type: string
              description: Code du type de mission
            location:
              type: object
              required:
                - country
                - city
                - neighborhood
              properties:
                country:
                  type: string
                city:
                  type: string
                neighborhood:
                  type: string
            budget:
              type: number
              description: Budget de la mission
            publisher_id:
              type: string
              description: ID de l'utilisateur publiant la mission
            publish:
              type: boolean
              default: false
              description: Publier immediatement ou sauvegarder en brouillon
            work_days:
              type: array
              items:
                type: object
                required:
                  - day
                  - start_time
                  - end_time
                properties:
                  day:
                    type: string
                    format: date
                    description: Date du jour de travail (YYYY-MM-DD)
                  start_time:
                    type: string
                    format: time
                    description: Heure de debut (HH:MM:SS)
                  end_time:
                    type: string
                    format: time
                    description: Heure de fin (HH:MM:SS)
    responses:
      201:
        description: Mission creee avec succes
      400:
        description: Donnees invalides
      401:
        description: Non autorise
      500:
        description: Erreur serveur
    """
    try:
        data = request.get_json()
        if not data:
            response = ApiResponse(success=False, message="Corps de la requete vide")
            return jsonify(response.to_dict()), 400

        success, message, mission_response = _service.create_mission(data)

        if success:
            response = ApiResponse(success=True, message=message, data=mission_response.to_dict())
            return jsonify(response.to_dict()), 201

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), 400
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@mission_bp.route("/search", methods=["POST"])
@optional_token
def get_missions_by_filters():
    """Recherche des missions avec des filtres
    ---
    tags:
      - EQOS : Missions
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Filtre par titre (partiel)
            type_code:
              type: string
              description: Filtre par code de type
            country:
              type: string
              description: Filtre par pays
            city:
              type: string
              description: Filtre par ville
            neighborhood:
              type: string
              description: Filtre par quartier
            budget_min:
              type: number
              description: Budget minimum
            budget_max:
              type: number
              description: Budget maximum
            publisher_id:
              type: string
              description: Filtre par ID du publisher
            status:
              type: string
              description: Filtre par statut (DRAFT, PUBLISHED, ASSIGNED, COMPLETED, CANCELLED)
    responses:
      200:
        description: Missions filtrees
      400:
        description: Filtres invalides
      500:
        description: Erreur serveur
    """
    try:
        filters = request.get_json() or {}
        missions = _service.get_missions_by_filters(filters)
        response = ApiResponse(success=True, message="Missions recuperees avec succes", data=[m.to_dict() for m in missions])
        return jsonify(response.to_dict()), 200
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@mission_bp.route("/<mission_id>", methods=["GET"])
@optional_token
def retrieve_mission(mission_id):
    """Recupere une mission par son ID
    ---
    tags:
      - EQOS : Missions
    parameters:
      - in: path
        name: mission_id
        required: true
        type: string
        description: ID de la mission
    responses:
      200:
        description: Mission recuperee avec succes
      404:
        description: Mission non trouvee
      500:
        description: Erreur serveur
    """
    try:
        mission = _service.get_mission_by_id(mission_id)

        if not mission:
            response = ApiResponse(success=False, message="Mission non trouvee")
            return jsonify(response.to_dict()), 404

        response = ApiResponse(success=True, message="Mission recuperee avec succes", data=mission.to_dict())
        return jsonify(response.to_dict()), 200
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@mission_bp.route("/<mission_id>/publish", methods=["POST"])
@token_required
def publish_mission(mission_id):
    """Publie une mission (passe du statut DRAFT a PUBLISHED)
    ---
    tags:
      - EQOS : Missions
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer token JWT
      - in: path
        name: mission_id
        required: true
        type: string
        description: ID de la mission a publier
    responses:
      200:
        description: Mission publiee avec succes
      400:
        description: Mission deja publiee ou statut invalide
      401:
        description: Non autorise
      403:
        description: Vous n'etes pas le proprietaire de cette mission
      404:
        description: Mission non trouvee
      500:
        description: Erreur serveur
    """
    try:
        # Recuperer l'utilisateur courant depuis le token
        current_user_id = request.current_user.get('user_id')

        success, message, mission_response = _service.publish_mission(mission_id, current_user_id)

        if success:
            response = ApiResponse(success=True, message=message, data=mission_response.to_dict())
            return jsonify(response.to_dict()), 200

        # Determiner le code d'erreur selon le message
        status_code = 400
        if "non trouvee" in message.lower():
            status_code = 404
        elif "proprietaire" in message.lower() or "autorise" in message.lower():
            status_code = 403

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), status_code
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@mission_bp.route("/me", methods=["GET"])
@token_required
def get_my_missions():
    """Recupere toutes les missions de l'utilisateur connecte (creees + acceptees)
    ---
    tags:
      - EQOS : Missions
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer token JWT
    responses:
      200:
        description: Missions de l'utilisateur recuperees avec succes
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
                created_missions:
                  type: array
                  description: Missions creees par l'utilisateur
                  items:
                    type: object
                accepted_missions:
                  type: array
                  description: Missions acceptees par l'utilisateur
                  items:
                    type: object
                total_created:
                  type: integer
                total_accepted:
                  type: integer
                total:
                  type: integer
      401:
        description: Non autorise
      500:
        description: Erreur serveur
    """
    try:
        # Recuperer l'utilisateur courant depuis le token
        current_user_id = request.current_user.get('user_id')

        # Recuperer toutes les missions
        all_missions = _service.get_all_missions()

        # Filtrer les missions creees par l'utilisateur
        created_missions = [m for m in all_missions if m.publisher_id == current_user_id]

        # Filtrer les missions acceptees par l'utilisateur
        accepted_missions = [m for m in all_missions if hasattr(m, 'worker_id') and m.worker_id == current_user_id]

        # Convertir en dictionnaires
        created_missions_data = [m.to_dict() for m in created_missions]
        accepted_missions_data = [m.to_dict() for m in accepted_missions]

        # Preparer la reponse
        data = {
            "created_missions": created_missions_data,
            "accepted_missions": accepted_missions_data,
            "total_created": len(created_missions_data),
            "total_accepted": len(accepted_missions_data),
            "total": len(created_missions_data) + len(accepted_missions_data)
        }

        response = ApiResponse(
            success=True,
            message=f"Missions recuperees: {data['total_created']} creee(s), {data['total_accepted']} acceptee(s)",
            data=data
        )
        return jsonify(response.to_dict()), 200

    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@mission_bp.route("/<mission_id>/accept", methods=["POST"])
@token_required
def accept_mission(mission_id):
    """Accepte une mission - L'utilisateur devient le travailleur de la mission
    ---
    tags:
      - EQOS : Missions
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer token JWT
      - in: path
        name: mission_id
        required: true
        type: string
        description: ID de la mission a accepter
    responses:
      200:
        description: Mission acceptee avec succes
      400:
        description: Mission ne peut pas etre acceptee (statut invalide)
      401:
        description: Non autorise
      403:
        description: Vous ne pouvez pas accepter votre propre mission
      404:
        description: Mission non trouvee
      500:
        description: Erreur serveur
    """
    try:
        # Recuperer l'utilisateur courant depuis le token
        current_user_id = request.current_user.get('user_id')

        success, message, mission_response = _service.accept_mission(mission_id, current_user_id)

        if success:
            response = ApiResponse(success=True, message=message, data=mission_response.to_dict())
            return jsonify(response.to_dict()), 200

        # Determiner le code d'erreur selon le message
        status_code = 400
        if "non trouvee" in message.lower():
            status_code = 404
        elif "propre mission" in message.lower():
            status_code = 403

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), status_code
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


@mission_bp.route("/<mission_id>/complete", methods=["POST"])
@token_required
def complete_mission(mission_id):
    """Termine une mission - Peut etre fait par le proprietaire ou le travailleur
    ---
    tags:
      - EQOS : Missions
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer token JWT
      - in: path
        name: mission_id
        required: true
        type: string
        description: ID de la mission a terminer
    responses:
      200:
        description: Mission terminee avec succes
      400:
        description: Mission ne peut pas etre terminee (statut invalide)
      401:
        description: Non autorise
      403:
        description: Vous n'etes pas autorise a terminer cette mission
      404:
        description: Mission non trouvee
      500:
        description: Erreur serveur
    """
    try:
        # Recuperer l'utilisateur courant depuis le token
        current_user_id = request.current_user.get('user_id')

        success, message, mission_response = _service.complete_mission(mission_id, current_user_id)

        if success:
            response = ApiResponse(success=True, message=message, data=mission_response.to_dict())
            return jsonify(response.to_dict()), 200

        # Determiner le code d'erreur selon le message
        status_code = 400
        if "non trouvee" in message.lower():
            status_code = 404
        elif "autorise" in message.lower():
            status_code = 403

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), status_code
    except Exception as e:
        response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
        return jsonify(response.to_dict()), 500


def create_mission_blueprint_alias(service: MissionService):
    """
    Cree un blueprint alias pour /missions (sans /api)
    Pour compatibilite avec le frontend
    """
    alias_bp = Blueprint("mission_alias", __name__)

    @alias_bp.route("/", methods=["GET"])
    @optional_token
    def get_all_missions_alias():
        """Alias pour GET /missions/ - Liste toutes les missions"""
        # Appeler le service
        missions = service.get_all_missions()

        missions_data = [mission.to_dict() for mission in missions]
        response = ApiResponse(
            success=True,
            message="Missions recuperees avec succes",
            data=missions_data
        )
        return jsonify(response.to_dict()), 200

    @alias_bp.route("/user/<user_id>", methods=["GET"])
    @optional_token
    def get_user_missions(user_id):
        """GET /missions/user/<user_id> - Liste les missions d'un utilisateur
        ---
        tags:
          - EQOS : Missions
        parameters:
          - name: user_id
            in: path
            type: string
            required: true
            description: ID de l'utilisateur
        responses:
          200:
            description: Liste des missions de l'utilisateur
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
                data:
                  type: array
                  items:
                    type: object
          404:
            description: Aucune mission trouvee pour cet utilisateur
        """
        # Appeler le service
        missions = service.get_all_missions()

        # Filtrer les missions par publisher_id
        user_missions = [m for m in missions if m.publisher_id == user_id]

        missions_data = [mission.to_dict() for mission in user_missions]

        if len(user_missions) == 0:
            response = ApiResponse(
                success=True,
                message=f"Aucune mission trouvee pour l'utilisateur {user_id}",
                data=[]
            )
        else:
            response = ApiResponse(
                success=True,
                message=f"{len(user_missions)} mission(s) trouvee(s) pour l'utilisateur",
                data=missions_data
            )

        return jsonify(response.to_dict()), 200

    @alias_bp.route("/me", methods=["GET"])
    @token_required
    def get_my_missions_alias():
        """Alias pour GET /missions/me - Recupere les missions de l'utilisateur connecte"""
        try:
            current_user_id = request.current_user.get('user_id')

            # Recuperer toutes les missions
            all_missions = service.get_all_missions()

            # Filtrer les missions creees par l'utilisateur
            created_missions = [m for m in all_missions if m.publisher_id == current_user_id]

            # Filtrer les missions acceptees par l'utilisateur
            accepted_missions = [m for m in all_missions if hasattr(m, 'worker_id') and m.worker_id == current_user_id]

            # Convertir en dictionnaires
            created_missions_data = [m.to_dict() for m in created_missions]
            accepted_missions_data = [m.to_dict() for m in accepted_missions]

            # Preparer la reponse
            data = {
                "created_missions": created_missions_data,
                "accepted_missions": accepted_missions_data,
                "total_created": len(created_missions_data),
                "total_accepted": len(accepted_missions_data),
                "total": len(created_missions_data) + len(accepted_missions_data)
            }

            response = ApiResponse(
                success=True,
                message=f"Missions recuperees: {data['total_created']} creee(s), {data['total_accepted']} acceptee(s)",
                data=data
            )
            return jsonify(response.to_dict()), 200

        except Exception as e:
            response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
            return jsonify(response.to_dict()), 500

    @alias_bp.route("/<mission_id>", methods=["GET"])
    @optional_token
    def retrieve_mission_alias(mission_id):
        """Alias pour GET /missions/<id> - Recupere une mission par ID"""
        mission_display = service.get_mission_by_id(mission_id)

        if mission_display:
            response = ApiResponse(
                success=True,
                message="Mission recuperee avec succes",
                data=mission_display.to_dict()
            )
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message="Mission non trouvee")
        return jsonify(response.to_dict()), 404

    @alias_bp.route("/<mission_id>/accept", methods=["POST"])
    @token_required
    def accept_mission_alias(mission_id):
        """Alias pour POST /missions/<id>/accept - Accepte une mission"""
        try:
            current_user_id = request.current_user.get('user_id')
            success, message, mission_response = service.accept_mission(mission_id, current_user_id)

            if success:
                response = ApiResponse(success=True, message=message, data=mission_response.to_dict())
                return jsonify(response.to_dict()), 200

            status_code = 400
            if "non trouvee" in message.lower():
                status_code = 404
            elif "propre mission" in message.lower():
                status_code = 403

            response = ApiResponse(success=False, message=message)
            return jsonify(response.to_dict()), status_code
        except Exception as e:
            response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
            return jsonify(response.to_dict()), 500

    @alias_bp.route("/<mission_id>/complete", methods=["POST"])
    @token_required
    def complete_mission_alias(mission_id):
        """Alias pour POST /missions/<id>/complete - Termine une mission"""
        try:
            current_user_id = request.current_user.get('user_id')
            success, message, mission_response = service.complete_mission(mission_id, current_user_id)

            if success:
                response = ApiResponse(success=True, message=message, data=mission_response.to_dict())
                return jsonify(response.to_dict()), 200

            status_code = 400
            if "non trouvee" in message.lower():
                status_code = 404
            elif "autorise" in message.lower():
                status_code = 403

            response = ApiResponse(success=False, message=message)
            return jsonify(response.to_dict()), status_code
        except Exception as e:
            response = ApiResponse(success=False, message=f"Erreur serveur: {str(e)}")
            return jsonify(response.to_dict()), 500

    return alias_bp
