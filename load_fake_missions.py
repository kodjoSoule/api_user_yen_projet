"""
Script de chargement des missions fictives
Ce script convertit les données TypeScript en format Python et les charge dans la base de données
"""

import json
import os
from datetime import datetime
from repositories.mission_repository import MissionRepository
from models.mission_model import MissionModel
from dto.mission import AddressDto, WorkDayDto

# Chemin vers le fichier de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MISSIONS_DATA_FILE = os.path.join(BASE_DIR, "data", "missions.json")


def convert_fake_missions_to_system_format():
    """
    Convertit les missions fictives du format TypeScript
    vers le format de notre système
    """

    # Données fictives converties - Basées sur l'exemple fourni
    # Format: id, type, ville, quartier, tarif, duree, date, statut, photos, description
    missions = [
        {
            "title": "Nettoyage",
            "description": "Nettoyage complet d'un appartement de 3 pieces.",
            "type_code": "CLEANING",
            "location": {
                "country": "Guinee",
                "city": "Conakry",
                "neighborhood": "Ratoma"
            },
            "budget": 150000,  # GNF
            "publisher_id": "user-1",
            "status": "ASSIGNED",  # en_cours
            "work_days": [
                {
                    "day": "2025-09-28",
                    "start_time": "09:00:00",
                    "end_time": "11:00:00"  # duree: 2h
                }
            ],
            "metadata": {
                "photos": ["https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80"],
                "duration_hours": 2
            }
        },
        {
            "title": "Livraison",
            "description": "Livraison de colis a domicile.",
            "type_code": "DELIVERY",
            "location": {
                "country": "Guinee",
                "city": "Matoto",
                "neighborhood": "Kipe"
            },
            "budget": 120000,  # GNF
            "publisher_id": "user-2",
            "status": "COMPLETED",  # terminee
            "work_days": [
                {
                    "day": "2025-09-18",
                    "start_time": "14:00:00",
                    "end_time": "15:00:00"  # duree: 1h
                }
            ],
            "metadata": {
                "photos": ["https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80"],
                "duration_hours": 1
            }
        },
        {
            "title": "Jardinage",
            "description": "Plantation de fleurs et entretien du potager.",
            "type_code": "GARDENING",
            "location": {
                "country": "Guinee",
                "city": "Dixinn",
                "neighborhood": "Landreah"
            },
            "budget": 100000,  # GNF
            "publisher_id": "user-3",
            "status": "COMPLETED",  # terminee
            "work_days": [
                {
                    "day": "2025-09-20",
                    "start_time": "08:00:00",
                    "end_time": "10:30:00"  # duree: 2.5h
                }
            ],
            "metadata": {
                "photos": ["https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?auto=format&fit=crop&w=400&q=80"],
                "duration_hours": 2.5
            }
        },
        {
            "title": "Informatique",
            "description": "Depannage et maintenance d'ordinateurs.",
            "type_code": "OTHER",  # Informatique -> OTHER car pas dans les types prédéfinis
            "location": {
                "country": "Guinee",
                "city": "Kaloum",
                "neighborhood": "Centre-ville"
            },
            "budget": 200000,  # GNF
            "publisher_id": "user-4",
            "status": "COMPLETED",  # terminee
            "work_days": [
                {
                    "day": "2025-09-22",
                    "start_time": "10:00:00",
                    "end_time": "12:00:00"  # duree: 2h
                }
            ],
            "metadata": {
                "photos": ["https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=400&q=80"],
                "duration_hours": 2,
                "specialization": "Informatique"
            }
        },
        {
            "title": "Menage",
            "description": "Nettoyage bureaux administratifs.",
            "type_code": "CLEANING",
            "location": {
                "country": "Guinee",
                "city": "Conakry",
                "neighborhood": "Kaloum"
            },
            "budget": 80000,  # GNF
            "publisher_id": "user-5",
            "status": "COMPLETED",  # terminee
            "work_days": [
                {
                    "day": "2025-09-15",
                    "start_time": "09:00:00",
                    "end_time": "10:30:00"  # duree: 1.5h
                }
            ],
            "metadata": {
                "photos": ["https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80"],
                "duration_hours": 1.5
            }
        }
    ]

    return missions


