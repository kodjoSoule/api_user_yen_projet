import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from config.settings import SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRES_IN_MINUTES


def generate_token(user_id: str, email: str) -> str:
    """Génère un token JWT pour un utilisateur"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_IN_MINUTES),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token: str) -> Optional[Dict]:
    """Vérifie et décode un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def extract_token_from_header(auth_header: str) -> Optional[str]:
    """Extrait le token du header Authorization"""
    if not auth_header:
        return None

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None

    return parts[1]
