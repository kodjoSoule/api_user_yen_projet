# 📋 API Missions - Documentation

## Vue d'ensemble

Le microservice **Missions** permet de gérer des missions/tâches que les utilisateurs peuvent publier et rechercher. Chaque mission contient des informations sur le travail à effectuer, la localisation, le budget et les horaires.

## Endpoints disponibles

### Base URL
```
http://localhost:5000/api/missions
```

---

## 1. Récupérer toutes les missions

**GET** `/api/missions/`

Récupère la liste complète de toutes les missions (brouillons et publiées).

### Paramètres
Aucun

### Réponse 200 - Succès

```json
{
  "success": true,
  "message": "Missions recuperees avec succes",
  "data": [
    {
      "id": "uuid-mission",
      "title": "Nettoyage de bureau",
      "description": "Recherche personne pour nettoyer un bureau de 50m2",
      "type": {
        "code": "CLEANING",
        "name": "Nettoyage",
        "description": "Services de nettoyage et entretien"
      },
      "location": {
        "country": "France",
        "city": "Paris",
        "neighborhood": "Marais"
      },
      "budget": "150.50",
      "publisher_id": "user-id",
      "status": "PUBLISHED",
      "work_days": [
        {
          "day": "2025-12-01",
          "start_time": "09:00:00",
          "end_time": "17:00:00"
        }
      ]
    }
  ]
}
```

---

## 2. Créer une mission

**POST** `/api/missions/`

Crée une nouvelle mission. Nécessite une authentification.

### Headers
```
Authorization: Bearer <access_token>
```

### Body

```json
{
  "title": "Titre de la mission",
  "description": "Description détaillée",
  "type_code": "CLEANING",
  "location": {
    "country": "France",
    "city": "Paris",
    "neighborhood": "Marais"
  },
  "budget": 150.50,
  "publisher_id": "user-id",
  "publish": false,
  "work_days": [
    {
      "day": "2025-12-01",
      "start_time": "09:00:00",
      "end_time": "17:00:00"
    }
  ]
}
```

### Types de missions disponibles

| Code | Nom | Description |
|------|-----|-------------|
| `CLEANING` | Nettoyage | Services de nettoyage et entretien |
| `DELIVERY` | Livraison | Services de livraison et transport |
| `HANDYMAN` | Bricolage | Travaux de bricolage et réparations |
| `GARDENING` | Jardinage | Services de jardinage et espaces verts |
| `TUTORING` | Cours particuliers | Enseignement et soutien scolaire |
| `OTHER` | Autre | Autres types de missions |

### Paramètre `publish`

- `false` (défaut) : La mission est créée en **brouillon** (status: DRAFT)
- `true` : La mission est **publiée immédiatement** (status: PUBLISHED)

### Réponse 201 - Créée

```json
{
  "success": true,
  "message": "Mission creee en brouillon avec succes",
  "data": {
    "id": "uuid-mission",
    "title": "Nettoyage de bureau",
    "status": "DRAFT",
    ...
  }
}
```

### Erreurs possibles

- **400** : Données invalides
- **401** : Token manquant ou invalide

---

## 3. Rechercher des missions

**POST** `/api/missions/search`

Recherche des missions selon des critères de filtrage.

### Body (tous les champs sont optionnels)

```json
{
  "title": "nettoyage",
  "type_code": "CLEANING",
  "country": "France",
  "city": "Paris",
  "neighborhood": "Marais",
  "budget_min": 100,
  "budget_max": 200,
  "publisher_id": "user-id",
  "status": "PUBLISHED"
}
```

### Statuts disponibles

- `DRAFT` : Brouillon (non publié)
- `PUBLISHED` : Publié (visible par tous)
- `ASSIGNED` : Assigné à un travailleur
- `COMPLETED` : Terminé
- `CANCELLED` : Annulé

### Réponse 200 - Succès

```json
{
  "success": true,
  "message": "Missions recuperees avec succes",
  "data": [
    {
      "id": "uuid",
      "title": "Nettoyage de bureau",
      ...
    }
  ]
}
```

---

## 4. Récupérer une mission spécifique

**GET** `/api/missions/{mission_id}`

Récupère les détails d'une mission par son ID.

### Paramètres

- `mission_id` (path) : ID de la mission

### Réponse 200 - Succès

```json
{
  "success": true,
  "message": "Mission recuperee avec succes",
  "data": {
    "id": "uuid-mission",
    "title": "Nettoyage de bureau",
    "description": "Description complète...",
    "type": {
      "code": "CLEANING",
      "name": "Nettoyage",
      "description": "Services de nettoyage et entretien"
    },
    "location": {
      "country": "France",
      "city": "Paris",
      "neighborhood": "Marais"
    },
    "budget": "150.50",
    "publisher_id": "user-id",
    "status": "DRAFT",
    "work_days": [
      {
        "day": "2025-12-01",
        "start_time": "09:00:00",
        "end_time": "17:00:00"
      }
    ]
  }
}
```

