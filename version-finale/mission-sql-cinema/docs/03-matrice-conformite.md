# Matrice de conformité au cahier des charges

Cette synthèse décrit les fichiers et les contrôles prévus. Un statut « en place » signifie que le code ou le document existe. Il ne prouve pas qu'un test a été exécuté sur un vrai serveur ou avec un visiteur.

## En place dans le dépôt

- Activité guidée sur le thème du cinéma : trois défis sont présents dans l'application Flask.
- Utilisation de Microsoft SQL Server : connexion pyodbc et scripts T-SQL présents.
- Données synthétiques : schéma relationnel et générateur visant 10 000 000 réservations.
- Notions SQL : SELECT, jointures, GROUP BY, COUNT_BIG, ORDER BY et DATEPART.
- Mode simulation : identifié à l'écran et séparé du mode SQL réel.
- Requêtes paramétrées : les réponses du visiteur sont comparées aux options connues ; elles ne sont pas concaténées dans une requête SQL.
- Lecture seule : un rôle SQL dédié peut être préparé avec le script 04.
- Tests : tests applicatifs et tests d'intégration SQL Server présents.
- Documentation : manuels d'installation et d'animation, rapport, fiche de validation, consignes visiteurs, affiche, journal modèle et plan des 32 périodes présents.

## À vérifier sur un vrai SQL Server

- La présence effective d'au moins 10 000 000 réservations.
- L'absence de références orphelines.
- Les résultats des trois requêtes et l'ordre des réponses.
- La durée de génération sur le PC de préparation.
- L'espace disque utilisé par les données, les index et le journal des transactions.
- Le temps de réponse des défis après la génération.
- L'exécution des tests d'intégration avec RUN_SQL_INTEGRATION=1.
- L'installation complète sur un PC Windows distinct, avec exécution réelle de `setup.bat`.

## À valider avec l'enseignant et les visiteurs

- L'adéquation du scénario au public des Portes ouvertes.
- La correspondance des notions avec le programme ICT et le livre SQL Server 2022 de J. Poirier.
- La compréhension des consignes par un visiteur débutant.
- La durée réelle du parcours, remise à zéro comprise.
- La procédure d'animation et l'activité de secours.

## Preuves à conserver

1. Résultats complets de sql/03_verify_volume.sql.
2. Temps de génération et espace disque relevés.
3. Sortie des tests unitaires et des tests SQL Server.
4. Mesures de plusieurs parcours chronométrés.
5. Résultat d'installation sur le PC de Sébeillon.
6. Décision de validation du scénario par l'enseignant.

## Règle de mise à jour

Ne passer une exigence de « à vérifier » à « validée » qu'après avoir conservé une preuve datée. Une exécution réussie des tests unitaires ne valide ni les données SQL réelles ni l'installation sur le poste final.
