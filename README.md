# Mission SQL Cinéma

Projet scolaire destiné aux Journées Portes Ouvertes de l'ETML. L'activité propose trois défis guidés pour découvrir les jointures, les regroupements, les agrégations et l'analyse de dates avec Microsoft SQL Server.

## Projet actif

Le projet à utiliser se trouve dans [version-finale/mission-sql-cinema](version-finale/mission-sql-cinema/README.md).

Il comprend :
- une application locale Flask connectée à SQL Server avec pyodbc ;
- un schéma relationnel consacré aux films, cinémas, séances, clients et réservations ;
- un générateur visant 10 000 000 réservations synthétiques ;
- des scripts de vérification et de préparation d'un rôle SQL en lecture seule ;
- des tests applicatifs et des tests d'intégration SQL Server ;
- les manuels et documents de préparation.


## Installation rapide sous Windows

Depuis l'Explorateur Windows, double-cliquer sur `setup.bat` à la racine du dépôt.

Depuis PowerShell, il est également possible d'exécuter :

```powershell
.\setup.bat
```

Le fichier `setup.bat` lance `setup.ps1` avec une politique d'exécution limitée à ce processus. Pour personnaliser l'instance ou le port, utiliser directement PowerShell avec `setup.ps1`.

Le script vérifie SQL Server, sqlcmd, Python et ODBC Driver 18. Il crée la base si nécessaire, installe le schéma sur une base vide, reprend la génération des réservations si elle a été interrompue, vérifie les données, installe les dépendances, exécute les tests puis lance Flask et ouvre `http://127.0.0.1:5000`.

Le moteur SQL Server et les outils `sqlcmd` doivent être installés au préalable. L'utilisateur Windows doit avoir les droits nécessaires pour créer la base et lire les tables. Le script ne supprime pas de base ni de table existante. Il s'arrête si le schéma est partiel.

Pour choisir un autre port ou une autre instance :

```powershell
.\setup.ps1 -SqlServer ".\SQLEXPRESS" -Port 5001
```

Le setup ouvre le navigateur une fois le port disponible et laisse Flask tourner dans un processus séparé. Pour arrêter le serveur, utiliser `Stop-Process -Id` avec le PID affiché par le script. Les journaux sont enregistrés dans `version-finale/mission-sql-cinema/logs/`.

## Démarrage

Lire d'abord le [manuel d'installation](version-finale/mission-sql-cinema/docs/04-manuel-installation.md). La base de données doit être préparée avant le lancement de l'application.

Les tests unitaires peuvent être exécutés sans SQL Server. Les tests d'intégration, la génération réelle des données et la mesure des performances exigent une instance SQL Server accessible.

Le mode simulation est réservé aux répétitions de l'interface. Il affiche une bannière explicite et ne constitue pas une validation SQL.

## Documentation

- [Manuel d'installation](version-finale/mission-sql-cinema/docs/04-manuel-installation.md)
- [Manuel d'animation](version-finale/mission-sql-cinema/docs/05-manuel-animation.md)
- [Fiche de validation du scénario](version-finale/mission-sql-cinema/docs/02-fiche-validation-scenario.md)
- [Matrice de conformité](version-finale/mission-sql-cinema/docs/03-matrice-conformite.md)
- [Rapport de projet](version-finale/mission-sql-cinema/docs/06-rapport-projet.md)
- [Journal de travail](version-finale/mission-sql-cinema/docs/07-journal-travail-modele.md)
- [Planification des 32 périodes](version-finale/mission-sql-cinema/docs/08-plan-32-periodes.md)
- [Checklist de migration](version-finale/mission-sql-cinema/docs/11-checklist-migration.md)
- [Affiche imprimable](version-finale/mission-sql-cinema/docs/12-affiche.html)
- [Consignes visiteurs](version-finale/mission-sql-cinema/docs/13-document-visiteur.html)

## Archives

Le dossier archive conserve les versions précédentes du travail. Les anciens fichiers de version-finale qui ne font pas partie du dossier mission-sql-cinema sont également historiques. Ils ne constituent pas le parcours d'installation de l'activité actuelle.

## État et limites

Le scénario doit encore être validé par l'enseignant. Le volume de 10 millions de lignes, le temps de génération, l'espace disque, les performances des requêtes et l'installation sur le poste de Sébeillon doivent être vérifiés sur une véritable instance SQL Server et le PC cible.

Les documents et scripts décrivent la procédure prévue ; ils ne remplacent pas les preuves des essais réels.
