# Manuel d'installation

## Objectif

Ce manuel explique comment installer Mission SQL Cinéma sur un poste Windows. Il s'adresse à la personne qui prépare SQL Server et à l'élève qui lance l'application.

Effectuer les étapes dans l'ordre. La génération de données doit être terminée avant la démonstration.

## Prérequis

- Windows 10 ou Windows 11.
- SQL Server 2019 ou plus récent, installé et démarré.
- SQL Server Management Studio (SSMS).
- Outil en ligne de commande `sqlcmd`.
- Python 3.10 ou plus récent.
- Microsoft ODBC Driver 18 for SQL Server.
- Un compte Windows autorisé à créer la base et à installer les objets SQL.
- De l'espace disque disponible pour les données, les index et le journal des transactions. La taille nécessaire doit être mesurée sur le poste utilisé.

Le moteur SQL Server, SSMS, `sqlcmd` et Microsoft ODBC Driver 18 sont des composants distincts. Ils doivent être installés avant de commencer.

## Installation automatisee

Un script PowerShell est disponible à la racine du dépôt : `setup.ps1`.

Cette méthode effectue les étapes de préparation, les contrôles, l'installation des dépendances Python et le démarrage de l'application. Le moteur SQL Server doit déjà être installé et démarré. L'outil `sqlcmd` et Microsoft ODBC Driver 18 sont deux composants distincts à installer. Microsoft distribue séparément les outils en ligne de commande et le pilote ODBC : [installation de sqlcmd](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-download-install?view=sql-server-ver17) et [téléchargement du pilote ODBC](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver17).

Depuis l'Explorateur Windows, double-cliquer sur `setup.bat` à la racine du dépôt. Le fichier lance `setup.ps1` avec une politique d'exécution limitée à ce processus.

Depuis PowerShell, il est également possible d'exécuter :

```powershell
.\setup.bat
```

Pour préciser l'instance ou utiliser un autre port :

```powershell
.\setup.ps1 -SqlServer ".\SQLEXPRESS" -Port 5001
```

Le script vérifie les prérequis, crée la base si elle n'existe pas, installe le schéma uniquement si la base est vide, reprend la génération si des identifiants continus sont déjà présents, exécute les contrôles et les tests, puis ouvre le navigateur sur l'adresse locale.

Si le compte Windows ne possède pas le droit de lecture, un administrateur doit exécuter `sql/04_role_lecture.sql` et ajouter ce compte au rôle `mission_cinema_lecture`.

Le setup ne supprime aucune base ni table. Si le schéma est partiel ou incohérent, il s'arrête et demande une vérification manuelle. La première génération des dix millions de lignes peut prendre du temps.

Le processus Flask est lancé séparément. Le setup affiche son identifiant et le chemin des journaux dans `version-finale/mission-sql-cinema/logs/`. Pour arrêter le serveur, utiliser `Stop-Process -Id` suivi de l'identifiant affiché. Le navigateur s'ouvre après que le port répond.

## 1. Créer la base

Ouvrir SSMS et se connecter à l'instance prévue. Ouvrir sql/00_create_database.sql et exécuter le script.

La base créée s'appelle MissionCinema. Si elle existe déjà, le script ne la supprime pas et n'efface aucune donnée.

## 2. Créer le schéma

Dans SSMS, sélectionner MissionCinema, ouvrir sql/01_schema.sql et exécuter le script.

Le script crée les tables Films, Cinemas, Clients, Seances et Reservations, leurs clés et contraintes, puis les données de référence.

Le script refuse de continuer si des tables existent déjà dans le schéma dbo. Ce comportement est volontaire : il évite de supprimer ou d'écraser des données existantes. Pour une nouvelle installation, utiliser une base vide créée pour cette activité.

## 3. Générer les réservations

Exécuter sql/02_generate_reservations.sql sur MissionCinema.

Le générateur :
- vise exactement 10 000 000 réservations ;
- insère les données par lots de 500 000 lignes ;
- valide le nombre inséré pour chaque lot ;
- utilise une transaction par lot ;
- affiche l'avancement et la durée de chaque lot ;
- peut reprendre après une interruption si les identifiants déjà présents forment une suite continue de 1 jusqu'au nombre de lignes ;
- crée les index nécessaires après la génération.

Ne lancer qu'une seule génération à la fois. Surveiller l'espace disque, notamment celui du journal des transactions. Le temps nécessaire dépend du matériel, de la configuration SQL Server et du disque.

La répartition des données est construite pour rendre les trois défis compréhensibles :
- le Cinéma du Centre reçoit la plus grande part des réservations ;
- la science-fiction possède le plus grand nombre de réservations par genre ;
- le samedi est le jour de réservation le plus fréquent.

Ces répartitions sont des choix de génération synthétique. Elles ne représentent pas des statistiques réelles de cinémas.

Si la génération est interrompue, vérifier le dernier message affiché, puis relancer le même script. Ne pas vider la table ni modifier les identifiants à la main.

## 4. Vérifier les données

Exécuter sql/03_verify_volume.sql et conserver tous les résultats.

Le script affiche :
- le nombre de lignes par table ;
- le nombre exact de réservations et les volumes de référence ;
- le nombre de réservations sans séance ou sans client ;
- la répartition par genre, cinéma et jour de semaine ;
- une estimation de l'espace utilisé par les tables et leurs index.

