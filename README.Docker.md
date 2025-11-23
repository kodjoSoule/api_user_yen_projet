# 🐳 Guide Docker - Flask Users API

## 📋 Prérequis

- Docker installé (version 20.10+)
- Docker Compose installé (version 2.0+)

## 🚀 Démarrage rapide

### 1. Construire et lancer l'application

```bash
# Construire l'image et lancer le conteneur
docker-compose up -d

# Voir les logs
docker-compose logs -f
```

L'API sera accessible à : **http://localhost:5000**

Documentation Swagger : **http://localhost:5000/apidocs**

### 2. Arrêter l'application

```bash
# Arrêter les conteneurs
docker-compose down

# Arrêter et supprimer les volumes (ATTENTION: supprime les données)
docker-compose down -v
```

## 🛠️ Commandes utiles

### Construction et déploiement

```bash
# Reconstruire l'image (après modification du code)
docker-compose build

# Reconstruire sans cache
docker-compose build --no-cache

# Redémarrer l'application
docker-compose restart

# Voir les conteneurs en cours
docker-compose ps
```

### Logs et debugging

```bash
# Voir tous les logs
docker-compose logs

# Suivre les logs en temps réel
docker-compose logs -f flask-api

# Voir les dernières 50 lignes
docker-compose logs --tail=50 flask-api
```

### Accès au conteneur

```bash
# Ouvrir un shell dans le conteneur
docker-compose exec flask-api /bin/bash

# Exécuter une commande Python
docker-compose exec flask-api python -c "print('Hello from container')"
```

## 📁 Structure des volumes

Les données sont persistées via des volumes Docker :

```
├── ./data       → /app/data       (fichiers JSON des utilisateurs)
├── ./uploads    → /app/uploads    (photos des utilisateurs)
```

Les fichiers restent accessibles même après l'arrêt des conteneurs.

## 🔐 Configuration de production

### 1. Créer un fichier `.env`

```bash
# Copier le template
cp .env.example .env

# Éditer avec vos valeurs
nano .env
```

### 2. Modifier le SECRET_KEY

**IMPORTANT** : Générez une clé secrète forte :

```bash
# Générer une clé aléatoire
python -c "import secrets; print(secrets.token_hex(32))"
```

Copiez cette clé dans votre fichier `.env` :

```env
SECRET_KEY=votre_cle_secrete_generee_ici
```

### 3. Configuration SSL/HTTPS (Production)

Pour la production, utilisez un reverse proxy (Nginx/Traefik) avec SSL :

```yaml
# docker-compose.prod.yml (exemple)
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - flask-api

  flask-api:
    build: .
    expose:
      - "5000"
    environment:
      - FLASK_ENV=production
```

## 🧪 Tests avec Docker

```bash
# Lancer les tests dans un conteneur
docker-compose exec flask-api python test_api.py

# Tester un endpoint spécifique
docker-compose exec flask-api curl http://localhost:5000/api/users
```

## 📊 Surveillance et monitoring

### Vérifier la santé du conteneur

```bash
# Stats en temps réel
docker stats flask_users_api

# Informations détaillées
docker inspect flask_users_api
```

### Limites de ressources (optionnel)

Ajoutez dans `docker-compose.yml` :

```yaml
services:
  flask-api:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## 🌍 Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `FLASK_APP` | `app.py` | Point d'entrée Flask |
| `FLASK_ENV` | `production` | Environnement (development/production) |
| `SECRET_KEY` | `dev-secret-key...` | Clé secrète JWT |
| `JWT_EXPIRES_IN_MINUTES` | `60` | Durée de vie access token |
| `HOST` | `0.0.0.0` | Adresse d'écoute |
| `PORT` | `5000` | Port d'écoute |

## 🔄 Mise à jour de l'application

```bash
# 1. Arrêter l'ancienne version
docker-compose down

# 2. Récupérer les derniers changements (si Git)
git pull

# 3. Reconstruire l'image
docker-compose build

# 4. Relancer avec la nouvelle version
docker-compose up -d

# 5. Vérifier les logs
docker-compose logs -f
```

## 🐛 Dépannage

### L'application ne démarre pas

```bash
# Vérifier les logs d'erreur
docker-compose logs flask-api

# Vérifier que le port n'est pas déjà utilisé
netstat -ano | findstr :5000  # Windows
lsof -i :5000                  # Linux/Mac
```

### Problèmes de permissions (Linux)

```bash
# Corriger les permissions des volumes
sudo chown -R $USER:$USER ./data ./uploads
```

### Réinitialiser complètement

```bash
# Supprimer tout (conteneurs, images, volumes)
docker-compose down -v
docker rmi flask_api_project_flask-api
docker-compose up -d --build
```

## 📦 Build pour production

### Créer une image pour déploiement

```bash
# Tag avec version
docker build -t flask-users-api:1.0.0 .

# Tag pour registry (exemple)
docker tag flask-users-api:1.0.0 myregistry.io/flask-users-api:1.0.0

# Pousser vers un registry
docker push myregistry.io/flask-users-api:1.0.0
```

## 🎯 Exemples de déploiement

### Sur un serveur distant

```bash
# Via SSH
scp docker-compose.yml user@server:/app/
scp .env user@server:/app/
ssh user@server "cd /app && docker-compose up -d"
```

### Avec Docker Swarm

```bash
docker stack deploy -c docker-compose.yml flask-api-stack
```

### Avec Kubernetes (via Kompose)

```bash
# Convertir docker-compose.yml en manifests K8s
kompose convert

# Déployer
kubectl apply -f .
```

## 📞 Support

Pour toute question ou problème :
- Consultez les logs : `docker-compose logs -f`
- Vérifiez la configuration : `docker-compose config`
- Inspectez le conteneur : `docker inspect flask_users_api`

---

**Bon déploiement ! 🚀**
