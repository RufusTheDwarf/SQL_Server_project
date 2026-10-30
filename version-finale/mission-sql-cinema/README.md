# Mission SQL : enquête au cinéma

Cette application est le projet actif pour les Journées Portes Ouvertes de l'ETML. Le scénario et le parcours doivent encore être validés par l'enseignant et chronométrés avec des visiteurs.

## Principe

Le visiteur aide un festival à comprendre les préférences du public. Il répond à trois questions fondées sur des réservations synthétiques. Les résultats sont calculés par SQL Server et servent à expliquer les jointures, les regroupements, les agrégations et l'analyse des dates.

Le parcours vise 5 à 8 minutes. Cette durée n'a pas encore été mesurée avec des visiteurs.

## Contenu

- `app.py` : application Flask locale et requêtes SQL utilisées par les défis.
- `templates/index.html` : interface des visiteurs.
- `static/style.css` : styles de l'application.
- `sql/00_create_database.sql` : création de la base vide.
- `sql/01_schema.sql` : création du schéma et des données de référence.
- `sql/02_generate_reservations.sql` : génération par lots de 10 millions de réservations.
- `sql/03_verify_volume.sql` : vérification des volumes, des relations et de l'espace utilisé.
- `sql/04_role_lecture.sql` : préparation d'un rôle SQL en lecture seule.
- `tests/` : tests applicatifs et tests d'intégration SQL Server.
- `docs/` : audit, validation, conformité, manuels, rapport, planification et supports visiteurs.

## Prérequis

- Windows 10 ou Windows 11.
- SQL Server 2019 ou une version plus récente.
- SQL Server Management Studio (SSMS).
- Python 3.10 ou une version plus récente.
- Microsoft ODBC Driver 18 for SQL Server.
- Espace disque suffisant pour les données, les index et le journal des transactions. La taille réelle doit être mesurée sur le poste cible.

## Installation automatisee sous Windows

Le dépôt contient un lanceur simple à utiliser : depuis l'Explorateur Windows, double-cliquer sur `setup.bat` à la racine du dépôt. Il lance automatiquement `setup.ps1`.

Depuis PowerShell, il est également possible d'exécuter :

```powershell
.\setup.bat
```

Le script vérifie les prérequis, prépare la base et les dix millions de réservations, installe les dépendances, lance les tests, puis démarre l'application sur `http://127.0.0.1:5000` et ouvre le navigateur.

Le moteur SQL Server et l'outil `sqlcmd` doivent déjà être installés. Le compte Windows doit disposer des droits nécessaires pour créer la base, puis lire les tables. Le script ne supprime aucune base ni table existante. Il s'arrête si le schéma est partiel.

Pour choisir une instance ou un autre port :

```powershell
.\setup.ps1 -SqlServer ".\SQLEXPRESS" -Port 5001
```

Le setup ouvre le navigateur lorsque le port répond et laisse Flask tourner dans un processus séparé. Pour arrêter le serveur, utiliser `Stop-Process -Id` avec le PID affiché par le script. Les journaux se trouvent dans `logs/`.

## Installation

1. Dans SSMS, exécuter `sql/00_create_database.sql`.
2. Sélectionner `MissionCinema`, puis exécuter `sql/01_schema.sql`.
3. Exécuter `sql/02_generate_reservations.sql`. Le script vise exactement 10 000 000 réservations et affiche l'avancement de chaque lot.
4. Exécuter `sql/03_verify_volume.sql` et conserver les résultats.
5. Dans PowerShell, se placer dans ce dossier, puis exécuter :

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

6. Configurer la connexion Windows. Adapter le nom du serveur et du pilote à l'installation :

   ```powershell
   $env:SQL_SERVER = ".\SQLEXPRESS"
   $env:SQL_DATABASE = "MissionCinema"
   $env:SQL_DRIVER = "ODBC Driver 18 for SQL Server"
   ```

7. Lancer `python app.py`, puis ouvrir `http://127.0.0.1:5000`.

Aucun mot de passe SQL n'est enregistré dans le dépôt. L'application utilise l'authentification Windows.

## Mode simulation

Pour répéter l'interface sans connexion SQL Server, définir `DEMO_MODE=1` avant le lancement. Dans ce mode, l'application ne tente pas de connexion SQL et affiche une bannière explicite. Les chiffres sont des exemples et ne prouvent pas que les requêtes SQL ont été exécutées.

Pour revenir au mode réel, fermer l'application et exécuter :

```powershell
Remove-Item Env:DEMO_MODE -ErrorAction SilentlyContinue
python app.py
```

## Tests

Depuis ce dossier, exécuter les tests applicatifs :

```powershell
python -m unittest discover -s tests -v
```

Ces tests ne nécessitent pas SQL Server. Les tests d'intégration sont ignorés par défaut. Sur un poste de test équipé de SQL Server, configurer la connexion, puis définir `RUN_SQL_INTEGRATION=1` avant de lancer les tests. Ils contrôlent le volume, les relations et les réponses principales des trois défis.

## État de vérification

Les tests GitHub Actions historiques ne constituent pas une validation de SQL Server. La génération réelle, les résultats de `03_verify_volume.sql`, les durées, l'espace disque, les performances et l'installation sur le PC cible doivent être mesurés et conservés comme preuves.
