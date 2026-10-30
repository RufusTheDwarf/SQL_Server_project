# Manuel d'installation
Mission SQL Cinéma
ETML - Journées Portes Ouvertes
Version du 30 octobre 2026

## 1. Objectif

Ce manuel explique comment préparer et lancer Mission SQL Cinéma sur un ordinateur Windows. Il s'adresse à la personne qui installe SQL Server et à l'élève qui prépare le poste de démonstration.

La méthode recommandée est le lancement automatique avec le fichier setup.bat. Le script prépare la base, génère les réservations, vérifie les données, installe les dépendances Python, exécute les tests et ouvre l'interface dans le navigateur.

## 2. Prérequis

Les éléments suivants doivent être installés avant le lancement de setup.bat :

- Windows 10 ou Windows 11.
- Microsoft SQL Server 2019 ou une version plus récente, installé et démarré.
- SQL Server Management Studio (SSMS), pour administrer et contrôler la base.
- L'outil en ligne de commande sqlcmd.
- Python 3.10 ou une version plus récente.
- Microsoft ODBC Driver 18 for SQL Server.
- Un accès Internet lors de la première installation des bibliothèques Python.
- Un espace disque suffisant pour les données, les index et le journal SQL Server. La place réellement nécessaire doit être mesurée sur le poste de préparation.

Le moteur SQL Server, sqlcmd et le pilote ODBC sont des composants différents. Le fichier setup.bat ne les installe pas. Il vérifie leur présence et s'arrête en indiquant le composant manquant.

Téléchargements Microsoft :
- sqlcmd : https://learn.microsoft.com/sql/tools/sqlcmd/sqlcmd-download-install
- ODBC Driver 18 : https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server

## 3. Installation automatique recommandée

### 3.1 Récupérer le projet

Télécharger ou cloner le dépôt complet, puis extraire le dossier. Ne pas déplacer uniquement le dossier de l'application : le fichier setup.bat doit rester à la racine du dépôt, au même niveau que setup.ps1 et version-finale.

Dépôt : https://github.com/RufusTheDwarf/SQL_Server_project

### 3.2 Lancer le setup

Depuis l'Explorateur Windows, double-cliquer sur le fichier setup.bat situé à la racine du dépôt.

Une fenêtre de commande s'ouvre. Le script effectue successivement les opérations suivantes :

1. Vérifie le dossier du projet et les fichiers indispensables.
2. Vérifie que le port demandé n'est pas déjà utilisé.
3. Vérifie que SQL Server répond et que sqlcmd peut s'y connecter avec l'authentification Windows.
4. Vérifie Python 3.10 ou plus récent.
5. Crée l'environnement Python .venv si nécessaire.
6. Installe les dépendances de requirements.txt.
7. Vérifie la présence de ODBC Driver 18.
8. Crée la base MissionCinema si elle n'existe pas.
9. Installe le schéma uniquement si la base est vide.
10. Vérifie que le compte Windows possède le droit de lecture.
11. Génère ou reprend les dix millions de réservations.
12. Exécute les contrôles de volume, de relations et de résultats.
13. Exécute les tests applicatifs et les tests d'intégration SQL.
14. Démarre Flask et ouvre l'adresse locale dans le navigateur lorsque le port répond.

La première génération des dix millions de réservations peut être longue. Les données sont insérées par lots de 500 000 lignes. Chaque lot est validé avant de passer au suivant.

### 3.3 Paramètres facultatifs

La configuration par défaut utilise l'instance SQL Server .\SQLEXPRESS et le port local 5000.

Pour utiliser un autre nom d'instance ou un autre port, ouvrir PowerShell à la racine du dépôt et exécuter par exemple :

```powershell
.\setup.ps1 -SqlServer ".\SQLEXPRESS" -Port 5001
```

L'adresse devient alors http://127.0.0.1:5001.

### 3.4 Fin du setup et arrêt de l'application

