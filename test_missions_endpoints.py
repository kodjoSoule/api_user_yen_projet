"""
Script de test pour les endpoints missions
Teste les deux URLs: /api/missions et /missions
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_missions_endpoints():
    """Teste les différents endpoints missions"""

    print("\n" + "="*70)
    print("TEST DES ENDPOINTS MISSIONS")
    print("="*70 + "\n")

    # Test 1: GET /api/missions/
    print("📝 Test 1: GET /api/missions/")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/api/missions/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Succès! {len(data.get('data', []))} missions trouvées")
            print(f"Message: {data.get('message', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    print()

    # Test 2: GET /missions/
    print("📝 Test 2: GET /missions/ (sans /api)")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/missions/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Succès! {len(data.get('data', []))} missions trouvées")
            print(f"Message: {data.get('message', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    print()

    # Test 3: GET /missions/user/{user_id}
    user_id = "user-1"
    print(f"📝 Test 3: GET /missions/user/{user_id}")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/missions/user/{user_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            missions = data.get('data', [])
            print(f"✅ Succès! {len(missions)} mission(s) trouvée(s) pour user_id={user_id}")
            print(f"Message: {data.get('message', 'N/A')}")

            if missions:
                print("\nDétails des missions:")
                for i, mission in enumerate(missions, 1):
                    print(f"  {i}. {mission.get('title', 'N/A')}")
                    print(f"     Type: {mission.get('type', {}).get('name', 'N/A')}")
                    print(f"     Budget: {mission.get('budget', 'N/A')} GNF")
                    print(f"     Statut: {mission.get('status', 'N/A')}")
                    location = mission.get('location', {})
                    print(f"     Lieu: {location.get('city', 'N/A')} - {location.get('neighborhood', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    print()

    # Test 4: GET /missions/user/{user_id} (avec un user_id qui n'existe pas)
    fake_user_id = "e58119b7-a28e-446c-9cd9-bf90a9733ba0"
    print(f"📝 Test 4: GET /missions/user/{fake_user_id} (user inexistant)")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/missions/user/{fake_user_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            missions = data.get('data', [])
            print(f"✅ Succès! {len(missions)} mission(s) trouvée(s)")
            print(f"Message: {data.get('message', 'N/A')}")
            if len(missions) == 0:
                print("   ℹ️  Aucune mission pour cet utilisateur (normal)")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    print()

    # Test 5: Récupérer toutes les missions et afficher les publisher_id disponibles
    print("📝 Test 5: Afficher tous les publisher_id disponibles")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/missions/")
        if response.status_code == 200:
            data = response.json()
            missions = data.get('data', [])

            publisher_ids = set()
            for mission in missions:
                publisher_ids.add(mission.get('publisher_id', 'N/A'))

            print(f"✅ Publisher IDs trouvés:")
            for pid in sorted(publisher_ids):
                count = sum(1 for m in missions if m.get('publisher_id') == pid)
                print(f"   • {pid}: {count} mission(s)")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    print()

    # Test 6: Tester /missions/user/{user_id} pour chaque publisher trouvé
    print("📝 Test 6: Tester /missions/user/{user_id} pour chaque publisher")
    print("-" * 70)
    try:
        # Récupérer d'abord la liste des publishers
        response = requests.get(f"{BASE_URL}/missions/")
        if response.status_code == 200:
            data = response.json()
            missions = data.get('data', [])

            publisher_ids = set()
            for mission in missions:
                publisher_ids.add(mission.get('publisher_id', 'N/A'))

            # Tester chaque publisher
            print(f"✅ Test de {len(publisher_ids)} publisher(s):\n")
            for pid in sorted(publisher_ids):
                response = requests.get(f"{BASE_URL}/missions/user/{pid}")
                if response.status_code == 200:
                    data = response.json()
                    missions = data.get('data', [])
                    print(f"   • {pid}: {len(missions)} mission(s)")
                    for mission in missions:
                        print(f"      - {mission.get('title', 'N/A')} ({mission.get('status', 'N/A')})")
                else:
                    print(f"   • {pid}: ❌ Erreur {response.status_code}")
        else:
            print(f"❌ Erreur lors de la récupération des publishers")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    print()

    print("="*70)
    print("FIN DES TESTS")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_missions_endpoints()
