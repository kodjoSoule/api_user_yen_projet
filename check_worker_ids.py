import json

# Lire les missions
with open('data/missions.json', 'r', encoding='utf-8') as f:
    missions = json.load(f)

print("=" * 60)
print("VÉRIFICATION DES WORKER_ID")
print("=" * 60)

assigned_missions = [m for m in missions if m.get('status') == 'ASSIGNED']
completed_missions = [m for m in missions if m.get('status') == 'COMPLETED']

print(f"\n📊 Missions ASSIGNED: {len(assigned_missions)}")
for m in assigned_missions:
    worker_id = m.get('worker_id', 'NON DÉFINI')
    print(f"  • {m['title']}")
    print(f"    worker_id: {worker_id}")
    print(f"    publisher_id: {m['publisher_id']}")

print(f"\n📊 Missions COMPLETED: {len(completed_missions)}")
for m in completed_missions:
    worker_id = m.get('worker_id', 'NON DÉFINI')
    print(f"  • {m['title']}")
    print(f"    worker_id: {worker_id}")
    print(f"    publisher_id: {m['publisher_id']}")

print("\n" + "=" * 60)
