# 🔄 Mapping Mission Frontend ↔️ Backend

## Vue d'ensemble

Ce document explique la correspondance entre les données des missions du frontend (TypeScript) et du backend (Python/Flask).

---

## 📋 Structure Frontend (TypeScript)

```typescript
interface Mission {
  id: number;
  type: string;           // Ex: "Nettoyage", "Livraison", "Jardinage"
  ville: string;          // Ex: "Conakry", "Matoto", "Dixinn"
  quartier: string;       // Ex: "Ratoma", "Kipé", "Landréah"
  tarif: number;          // En GNF (Francs guinéens)
  duree: number;          // En heures (peut être décimal: 2.5)
  date: string;           // Format: "YYYY-MM-DD"
  statut: string;         // "en_cours" | "terminee" | "disponible" | "annulee"
  photos: string[];       // URLs des photos
  description: string;
}
```

---

## 🔧 Structure Backend (Python/Flask)

```python
@dataclass
class MissionModel:
    id: str                      # UUID généré automatiquement
    title: str                   # Titre de la mission
    description: str             # Description détaillée
    type_code: str               # Code du type (voir mapping ci-dessous)
    location: AddressDto         # Objet avec country, city, neighborhood
    budget: float                # Montant en GNF
    publisher_id: str            # ID de l'utilisateur créateur
    status: str                  # Statut normalisé (voir mapping)
    work_days: List[WorkDayDto]  # Liste des jours de travail
    created_at: str              # Timestamp de création
    updated_at: str              # Timestamp de modification
```

---

## 🗺️ Mapping des champs

| Frontend          | Backend            | Transformation                                     |
|-------------------|--------------------|----------------------------------------------------|
| `id` (number)     | `id` (UUID string) | Généré automatiquement par le backend              |
| `type` (string)   | `type_code`        | Voir tableau de mapping des types ⬇️               |
| `ville`           | `location.city`    | Direct                                             |
| `quartier`        | `location.neighborhood` | Direct                                        |
| -                 | `location.country` | Toujours "Guinée" (ajouté par défaut)              |
| `tarif`           | `budget`           | Direct (float)                                     |
| `duree`           | Calculé depuis `work_days` | Différence entre end_time et start_time   |
| `date`            | `work_days[0].day` | La date du premier jour de travail                 |
| `statut`          | `status`           | Voir tableau de mapping des statuts ⬇️             |
| `photos`          | `metadata.photos`  | Stocké dans les métadonnées (optionnel)            |
| `description`     | `description`      | Direct                                             |
| -                 | `title`            | Peut être le même que `type` ou une version courte |
| -                 | `publisher_id`     | ID de l'utilisateur qui crée la mission            |
| -                 | `work_days[].start_time` | Heure de début (format "HH:MM:SS")       |
| -                 | `work_days[].end_time`   | Heure de fin (format "HH:MM:SS")         |

---

## 🏷️ Mapping des Types de Mission

| Frontend (type) | Backend (type_code) | Description                        |
|-----------------|---------------------|------------------------------------|
| Nettoyage       | CLEANING            | Services de nettoyage              |
| Ménage          | CLEANING            | Idem (synonyme)                    |
| Livraison       | DELIVERY            | Services de livraison              |
| Jardinage       | GARDENING           | Entretien de jardin                |
| Informatique    | OTHER               | Services informatiques             |
| Bricolage       | HANDYMAN            | Travaux divers                     |
| Plomberie       | HANDYMAN            | Travaux de plomberie               |
| Électricité     | HANDYMAN            | Travaux électriques                |
| Cours           | TUTORING            | Cours particuliers                 |

### Types disponibles dans le backend :
```python
MISSION_TYPES = {
    "CLEANING": {
        "code": "CLEANING",
        "name": "Nettoyage",
        "description": "Services de nettoyage et d'entretien"
    },
    "DELIVERY": {
        "code": "DELIVERY",
        "name": "Livraison",
        "description": "Services de livraison"
    },
    "HANDYMAN": {
        "code": "HANDYMAN",
        "name": "Bricolage",
        "description": "Travaux de bricolage et réparations"
    },
    "GARDENING": {
        "code": "GARDENING",
        "name": "Jardinage",
        "description": "Entretien de jardin et espaces verts"
    },
    "TUTORING": {
        "code": "TUTORING",
        "name": "Cours particuliers",
        "description": "Enseignement et formation"
    },
    "OTHER": {
        "code": "OTHER",
        "name": "Autre",
        "description": "Autres types de missions"
    }
}
```

---

## 🚦 Mapping des Statuts

| Frontend (statut) | Backend (status) | Description                           |
|-------------------|------------------|---------------------------------------|
| disponible        | PUBLISHED        | Mission publiée et disponible         |
| en_cours          | ASSIGNED         | Mission assignée à un prestataire     |
| terminee          | COMPLETED        | Mission terminée                      |
| annulee           | CANCELLED        | Mission annulée                       |
| -                 | DRAFT            | Brouillon (pas encore publié)         |

---

## 🔄 Exemple de conversion

### Frontend → Backend

```javascript
// Frontend (TypeScript)
const mission = {
  id: 1,
  type: 'Nettoyage',
  ville: 'Conakry',
  quartier: 'Ratoma',
  tarif: 150000,
  duree: 2,
  date: '2025-09-28',
  statut: 'en_cours',
  photos: ['https://...'],
  description: 'Nettoyage complet...'
}
```

```python
# Backend (Python)
mission = MissionModel(
    title="Nettoyage",
    description="Nettoyage complet...",
    type_code="CLEANING",
    location=AddressDto(
        country="Guinée",
        city="Conakry",
        neighborhood="Ratoma"
    ),
    budget=150000.0,
    publisher_id="user-1",
    status="ASSIGNED",  # "en_cours" → "ASSIGNED"
    work_days=[
        WorkDayDto(
            day="2025-09-28",
            start_time="09:00:00",
            end_time="11:00:00"  # duree: 2h
        )
    ]
)
```

