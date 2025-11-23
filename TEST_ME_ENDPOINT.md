# Guide de test rapide de l'endpoint /auth/me

## Étape 1 : Démarrer l'application

```powershell
.\start.ps1
```

Attendez que l'application démarre (vous devriez voir "Running on http://0.0.0.0:5000")

## Étape 2 : Tester avec PowerShell

Ouvrez un nouveau terminal PowerShell et exécutez :

```powershell
# 1. Se connecter pour obtenir un token
$loginData = @{
    email = "jean.dupont@example.com"
    password = "password123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://localhost:5000/auth/login" `
    -Method Post `
    -Body $loginData `
    -ContentType "application/json"

# Extraire le token
$token = $loginResponse.data.access_token
Write-Host "Token obtenu: $($token.Substring(0, 50))..." -ForegroundColor Green

# 2. Utiliser le token pour récupérer l'utilisateur courant
$headers = @{
    Authorization = "Bearer $token"
}

$meResponse = Invoke-RestMethod -Uri "http://localhost:5000/auth/me" `
    -Method Get `
    -Headers $headers

# Afficher le résultat
Write-Host "`n✅ Informations de l'utilisateur courant:" -ForegroundColor Green
$meResponse.data | Format-List

Write-Host "`n✅ L'endpoint /auth/me fonctionne correctement!" -ForegroundColor Green
```

## Étape 3 : Tester avec le script Python

```powershell
python test_auth_me.py
```

## Étape 4 : Tester dans Swagger UI

1. Ouvrez votre navigateur : `http://localhost:5000/apidocs`
2. Trouvez l'endpoint **POST /auth/login**
3. Cliquez sur "Try it out"
4. Entrez les credentials :
   ```json
   {
     "email": "jean.dupont@example.com",
     "password": "password123"
   }
   ```
5. Cliquez sur "Execute"
6. Copiez le `access_token` de la réponse
7. Cliquez sur le bouton **Authorize** en haut
8. Entrez : `Bearer <votre_token>`
9. Cliquez sur "Authorize"
10. Trouvez l'endpoint **GET /auth/me**
11. Cliquez sur "Try it out" puis "Execute"
12. ✅ Vous devriez voir les informations de l'utilisateur !

## Résultat attendu

```json
{
  "success": true,
  "message": "Utilisateur recupere avec succes",
  "data": {
    "id": "uuid-de-l-utilisateur",
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean.dupont@example.com",
    "phone_number": "+33612345678",
    "birth_date": "1990-01-15",
    "photo_url": null,
    "created_at": "2025-11-23T...",
    "updated_at": "2025-11-23T..."
  }
}
```

## Tests de sécurité

### Test 1 : Sans token (doit échouer avec 401)
```powershell
try {
    Invoke-RestMethod -Uri "http://localhost:5000/auth/me" -Method Get
} catch {
    Write-Host "✅ Erreur 401 attendue : Token manquant" -ForegroundColor Green
}
```

### Test 2 : Avec un mauvais token (doit échouer avec 401)
```powershell
$badHeaders = @{
    Authorization = "Bearer invalid.token.here"
}

try {
    Invoke-RestMethod -Uri "http://localhost:5000/auth/me" `
        -Method Get `
        -Headers $badHeaders
} catch {
    Write-Host "✅ Erreur 401 attendue : Token invalide" -ForegroundColor Green
}
```

## Troubleshooting

### Erreur "Utilisateur non trouvé"
Si vous n'avez pas d'utilisateur, créez-en un d'abord :

```powershell
$registerData = @{
    first_name = "Jean"
    last_name = "Dupont"
    email = "jean.dupont@example.com"
    password = "password123"
    phone_number = "+33612345678"
    birth_date = "1990-01-15"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/auth/register" `
    -Method Post `
    -Body $registerData `
    -ContentType "application/json"
```

### Erreur "Token expiré"
Les access tokens expirent après 60 minutes. Reconnectez-vous pour obtenir un nouveau token.

---

**L'endpoint /auth/me est prêt à utiliser ! 🎉**
