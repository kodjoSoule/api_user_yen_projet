✅ 1. Créer l’environnement virtuel

Dans le dossier de ton projet Flask :

python -m venv .env


👉 Cela crée un dossier .env (le nom est correct, aucun problème à l’appeler .env).

✅ 2. Activer l’environnement virtuel

Toujours dans PowerShell :

.\.env\Scripts\Activate.ps1


Une fois activé, tu verras :

(.env) PS C:\Users\Kodjo\Desktop\Develop\flask_api_project>

❗ Si tu obtiens une erreur « script not allowed »

Activer la politique d’exécution :

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass


Puis réessaye :

.\.env\Scripts\Activate.ps1

✅ 3. Installer les dépendances

Assure-toi que ton fichier s’appelle requirements.txt, puis :

pip install -r requirements.txt

🔥 4. Lancer ton API Flask
python app.py


Puis ouvre Swagger :

👉 http://127.0.0.1:5000/docs
