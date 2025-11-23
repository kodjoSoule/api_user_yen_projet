# ✅ Solution: Endpoint `/missions` pour compatibilité Frontend

## 🎯 Problème identifié

Le frontend appelle `/missions?user_id=...` mais l'API utilise `/api/missions/`.

**Erreur observée:**
```
192.168.1.11 - - [23/Nov/2025 15:52:02] "GET /missions?user_id=... HTTP/1.1" 404 -
```

---

## 🔧 Solution implémentée

### 1. **Modification de `controllers/mission_controller.py`**

Ajout d'une fonction pour créer un blueprint alias :

```python
def create_mission_blueprint_alias(service: MissionService):
    """
    Crée un blueprint alias pour /missions (sans /api)
    Pour compatibilité avec le frontend
    """
    alias_bp = Blueprint("mission_alias", __name__)

    @alias_bp.route("/", methods=["GET"])
    @optional_token
    def get_all_missions_alias():
        """Alias pour GET /missions/ - Liste toutes les missions"""
        # Récupérer les paramètres de query
        user_id = request.args.get('user_id')

        # Appeler le service
        success, message, missions = service.get_all_missions()

        if success:
            # Filtrer par user_id si fourni
            if user_id:
                missions = [m for m in missions if m.publisher_id == user_id]

            missions_data = [mission.to_dict() for mission in missions]
            response = ApiResponse(success=True, message=message, data=missions_data)
            return jsonify(response.to_dict()), 200

        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), 500

    @alias_bp.route("/<mission_id>", methods=["GET"])
    @optional_token
    def retrieve_mission_alias(mission_id):
        """Alias pour GET /missions/<id> - Récupère une mission par ID"""
        success, message, mission_model = service.get_mission_by_id(mission_id)

        if success:
            mission_response = mission_model.to_display_dto()
            response = ApiResponse(success=True, message=message, data=mission_response.to_dict())
            return jsonify(response.to_dict()), 200

        status_code = 404 if "non trouvee" in message.lower() else 500
        response = ApiResponse(success=False, message=message)
        return jsonify(response.to_dict()), status_code

    return alias_bp
```

### 2. **Modification de `app.py`**

Enregistrement du blueprint alias :

```python
# Enregistrer le blueprint missions avec deux préfixes pour compatibilité
app.register_blueprint(mission_bp, url_prefix="/api/missions")

# Créer un blueprint alias pour /missions (sans /api)
from controllers.mission_controller import create_mission_blueprint_alias
mission_alias_bp = create_mission_blueprint_alias(mission_service)
app.register_blueprint(mission_alias_bp, url_prefix="/missions")
```

---

## 🌐 Endpoints disponibles

### URL principale (recommandée)
- **GET** `/api/missions/` - Liste toutes les missions
- **POST** `/api/missions/` - Créer une mission
- **POST** `/api/missions/search` - Rechercher des missions
- **GET** `/api/missions/<id>` - Récupérer une mission
- **POST** `/api/missions/<id>/publish` - Publier une mission

### URL alias (pour compatibilité frontend)
- **GET** `/missions/` - Liste toutes les missions
- **GET** `/missions/<id>` - Récupérer une mission

---

## 📝 Exemples d'utilisation

### 1. Récupérer toutes les missions

```bash
curl http://localhost:5000/missions/
```

```javascript
// Frontend (JavaScript/TypeScript)
fetch('http://localhost:5000/missions/')
  .then(res => res.json())
  .then(data => console.log(data));
```

### 2. Filtrer par user_id

```bash
curl "http://localhost:5000/missions/?user_id=user-1"
```

```javascript
// Frontend
const userId = 'user-1';
fetch(`http://localhost:5000/missions/?user_id=${userId}`)
  .then(res => res.json())
  .then(data => {
    console.log(`Missions de ${userId}:`, data.data);
  });
