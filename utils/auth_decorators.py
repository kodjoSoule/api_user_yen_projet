from functools import wraps
from flask import request, jsonify
from utils.jwt_utils import extract_token_from_header, verify_token


def token_required(f):
    """Décorateur pour protéger les routes nécessitant une authentification"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'success': False,
                'message': 'Token manquant'
            }), 401

        token = extract_token_from_header(auth_header)

        if not token:
            return jsonify({
                'success': False,
                'message': 'Format de token invalide'
            }), 401

        payload = verify_token(token)

        if not payload:
            return jsonify({
                'success': False,
                'message': 'Token invalide ou expiré'
            }), 401

        # Ajoute les infos de l'utilisateur au contexte de la requête
        request.current_user = payload

        return f(*args, **kwargs)

    return decorated


def optional_token(f):
    """Décorateur pour les routes où le token est optionnel"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = extract_token_from_header(auth_header)
            if token:
                payload = verify_token(token)
                if payload:
                    request.current_user = payload

        return f(*args, **kwargs)

    return decorated