### Erreurs possibles

- **404** : Mission non trouvée

---

## 5. Publier une mission

**POST** `/api/missions/{mission_id}/publish`

Publie une mission (passe du statut DRAFT à PUBLISHED). Nécessite une authentification.

### Headers
```
Authorization: Bearer <access_token>
```

### Paramètres

- `mission_id` (path) : ID de la mission à publier

### Conditions

- La mission doit être en statut `DRAFT`
- L'utilisateur doit être le propriétaire de la mission (publisher_id)

### Réponse 200 - Succès

```json
{
  "success": true,
  "message": "Mission publiee avec succes",
  "data": {
    "id": "uuid-mission",
    "status": "PUBLISHED",
    ...
  }
}
```

### Erreurs possibles

- **400** : Mission déjà publiée ou statut invalide
- **401** : Token manquant ou invalide
- **403** : Vous n'êtes pas le propriétaire de cette mission
- **404** : Mission non trouvée

---

## Exemples d'utilisation

### PowerShell

```powershell
# 1. Login
$token = (Invoke-RestMethod -Uri "http://localhost:5000/auth/login" `
    -Method Post `
    -Body (@{email="user@example.com"; password="pass123"} | ConvertTo-Json) `
    -ContentType "application/json").data.access_token

# 2. Créer une mission
$mission = @{
    title = "Nettoyage appartement"
    description = "Nettoyage complet"
    type_code = "CLEANING"
    location = @{
        country = "France"
        city = "Paris"
        neighborhood = "Marais"
    }
    budget = 120.0
    publisher_id = "user-123"
    publish = $false
    work_days = @(
        @{
            day = "2025-12-01"
            start_time = "09:00:00"
            end_time = "17:00:00"
        }
    )
} | ConvertTo-Json -Depth 4

$result = Invoke-RestMethod -Uri "http://localhost:5000/api/missions/" `
    -Method Post `
    -Body $mission `
    -Headers @{Authorization="Bearer $token"} `
    -ContentType "application/json"

$missionId = $result.data.id

# 3. Publier la mission
Invoke-RestMethod -Uri "http://localhost:5000/api/missions/$missionId/publish" `
    -Method Post `
    -Headers @{Authorization="Bearer $token"}

# 4. Rechercher des missions
$filters = @{
    city = "Paris"
    status = "PUBLISHED"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/missions/search" `
    -Method Post `
    -Body $filters `
    -ContentType "application/json"
```

### Python

```python
import requests

BASE_URL = "http://localhost:5000"

# 1. Login
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "user@example.com",
    "password": "pass123"
})
token = login_response.json()["data"]["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Créer une mission
mission_data = {
    "title": "Livraison urgente",
    "description": "Livraison de colis",
    "type_code": "DELIVERY",
    "location": {
        "country": "France",
        "city": "Lyon",
        "neighborhood": "Bellecour"
    },
    "budget": 50.0,
    "publisher_id": "user-123",
    "publish": True,
    "work_days": [
        {
            "day": "2025-11-25",
            "start_time": "14:00:00",
            "end_time": "16:00:00"
        }
    ]
}

response = requests.post(
    f"{BASE_URL}/api/missions/",
    json=mission_data,
    headers=headers
)

mission = response.json()["data"]
print(f"Mission créée: {mission['id']}")

# 3. Rechercher des missions
filters = {"city": "Lyon", "status": "PUBLISHED"}
search_response = requests.post(
    f"{BASE_URL}/api/missions/search",
    json=filters
)

missions = search_response.json()["data"]
print(f"Trouvé {len(missions)} missions")
```

### cURL

```bash
# 1. Créer une mission
curl -X POST http://localhost:5000/api/missions/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nettoyage",
    "description": "Nettoyage bureau",
    "type_code": "CLEANING",
    "location": {
      "country": "France",
      "city": "Paris",
      "neighborhood": "Marais"
    },
    "budget": 150.50,
    "publisher_id": "user-123",
    "publish": false,
    "work_days": [
      {
        "day": "2025-12-01",
        "start_time": "09:00:00",
        "end_time": "17:00:00"
      }
    ]
  }'

# 2. Récupérer toutes les missions
curl http://localhost:5000/api/missions/

# 3. Rechercher des missions
curl -X POST http://localhost:5000/api/missions/search \
  -H "Content-Type: application/json" \
  -d '{"city": "Paris", "status": "PUBLISHED"}'
```

---

## Tests

Utilisez le script de test fourni :

```powershell
python test_missions.py
```

Ce script teste automatiquement tous les endpoints du microservice missions.

---

## Architecture

```
Controller (mission_controller.py)
    ↓
Service (mission_service.py)
    ↓
Repository (mission_repository.py)
    ↓
Fichier JSON (data/missions.json)
```

---

**Microservice Missions prêt à l'emploi ! 🎉**
