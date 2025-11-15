# Gestion des stocks - Application de bureau (Tkinter + MySQL + JSON)

Petit projet d'exemple pour suivre et gérer un stock localement.

Technos:
- Python 3.10 
- Tkinter
- MySQL
- JSON
- PyInstaller

Fichiers principaux:
- `main.py` : interface Tkinter
- `db.py` : gestion de la persistance (MySQL ou JSON fallback)
- `models.py` : modèle `Item`
- `config.json` : configuration de la base de données
- `storage.json` : exemple de stockage local
- `requirements.txt` : dépendances

Installation et exécution:

1. Installer Python 3.10 (ou compatible)
2. Créer un environnement virtuel et installer les dépendances:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

3. Configurer `config.json` si vous utilisez MySQL (ou laissez par défaut pour utiliser JSON):

```json
{
  "host": "localhost",
  "user": "root",
  "password": "password",
  "database": "inventory_db"
}
```

4. Lancer l'application:

```powershell
python main.py
```

Générer un exécutable avec PyInstaller:

```powershell
pyinstaller --onefile --windowed main.py
```


