"""
Script de test pour l'endpoint /missions/me
"""
import requests
import json

BASE_URL = "http://localhost:5000"

# Couleurs pour l'affichage
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_separator():
    print("=" * 70)

def print_test_header(test_name):
    print(f"\n{BLUE}📝 {test_name}{RESET}")
    print("-" * 70)

def login_user(email, password):
    """Authentifie un utilisateur et retourne le token"""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            token = data.get('data', {}).get('access_token')
            user_id = data.get('data', {}).get('user', {}).get('user_id')
            print(f"{GREEN}✅ Login réussi pour {email}{RESET}")
            print(f"   User ID: {user_id}")
            return token, user_id

    print(f"{RED}❌ Erreur login pour {email}{RESET}")
    return None, None

def get_headers(token):
    """Retourne les headers avec le token"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def test_get_my_missions():
    """Test: Récupérer mes missions"""
    print_test_header("Test 1: GET /missions/me - Mes missions")

    # Login
    token, user_id = login_user("admin@example.com", "admin")
    if not token:
        print(f"{RED}❌ Impossible de se connecter{RESET}")
        return

    # Appeler l'endpoint /missions/me
    url = f"{BASE_URL}/missions/me"
    response = requests.get(url, headers=get_headers(token))

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"{GREEN}✅ Succès!{RESET}")
        print(f"Message: {data.get('message')}")

        mission_data = data.get('data', {})
        created = mission_data.get('created_missions', [])
        accepted = mission_data.get('accepted_missions', [])

        print(f"\n{BLUE}📊 Statistiques:{RESET}")
        print(f"   Missions créées: {mission_data.get('total_created', 0)}")
        print(f"   Missions acceptées: {mission_data.get('total_accepted', 0)}")
        print(f"   Total: {mission_data.get('total', 0)}")

        if created:
            print(f"\n{BLUE}📝 Missions créées par moi:{RESET}")
            for mission in created:
                print(f"   • {mission['title']}")
                print(f"     Type: {mission.get('type', {}).get('name', 'N/A')}")
                print(f"     Statut: {mission['status']}")
                print(f"     Budget: {mission['budget']} GNF")
        else:
            print(f"\n{YELLOW}⚠️  Aucune mission créée{RESET}")

        if accepted:
            print(f"\n{BLUE}✅ Missions acceptées par moi:{RESET}")
            for mission in accepted:
                print(f"   • {mission['title']}")
                print(f"     Type: {mission.get('type', {}).get('name', 'N/A')}")
                print(f"     Statut: {mission['status']}")
                print(f"     Budget: {mission['budget']} GNF")
        else:
            print(f"\n{YELLOW}⚠️  Aucune mission acceptée{RESET}")
    else:
        print(f"{RED}❌ Erreur{RESET}")
        try:
            error_data = response.json()
            print(f"Message: {error_data.get('message')}")
        except:
            print(response.text)

def test_get_my_missions_alias():
    """Test: Récupérer mes missions via l'alias"""
    print_test_header("Test 2: GET /api/missions/me - Mes missions (endpoint standard)")

    # Login
    token, user_id = login_user("admin@example.com", "admin")
    if not token:
        print(f"{RED}❌ Impossible de se connecter{RESET}")
        return

    # Appeler l'endpoint /api/missions/me
    url = f"{BASE_URL}/api/missions/me"
    response = requests.get(url, headers=get_headers(token))

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"{GREEN}✅ Succès!{RESET}")
        mission_data = data.get('data', {})
        print(f"Total missions: {mission_data.get('total', 0)}")
        print(f"   Créées: {mission_data.get('total_created', 0)}")
        print(f"   Acceptées: {mission_data.get('total_accepted', 0)}")
    else:
        print(f"{RED}❌ Erreur{RESET}")

def test_workflow_accept_and_check():
    """Test: Accepter une mission puis vérifier qu'elle apparaît dans /me"""
    print_test_header("Test 3: Workflow - Accepter une mission puis vérifier /me")

    # Login
    token, user_id = login_user("admin@example.com", "admin")
    if not token:
        return

    # Trouver une mission PUBLISHED
    url = f"{BASE_URL}/missions/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        missions = data.get('data', [])
        published_missions = [m for m in missions if m.get('status') == 'PUBLISHED']

        if published_missions:
            mission = published_missions[0]
            mission_id = mission['id']
            print(f"\n{BLUE}Mission trouvée: {mission['title']}{RESET}")

            # Accepter la mission
            accept_url = f"{BASE_URL}/missions/{mission_id}/accept"
            accept_response = requests.post(accept_url, headers=get_headers(token))

            if accept_response.status_code == 200:
                print(f"{GREEN}✅ Mission acceptée{RESET}")

                # Vérifier dans /missions/me
                me_url = f"{BASE_URL}/missions/me"
                me_response = requests.get(me_url, headers=get_headers(token))

                if me_response.status_code == 200:
                    me_data = me_response.json()
                    accepted = me_data.get('data', {}).get('accepted_missions', [])

                    # Chercher la mission dans les missions acceptées
                    found = any(m['id'] == mission_id for m in accepted)

                    if found:
                        print(f"{GREEN}✅ Mission trouvée dans les missions acceptées!{RESET}")
                    else:
                        print(f"{YELLOW}⚠️  Mission non trouvée dans /me{RESET}")
            else:
                result = accept_response.json()
                print(f"{YELLOW}⚠️  Impossible d'accepter: {result.get('message')}{RESET}")
        else:
            print(f"{YELLOW}⚠️  Aucune mission PUBLISHED disponible{RESET}")

def main():
    print_separator()
    print(f"{GREEN}TEST ENDPOINT /missions/me{RESET}")
    print_separator()

    # Test 1: Récupérer mes missions
    test_get_my_missions()

    # Test 2: Endpoint standard
    test_get_my_missions_alias()

    # Test 3: Workflow complet
    test_workflow_accept_and_check()

    print_separator()
    print(f"{GREEN}FIN DES TESTS{RESET}")
    print_separator()

if __name__ == "__main__":
    main()
