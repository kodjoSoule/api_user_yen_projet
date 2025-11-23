# Documentation des Workflows de Mission

## Vue d'ensemble

Cette documentation décrit les nouveaux endpoints pour gérer le cycle de vie complet d'une mission, de l'acceptation à la complétion.

## Cycle de vie d'une mission

```
DRAFT → PUBLISHED → ASSIGNED → COMPLETED
   ↓         ↓          ↓
(création) (publication) (acceptation) (complétion)
```

## Endpoints disponibles

### 1. Accepter une mission

**Endpoint:** `POST /api/missions/{mission_id}/accept`  
**Alias:** `POST /missions/{mission_id}/accept`

Permet à un utilisateur d'accepter une mission publiée et de devenir le travailleur assigné.

#### Prérequis
- La mission doit avoir le statut `PUBLISHED`
- L'utilisateur ne doit pas être le propriétaire de la mission
- L'utilisateur doit être authentifié (token JWT requis)

#### Headers
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

#### Réponse succès (200)
```json
{
  "success": true,
  "message": "Mission acceptee avec succes",
  "data": {
    "id": "2d0a7b6b-a390-4abb-815f-d0fc39fca737",
    "title": "Livraison urgente documents",
    "description": "Livraison de documents administratifs",
    "type": {
      "code": "DELIVERY",
      "name": "Livraison",
      "description": "Services de livraison et transport"
    },
    "location": {
      "country": "Guinée",
      "city": "Conakry",
      "district": "Kaloum"
    },
    "budget": "25000.0",
    "publisher_id": "client-alpha-conde",
    "worker_id": "e58119b7-a28e-446c-9cd9-bf90a9733ba0",
    "status": "ASSIGNED",
    "work_days": [...]
  }
}
```

#### Erreurs possibles

**400 - Statut invalide**
```json
{
  "success": false,
  "message": "Cette mission ne peut pas etre acceptee (statut: ASSIGNED)"
}
```

**403 - Mission propre**
```json
{
  "success": false,
  "message": "Vous ne pouvez pas accepter votre propre mission"
}
```

**404 - Mission introuvable**
```json
{
  "success": false,
  "message": "Mission non trouvee"
}
```

**401 - Non authentifié**
```json
{
  "success": false,
  "message": "Token manquant ou invalide"
}
```

---

### 2. Terminer une mission

**Endpoint:** `POST /api/missions/{mission_id}/complete`  
**Alias:** `POST /missions/{mission_id}/complete`

Permet de marquer une mission comme terminée. Peut être effectué par le propriétaire ou le travailleur assigné.

#### Prérequis
- La mission doit avoir le statut `ASSIGNED`
- L'utilisateur doit être soit le propriétaire soit le travailleur assigné
- L'utilisateur doit être authentifié (token JWT requis)

#### Headers
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

#### Réponse succès (200)
```json
{
  "success": true,
  "message": "Mission terminee avec succes",
  "data": {
    "id": "2d0a7b6b-a390-4abb-815f-d0fc39fca737",
    "title": "Livraison urgente documents",
    "status": "COMPLETED",
    "worker_id": "e58119b7-a28e-446c-9cd9-bf90a9733ba0",
    ...
  }
}
```

#### Erreurs possibles

**400 - Statut invalide**
```json
{
  "success": false,
  "message": "Cette mission ne peut pas etre terminee (statut: PUBLISHED)"
}
```

**403 - Non autorisé**
```json
{
  "success": false,
  "message": "Vous n'etes pas autorise a terminer cette mission"
}
```

**404 - Mission introuvable**
```json
{
  "success": false,
  "message": "Mission non trouvee"
}
```

---

## Exemples d'utilisation

### Workflow complet avec cURL

#### 1. Se connecter
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin"
  }'
```

**Réponse:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {...}
  }
}
```

#### 2. Lister les missions disponibles
```bash
curl -X GET http://localhost:5000/missions/
```

#### 3. Accepter une mission
```bash
curl -X POST http://localhost:5000/missions/2d0a7b6b-a390-4abb-815f-d0fc39fca737/accept \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json"
```

#### 4. Terminer la mission
```bash
curl -X POST http://localhost:5000/missions/2d0a7b6b-a390-4abb-815f-d0fc39fca737/complete \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json"
```

---

### Workflow complet avec Python

