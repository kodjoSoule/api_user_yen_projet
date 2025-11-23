# Test des endpoints missions
# Ce script teste tous les endpoints du microservice missions

import requests
import json

BASE_URL = "http://localhost:5000"

def print_section(title):
    print("\n" + "="*60)
    print(title)
    print("="*60)

def test_missions():
    print_section("TEST DU MICROSERVICE MISSIONS")

    # Variables globales
    access_token = None
    mission_id = None

    # 1. Login pour obtenir un token
    print("\n1. Login pour obtenir un token...")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }

    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

        if login_response.status_code == 200:
            access_token = login_response.json()["data"]["access_token"]
            print(f"✅ Token obtenu: {access_token[:50]}...")
        else:
            print("❌ Erreur login, creation d'un utilisateur...")
            register_data = {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "password": "password123",
                "phone_number": "+33600000001",
                "birth_date": "1990-01-01"
            }
            requests.post(f"{BASE_URL}/auth/register", json=register_data)
            login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            access_token = login_response.json()["data"]["access_token"]
            print(f"✅ Utilisateur cree et token obtenu")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    headers = {"Authorization": f"Bearer {access_token}"}

    # 2. Creer une mission en brouillon
    print("\n2. Creation d'une mission en brouillon...")
    mission_data = {
        "title": "Nettoyage de bureau",
        "description": "Recherche personne pour nettoyer un bureau de 50m2",
        "type_code": "CLEANING",
        "location": {
            "country": "France",
            "city": "Paris",
            "neighborhood": "Marais"
        },
        "budget": 150.50,
        "publisher_id": "user-test-123",
        "publish": False,
        "work_days": [
            {
                "day": "2025-12-01",
                "start_time": "09:00:00",
                "end_time": "17:00:00"
            },
            {
                "day": "2025-12-02",
                "start_time": "09:00:00",
                "end_time": "13:00:00"
            }
        ]
    }

    create_response = requests.post(
        f"{BASE_URL}/api/missions/",
        json=mission_data,
        headers=headers
    )

    print(f"Status: {create_response.status_code}")
    if create_response.status_code == 201:
        result = create_response.json()
        mission_id = result["data"]["id"]
        print(f"✅ Mission creee (brouillon): {result['data']['title']}")
        print(f"   ID: {mission_id}")
        print(f"   Statut: {result['data']['status']}")
        print(f"   Budget: {result['data']['budget']} €")
    else:
        print(f"❌ Erreur: {create_response.text}")

    # 3. Recuperer toutes les missions
    print("\n3. Recuperation de toutes les missions...")
    all_missions_response = requests.get(f"{BASE_URL}/api/missions/")
    print(f"Status: {all_missions_response.status_code}")

    if all_missions_response.status_code == 200:
        missions = all_missions_response.json()["data"]
        print(f"✅ {len(missions)} mission(s) trouvee(s)")
        for m in missions:
            print(f"   - {m['title']} ({m['status']})")

    # 4. Recuperer une mission specifique
    if mission_id:
        print(f"\n4. Recuperation de la mission {mission_id}...")
        get_response = requests.get(f"{BASE_URL}/api/missions/{mission_id}")
        print(f"Status: {get_response.status_code}")

        if get_response.status_code == 200:
            mission = get_response.json()["data"]
            print(f"✅ Mission recuperee:")
            print(json.dumps(mission, indent=2, ensure_ascii=False))

    # 5. Rechercher des missions par filtres
    print("\n5. Recherche de missions par filtres...")
    filters = {
        "city": "Paris",
        "budget_min": 100,
        "budget_max": 200
    }

    search_response = requests.post(
        f"{BASE_URL}/api/missions/search",
        json=filters
    )
    print(f"Status: {search_response.status_code}")

    if search_response.status_code == 200:
        filtered = search_response.json()["data"]
        print(f"✅ {len(filtered)} mission(s) trouvee(s) avec les filtres")
        for m in filtered:
            print(f"   - {m['title']} a {m['location']['city']}")

    # 6. Publier la mission
    if mission_id:
        print(f"\n6. Publication de la mission {mission_id}...")
        publish_response = requests.post(
            f"{BASE_URL}/api/missions/{mission_id}/publish",
            headers=headers
        )
        print(f"Status: {publish_response.status_code}")

        if publish_response.status_code == 200:
            published = publish_response.json()["data"]
            print(f"✅ Mission publiee!")
            print(f"   Nouveau statut: {published['status']}")
        else:
            print(f"⚠️  Erreur: {publish_response.json()['message']}")

    # 7. Creer une mission publiee directement
    print("\n7. Creation d'une mission publiee directement...")
    mission_data_2 = {
        "title": "Livraison de colis",
        "description": "Livraison urgente d'un colis",
        "type_code": "DELIVERY",
        "location": {
            "country": "France",
            "city": "Lyon",
            "neighborhood": "Bellecour"
        },
        "budget": 50.0,
        "publisher_id": "user-test-123",
        "publish": True,
        "work_days": [
            {
                "day": "2025-11-25",
                "start_time": "14:00:00",
                "end_time": "16:00:00"
            }
        ]
    }

    create_response_2 = requests.post(
        f"{BASE_URL}/api/missions/",
        json=mission_data_2,
        headers=headers
    )

    if create_response_2.status_code == 201:
        result = create_response_2.json()
        print(f"✅ Mission creee et publiee: {result['data']['title']}")
        print(f"   Statut: {result['data']['status']}")

    # 8. Rechercher les missions publiees
    print("\n8. Recherche des missions publiees...")
    published_filters = {"status": "PUBLISHED"}

    published_response = requests.post(
        f"{BASE_URL}/api/missions/search",
        json=published_filters
    )

    if published_response.status_code == 200:
        published_missions = published_response.json()["data"]
        print(f"✅ {len(published_missions)} mission(s) publiee(s)")
        for m in published_missions:
            print(f"   - {m['title']} ({m['type']['name']})")

    print("\n" + "="*60)
    print("FIN DES TESTS")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        test_missions()
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter au serveur")
        print("Assurez-vous que l'application Flask tourne sur http://localhost:5000")
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        import traceback
        traceback.print_exc()
