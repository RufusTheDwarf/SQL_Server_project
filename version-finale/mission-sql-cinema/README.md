# Mission SQL : enquête au cinéma

Cette activité est une nouvelle piste de refonte pour les Portes ouvertes de l'ETML. Elle n'est pas encore validée par l'enseignant.

## Principe

Le visiteur aide un festival à choisir les tendances de sa programmation. Il répond à trois questions fondées sur les réservations d'un cinéma fictif. Les réponses sont calculées par SQL Server et permettent d'expliquer les filtres, les jointures, les agrégations et le tri.

Le parcours cible est de 5 à 8 minutes. Cette durée reste à mesurer avec des visiteurs tests.

## Contenu

- `app.py` : application Flask locale.
- `templates/index.html` : interface.
- `static/style.css` : mise en page.
- `sql/00_create_database.sql` : création de la base vide.\n- `sql/01_schema.sql` : création des tables et des données de référence.
- `sql/02_generate_reservations.sql` : génération de dix millions de réservations synthétiques.
- `sql/03_verify_volume.sql` : contrôle des volumes et des relations.\n- `sql/04_role_lecture.sql` : préparation d'un rôle de lecture seule à attribuer au compte Windows par un administrateur.
- `tests/` : tests unitaires sans serveur SQL.
- `docs/` : audit, fiche de validation, manuels, rapport, journal et conformité.

## Prérequis

- Windows 10 ou 11.
- SQL Server 2019 ou plus récent, à confirmer sur le poste cible.
- Python 3.10 ou plus récent.
- Pilote Microsoft ODBC Driver 18 for SQL Server.
- Plusieurs Go d'espace disque libre et une marge supplémentaire. La taille réelle doit être mesurée sur le poste cible.

## Installation

1. Créer la base `MissionCinema` dans SSMS.
2. Exécuter `sql/01_schema.sql`.
3. Exécuter `sql/02_generate_reservations.sql`. Ce script insère dix millions de réservations synthétiques. Il peut prendre du temps et doit être exécuté avant la démonstration.
4. Exécuter `sql/03_verify_volume.sql` et conserver les résultats.
5. Dans PowerShell, se placer dans ce dossier et créer un environnement Python :
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
6. Configurer la connexion Windows :
   ```powershell
   $env:SQL_SERVER = ".\\SQLEXPRESS"
   $env:SQL_DATABASE = "MissionCinema"
   $env:SQL_DRIVER = "ODBC Driver 18 for SQL Server"
   ```
7. Lancer `python app.py` et ouvrir `http://127.0.0.1:5000`.

Le nom du serveur et le pilote doivent correspondre à l'installation locale. Aucun mot de passe SQL n'est enregistré dans le dépôt.

## Mode de simulation

Par défaut, l'application exige SQL Server. Pour une répétition sans serveur, définir `DEMO_MODE=1` avant le lancement. Une bannière indique alors clairement que les résultats sont simulés. Ne pas utiliser ce mode pour prétendre que les requêtes ont été exécutées sur SQL Server.

## Contrôles

Lancer `python -m unittest discover -s tests -v`. Ces tests vérifient la logique applicative isolée, mais ne remplacent pas les tests d'intégration sur SQL Server.

## État de vérification

Le code a été ajouté au dépôt par modification distante. Les scripts SQL n'ont pas été exécutés sur un serveur SQL dans cet environnement. Le volume réel, la durée de génération, l'espace disque et la durée de la partie doivent donc être mesurés sur un poste Windows équipé de SQL Server.
