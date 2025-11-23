# Structure des DTOs

Cette documentation explique l'organisation des DTOs (Data Transfer Objects) par domaine.

## 📁 Organisation

```
dto/
├── __init__.py                 # Point d'entrée principal avec tous les exports
├── common/                     # DTOs communs à toute l'application
│   ├── __init__.py
│   └── base_dto.py            # ApiResponse, ValidationError
├── user/                       # DTOs pour le domaine User
│   ├── __init__.py
│   ├── user_request_dto.py    # CreateUserRequest, UpdateUserRequest, UploadPhotoRequest
│   └── user_response_dto.py   # UserResponse, UserListResponse, PhotoUploadResponse
└── auth/                       # DTOs pour le domaine Auth
    ├── __init__.py
    ├── auth_request_dto.py    # LoginRequest, RegisterRequest
    └── auth_response_dto.py   # LoginResponse, RegisterResponse
```

## 📦 Packages

### `dto.common` - DTOs Communs
DTOs utilisés dans toute l'application, quelle que soit le domaine.

#### `ApiResponse`
Réponse standardisée pour tous les endpoints.
```python
from dto.common import ApiResponse

response = ApiResponse(
    success=True,
    message="Opération réussie",
    data={"key": "value"}
)
```

#### `ValidationError`
Structure pour les erreurs de validation.
```python
from dto.common import ValidationError

error = ValidationError(
    field="email",
    message="Email invalide"
)
```

---

### `dto.user` - Domaine User

#### Request DTOs

**`CreateUserRequest`**
- Création d'un nouvel utilisateur
- Validation complète de tous les champs requis
- Méthodes: `from_dict()`, `to_dict()`, `validate()`

**`UpdateUserRequest`**
- Mise à jour partielle d'un utilisateur
- Tous les champs optionnels
- Méthodes: `from_dict()`, `to_dict()`, `validate()`

**`UploadPhotoRequest`**
- Upload de photo de profil
- Validation de l'ID utilisateur
- Méthodes: `from_form()`, `validate()`

#### Response DTOs

**`UserResponse`**
- Données complètes d'un utilisateur (sans mot de passe)
- Conversion depuis UserModel
- Méthode: `from_model()`, `to_dict()`

**`UserListResponse`**
- Liste d'utilisateurs avec compteur
- Structure: `{ users: [...], total: int }`
- Méthode: `to_dict()`

**`PhotoUploadResponse`**
- URL de la photo uploadée
- Structure: `{ photo_url: str }`
- Méthode: `to_dict()`

---

### `dto.auth` - Domaine Auth

#### Request DTOs

**`LoginRequest`**
- Connexion avec email/téléphone + mot de passe
- Au moins un identifiant requis (email OU phone_number)
- Méthodes: `from_dict()`, `to_dict()`, `validate()`

**`RegisterRequest`**
- Enregistrement d'un nouvel utilisateur
- Identique à `CreateUserRequest` mais dans le contexte Auth
- Méthodes: `from_dict()`, `to_dict()`, `validate()`

#### Response DTOs

**`LoginResponse`**
- Réponse d'authentification avec token JWT
- Structure: `{ token: str, user: UserResponse }`
- Méthode: `to_dict()`

**`RegisterResponse`**
- Réponse d'enregistrement
- Structure: `{ user: UserResponse, message: str }`
- Méthode: `to_dict()`

---

## 🎯 Utilisation

### Import simplifié depuis le package principal

```python
# Import depuis le package principal
from dto import (
    ApiResponse,           # Common
    UserResponse,          # User
    LoginRequest,          # Auth
)
```

### Import depuis les sous-packages

```python
# Import depuis les sous-packages
from dto.common import ApiResponse, ValidationError
from dto.user import CreateUserRequest, UserResponse
from dto.auth import LoginRequest, LoginResponse
```

### Exemple dans un contrôleur

```python
from flask import request, jsonify
from dto.common import ApiResponse
from dto.user import CreateUserRequest

def create_user():
    # Validation des données
    data = request.get_json()
    if not data:
        response = ApiResponse(success=False, message="Corps vide")
        return jsonify(response.to_dict()), 400
    
    # Création du DTO de requête
    create_request = CreateUserRequest.from_dict(data)
    
    # Validation
    is_valid, error_msg = create_request.validate()
    if not is_valid:
        response = ApiResponse(success=False, message=error_msg)
        return jsonify(response.to_dict()), 400
    
    # Traitement...
    success, message, user_response = service.create_user(create_request)
    
    if success:
        response = ApiResponse(
            success=True,
            message=message,
            data=user_response.to_dict()
        )
        return jsonify(response.to_dict()), 201
```

---

## ✅ Avantages de cette organisation

1. **Séparation par domaine** : Chaque domaine métier a ses propres DTOs
2. **Cohérence** : Les DTOs communs sont centralisés
3. **Maintenabilité** : Facile de trouver et modifier un DTO
4. **Scalabilité** : Facile d'ajouter de nouveaux domaines
5. **Import clair** : Import depuis le package principal ou les sous-packages
6. **Type safety** : Utilisation de dataclasses avec type hints

---

## 🔄 Flow de données

```
┌─────────────┐
│   Request   │
│  (JSON/Form)│
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Request DTO    │  ◄── Validation
│  .from_dict()   │
│  .validate()    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│    Service      │  ◄── Business Logic
│  (UserService)  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Response DTO   │
│  .to_dict()     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   ApiResponse   │  ◄── Format standardisé
│   .to_dict()    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  JSON Response  │
└─────────────────┘
```
