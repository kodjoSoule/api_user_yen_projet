"""Script de débogage pour tester l'attribut worker_id"""
import sys
sys.path.insert(0, '.')

from services.mission_service import MissionService
from repositories.mission_repository import MissionRepository

# Initialiser le service
repo = MissionRepository('data/missions.json')
service = MissionService(repo)

# Récupérer toutes les missions
all_missions = service.get_all_missions()

user_id = "e58119b7-a28e-446c-9cd9-bf90a9733ba0"

print("=" * 60)
print("DEBUG: Vérification des missions")
print("=" * 60)

print(f"\nTotal missions: {len(all_missions)}")
print(f"User ID à chercher: {user_id}\n")

# Tester les missions acceptées
accepted_count = 0
for m in all_missions:
    has_attr = hasattr(m, 'worker_id')
    worker_id_value = getattr(m, 'worker_id', 'NO_ATTR')
    matches = worker_id_value == user_id if has_attr else False

    # Debug: afficher toutes les missions avec leur worker_id
    status_icon = "✅" if matches else "•"
    print(f"{status_icon} {m.title[:40]}")
    print(f"   hasattr(worker_id): {has_attr}")
    print(f"   worker_id value: {worker_id_value}")
    print(f"   matches: {matches}")
    print(f"   status: {m.status}")

    if matches:
        accepted_count += 1

print(f"\n📊 Résultat: {accepted_count} mission(s) acceptée(s) par {user_id}")
print("=" * 60)
