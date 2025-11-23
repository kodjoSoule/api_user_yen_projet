project/
│
├── app.py                 → Point d’entrée (DIP)
│
├── config/
│   └── settings.py        → Configuration application
│
├── controllers/           → C (MVC) / Interface
│   └── user_controller.py
│
├── services/              → Services métiers (SRP, OCP)
│   └── user_service.py
│
├── repositories/          → Gestion de la data (Repository Pattern)
│   └── user_repository.py
│
├── models/
│   └── user_model.py      → Entité métier
│
├── utils/
│   └── file_upload.py     → Gestion upload fichier
│
├── data/
│   └── users.json         → "Database" JSON
│
└── uploads/
