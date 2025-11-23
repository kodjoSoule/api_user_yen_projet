# 📖 Exemples d'utilisation de l'API

Ce document contient des exemples pratiques d'utilisation de l'API Users Microservice.

## Table des matières
1. [Inscription et connexion](#inscription-et-connexion)
2. [Gestion du profil](#gestion-du-profil)
3. [Recherche d'utilisateurs](#recherche-dutilisateurs)
4. [Upload de fichiers](#upload-de-fichiers)
5. [Cas d'usage complets](#cas-dusage-complets)

---

## Inscription et connexion

### 1. Créer un compte utilisateur PARTICULIER

**Requête:**
```http
POST /users/
Content-Type: application/json

{
  "first_name": "Marie",
  "last_name": "Martin",
  "birth_date": "1995-06-20",
  "email": "marie.martin@example.com",
  "phone_number": "+33698765432",
  "password": "MonMotDePasse123!",
  "user_type": "PARTICULIER",
  "country": "France",
  "address": "45 Avenue des Champs-Élysées, 75008 Paris"
}
```

**Réponse (201 Created):**
```json
{
  "success": true,
  "message": "Utilisateur créé avec succès",
  "data": {
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "first_name": "Marie",
    "last_name": "Martin",
    "email": "marie.martin@example.com",
    "user_type": "PARTICULIER",
    "is_active": false,
    "is_verified": false,
    "created_at": "2025-11-23T10:30:00.000Z"
  }
}
```

### 2. Créer un compte ENTREPRISE

**Requête:**
```http
POST /users/
Content-Type: application/json

{
  "first_name": "Tech",
  "last_name": "Solutions SA",
  "birth_date": "2010-01-01",
  "email": "contact@techsolutions.fr",
  "phone_number": "+33144556677",
  "password": "EntrepriseSecure2024!",
  "user_type": "ENTREPRISE",
  "country": "France",
  "address": "10 Rue de la Innovation, 69001 Lyon"
}
```

### 3. Se connecter avec email

**Requête:**
```http
POST /users/verify-users-creds
Content-Type: application/json

{
  "email": "marie.martin@example.com",
  "password": "MonMotDePasse123!"
}
```

**Réponse (200 OK):**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTFiMmMzZDQtZTVmNi03ODkwLWFiY2QtZWYxMjM0NTY3ODkwIiwiZW1haWwiOiJtYXJpZS5tYXJ0aW5AZXhhbXBsZS5jb20iLCJleHAiOjE3MDA3NDE0MDAsImlhdCI6MTcwMDczNzgwMH0.Xy9s8qk3JmN8K5vL2wP4rT6uY1aZ3bC4dE5fG6hI7jK8",
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "first_name": "Marie",
    "last_name": "Martin",
    "email": "marie.martin@example.com",
    "last_login": "2025-11-23T11:00:00.000Z"
  }
}
```

### 4. Se connecter avec numéro de téléphone

**Requête:**
```http
POST /users/verify-users-creds
Content-Type: application/json

{
  "phone_number": "+33698765432",
  "password": "MonMotDePasse123!"
}
```

---

## Gestion du profil

### 5. Consulter son profil

**Requête:**
```http
GET /users/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Réponse:**
```json
{
  "success": true,
  "data": {
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "first_name": "Marie",
    "last_name": "Martin",
    "birth_date": "1995-06-20",
    "email": "marie.martin@example.com",
    "phone_number": "+33698765432",
    "user_type": "PARTICULIER",
    "country": "France",
    "address": "45 Avenue des Champs-Élysées, 75008 Paris",
    "photo_url": null,
    "is_active": false,
    "is_verified": false,
    "is_completed": false,
    "is_deleted": false,
    "created_at": "2025-11-23T10:30:00.000Z",
    "updated_at": null,
    "last_login": "2025-11-23T11:00:00.000Z",
    "last_password_change": "2025-11-23T10:30:00.000Z"
  }
}
```

### 6. Mettre à jour son profil

**Requête:**
```http
PUT /users/a1b2c3d4-e5f6-7890-abcd-ef1234567890
Content-Type: application/json

{
  "first_name": "Marie-Claire",
  "last_name": "Martin-Dubois",
  "birth_date": "1995-06-20",
  "email": "marie.martin@example.com",
  "phone_number": "+33698765432",
  "user_type": "PARTICULIER",
  "country": "France",
  "address": "78 Boulevard Saint-Germain, 75006 Paris"
}
```

**Réponse:**
```json
{
  "success": true,
  "message": "Utilisateur mis à jour avec succès",
  "data": {
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "first_name": "Marie-Claire",
    "last_name": "Martin-Dubois",
    "address": "78 Boulevard Saint-Germain, 75006 Paris",
    "updated_at": "2025-11-23T11:15:00.000Z"
  }
}
```

### 7. Changer son mot de passe

**Requête:**
```http
PUT /users/a1b2c3d4-e5f6-7890-abcd-ef1234567890
Content-Type: application/json

{
  "first_name": "Marie-Claire",
  "last_name": "Martin-Dubois",
  "birth_date": "1995-06-20",
  "email": "marie.martin@example.com",
  "phone_number": "+33698765432",
  "password": "NouveauMotDePasse456!",
  "user_type": "PARTICULIER",
  "country": "France",
  "address": "78 Boulevard Saint-Germain, 75006 Paris"
}
```

---

## Recherche d'utilisateurs

### 8. Rechercher par email

**Requête:**
```http
GET /users/email/marie.martin@example.com
```

**Réponse:**
```json
{
  "success": true,
  "data": {
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "first_name": "Marie-Claire",
    "email": "marie.martin@example.com"
  }
}
```

### 9. Rechercher par téléphone

**Requête:**
```http
GET /users/phone_number/+33698765432
```

### 10. Lister tous les utilisateurs

**Requête:**
```http
GET /users/all
```

**Réponse:**
```json
{
  "success": true,
  "data": [
    {
      "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "first_name": "Marie-Claire",
      "last_name": "Martin-Dubois",
      "email": "marie.martin@example.com",
      "user_type": "PARTICULIER"
    },
    {
      "user_id": "b2c3d4e5-f6g7-8901-bcde-fg2345678901",
      "first_name": "Tech",
      "last_name": "Solutions SA",
      "email": "contact@techsolutions.fr",
      "user_type": "ENTREPRISE"
    }
  ]
}
```

---

## Upload de fichiers

### 11. Upload d'une photo de profil

**Requête (multipart/form-data):**
```http
POST /users/upload-profile-photo
Content-Type: multipart/form-data

photo: [fichier image]
user_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Exemple avec cURL:**
```bash
curl -X POST http://localhost:5000/users/upload-profile-photo \
  -F "photo=@/chemin/vers/photo.jpg" \
  -F "user_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

**Réponse:**
```json
{
  "success": true,
  "message": "Photo de profil mise à jour avec succès",
  "data": {
    "photo_url": "http://localhost:5000/uploads/f1e2d3c4-b5a6-7890-cdef-123456789abc.jpg"
  }
}
```

---

## Cas d'usage complets

### Scénario 1 : Inscription complète d'un utilisateur

```javascript
// Étape 1 : Créer le compte
const createResponse = await fetch('http://localhost:5000/users/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    first_name: "Sophie",
    last_name: "Bernard",
    birth_date: "1992-03-15",
    email: "sophie.bernard@example.com",
    phone_number: "+33687654321",
    password: "SecurePass789!",
    user_type: "PARTICULIER",
    country: "France",
    address: "12 Rue Victor Hugo, Marseille"
  })
});

const userData = await createResponse.json();
const userId = userData.data.user_id;

// Étape 2 : Upload photo de profil
const formData = new FormData();
formData.append('photo', photoFile);
formData.append('user_id', userId);

const photoResponse = await fetch('http://localhost:5000/users/upload-profile-photo', {
  method: 'POST',
  body: formData
});

// Étape 3 : Se connecter
const loginResponse = await fetch('http://localhost:5000/users/verify-users-creds', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: "sophie.bernard@example.com",
    password: "SecurePass789!"
  })
});

const loginData = await loginResponse.json();
const token = loginData.data.token;

// Utiliser le token pour les requêtes authentifiées
const authHeaders = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

### Scénario 2 : Gestion d'entreprise

```python
import requests

BASE_URL = "http://localhost:5000"

# 1. Créer le compte entreprise
company_data = {
    "first_name": "Innovation",
    "last_name": "Digital SARL",
    "birth_date": "2015-09-01",
    "email": "contact@innovation-digital.fr",
    "phone_number": "+33155443322",
    "password": "CompanySecure2024!",
    "user_type": "ENTREPRISE",
    "country": "France",
    "address": "250 Rue de la Tech, Lille"
}

response = requests.post(f"{BASE_URL}/users/", json=company_data)
company_id = response.json()['data']['user_id']

# 2. Connexion
login_data = {
    "email": "contact@innovation-digital.fr",
    "password": "CompanySecure2024!"
}

login_response = requests.post(
    f"{BASE_URL}/users/verify-users-creds",
    json=login_data
)

token = login_response.json()['data']['token']

# 3. Mettre à jour les informations
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

update_data = {
    **company_data,
    "address": "250 Rue de la Tech, Parc d'Innovation, 59000 Lille"
}

requests.put(f"{BASE_URL}/users/{company_id}", json=update_data, headers=headers)
```

### Scénario 3 : Recherche et filtrage

```python
import requests

BASE_URL = "http://localhost:5000"

# Récupérer tous les utilisateurs
all_users = requests.get(f"{BASE_URL}/users/all").json()['data']

# Filtrer les entreprises
entreprises = [u for u in all_users if u['user_type'] == 'ENTREPRISE']

# Filtrer les particuliers
particuliers = [u for u in all_users if u['user_type'] == 'PARTICULIER']

# Recherche spécifique par email
user = requests.get(f"{BASE_URL}/users/email/marie.martin@example.com").json()['data']

print(f"Trouvé: {user['first_name']} {user['last_name']}")
```

---

## Gestion des erreurs

### Erreur : Email déjà utilisé

**Requête:**
```http
POST /users/
Content-Type: application/json

{
  "email": "marie.martin@example.com",
  ...
}
```

**Réponse (400 Bad Request):**
```json
{
  "success": false,
  "message": "Un utilisateur avec cet email existe déjà"
}
```

### Erreur : Identifiants incorrects

**Requête:**
```http
POST /users/verify-users-creds
Content-Type: application/json

{
  "email": "marie.martin@example.com",
  "password": "MauvaisMotDePasse"
}
```

**Réponse (401 Unauthorized):**
```json
{
  "success": false,
  "message": "Identifiants incorrects"
}
```

### Erreur : Utilisateur non trouvé

**Requête:**
```http
GET /users/uuid-inexistant
```

**Réponse (404 Not Found):**
```json
{
  "success": false,
  "message": "Utilisateur non trouvé"
}
```

---

## Notes importantes

1. **Validation des données** : Tous les champs requis doivent être fournis lors de la création
2. **Format de date** : `AAAA-MM-JJ` ou `JJ/MM/AAAA`
3. **Types d'utilisateurs** : `PARTICULIER` ou `ENTREPRISE` (sensible à la casse)
4. **Authentification** : Email OU téléphone (au moins un des deux)
5. **Tokens JWT** : Valides pendant 60 minutes par défaut
6. **Photos** : Extensions autorisées : PNG, JPG, JPEG, GIF, WEBP

---

## Ressources supplémentaires

- Documentation complète : `README.md`
- Architecture : `ARCHITECTURE.md`
- Guide rapide : `QUICKSTART.md`
- Tests automatisés : `test_api.py`
