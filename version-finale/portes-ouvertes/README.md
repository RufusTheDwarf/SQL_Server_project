# Portes Ouvertes

Interface locale de démonstration pour détecter des joueurs suspects dans la base SQL Server.

## Installation

Dans ce dossier :

```powershell
python -m pip install -r requirements.txt
```

## Configuration

Par défaut, l'application utilise :

- Serveur SQL : `.\SQLEXPRESS`
- Base : `SQL_Server_Project`
- Authentification : Windows
- Pilote : `ODBC Driver 17 for SQL Server`

Si le serveur SQL utilise une autre instance ou un autre nom de base, définir les variables d'environnement :

```powershell
$env:SQL_SERVER=".\SQLEXPRESS"
$env:SQL_DATABASE="SQL_Server_Project"
```

## Lancement

```powershell
python app.py
```

Puis ouvrir :

http://127.0.0.1:5000

## Démo

Les valeurs du formulaire commencent à zéro. La détection utilise un score de suspicion : chaque critère validé ajoute des points et un signalement « Triche » ajoute deux points. Un joueur est affiché à partir de 3 points. Les 100 profils les plus suspects sont affichés.

L'interface est en lecture seule : elle effectue uniquement des requêtes SELECT paramétrées.
