# 🚀 Guide de démarrage rapide

## Installation et lancement (5 minutes)

### Option 1 : Script automatique (Recommandé)

```powershell
.\start.ps1
```

Ce script va automatiquement :
- Créer l'environnement virtuel s'il n'existe pas
- Installer les dépendances
- Lancer l'application

### Option 2 : Installation manuelle

```powershell
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement
.\venv\Scripts\Activate.ps1

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python app.py
```

## 🎯 URLs importantes

- **API** : http://localhost:5000
- **Documentation Swagger** : http://localhost:5000/docs/
- **Spécification OpenAPI** : http://localhost:5000/apispec.json

## 📝 Premiers pas

### 1. Créer un utilisateur

```bash
curl -X POST http://localhost:5000/users/ ^
  -H "Content-Type: application/json" ^
  -d "{\"first_name\":\"Jean\",\"last_name\":\"Dupont\",\"birth_date\":\"1990-01-15\",\"email\":\"jean@example.com\",\"phone_number\":\"+33612345678\",\"password\":\"Pass123!\",\"user_type\":\"PARTICULIER\",\"country\":\"France\",\"address\":\"Paris\"}"
```

### 2. Se connecter

```bash
curl -X POST http://localhost:5000/users/verify-users-creds ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"jean@example.com\",\"password\":\"Pass123!\"}"
```

Vous recevrez un token JWT dans la réponse.

### 3. Récupérer tous les utilisateurs

```bash
curl http://localhost:5000/users/all
```

## 🧪 Tester l'API

### Avec le script de test

```powershell
python test_api.py
```

### Avec Swagger UI

Ouvrez http://localhost:5000/docs/ dans votre navigateur et testez directement les endpoints.

## 📚 Documentation complète

Consultez `README.md` pour la documentation complète de l'API.

## 🆘 Problèmes courants

### Erreur : "Le module 'flask' n'est pas installé"
```powershell
pip install -r requirements.txt
```

### Erreur : "Port 5000 déjà utilisé"
Modifiez le port dans `app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Erreur d'activation de l'environnement virtuel
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📦 Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | /users/ | Créer un utilisateur |
| GET | /users/all | Liste des utilisateurs |
| GET | /users/{id} | Utilisateur par ID |
| GET | /users/email/{email} | Utilisateur par email |
| GET | /users/phone_number/{phone} | Utilisateur par téléphone |
| PUT | /users/{id} | Mettre à jour |
| DELETE | /users/{id} | Supprimer |
| POST | /users/verify-users-creds | Connexion |
| POST | /users/upload-profile-photo | Upload photo |

## 🔑 Structure des données

### Créer un utilisateur (UserModel)
```json
{
  "first_name": "Jean",
  "last_name": "Dupont",
  "birth_date": "1990-01-15",
  "email": "jean@example.com",
  "phone_number": "+33612345678",
  "password": "SecurePass123!",
  "user_type": "PARTICULIER",
  "country": "France",
  "address": "123 Rue de la Paix, Paris"
}
```

### Se connecter (LoginModel)
```json
{
  "email": "jean@example.com",
  "password": "SecurePass123!"
}
```

OU

```json
{
  "phone_number": "+33612345678",
  "password": "SecurePass123!"
}
```

## ✨ Prêt à commencer !

Votre API est maintenant prête à l'emploi. Bon développement ! 🎉
