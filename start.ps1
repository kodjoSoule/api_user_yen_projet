# Script de démarrage rapide pour Windows PowerShell
# Usage: .\start.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Users Microservice - EQOS" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Vérifie si venv existe
if (-Not (Test-Path "venv")) {
    Write-Host "⚠️  Environnement virtuel non trouvé" -ForegroundColor Yellow
    Write-Host "Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Environnement virtuel créé" -ForegroundColor Green
}

# Active l'environnement virtuel
Write-Host "🔄 Activation de l'environnement virtuel..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Vérifie si les dépendances sont installées
Write-Host "🔄 Vérification des dépendances..." -ForegroundColor Cyan
$pipList = pip list
if ($pipList -notmatch "Flask") {
    Write-Host "⚠️  Dépendances non installées" -ForegroundColor Yellow
    Write-Host "Installation des dépendances..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✅ Dépendances installées" -ForegroundColor Green
} else {
    Write-Host "✅ Dépendances déjà installées" -ForegroundColor Green
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "🚀 Lancement de l'application..." -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 API: http://localhost:5000" -ForegroundColor Yellow
Write-Host "📚 Documentation: http://localhost:5000/docs/" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Gray
Write-Host ""

# Lance l'application
python app.py
