# Users Microservice - EQOS

API REST pour la gestion des utilisateurs conforme à la spécification OpenAPI 3.1.0.

## 📋 Description

Ce microservice gère les opérations CRUD (Create, Read, Update, Delete) pour les utilisateurs, incluant :
- Création et gestion de comptes utilisateurs
- Authentification et vérification des identifiants
- Upload de photos de profil
- Recherche par ID, email ou numéro de téléphone

## 🏗️ Architecture

Le projet suit une architecture en couches respectant les principes SOLID :

```
project/
├── app.py                 → Point d'entrée (DIP)
├── config/
│   └── settings.py        → Configuration application
├── controllers/           → Couche présentation (MVC)
│   └── user_controller.py
├── services/              → Logique métier (SRP, OCP)
│   └── user_service.py
├── repositories/          → Accès aux données (Repository Pattern)
│   └── user_repository.py
├── models/
│   └── user_model.py      → Entités métier
├── utils/
│   ├── auth_decorators.py → Décorateurs d'authentification
│   ├── file_upload.py     → Gestion upload fichiers
│   └── jwt_utils.py       → Utilitaires JWT
├── data/
│   └── users.json         → Base de données JSON
└── uploads/               → Fichiers uploadés
```

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd flask_api_project
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
   - Windows PowerShell :
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   - Windows CMD :
   ```cmd
   venv\Scripts\activate.bat
   ```
   - Linux/Mac :
   ```bash
   source venv/bin/activate
   ```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Lancer l'application**
```bash
python app.py
```

L'API sera accessible sur : `http://localhost:5000`

## 📚 Documentation API

### Swagger UI
La documentation interactive est disponible sur : `http://localhost:5000/docs/`

### Endpoints disponibles

#### 1. Créer un utilisateur
```http
POST /users/
Content-Type: application/json

{
  "first_name": "Jean",
  "last_name": "Dupont",
  "birth_date": "1990-01-15",
  "email": "jean.dupont@example.com",
  "phone_number": "+33612345678",
  "password": "SecurePass123!",
  "user_type": "PARTICULIER",
  "country": "France",
  "address": "123 Rue de la Paix, Paris"
}
```

#### 2. Récupérer tous les utilisateurs
```http
GET /users/all
```

#### 3. Récupérer un utilisateur par ID
```http
GET /users/{id}
```

#### 4. Récupérer un utilisateur par email
```http
GET /users/email/{email}
```

#### 5. Récupérer un utilisateur par téléphone
```http
GET /users/phone_number/{phone_num}
```

#### 6. Mettre à jour un utilisateur
```http
PUT /users/{id}
Content-Type: application/json

{
  "first_name": "Jean",
  "last_name": "Dupont",
  ...
}
```

#### 7. Supprimer un utilisateur
```http
DELETE /users/{id}
```

#### 8. Vérifier les identifiants
```http
POST /users/verify-users-creds
Content-Type: application/json

{
  "email": "jean.dupont@example.com",
  "password": "SecurePass123!"
}
```

**Réponse :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_id": "...",
    "email": "...",
    ...
  }
}
```

#### 9. Upload photo de profil
```http
POST /users/upload-profile-photo
Content-Type: multipart/form-data

photo: <fichier>
user_id: "uuid-de-l-utilisateur"
```

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

1. **Obtenir un token** : Utilisez l'endpoint `/users/verify-users-creds`
2. **Utiliser le token** : Ajoutez le header suivant à vos requêtes :
```
Authorization: Bearer <votre-token>
```

## 📊 Modèles de données

### UserModel
```json
{
  "user_id": "string (UUID)",
  "first_name": "string",
  "last_name": "string",
  "birth_date": "string (AAAA-MM-JJ)",
  "email": "string",
  "phone_number": "string",
  "password": "string (hashé)",
  "user_type": "PARTICULIER | ENTREPRISE",
  "country": "string",
  "address": "string",
  "photo_url": "string | null",
  "is_active": "boolean",
  "is_verified": "boolean",
  "is_completed": "boolean",
  "is_deleted": "boolean",
  "created_at": "string (ISO 8601)",
  "updated_at": "string | null",
  "last_login": "string | null",
  "last_password_change": "string | null"
}
```

### LoginModel
```json
{
  "email": "string | null",
  "phone_number": "string | null",
  "password": "string"
}
```

**Note** : Un des deux champs `email` ou `phone_number` doit être fourni.

## 🛠️ Technologies utilisées

- **Flask** : Framework web Python
- **Flask-CORS** : Gestion des CORS
- **Flasgger** : Documentation Swagger/OpenAPI
- **PyJWT** : Gestion des tokens JWT
- **Werkzeug** : Utilitaires web (hash de mots de passe, upload de fichiers)

## 🔧 Configuration

Modifiez le fichier `config/settings.py` pour personnaliser :
- `SECRET_KEY` : Clé secrète pour JWT (à changer en production !)
- `JWT_EXPIRES_IN_MINUTES` : Durée de validité des tokens
- `UPLOAD_FOLDER` : Dossier de stockage des uploads

## 📝 Principes SOLID appliqués

- **SRP (Single Responsibility Principle)** : Chaque classe a une responsabilité unique
- **OCP (Open/Closed Principle)** : Les services sont ouverts à l'extension
- **LSP (Liskov Substitution Principle)** : Les modèles sont interchangeables
- **ISP (Interface Segregation Principle)** : Interfaces spécifiques par besoin
- **DIP (Dependency Inversion Principle)** : Injection de dépendances dans app.py

## 🧪 Tests

Pour tester l'API, vous pouvez utiliser :
- Swagger UI : `http://localhost:5000/docs/`
- Postman
- cURL
- HTTPie

### Exemple avec cURL
```bash
# Créer un utilisateur
curl -X POST http://localhost:5000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jean",
    "last_name": "Dupont",
    "birth_date": "1990-01-15",
    "email": "jean.dupont@example.com",
    "phone_number": "+33612345678",
    "password": "SecurePass123!",
    "user_type": "PARTICULIER",
    "country": "France",
    "address": "123 Rue de la Paix, Paris"
  }'
```

## 🚨 Sécurité

⚠️ **Important pour la production** :
- Changez le `SECRET_KEY` dans `config/settings.py`
- Utilisez une vraie base de données (PostgreSQL, MySQL, etc.)
- Ajoutez une validation d'email
- Implémentez un rate limiting
- Utilisez HTTPS
- Ajoutez des logs de sécurité

## 📄 Licence

Ce projet est développé pour EQOS.

## 👥 Contributeurs

- Votre équipe EQOS

## 📧 Contact

Pour toute question ou suggestion, contactez l'équipe de développement.
