"""
Script de test simple pour les nouveaux endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoints_info():
    """Affiche les informations sur les missions disponibles"""
    print("=" * 70)
    print("INFORMATIONS SUR LES MISSIONS")
    print("=" * 70)

    # Récupérer toutes les missions
    response = requests.get(f"{BASE_URL}/missions/")

    if response.status_code == 200:
        data = response.json()
        missions = data.get('data', [])

        print(f"\n✅ Total missions: {len(missions)}")

        # Compter par statut
        status_count = {}
        for mission in missions:
            status = mission.get('status', 'UNKNOWN')
            status_count[status] = status_count.get(status, 0) + 1

        print("\n📊 Répartition par statut:")
        for status, count in status_count.items():
            print(f"   • {status}: {count} mission(s)")

        # Afficher quelques missions PUBLISHED
        published = [m for m in missions if m.get('status') == 'PUBLISHED']
        if published:
            print(f"\n📋 Missions PUBLISHED disponibles pour acceptation:")
            for mission in published[:3]:
                print(f"   • {mission.get('title')} (ID: {mission.get('id')[:8]}...)")
                print(f"     Publisher: {mission.get('publisher_id')}")

        # Afficher quelques missions ASSIGNED
        assigned = [m for m in missions if m.get('status') == 'ASSIGNED']
        if assigned:
            print(f"\n📋 Missions ASSIGNED disponibles pour complétion:")
            for mission in assigned[:3]:
                print(f"   • {mission.get('title')} (ID: {mission.get('id')[:8]}...)")
                print(f"     Publisher: {mission.get('publisher_id')}")
                if 'worker_id' in mission:
                    print(f"     Worker: {mission.get('worker_id')}")

        print("\n" + "=" * 70)
        print("NOUVEAUX ENDPOINTS DISPONIBLES")
        print("=" * 70)
        print("\n1️⃣  Accepter une mission:")
        print(f"   POST {BASE_URL}/missions/<mission_id>/accept")
        print("   Headers: Authorization: Bearer <token>")
        print("   Conditions:")
        print("     - Mission doit être PUBLISHED")
        print("     - Utilisateur ne doit pas être le propriétaire")
        print("     - Change le statut vers ASSIGNED")

        print("\n2️⃣  Terminer une mission:")
        print(f"   POST {BASE_URL}/missions/<mission_id>/complete")
        print("   Headers: Authorization: Bearer <token>")
        print("   Conditions:")
        print("     - Mission doit être ASSIGNED")
        print("     - Utilisateur doit être le propriétaire OU le worker")
        print("     - Change le statut vers COMPLETED")

        print("\n💡 Les mêmes endpoints sont disponibles sur:")
        print(f"   - {BASE_URL}/api/missions/<mission_id>/accept")
        print(f"   - {BASE_URL}/api/missions/<mission_id>/complete")

        print("\n" + "=" * 70)
        print("POUR TESTER")
        print("=" * 70)
        print("\nÉtapes:")
        print("1. S'authentifier pour obtenir un token:")
        print(f'   POST {BASE_URL}/auth/login')
        print('   Body: {"email": "admin@example.com", "password": "<votre_password>"}')
        print("\n2. Accepter une mission PUBLISHED:")
        print('   POST {BASE_URL}/missions/<mission_id>/accept')
        print('   Headers: {"Authorization": "Bearer <token>"}')
        print("\n3. Terminer la mission acceptée:")
        print('   POST {BASE_URL}/missions/<mission_id>/complete')
        print('   Headers: {"Authorization": "Bearer <token>"}')

    else:
        print(f"❌ Erreur: {response.status_code}")

if __name__ == "__main__":
    test_endpoints_info()
