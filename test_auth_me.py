# Test de l'endpoint /auth/me
# Ce script teste la recuperation de l'utilisateur courant via token JWT

import requests
import json

BASE_URL = "http://localhost:5000"

def test_auth_me():
    print("\n" + "="*60)
    print("TEST DE L'ENDPOINT /auth/me")
    print("="*60)

    # 1. D'abord, on se connecte pour obtenir un token
    print("\n1. Connexion pour obtenir un token...")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }

    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    if login_response.status_code != 200:
        print("❌ Erreur lors de la connexion")
        print(f"Status Code: {login_response.status_code}")
        print(f"Response: {login_response.text}")

        # Essayons de creer l'utilisateur d'abord
        print("\n2. Creation d'un utilisateur de test...")
        register_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "password123",
            "phone_number": "+33600000000",
            "birth_date": "1990-01-01"
        }

        register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Status Code: {register_response.status_code}")

        # Reessayons de se connecter
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    if login_response.status_code == 200:
        login_result = login_response.json()
        print("✅ Connexion reussie")

        # Extraire le token
        access_token = login_result.get("data", {}).get("access_token")
        print(f"Token obtenu: {access_token[:50]}...")

        # 2. Tester l'endpoint /auth/me avec le token
        print("\n3. Test de l'endpoint /auth/me...")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Status Code: {me_response.status_code}")

        if me_response.status_code == 200:
            me_result = me_response.json()
            print("✅ Utilisateur courant recupere avec succes!")
            print("\nInformations de l'utilisateur:")
            print(json.dumps(me_result, indent=2, ensure_ascii=False))
        else:
            print("❌ Erreur lors de la recuperation de l'utilisateur")
            print(f"Response: {me_response.text}")

        # 3. Tester sans token (doit echouer)
        print("\n4. Test sans token (doit echouer)...")
        no_token_response = requests.get(f"{BASE_URL}/auth/me")
        print(f"Status Code: {no_token_response.status_code}")
        if no_token_response.status_code == 401:
            print("✅ Erreur 401 attendue (token manquant)")
        else:
            print(f"❌ Code inattendu: {no_token_response.status_code}")

        # 4. Tester avec un mauvais token (doit echouer)
        print("\n5. Test avec un token invalide (doit echouer)...")
        bad_headers = {
            "Authorization": "Bearer invalid.token.here"
        }
        bad_token_response = requests.get(f"{BASE_URL}/auth/me", headers=bad_headers)
        print(f"Status Code: {bad_token_response.status_code}")
        if bad_token_response.status_code == 401:
            print("✅ Erreur 401 attendue (token invalide)")
        else:
            print(f"❌ Code inattendu: {bad_token_response.status_code}")

    print("\n" + "="*60)
    print("FIN DES TESTS")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        test_auth_me()
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter au serveur")
        print("Assurez-vous que l'application Flask tourne sur http://localhost:5000")
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
