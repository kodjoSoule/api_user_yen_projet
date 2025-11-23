# Utilise une image Python officielle comme base
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code de l'application
COPY . .

# Crée les répertoires nécessaires pour les données et uploads
RUN mkdir -p data uploads

# Expose le port sur lequel Flask va tourner
EXPOSE 5000

# Variables d'environnement par défaut
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV SECRET_KEY=change-me-in-production

# Commande pour lancer l'application
CMD ["python", "app.py"]
