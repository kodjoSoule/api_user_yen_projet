# Structure du projet - Users Microservice

## Architecture complète

```
project/
│
├── app.py                     → Point d'entrée de l'application (DIP - Dependency Inversion)
│
├── config/
│   └── settings.py            → Configuration centralisée (chemins, JWT, Swagger)
│
├── controllers/               → Couche présentation - Controller (MVC)
│   └── user_controller.py     → Routes et endpoints Flask (Blueprint)
│
├── services/                  → Couche logique métier (SRP, OCP)
│   └── user_service.py        → Logique métier des utilisateurs
│
├── repositories/              → Couche d'accès aux données (Repository Pattern)
│   └── user_repository.py     → CRUD sur le fichier JSON
│
├── models/
│   └── user_model.py          → Entités métier (UserModel, LoginModel, UserType)
│
├── utils/                     → Utilitaires transversaux
│   ├── auth_decorators.py     → Décorateurs d'authentification JWT
│   ├── file_upload.py         → Gestion des uploads de fichiers
│   └── jwt_utils.py           → Génération et validation de tokens JWT
│
├── data/
│   └── users.json             → "Base de données" JSON (stockage persistant)
│
├── uploads/                   → Dossier des fichiers uploadés (photos)
│   └── .gitkeep               → Garde le dossier dans git
│
├── requirements.txt           → Dépendances Python
├── .env.example               → Exemple de configuration d'environnement
├── .gitignore                 → Fichiers à ignorer par git
├── README.md                  → Documentation principale
├── doc.md                     → Documentation détaillée
├── folder-struct.md           → Ce fichier (structure du projet)
└── test_api.py                → Script de tests de l'API
```

## Principes d'architecture appliqués

### 1. **MVC (Model-View-Controller)**
- **Model** : `models/user_model.py` - Représentation des données
- **View** : Réponses JSON via Flask
- **Controller** : `controllers/user_controller.py` - Gestion des requêtes HTTP

### 2. **Repository Pattern**
- `repositories/user_repository.py` : Abstraction de l'accès aux données
- Permet de changer facilement de système de stockage (JSON → SQL)

### 3. **Service Layer**
- `services/user_service.py` : Contient toute la logique métier
- Validation, hachage des mots de passe, génération de tokens
- Indépendant du framework web

### 4. **Dependency Injection (DIP)**
- Injection dans `app.py` : `inject(service)`
- Facilite les tests et le découplage

### 5. **Single Responsibility (SRP)**
- Chaque module a une responsabilité unique et claire
- Controllers : Routes HTTP
- Services : Logique métier
- Repositories : Accès données
- Utils : Fonctions utilitaires

## Flux de données

```
Client HTTP Request
        ↓
[Controller] → Validation de la requête
        ↓
[Service] → Logique métier + Validation
        ↓
[Repository] → Accès aux données (JSON)
        ↓
[Model] → Objets métier
        ↓
Response JSON
```

## Extensions possibles

- Ajouter une vraie base de données (PostgreSQL, MySQL)
- Implémenter des tests unitaires et d'intégration
- Ajouter une validation d'email par code OTP
- Implémenter un système de rôles et permissions
- Ajouter un rate limiting
- Créer des migrations de base de données
