# Manuel d'installation

## Objectif

Ce manuel décrit l'installation de Mission SQL au cinéma sur un poste Windows équipé de SQL Server. Les commandes doivent être exécutées dans l'ordre indiqué.

## Prérequis

- Windows 10 ou Windows 11.
- SQL Server installé et démarré.
- SQL Server Management Studio (SSMS).
- Python 3.10 ou une version compatible plus récente.
- Microsoft ODBC Driver 18 for SQL Server.
- Espace disque libre suffisant pour la base, les index et les journaux. La taille réelle doit être mesurée sur le poste cible.

## 1. Créer la base de données

Dans SSMS, se connecter à l'instance SQL Server utilisée pour l'activité. Ouvrir le script `sql/00_create_database.sql` et l'exécuter pour créer la base vide `MissionCinema`.

Vérifier ensuite que la base `MissionCinema` est sélectionnée avant d'exécuter les scripts suivants.

## 2. Créer les tables

Ouvrir `sql/01_schema.sql` dans SSMS et l'exécuter sur `MissionCinema`.

Le script crée les tables et les données de référence. Il refuse de continuer si des tables du projet existent déjà. En cas de blocage, vérifier la base sélectionnée. Ne pas supprimer une base contenant des données utiles.

## 3. Générer les réservations

Ouvrir `sql/02_generate_reservations.sql` et l'exécuter sur la base `MissionCinema`.

Le générateur vise dix millions de réservations synthétiques. L'opération peut prendre du temps et consommer plusieurs Go d'espace disque. Le script utilise des lots et peut reprendre une génération interrompue. Ne pas lancer plusieurs générations simultanément.

## 4. Vérifier les données

Exécuter `sql/03_verify_volume.sql`.

Conserver les résultats de contrôle. Avant d'utiliser l'activité avec des visiteurs, vérifier que la table des réservations contient au moins 10 000 000 lignes et que les contrôles de relations ne signalent aucune référence orpheline.

Ne pas annoncer que le volume est atteint tant que cette vérification n'a pas été exécutée sur le poste cible.

## 5. Installer l'application Python

Ouvrir PowerShell dans le dossier `version-finale/mission-sql-cinema`, puis exécuter :

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloque l'activation de l'environnement, utiliser directement le programme `.venv\\Scripts\\python.exe` pour installer les dépendances et lancer l'application.

## 6. Configurer la connexion SQL Server

Exemple pour une instance locale nommée SQLEXPRESS :

```powershell
$env:SQL_SERVER = ".\\SQLEXPRESS"
$env:SQL_DATABASE = "MissionCinema"
$env:SQL_DRIVER = "ODBC Driver 18 for SQL Server"
```

Le nom de l'instance doit correspondre à celui installé sur le poste. L'application utilise l'authentification Windows. Le compte Windows courant doit disposer des droits de lecture nécessaires.

Aucun mot de passe ne doit être ajouté au dépôt Git.

## 7. Préparer le compte en lecture seule

Cette étape est facultative si un compte autorisé existe déjà.

Exécuter `sql/04_role_lecture.sql` avec un compte administrateur SQL Server. Le script prépare le rôle `mission_cinema_lecture` et lui accorde uniquement le droit SELECT sur les tables de l'activité.

Un administrateur doit ensuite créer ou sélectionner le principal Windows approprié et l'ajouter au rôle. Le nom exact du compte dépend de la configuration du poste.

## 8. Démarrer l'application

Dans PowerShell, exécuter :

```powershell
python app.py
```

Ouvrir ensuite l'adresse suivante dans le navigateur :

`http://127.0.0.1:5000`

Garder la fenêtre PowerShell ouverte pendant toute l'activité.

## 9. Utiliser le mode simulation

Pour tester l'interface sans connexion SQL Server, exécuter :

```powershell
$env:DEMO_MODE = "1"
python app.py
```

La bannière « MODE SIMULATION » doit rester visible. Les résultats affichés dans ce mode sont des exemples et ne prouvent pas que les requêtes ont été exécutées sur SQL Server.

Pour revenir au mode réel, fermer l'application, supprimer la variable et redémarrer :

```powershell
Remove-Item Env:DEMO_MODE
python app.py
```

## 10. Contrôles avant l'ouverture au public

- Exécuter le script de vérification du volume et conserver les résultats.
- Confirmer la présence d'au moins 10 000 000 réservations.
- Vérifier l'absence de références orphelines.
- Démarrer l'application sans le mode simulation.
- Vérifier que la connexion SQL Server fonctionne.
- Répondre aux trois défis.
- Tester le bouton de nouvelle partie.
- Chronométrer plusieurs parcours complets.
- Installer et tester l'ensemble sur le PC prévu pour les Portes ouvertes à Sébeillon.

La durée de cinq à huit minutes est un objectif. Elle doit être confirmée par des essais chronométrés.

## Dépannage

### La connexion SQL Server échoue

Vérifier que le service SQL Server est démarré, que le nom de l'instance est correct, que l'authentification Windows est configurée et que le compte possède les droits nécessaires.

### Le pilote ODBC est introuvable

Installer Microsoft ODBC Driver 18 for SQL Server, puis vérifier que le nom configuré dans `SQL_DRIVER` correspond au pilote installé.

### Le volume de données est insuffisant

Vérifier que le générateur a terminé, puis exécuter `03_verify_volume.sql`. Ne pas modifier manuellement les compteurs pour simuler un volume atteint.

### Le mode simulation apparaît

Arrêter l'application, supprimer la variable `DEMO_MODE`, vérifier les paramètres SQL puis redémarrer.

### Le script de schéma signale des tables existantes

Vérifier que la base sélectionnée est bien la base de test prévue. Le script ne supprime volontairement aucune table existante.

## Remise à zéro

Le bouton « Recommencer » réinitialise uniquement la progression de la partie dans le navigateur. Il ne supprime aucune donnée SQL.

Toute reconstruction de la base doit être réalisée par une personne autorisée, après vérification des sauvegardes et de la base sélectionnée.