### Backend → Frontend

```python
# Backend (Response DTO)
{
    "id": "37ab08d7-feaf-4bfe-862e-f947ca925b09",
    "title": "Nettoyage",
    "description": "Nettoyage complet...",
    "type": {
        "code": "CLEANING",
        "name": "Nettoyage",
        "description": "Services de nettoyage"
    },
    "location": {
        "country": "Guinée",
        "city": "Conakry",
        "neighborhood": "Ratoma"
    },
    "budget": "150000.0",
    "status": "ASSIGNED",
    "work_days": [
        {
            "day": "2025-09-28",
            "start_time": "09:00:00",
            "end_time": "11:00:00"
        }
    ]
}
```

```javascript
// Frontend (après transformation)
const mission = {
  id: 1,  // Peut être extrait de l'UUID ou auto-incrémenté
  type: response.type.name,  // "Nettoyage"
  ville: response.location.city,  // "Conakry"
  quartier: response.location.neighborhood,  // "Ratoma"
  tarif: parseFloat(response.budget),  // 150000
  duree: calculateDuration(response.work_days[0]),  // 2 heures
  date: response.work_days[0].day,  // "2025-09-28"
  statut: mapStatusToFrontend(response.status),  // "en_cours"
  photos: response.metadata?.photos || [],
  description: response.description
}
```

---

## 🛠️ Fonctions de transformation

### Frontend → Backend

```typescript
function transformToBackend(frontendMission: Mission) {
  return {
    title: frontendMission.type,
    description: frontendMission.description,
    type_code: mapTypeToBackend(frontendMission.type),
    location: {
      country: "Guinée",
      city: frontendMission.ville,
      neighborhood: frontendMission.quartier
    },
    budget: frontendMission.tarif,
    work_days: [
      {
        day: frontendMission.date,
        start_time: "09:00:00",
        end_time: calculateEndTime("09:00:00", frontendMission.duree)
      }
    ],
    status: mapStatutToStatus(frontendMission.statut)
  };
}

function mapTypeToBackend(type: string): string {
  const mapping = {
    'Nettoyage': 'CLEANING',
    'Ménage': 'CLEANING',
    'Livraison': 'DELIVERY',
    'Jardinage': 'GARDENING',
    'Informatique': 'OTHER',
    'Bricolage': 'HANDYMAN',
    'Plomberie': 'HANDYMAN',
    'Électricité': 'HANDYMAN',
    'Cours': 'TUTORING'
  };
  return mapping[type] || 'OTHER';
}

function mapStatutToStatus(statut: string): string {
  const mapping = {
    'disponible': 'PUBLISHED',
    'en_cours': 'ASSIGNED',
    'terminee': 'COMPLETED',
    'annulee': 'CANCELLED'
  };
  return mapping[statut] || 'PUBLISHED';
}
```

### Backend → Frontend

```typescript
function transformToFrontend(backendMission: any) {
  return {
    id: extractIdFromUuid(backendMission.id),
    type: backendMission.type.name,
    ville: backendMission.location.city,
    quartier: backendMission.location.neighborhood,
    tarif: parseFloat(backendMission.budget),
    duree: calculateDuration(backendMission.work_days[0]),
    date: backendMission.work_days[0].day,
    statut: mapStatusToStatut(backendMission.status),
    photos: backendMission.metadata?.photos || [],
    description: backendMission.description
  };
}

function mapStatusToStatut(status: string): string {
  const mapping = {
    'PUBLISHED': 'disponible',
    'ASSIGNED': 'en_cours',
    'COMPLETED': 'terminee',
    'CANCELLED': 'annulee',
    'DRAFT': 'disponible'
  };
  return mapping[status] || 'disponible';
}

function calculateDuration(workDay: any): number {
  const start = new Date(`2000-01-01T${workDay.start_time}`);
  const end = new Date(`2000-01-01T${workDay.end_time}`);
  return (end.getTime() - start.getTime()) / (1000 * 60 * 60);  // Heures
}
```

---

## 📝 Notes importantes

1. **IDs** : Le backend utilise des UUID (strings), le frontend utilise des numbers. Une conversion peut être nécessaire.

2. **Durée** : 
   - Frontend : un seul champ `duree` (nombre d'heures)
   - Backend : calculé depuis `start_time` et `end_time`

3. **Localisation** :
   - Frontend : `ville` + `quartier`
   - Backend : objet `AddressDto` avec `country`, `city`, `neighborhood`

4. **Type** :
   - Frontend : string libre ("Nettoyage", "Livraison", etc.)
   - Backend : code normalisé (CLEANING, DELIVERY, etc.)

5. **Photos** :
   - Frontend : tableau d'URLs obligatoire
   - Backend : optionnel, stocké dans metadata

6. **Work Days** :
   - Le backend supporte plusieurs jours de travail
   - Le frontend n'en affiche qu'un seul (le premier)

---

## 🧪 Tester le mapping

Utilisez le script `load_fake_missions.py` pour charger des données de test :

```bash
# Charger les missions
python load_fake_missions.py

# Afficher les missions chargées
python load_fake_missions.py display

# Effacer toutes les missions
python load_fake_missions.py clear
```

---

## 📚 Ressources

- **API Documentation** : http://localhost:5000/docs/
- **Mission Controller** : `controllers/mission_controller.py`
- **Mission DTOs** : `dto/mission/mission_dto.py`
- **Mission Model** : `models/mission_model.py`
- **Fake Data** : `fake_missions_data.json`
