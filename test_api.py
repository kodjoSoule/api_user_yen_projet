"""
Script de test pour l'API Users Microservice
Teste tous les endpoints principaux
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_create_user():
    """Test de création d'utilisateur"""
    print("\n=== TEST: Création d'utilisateur ===")

    user_data = {
        "first_name": "Jean",
        "last_name": "Dupont",
        "birth_date": "1990-01-15",
        "email": "jean.dupont@test.com",
        "phone_number": "+33612345678",
        "password": "SecurePass123!",
        "user_type": "PARTICULIER",
        "country": "France",
        "address": "123 Rue de la Paix, Paris"
    }

    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 201:
        return response.json()['data']['user_id']
    return None


def test_get_all_users():
    """Test de récupération de tous les utilisateurs"""
    print("\n=== TEST: Récupération de tous les utilisateurs ===")

    response = requests.get(f"{BASE_URL}/users/all")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Nombre d'utilisateurs: {len(data['data'])}")


def test_get_user_by_id(user_id):
    """Test de récupération d'un utilisateur par ID"""
    print(f"\n=== TEST: Récupération utilisateur par ID: {user_id} ===")

    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_user_by_email():
    """Test de récupération d'un utilisateur par email"""
    print("\n=== TEST: Récupération utilisateur par email ===")

    email = "jean.dupont@test.com"
    response = requests.get(f"{BASE_URL}/users/email/{email}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_verify_credentials():
    """Test de vérification des identifiants"""
    print("\n=== TEST: Vérification des identifiants ===")

    login_data = {
        "email": "jean.dupont@test.com",
        "password": "SecurePass123!"
    }

    response = requests.post(f"{BASE_URL}/users/verify-users-creds", json=login_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")

    if 'data' in result and 'token' in result['data']:
        return result['data']['token']
    return None


def test_update_user(user_id):
    """Test de mise à jour d'un utilisateur"""
    print(f"\n=== TEST: Mise à jour utilisateur {user_id} ===")

    update_data = {
        "first_name": "Jean-Michel",
        "last_name": "Dupont",
        "birth_date": "1990-01-15",
        "email": "jean.dupont@test.com",
        "phone_number": "+33612345678",
        "user_type": "PARTICULIER",
        "country": "France",
        "address": "456 Avenue des Champs-Élysées, Paris"
    }

    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_delete_user(user_id):
    """Test de suppression d'un utilisateur"""
    print(f"\n=== TEST: Suppression utilisateur {user_id} ===")

    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    print("=" * 50)
    print("TESTS DE L'API USERS MICROSERVICE")
    print("=" * 50)
    print(f"URL de base: {BASE_URL}")
    print("\nAssurez-vous que l'API est lancée (python app.py)")
    print("=" * 50)

    # Exécution des tests
    user_id = test_create_user()

    if user_id:
        test_get_all_users()
        test_get_user_by_id(user_id)
        test_get_user_by_email()
        token = test_verify_credentials()
        test_update_user(user_id)
        # test_delete_user(user_id)  # Commenté pour ne pas supprimer

        print("\n" + "=" * 50)
        print("TESTS TERMINÉS")
        print("=" * 50)
        if token:
            print(f"\n🔑 Token JWT généré: {token[:50]}...")
    else:
        print("\n❌ Échec de la création de l'utilisateur - Tests interrompus")