def load_fake_missions():
    """Charge les missions fictives dans la base de donnees"""

    print("\n" + "="*60)
    print("CHARGEMENT DES MISSIONS FICTIVES")
    print("="*60 + "\n")

    # Initialiser le repository
    repository = MissionRepository(MISSIONS_DATA_FILE)

    # Obtenir les missions converties
    missions_data = convert_fake_missions_to_system_format()

    print(f"📦 {len(missions_data)} missions a charger...\n")

    loaded_count = 0

    for mission_data in missions_data:
        try:
            # Creer l'objet AddressDto
            location = AddressDto(
                country=mission_data['location']['country'],
                city=mission_data['location']['city'],
                neighborhood=mission_data['location']['neighborhood']
            )

            # Creer les objets WorkDayDto
            work_days = []
            for wd in mission_data['work_days']:
                work_days.append(WorkDayDto(
                    day=wd['day'],
                    start_time=wd['start_time'],
                    end_time=wd['end_time']
                ))

            # Creer le modele de mission
            mission = MissionModel(
                title=mission_data['title'],
                description=mission_data['description'],
                type_code=mission_data['type_code'],
                location=location,
                budget=mission_data['budget'],
                publisher_id=mission_data['publisher_id'],
                work_days=work_days,
                status=mission_data['status']
            )

            # Sauvegarder
            repository.create(mission)

            loaded_count += 1
            print(f"✅ Mission chargee: {mission.title}")
            print(f"   ID: {mission.id}")
            print(f"   Type: {mission.type_code}")
            print(f"   Statut: {mission.status}")
            print(f"   Budget: {mission.budget} GNF")
            print(f"   Localisation: {location.city} - {location.neighborhood}")
            print()

        except Exception as e:
            print(f"❌ Erreur lors du chargement de '{mission_data['title']}': {str(e)}")
            print()

    print("="*60)
    print(f"✅ CHARGEMENT TERMINE: {loaded_count}/{len(missions_data)} missions chargees")
    print("="*60 + "\n")

    return loaded_count


def display_loaded_missions():
    """Affiche les missions chargees"""

    repository = MissionRepository(MISSIONS_DATA_FILE)
    missions = repository.find_all()

    print("\n" + "="*60)
    print("MISSIONS DANS LA BASE DE DONNEES")
    print("="*60 + "\n")

    if not missions:
        print("Aucune mission trouvee.")
        return

    print(f"Total: {len(missions)} mission(s)\n")

    # Grouper par statut
    by_status = {}
    for mission in missions:
        status = mission.status
        if status not in by_status:
            by_status[status] = []
        by_status[status].append(mission)

    for status, missions_list in by_status.items():
        print(f"\n📊 Statut: {status} ({len(missions_list)} mission(s))")
        print("-" * 60)
        for mission in missions_list:
            print(f"  • {mission.title}")
            print(f"    Type: {mission.type_code} | Budget: {mission.budget} GNF")
            print(f"    Ville: {mission.location.city}")

    print("\n" + "="*60 + "\n")


def clear_missions():
    """Vide toutes les missions (pour recommencer)"""

    print("\n⚠️  ATTENTION: Cette action va supprimer toutes les missions!")
    confirmation = input("Tapez 'OUI' pour confirmer: ")

    if confirmation.upper() == "OUI":
        with open(MISSIONS_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print("✅ Toutes les missions ont ete supprimees.\n")
    else:
        print("❌ Suppression annulee.\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_missions()
    elif len(sys.argv) > 1 and sys.argv[1] == "display":
        display_loaded_missions()
    else:
        # Charger les missions fictives
        load_fake_missions()

        # Afficher le resultat
        display_loaded_missions()
