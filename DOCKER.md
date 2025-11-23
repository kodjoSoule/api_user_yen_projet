# 🐳 Configuration Docker - Récapitulatif

## ✅ Fichiers créés

### 1. **Dockerfile**
- Image de base : `python:3.11-slim`
- Port exposé : `5000`
- Installation automatique des dépendances
- Création des dossiers `data/` et `uploads/`

### 2. **docker-compose.yml**
Configuration orchestration des services :
- Service `flask-api` avec build automatique
- Mapping de ports : `5000:5000`
- Volumes persistants :
  - `./data` → `/app/data`
  - `./uploads` → `/app/uploads`
- Variables d'environnement configurables
- Réseau Docker isolé : `flask-network`
- Restart policy : `unless-stopped`

### 3. **.dockerignore**
Exclusion des fichiers inutiles du build :
- Fichiers Python compilés (`__pycache__`, `*.pyc`)
- Environnements virtuels (`venv/`, `env/`)
- Configuration IDE (`.vscode/`, `.idea/`)
- Documentation (sauf README.md)
- Fichiers de test
- Données locales (montées via volumes)

### 4. **.env.example**
Template de configuration avec variables :
- `FLASK_APP`, `FLASK_ENV`
- `SECRET_KEY` (à changer en production !)
- `JWT_EXPIRES_IN_MINUTES`, `JWT_ALGORITHM`
- `HOST`, `PORT`

### 5. **docker.ps1**
Script PowerShell pour simplifier les commandes Docker :
- `.\docker.ps1 build` - Construire l'image
- `.\docker.ps1 up` - Démarrer l'application
- `.\docker.ps1 down` - Arrêter l'application
- `.\docker.ps1 logs` - Voir les logs
- `.\docker.ps1 restart` - Redémarrer
- `.\docker.ps1 ps` - Status des conteneurs
- `.\docker.ps1 shell` - Accéder au conteneur
- `.\docker.ps1 test` - Lancer les tests
- `.\docker.ps1 clean` - Nettoyer tout

### 6. **README.Docker.md**
Documentation complète Docker incluant :
- Guide de démarrage rapide
- Commandes utiles (build, logs, debug)
- Configuration de production
- Setup SSL/HTTPS avec Nginx
- Surveillance et monitoring
- Guide de déploiement
- Troubleshooting

## 🚀 Démarrage rapide

### Méthode 1 : Script PowerShell (Recommandé)
```powershell
# Démarrer
.\docker.ps1 up

# Voir les logs
.\docker.ps1 logs
```

### Méthode 2 : Docker Compose direct
```powershell
# Construire et démarrer
docker-compose up -d

# Vérifier les logs
docker-compose logs -f flask-api

# Arrêter
docker-compose down
```

## 🌐 Accès à l'application

Une fois démarré :
- **API** : <http://localhost:5000>
- **Swagger UI** : <http://localhost:5000/apidocs>

## 📊 Vérification

```powershell
# Vérifier que le conteneur tourne
docker ps

# Tester un endpoint
curl http://localhost:5000/api/users

# Voir les logs en temps réel
docker-compose logs -f
```

## 🔧 Configuration de production

### 1. Créer le fichier .env
```powershell
Copy-Item .env.example .env
```

### 2. Générer une clé secrète forte
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Éditer .env et remplacer SECRET_KEY
```env
SECRET_KEY=votre_nouvelle_cle_generee
```

### 4. Redémarrer avec la nouvelle config
```powershell
docker-compose down
docker-compose up -d
```

## 📁 Persistance des données

Les données sont persistées via volumes Docker :

```
Hôte (Windows)           →  Conteneur
./data/users.json        →  /app/data/users.json
./uploads/*.jpg          →  /app/uploads/*.jpg
```

Les fichiers restent intacts même après :
- `docker-compose down`
- `docker-compose restart`
- Reconstruction de l'image

**⚠️ ATTENTION** : `docker-compose down -v` supprime les volumes !

## 🧪 Tests

```powershell
# Avec le script
.\docker.ps1 test

# Ou directement
docker-compose exec flask-api python test_api.py
```

## 🔄 Mise à jour de l'application

```powershell
# 1. Arrêter
docker-compose down

# 2. Mettre à jour le code
git pull  # Si Git

# 3. Reconstruire l'image
docker-compose build --no-cache

# 4. Redémarrer
docker-compose up -d
```

## 🐛 Dépannage

### Problème : Port 5000 déjà utilisé
```powershell
# Windows : trouver le processus
netstat -ano | findstr :5000

# Tuer le processus
taskkill /PID <PID> /F

# Ou changer le port dans docker-compose.yml
ports:
  - "5001:5000"  # Port hôte 5001 → conteneur 5000
```

### Problème : L'image ne se construit pas
```powershell
# Nettoyer le cache Docker
docker system prune -a

# Reconstruire sans cache
docker-compose build --no-cache
```

### Problème : Les données ne persistent pas
```powershell
# Vérifier les volumes
docker volume ls

# Inspecter le volume
docker volume inspect flask_api_project_data
```

## 📦 Déploiement

### Option 1 : Serveur Linux avec Docker
```bash
# Copier les fichiers
scp -r . user@server:/opt/flask-api/

# Se connecter et démarrer
ssh user@server
cd /opt/flask-api
docker-compose up -d
```

### Option 2 : Cloud (AWS, Azure, GCP)
- AWS : Elastic Container Service (ECS)
- Azure : Container Instances
- GCP : Cloud Run

### Option 3 : Kubernetes
```powershell
# Générer les manifests K8s
kompose convert -f docker-compose.yml

# Déployer
kubectl apply -f .
```

## ✨ Avantages de Docker

✅ **Portabilité** : Fonctionne partout (Windows, Linux, Mac, Cloud)  
✅ **Isolation** : Environnement indépendant du système hôte  
✅ **Reproductibilité** : Même environnement dev/staging/prod  
✅ **Simplicité** : Une commande pour démarrer  
✅ **Scalabilité** : Facile à répliquer et scaler  
✅ **CI/CD Ready** : Intégration facile dans pipelines

## 📚 Ressources

- 📖 [README.Docker.md](README.Docker.md) - Documentation complète
- 📖 [README.md](README.md) - Documentation générale de l'API
- 🐳 [Docker Docs](https://docs.docker.com/)
- 🐙 [Docker Compose Reference](https://docs.docker.com/compose/)

---

**Prêt à déployer ! 🚀**