Le résultat attendu est d'au moins 10 000 000 réservations, zéro réservation orpheline, Science-fiction en tête des genres, Cinéma du Centre en tête des établissements et samedi en tête des jours.

La requête d'espace utilise sys.dm_db_partition_stats. Si SQL Server refuse cette partie pour un problème d'autorisation, la faire exécuter par un administrateur de la base. Ne pas remplacer un résultat manquant par une estimation inventée.

## 5. Installer Python

Ouvrir PowerShell dans le dossier version-finale/mission-sql-cinema. Exécuter :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si l'activation de l'environnement est bloquée par la politique PowerShell, utiliser directement l'exécutable de l'environnement :

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 6. Configurer la connexion

Pour une instance locale SQLEXPRESS, configurer les variables dans la même fenêtre PowerShell :

```powershell
$env:SQL_SERVER = ".\SQLEXPRESS"
$env:SQL_DATABASE = "MissionCinema"
$env:SQL_DRIVER = "ODBC Driver 18 for SQL Server"
```

Le nom du serveur doit correspondre à l'instance installée. L'application utilise l'authentification Windows. Le compte Windows courant doit avoir le droit SELECT sur les cinq tables.

La chaîne de connexion utilise TrustServerCertificate=yes pour faciliter une connexion locale avec un certificat SQL Server auto-signé. Pour une instance distante, utiliser un certificat correctement configuré plutôt que de désactiver sa validation.

## 7. Préparer le rôle en lecture seule

Cette étape est destinée à l'administrateur SQL Server.

Exécuter sql/04_role_lecture.sql. Le script crée le rôle mission_cinema_lecture et lui accorde uniquement SELECT sur les tables de l'activité.

Un administrateur doit ensuite ajouter le compte Windows utilisé par l'application à ce rôle. Le nom du compte dépend du poste et ne doit pas être deviné dans le script.

## 8. Lancer l'application

Dans PowerShell, depuis le dossier de l'application, exécuter :

```powershell
python app.py
```

Ouvrir un navigateur sur :

`http://127.0.0.1:5000`

Garder la fenêtre PowerShell ouverte pendant l'activité. L'application écoute uniquement sur l'ordinateur local.

## 9. Mode simulation

Pour répéter l'interface sans SQL Server, fermer d'abord l'application, puis exécuter :

```powershell
$env:DEMO_MODE = "1"
python app.py
```

En mode simulation, l'application ne tente aucune connexion SQL Server. Une bannière indique clairement que les chiffres sont des exemples. Ce mode sert à tester l'affichage et l'enchaînement des écrans, pas à valider la base de données.

Pour revenir au mode réel :

```powershell
Remove-Item Env:DEMO_MODE -ErrorAction SilentlyContinue
python app.py
```

Vérifier que la bannière de simulation n'est plus affichée. Si elle l'est encore, contrôler les variables d'environnement et redémarrer l'application.

## 10. Tests

Les tests applicatifs peuvent être lancés sans SQL Server :

```powershell
python -m unittest discover -s tests -v
```

Sur un poste de test équipé de SQL Server, configurer SQL_SERVER, SQL_DATABASE et SQL_DRIVER, puis lancer les tests d'intégration :

```powershell
$env:RUN_SQL_INTEGRATION = "1"
python -m unittest discover -s tests -v
Remove-Item Env:RUN_SQL_INTEGRATION -ErrorAction SilentlyContinue
```

Les tests d'intégration vérifient le volume, les relations et les réponses attendues des trois défis. Ils peuvent lire les dix millions de lignes et prendre du temps. Ne pas les lancer pendant l'accueil des visiteurs.

## 11. Contrôle avant ouverture

- [ ] La génération SQL est terminée.
- [ ] Le résultat de sql/03_verify_volume.sql a été conservé.
- [ ] Au moins 10 000 000 réservations sont présentes.
- [ ] Aucun lien orphelin n'est signalé.
- [ ] Les résultats des trois défis sont cohérents.
- [ ] Le mode simulation est désactivé.
- [ ] L'application répond à http://127.0.0.1:5000.
- [ ] Une partie complète et le bouton Recommencer ont été testés.
- [ ] La durée réelle a été mesurée.
- [ ] La migration a été répétée sur le PC de Sébeillon.

## Dépannage

### La connexion SQL Server échoue

Vérifier que le service SQL Server est démarré, que le nom d'instance est exact, que le pilote ODBC 18 est installé et que le compte Windows possède les droits SELECT.

### Le pilote ODBC est introuvable

Installer Microsoft ODBC Driver 18 for SQL Server. Le texte de SQL_DRIVER doit être identique au nom du pilote installé.

### Le générateur signale des identifiants non continus

Ne pas relancer en boucle et ne pas supprimer de données. Contrôler la table Reservations, les identifiants minimum et maximum, puis demander une vérification à l'administrateur.

### Le schéma refuse de s'installer

Vérifier que la base sélectionnée est bien la base vide prévue. Le script ne supprime volontairement aucune table existante.

### La page affiche le mode simulation

Fermer l'application, supprimer DEMO_MODE, vérifier les paramètres SQL et redémarrer.

## Remise à zéro

Le bouton Recommencer efface uniquement la progression de la partie dans la session du navigateur. Il ne supprime aucune donnée SQL.

Toute reconstruction de base doit être effectuée par une personne autorisée, après vérification de la base sélectionnée et des sauvegardes.
