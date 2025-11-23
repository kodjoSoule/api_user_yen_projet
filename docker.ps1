# Script PowerShell pour gérer l'application Docker
# Usage: .\docker.ps1 [commande]

param(
    [Parameter(Position=0)]
    [ValidateSet('build', 'up', 'down', 'logs', 'restart', 'ps', 'shell', 'test', 'clean')]
    [string]$Command = 'help'
)

function Show-Help {
    Write-Host "`n🐳 Flask Users API - Commandes Docker`n" -ForegroundColor Cyan
    Write-Host "Usage: .\docker.ps1 [commande]`n"
    Write-Host "Commandes disponibles:" -ForegroundColor Yellow
    Write-Host "  build     - Construire l'image Docker"
    Write-Host "  up        - Démarrer l'application"
    Write-Host "  down      - Arrêter l'application"
    Write-Host "  logs      - Afficher les logs"
    Write-Host "  restart   - Redémarrer l'application"
    Write-Host "  ps        - Voir les conteneurs actifs"
    Write-Host "  shell     - Ouvrir un shell dans le conteneur"
    Write-Host "  test      - Lancer les tests"
    Write-Host "  clean     - Nettoyer tout (conteneurs, volumes, images)`n"
}

switch ($Command) {
    'build' {
        Write-Host "🔨 Construction de l'image Docker..." -ForegroundColor Green
        docker-compose build
    }
    'up' {
        Write-Host "🚀 Démarrage de l'application..." -ForegroundColor Green
        docker-compose up -d
        Write-Host "`n✅ Application démarrée!" -ForegroundColor Green
        Write-Host "📍 API: http://localhost:5000" -ForegroundColor Cyan
        Write-Host "📚 Swagger: http://localhost:5000/apidocs`n" -ForegroundColor Cyan
    }
    'down' {
        Write-Host "🛑 Arrêt de l'application..." -ForegroundColor Yellow
        docker-compose down
    }
    'logs' {
        Write-Host "📋 Logs de l'application (Ctrl+C pour quitter):`n" -ForegroundColor Cyan
        docker-compose logs -f flask-api
    }
    'restart' {
        Write-Host "🔄 Redémarrage de l'application..." -ForegroundColor Yellow
        docker-compose restart
    }
    'ps' {
        Write-Host "📊 Conteneurs actifs:`n" -ForegroundColor Cyan
        docker-compose ps
    }
    'shell' {
        Write-Host "🐚 Ouverture du shell dans le conteneur...`n" -ForegroundColor Cyan
        docker-compose exec flask-api /bin/bash
    }
    'test' {
        Write-Host "🧪 Lancement des tests...`n" -ForegroundColor Cyan
        docker-compose exec flask-api python test_api.py
    }
    'clean' {
        Write-Host "🧹 Nettoyage complet..." -ForegroundColor Red
        $confirm = Read-Host "⚠️  Cela va supprimer tous les conteneurs, volumes et images. Continuer? (o/N)"
        if ($confirm -eq 'o' -or $confirm -eq 'O') {
            docker-compose down -v
            docker rmi flask_api_project_flask-api -f
            Write-Host "✅ Nettoyage terminé!" -ForegroundColor Green
        } else {
            Write-Host "❌ Annulé" -ForegroundColor Yellow
        }
    }
    default {
        Show-Help
    }
}
