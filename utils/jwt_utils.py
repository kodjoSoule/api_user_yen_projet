import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from config.settings import SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRES_IN_MINUTES


def generate_tokens(user_id: str, email: str) -> Tuple[str, str]:
    """
    Génère un access token et un refresh token pour un utilisateur
    Returns: (access_token, refresh_token)
    """
    # Access Token - courte durée (ex: 60 minutes)
    access_payload = {
        'user_id': user_id,
        'email': email,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_IN_MINUTES),
        'iat': datetime.utcnow()
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

    # Refresh Token - longue durée (ex: 7 jours)
    refresh_payload = {
        'user_id': user_id,
        'email': email,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

    return access_token, refresh_token


def generate_token(user_id: str, email: str) -> str:
    """
    Génère un token JWT pour un utilisateur (legacy - utiliser generate_tokens)
    Deprecated: Utiliser generate_tokens() pour avoir access + refresh tokens
    """
    access_token, _ = generate_tokens(user_id, email)
    return access_token


def verify_token(token: str, token_type: Optional[str] = None) -> Optional[Dict]:
    """
    Vérifie et décode un token JWT
    Args:
        token: Le token JWT à vérifier
        token_type: Type de token attendu ('access' ou 'refresh'). None = tous types acceptés
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])

        # Vérifie le type de token si spécifié
        if token_type and payload.get('type') != token_type:
            return None

        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Génère un nouveau access token à partir d'un refresh token valide
    Args:
        refresh_token: Le refresh token
    Returns:
        Nouveau access token ou None si le refresh token est invalide
    """
    payload = verify_token(refresh_token, token_type='refresh')
    if not payload:
        return None

    # Génère un nouveau access token
    new_access_token, _ = generate_tokens(payload['user_id'], payload['email'])
    return new_access_token


def extract_token_from_header(auth_header: str) -> Optional[str]:
    """Extrait le token du header Authorization"""
    if not auth_header:
        return None

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None

    return parts[1]