Quand le navigateur s'ouvre, l'application Flask fonctionne dans un processus séparé. La fenêtre du setup affiche son identifiant de processus (PID) et le chemin du journal d'erreurs.

Pour arrêter Flask, ouvrir PowerShell et exécuter la commande avec le PID affiché :

```powershell
Stop-Process -Id 12345
```

Remplacer 12345 par le PID réel. Les journaux sont conservés dans :

`version-finale/mission-sql-cinema/logs/`

Ne pas supprimer les journaux avant d'avoir analysé un éventuel problème.

## 4. Droits SQL Server

Le setup utilise l'authentification Windows. Le compte qui effectue la première installation doit pouvoir créer la base, installer les tables et insérer les réservations.

Après la préparation initiale, il est possible d'utiliser un compte Windows dédié à l'application avec des droits de lecture seule :

1. Un administrateur exécute sql/04_role_lecture.sql dans la base MissionCinema.
2. L'administrateur crée le login et l'utilisateur SQL correspondant au compte Windows du poste, si nécessaire.
3. L'administrateur ajoute cet utilisateur au rôle mission_cinema_lecture.
4. Ouvrir une session Windows avec ce compte de lecture seule et relancer setup.bat. La base étant déjà préparée, le générateur ne réinsère pas les dix millions de lignes. Le script vérifie l'accès, exécute les tests puis lance l'application sous ce compte.

Exemple à adapter dans SSMS, avec le nom Windows réel à la place de DOMAINE\ComptePO :

```sql
USE master;
GO
CREATE LOGIN [DOMAINE\ComptePO] FROM WINDOWS;
GO
USE MissionCinema;
GO
CREATE USER [DOMAINE\ComptePO] FOR LOGIN [DOMAINE\ComptePO];
ALTER ROLE mission_cinema_lecture ADD MEMBER [DOMAINE\ComptePO];
GO
```

Si le login ou l'utilisateur existe déjà, ne pas le recréer. L'administrateur vérifie alors son appartenance au rôle.

## 5. Ce que le setup ne fait pas

Le setup ne télécharge ni n'installe le moteur SQL Server, SSMS, sqlcmd ou ODBC Driver 18. Il ne supprime aucune base et aucune table existante.

Si la base MissionCinema contient un schéma partiel ou inattendu, le script s'arrête. Il faut faire vérifier la base avant de recommencer. Ne pas supprimer les tables pour contourner le message.

Le setup ne valide pas l'installation sur un autre ordinateur. Un essai réel reste nécessaire sur le PC prévu pour les Portes Ouvertes à Sébeillon.

## 6. Installation manuelle

Cette procédure est une solution de secours si le lancement automatique n'est pas possible.

### 6.1 Créer la base

Dans SSMS, se connecter à l'instance prévue et exécuter sql/00_create_database.sql.

La base s'appelle MissionCinema. Le script ne supprime pas une base existante.

### 6.2 Créer les tables et les données de référence

Sélectionner MissionCinema dans SSMS et exécuter sql/01_schema.sql.

Le script crée les tables Films, Cinemas, Clients, Seances et Reservations, les clés et contraintes, puis insère les données de référence. Il refuse de continuer si des tables existent déjà dans le schéma dbo.

### 6.3 Générer les réservations

Exécuter sql/02_generate_reservations.sql.

Le script vise dix millions de réservations, travaille par lots de 500 000 lignes, valide le nombre inséré dans chaque lot et peut reprendre une génération interrompue si les identifiants déjà présents forment une suite continue.

Ne pas lancer plusieurs générations simultanément. Ne pas vider la table et ne pas modifier manuellement les identifiants.

### 6.4 Vérifier les données

Exécuter sql/03_verify_volume.sql et conserver les résultats. Vérifier au minimum :

- Au moins 10 000 000 réservations.
- Zéro réservation sans séance.
- Zéro réservation sans client.
- Science-fiction en tête des genres.
- Cinéma du Centre en tête des cinémas.
- Samedi en tête des jours de réservation.

