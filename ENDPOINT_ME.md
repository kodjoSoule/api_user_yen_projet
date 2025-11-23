# 🔐 Endpoint /auth/me - Documentation

## Description

L'endpoint `/auth/me` permet de récupérer les informations de l'utilisateur actuellement authentifié à partir de son token JWT.

## Informations générales

- **URL** : `/auth/me`
- **Méthode HTTP** : `GET`
- **Authentification requise** : ✅ Oui (Bearer Token)
- **Tag Swagger** : EQOS : Authentification

## En-têtes requis

```http
Authorization: Bearer <access_token>
```

Le token doit être au format `Bearer <token>` où `<token>` est le `access_token` obtenu lors du login.

## Réponses

### ✅ 200 - Succès

L'utilisateur a été récupéré avec succès.

**Exemple de réponse :**

```json
{
  "success": true,
  "message": "Utilisateur recupere avec succes",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean.dupont@example.com",
    "phone_number": "+33612345678",
    "birth_date": "1990-01-15",
    "photo_url": "/uploads/photo_550e8400.jpg",
    "created_at": "2025-11-23T10:30:00",
    "updated_at": "2025-11-23T10:30:00"
  }
}
```

### ❌ 401 - Non autorisé

Le token est manquant, invalide ou expiré.

**Exemples de réponses :**

**Token manquant :**
```json
{
  "success": false,
  "message": "Token manquant"
}
```

**Format de token invalide :**
```json
{
  "success": false,
  "message": "Format de token invalide"
}
```

**Token invalide ou expiré :**
```json
{
  "success": false,
  "message": "Token invalide ou expire"
}
```

**ID utilisateur non trouvé dans le token :**
```json
{
  "success": false,
  "message": "ID utilisateur non trouve dans le token"
}
```

### ❌ 404 - Non trouvé

L'utilisateur n'existe pas ou a été supprimé.

**Exemple de réponse :**

```json
{
  "success": false,
  "message": "Utilisateur non trouve"
}
```

### ❌ 500 - Erreur serveur

Une erreur interne s'est produite.

**Exemple de réponse :**

```json
{
  "success": false,
  "message": "Erreur serveur: <détails de l'erreur>"
}
```

## Exemples d'utilisation

### cURL

```bash
# Avec un token valide
curl -X GET http://localhost:5000/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Python (requests)

```python
import requests

# Token obtenu après login
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Headers avec le token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Requête GET
response = requests.get("http://localhost:5000/auth/me", headers=headers)

# Traiter la réponse
if response.status_code == 200:
    user_data = response.json()
    print(f"Utilisateur: {user_data['data']['email']}")
else:
    print(f"Erreur: {response.json()['message']}")
```

### JavaScript (Fetch)

```javascript
// Token stocké dans localStorage ou autre
const accessToken = localStorage.getItem('access_token');

// Requête avec le token
fetch('http://localhost:5000/auth/me', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Utilisateur:', data.data);
  } else {
    console.error('Erreur:', data.message);
  }
})
.catch(error => console.error('Erreur réseau:', error));
```

### PowerShell

```powershell
# Token obtenu après login
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Headers
$headers = @{
    "Authorization" = "Bearer $token"
}

# Requête
$response = Invoke-RestMethod -Uri "http://localhost:5000/auth/me" `
    -Method Get `
    -Headers $headers

# Afficher le résultat
$response.data | Format-List
```

## Flux d'utilisation typique

```
1. Login
   POST /auth/login
   → Obtenir access_token et refresh_token

2. Utiliser le token pour récupérer l'utilisateur courant
   GET /auth/me
   Header: Authorization: Bearer <access_token>
   → Obtenir les infos de l'utilisateur

3. Si le token expire (après 60 minutes)
   POST /auth/refresh
   Body: { "refresh_token": "..." }
   → Obtenir un nouveau access_token

4. Continuer avec le nouveau token
   GET /auth/me
   Header: Authorization: Bearer <nouveau_access_token>
```

## Cas d'usage

### 1. Vérification de l'authentification

Utilisez cet endpoint pour vérifier si un utilisateur est authentifié et récupérer ses informations :

```python
def get_authenticated_user(token):
    """Vérifie si le token est valide et retourne l'utilisateur"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://localhost:5000/auth/me", headers=headers)
    
    if response.status_code == 200:
        return response.json()['data']
    return None
```

### 2. Affichage du profil utilisateur

```javascript
// Dans une application front-end
async function loadUserProfile() {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('/auth/me', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  if (response.ok) {
    const { data } = await response.json();
    document.getElementById('user-name').textContent = 
      `${data.first_name} ${data.last_name}`;
    document.getElementById('user-email').textContent = data.email;
  } else {
    // Token invalide, rediriger vers login
    window.location.href = '/login';
  }
}
```

### 3. Middleware d'authentification

```python
from functools import wraps

def require_auth(f):
    """Décorateur pour protéger les routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        # Vérifier le token via /auth/me
        response = requests.get(
            "http://localhost:5000/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            return jsonify({"error": "Non autorisé"}), 401
        
        # Ajouter l'utilisateur au contexte
        request.current_user = response.json()['data']
        return f(*args, **kwargs)
    
    return decorated
```

## Notes importantes

⚠️ **Sécurité**
- Ne jamais exposer les tokens dans les URLs
- Toujours utiliser HTTPS en production
- Stocker les tokens de manière sécurisée (httpOnly cookies ou localStorage chiffré)

💡 **Bonnes pratiques**
- Vérifier l'expiration du token avant chaque requête importante
- Implémenter un refresh automatique des tokens
- Logger les tentatives d'accès non autorisées

🔄 **Gestion du cycle de vie du token**
- Access token : 60 minutes
- Refresh token : 7 jours
- Après expiration du refresh token : nouvel login requis

## Test de l'endpoint

Utilisez le script de test fourni :

```powershell
python test_auth_me.py
```

Ce script teste automatiquement :
1. ✅ Récupération avec un token valide
2. ✅ Erreur sans token (401)
3. ✅ Erreur avec un token invalide (401)

## Swagger UI

L'endpoint est documenté dans Swagger UI : `http://localhost:5000/apidocs`

Vous pouvez y tester l'endpoint interactivement :
1. Cliquez sur "Authorize"
2. Entrez votre token : `Bearer <votre_token>`
3. Testez l'endpoint `/auth/me`

---

**Endpoint prêt à l'emploi ! 🚀**
