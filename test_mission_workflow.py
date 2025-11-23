"""
Script de test pour les endpoints d'acceptation et completion de missions
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
            print(f"{GREEN}✅ Login réussi pour {email}{RESET}")
            return token

    print(f"{RED}❌ Erreur login pour {email}{RESET}")
    return None

def get_headers(token):
    """Retourne les headers avec le token"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def test_accept_mission():
    """Test: Accepter une mission"""
    print_test_header("Test 1: Accepter une mission PUBLISHED")

    # Login utilisateur qui va accepter la mission
    worker_token = login_user("admin@example.com", "admin")
    if not worker_token:
        print(f"{RED}❌ Impossible de se connecter{RESET}")
        print(f"{YELLOW}ℹ️  Essayez de créer des utilisateurs de test d'abord{RESET}")
        return None

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
            print(f"{BLUE}Mission trouvée: {mission['title']} (ID: {mission_id}){RESET}")

            # Accepter la mission
            accept_url = f"{BASE_URL}/missions/{mission_id}/accept"
            accept_response = requests.post(accept_url, headers=get_headers(worker_token))

            print(f"Status: {accept_response.status_code}")
            result = accept_response.json()

            if accept_response.status_code == 200:
                print(f"{GREEN}✅ Mission acceptée avec succès!{RESET}")
                print(f"Message: {result.get('message')}")
                accepted_mission = result.get('data', {})
                print(f"Nouveau statut: {accepted_mission.get('status')}")
                return mission_id
            else:
                print(f"{RED}❌ Erreur: {result.get('message')}{RESET}")
        else:
            print(f"{YELLOW}⚠️  Aucune mission PUBLISHED disponible{RESET}")

    return None

def test_accept_own_mission():
    """Test: Essayer d'accepter sa propre mission"""
    print_test_header("Test 2: Essayer d'accepter sa propre mission (doit échouer)")

    # Login utilisateur qui est propriétaire
    owner_token = login_user("admin@example.com", "admin")
    if not owner_token:
        return

    # Trouver une mission dont on est le propriétaire
    url = f"{BASE_URL}/missions/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        missions = data.get('data', [])
        # Trouver une mission PUBLISHED de l'utilisateur alpha (client-alpha-conde)
        own_missions = [m for m in missions if m.get('status') == 'PUBLISHED' and 'alpha' in m.get('publisher_id', '').lower()]

        if own_missions:
            mission = own_missions[0]
            mission_id = mission['id']
            print(f"{BLUE}Mission: {mission['title']} (ID: {mission_id}){RESET}")

            # Essayer d'accepter
            accept_url = f"{BASE_URL}/missions/{mission_id}/accept"
            accept_response = requests.post(accept_url, headers=get_headers(owner_token))

            print(f"Status: {accept_response.status_code}")
            result = accept_response.json()

            if accept_response.status_code == 403:
                print(f"{GREEN}✅ Refus correct: {result.get('message')}{RESET}")
            else:
                print(f"{RED}❌ Comportement inattendu{RESET}")
                print(f"Message: {result.get('message')}")

def test_complete_mission(mission_id=None):
    """Test: Terminer une mission"""
    print_test_header("Test 3: Terminer une mission ASSIGNED")

    if not mission_id:
        # Trouver une mission ASSIGNED
        url = f"{BASE_URL}/missions/"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            missions = data.get('data', [])
            assigned_missions = [m for m in missions if m.get('status') == 'ASSIGNED']

            if assigned_missions:
                mission_id = assigned_missions[0]['id']
            else:
                print(f"{YELLOW}⚠️  Aucune mission ASSIGNED disponible{RESET}")
                return

    # Login utilisateur (travailleur qui a accepté la mission)
    worker_token = login_user("admin@example.com", "admin")
    if not worker_token:
        return

    print(f"{BLUE}Mission ID: {mission_id}{RESET}")

    # Terminer la mission
    complete_url = f"{BASE_URL}/missions/{mission_id}/complete"
    complete_response = requests.post(complete_url, headers=get_headers(worker_token))

    print(f"Status: {complete_response.status_code}")
    result = complete_response.json()

    if complete_response.status_code == 200:
        print(f"{GREEN}✅ Mission terminée avec succès!{RESET}")
        print(f"Message: {result.get('message')}")
        completed_mission = result.get('data', {})
        print(f"Nouveau statut: {completed_mission.get('status')}")
    else:
        print(f"{RED}❌ Erreur: {result.get('message')}{RESET}")

def test_complete_without_accept():
    """Test: Essayer de terminer une mission non assignée"""
    print_test_header("Test 4: Essayer de terminer une mission PUBLISHED (doit échouer)")

    worker_token = login_user("admin@example.com", "admin")
    if not worker_token:
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
            print(f"{BLUE}Mission: {mission['title']} (ID: {mission_id}){RESET}")

            # Essayer de terminer
            complete_url = f"{BASE_URL}/missions/{mission_id}/complete"
            complete_response = requests.post(complete_url, headers=get_headers(worker_token))

            print(f"Status: {complete_response.status_code}")
            result = complete_response.json()

            if complete_response.status_code == 400:
                print(f"{GREEN}✅ Refus correct: {result.get('message')}{RESET}")
            else:
                print(f"{RED}❌ Comportement inattendu{RESET}")
                print(f"Message: {result.get('message')}")

def test_workflow_complet():
    """Test: Workflow complet - Accepter puis terminer"""
    print_test_header("Test 5: Workflow complet (Accept → Complete)")

    # Étape 1: Accepter une mission
    mission_id = test_accept_mission()

    if mission_id:
        print(f"\n{BLUE}Passage à l'étape suivante...{RESET}\n")
        # Étape 2: Terminer la mission acceptée
        test_complete_mission(mission_id)

def main():
    print_separator()
    print(f"{GREEN}TEST DES WORKFLOWS DE MISSIONS{RESET}")
    print_separator()

    # Test 1: Accepter une mission
    accepted_mission_id = test_accept_mission()

    # Test 2: Essayer d'accepter sa propre mission
    test_accept_own_mission()

    # Test 3: Terminer une mission
    if accepted_mission_id:
        test_complete_mission(accepted_mission_id)
    else:
        test_complete_mission()

    # Test 4: Essayer de terminer sans accepter
    test_complete_without_accept()

    print_separator()
    print(f"{GREEN}FIN DES TESTS{RESET}")
    print_separator()

if __name__ == "__main__":
    main()