```python
import requests

BASE_URL = "http://localhost:5000"

# 1. Connexion
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@example.com",
    "password": "admin"
})
token = response.json()['data']['access_token']

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 2. Trouver une mission PUBLISHED
response = requests.get(f"{BASE_URL}/missions/")
missions = response.json()['data']
published_missions = [m for m in missions if m['status'] == 'PUBLISHED']

if published_missions:
    mission_id = published_missions[0]['id']
    
    # 3. Accepter la mission
    response = requests.post(
        f"{BASE_URL}/missions/{mission_id}/accept",
        headers=headers
    )
    print(f"Mission acceptée: {response.json()['message']}")
    
    # 4. Terminer la mission
    response = requests.post(
        f"{BASE_URL}/missions/{mission_id}/complete",
        headers=headers
    )
    print(f"Mission terminée: {response.json()['message']}")
```

---

## Modèle de données

### Champ worker_id

Un nouveau champ `worker_id` a été ajouté au modèle de mission :

```python
{
  "id": "string (UUID)",
  "title": "string",
  "description": "string",
  "type_code": "string (CLEANING|DELIVERY|HANDYMAN|GARDENING|TUTORING|OTHER)",
  "location": {...},
  "budget": "float",
  "publisher_id": "string (UUID)", # Créateur de la mission
  "worker_id": "string (UUID)",    # Travailleur assigné (après accept)
  "status": "string (DRAFT|PUBLISHED|ASSIGNED|COMPLETED)",
  "work_days": [...],
  "created_at": "ISO 8601",
  "updated_at": "ISO 8601"
}
```

---

## Logique métier

### Règles d'acceptation
1. ✅ Mission avec statut `PUBLISHED`
2. ✅ Utilisateur différent du propriétaire
3. ✅ Token JWT valide
4. ❌ Mission déjà assignée (`ASSIGNED`)
5. ❌ Mission terminée (`COMPLETED`)
6. ❌ Mission en brouillon (`DRAFT`)

### Règles de complétion
1. ✅ Mission avec statut `ASSIGNED`
2. ✅ Utilisateur = propriétaire OU travailleur assigné
3. ✅ Token JWT valide
4. ❌ Mission non assignée (`PUBLISHED`, `DRAFT`)
5. ❌ Mission déjà terminée (`COMPLETED`)
6. ❌ Utilisateur non autorisé (ni propriétaire ni travailleur)

---

## Tests

Un script de test complet est disponible : `test_mission_workflow.py`

```bash
# Exécuter les tests
python test_mission_workflow.py
```

Le script teste :
1. ✅ Acceptation d'une mission PUBLISHED
2. ⚠️ Tentative d'accepter sa propre mission
3. ✅ Complétion d'une mission ASSIGNED
4. ⚠️ Tentative de terminer une mission non assignée

---

## Notes importantes

### Sécurité
- Tous les endpoints nécessitent une authentification JWT
- Les vérifications de propriété sont effectuées côté serveur
- Les transitions de statut sont validées pour éviter les états incohérents

### Compatibilité
- Les endpoints sont disponibles avec préfixe `/api/missions` (standard)
- Les endpoints sont également disponibles avec préfixe `/missions` (alias frontend)
- Les deux versions fonctionnent de manière identique

### Statuts de mission
| Statut | Description | Transitions possibles |
|--------|-------------|----------------------|
| `DRAFT` | Mission créée mais non publiée | → `PUBLISHED` |
| `PUBLISHED` | Mission publiée, visible par tous | → `ASSIGNED` |
| `ASSIGNED` | Mission acceptée par un travailleur | → `COMPLETED` |
| `COMPLETED` | Mission terminée | ∅ (état final) |

---

## Résumé des modifications

### Fichiers modifiés

1. **models/mission_model.py**
   - Ajout du champ `worker_id`
   - Méthode `accept(user_id)` pour accepter une mission
   - Méthode `complete()` pour terminer une mission
   - Méthode `is_worker(user_id)` pour vérifier si l'utilisateur est le travailleur

2. **services/mission_service.py**
   - Méthode `accept_mission(mission_id, user_id)` avec validation
   - Méthode `complete_mission(mission_id, user_id)` avec validation

3. **controllers/mission_controller.py**
   - Endpoint `POST /api/missions/{id}/accept`
   - Endpoint `POST /api/missions/{id}/complete`
   - Endpoints alias sur `/missions/{id}/accept` et `/missions/{id}/complete`

4. **Nouveaux fichiers**
   - `test_mission_workflow.py` - Tests automatisés
   - `MISSION_WORKFLOW.md` - Cette documentation

---

## Support

Pour toute question ou problème :
1. Vérifier que le serveur Flask est en cours d'exécution
2. Vérifier que le token JWT est valide
3. Consulter les logs du serveur pour plus de détails
4. Vérifier le statut actuel de la mission avec `GET /missions/{id}`