```

### 3. Récupérer une mission spécifique

```bash
curl http://localhost:5000/missions/37ab08d7-feaf-4bfe-862e-f947ca925b09
```

```javascript
// Frontend
const missionId = '37ab08d7-feaf-4bfe-862e-f947ca925b09';
fetch(`http://localhost:5000/missions/${missionId}`)
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## 📊 Format de réponse

### Liste de missions

```json
{
  "success": true,
  "message": "Missions recuperees avec succes",
  "data": [
    {
      "id": "37ab08d7-feaf-4bfe-862e-f947ca925b09",
      "title": "Nettoyage",
      "description": "Nettoyage complet d'un appartement de 3 pieces.",
      "type": {
        "code": "CLEANING",
        "name": "Nettoyage",
        "description": "Services de nettoyage et d'entretien"
      },
      "location": {
        "country": "Guinee",
        "city": "Conakry",
        "neighborhood": "Ratoma"
      },
      "budget": "150000.0",
      "publisher_id": "user-1",
      "status": "ASSIGNED",
      "work_days": [
        {
          "day": "2025-09-28",
          "start_time": "09:00:00",
          "end_time": "11:00:00"
        }
      ]
    }
  ]
}
```

### Mission unique

```json
{
  "success": true,
  "message": "Mission recuperee avec succes",
  "data": {
    "id": "37ab08d7-feaf-4bfe-862e-f947ca925b09",
    "title": "Nettoyage",
    "description": "Nettoyage complet d'un appartement de 3 pieces.",
    ...
  }
}
```

### Erreur 404 (mission non trouvée)

```json
{
  "success": false,
  "message": "Mission non trouvee"
}
```

---

## 🧪 Test de l'implémentation

Utilisez le script `test_missions_endpoints.py` pour tester :

```bash
python test_missions_endpoints.py
```

Le script teste :
- ✅ GET `/api/missions/` (endpoint principal)
- ✅ GET `/missions/` (endpoint alias)
- ✅ GET `/missions/?user_id=...` (filtrage par utilisateur)
- ✅ Affichage des publisher_id disponibles

---

## 🔍 Filtrage par user_id

La fonctionnalité de filtrage côté serveur est implémentée dans le blueprint alias :

```python
# Récupérer les paramètres de query
user_id = request.args.get('user_id')

# Filtrer par user_id si fourni
if user_id:
    missions = [m for m in missions if m.publisher_id == user_id]
```

### Exemples de requêtes

| Requête | Description | Résultat |
|---------|-------------|----------|
| `/missions/` | Toutes les missions | 11 missions |
| `/missions/?user_id=user-1` | Missions de user-1 | 1 mission (Nettoyage) |
| `/missions/?user_id=user-2` | Missions de user-2 | 1 mission (Livraison) |
| `/missions/?user_id=user-3` | Missions de user-3 | 1 mission (Jardinage) |
| `/missions/?user_id=inexistant` | User sans missions | 0 missions (tableau vide) |

---

## ⚠️ Notes importantes

1. **Deux URLs disponibles** :
   - `/api/missions/` (complète avec POST, search, publish)
   - `/missions/` (GET uniquement pour compatibilité)

2. **Authentification** :
   - Les endpoints utilisent `@optional_token`
   - Fonctionne avec ou sans token JWT

3. **Filtrage** :
   - Le filtrage par `user_id` est géré côté serveur
   - Retourne toujours un tableau (vide si aucune mission)

4. **IDs** :
   - Le backend utilise des UUID (strings)
   - Le frontend peut utiliser des numbers ou strings

---

## 🔗 Ressources

- **Documentation API** : http://localhost:5000/docs/
- **Script de test** : `test_missions_endpoints.py`
- **Mapping Frontend ↔ Backend** : `MISSION_MAPPING.md`
- **Données fake** : `fake_missions_data.json`
- **Loader de données** : `load_fake_missions.py`

---

## ✅ Statut

- [x] Endpoint `/missions/` créé
- [x] Filtrage par `user_id` implémenté
- [x] Compatible avec les requêtes frontend
- [x] Script de test fourni
- [x] Documentation mise à jour