Le script affiche également une estimation de l'espace utilisé par les tables et leurs index.

### 6.5 Installer Python

Ouvrir PowerShell dans version-finale/mission-sql-cinema et exécuter :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si l'activation de l'environnement est bloquée, utiliser directement .venv\Scripts\python.exe.

### 6.6 Configurer et démarrer Flask

Pour une instance locale nommée SQLEXPRESS :

```powershell
$env:SQL_SERVER = ".\SQLEXPRESS"
$env:SQL_DATABASE = "MissionCinema"
$env:SQL_DRIVER = "ODBC Driver 18 for SQL Server"
python app.py
```

Ouvrir ensuite http://127.0.0.1:5000. L'application écoute uniquement sur l'ordinateur local.

## 7. Mode simulation

Le mode simulation sert uniquement à répéter l'interface lorsque SQL Server n'est pas disponible. Il ne doit pas être présenté comme une démonstration SQL en direct.

Dans PowerShell, depuis le dossier de l'application :

```powershell
$env:DEMO_MODE = "1"
python app.py
```

Une bannière MODE SIMULATION est affichée et les chiffres sont des exemples. Pour revenir au mode réel :

```powershell
Remove-Item Env:DEMO_MODE -ErrorAction SilentlyContinue
python app.py
```

Vérifier que la bannière de simulation a disparu.

## 8. Tests

Les tests applicatifs ne nécessitent pas SQL Server :

```powershell
python -m unittest discover -s tests -p test_app.py -v
```

Les tests d'intégration nécessitent une base MissionCinema complète et au moins dix millions de réservations :

```powershell
$env:RUN_SQL_INTEGRATION = "1"
python -m unittest discover -s tests -p test_sql_integration.py -v
Remove-Item Env:RUN_SQL_INTEGRATION -ErrorAction SilentlyContinue
```

Ces tests contrôlent le volume, les relations et le résultat des trois défis. Ils peuvent lire un grand nombre de lignes et ne doivent pas être lancés pendant l'accueil du public.

## 9. Dépannage

### sqlcmd est introuvable

Installer les outils en ligne de commande SQL Server, puis fermer et rouvrir PowerShell pour actualiser le PATH.

### SQL Server ne répond pas

Vérifier que le service est démarré et que le nom de l'instance correspond au paramètre -SqlServer.

### Le pilote ODBC est introuvable

Installer Microsoft ODBC Driver 18 for SQL Server. Vérifier que son nom correspond à la valeur SQL_DRIVER.

### Le droit SELECT est absent

Un administrateur doit exécuter sql/04_role_lecture.sql puis ajouter le compte Windows au rôle mission_cinema_lecture. Relancer le setup sous ce compte.

### Le schéma est partiel

Ne pas supprimer de tables à la main. Faire contrôler la base MissionCinema par l'administrateur et décider d'une procédure de réparation ou de réinstallation sur une base de test.

### Le port 5000 est déjà utilisé

Fermer l'application qui occupe le port ou lancer setup.ps1 avec -Port 5001.

### L'application ne démarre pas

Consulter logs/flask-stderr.log dans le dossier de l'application. Vérifier les paramètres SQL et les droits du compte Windows.

## 10. Contrôle avant ouverture au public

- [ ] SQL Server est démarré.
- [ ] La base MissionCinema est accessible.
- [ ] Le setup termine sans erreur.
- [ ] Le contrôle indique au moins dix millions de réservations.
- [ ] Aucune réservation orpheline n'est signalée.
- [ ] Les trois défis affichent des résultats.
- [ ] La bannière MODE SIMULATION n'est pas affichée.
- [ ] Une partie complète a été effectuée.
- [ ] Le bouton Recommencer a été testé.
- [ ] Le port et l'adresse locale fonctionnent sur l'écran prévu.
- [ ] L'installation a été essayée sur le PC de Sébeillon.

La durée de cinq à huit minutes est un objectif. Elle doit être confirmée par des essais chronométrés avec plusieurs personnes.
