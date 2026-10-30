# Rapport de projet : Mission SQL au cinéma

## Problème initial

Le dépôt contenait une activité d'analyse de joueurs suspects. Le scénario demandait au visiteur de régler plusieurs critères techniques et ne rendait pas immédiatement visible l'intérêt des opérations SQL. La nouvelle activité doit être plus accessible à un public qui découvre la filière informatique.

## Choix du scénario

La piste du cinéma met en scène des films, des séances, des établissements et des réservations. Ces informations sont compréhensibles sans connaissances informatiques. Le visiteur devient analyste et répond à trois questions en observant les résultats d'une base relationnelle.

Le scénario doit encore être présenté à l'enseignant. Sa validation pédagogique n'est pas acquise.

## Architecture

L'interface est développée avec Flask. La bibliothèque pyodbc relie Python à Microsoft SQL Server. Les requêtes de l'activité sont des SELECT avec jointures et agrégations.

Le schéma contient les tables Films, Cinemas, Clients, Seances et Reservations. Les clés étrangères relient les réservations aux séances et aux clients, puis les séances aux films et aux cinémas.

Un générateur T-SQL produit jusqu'à 10 000 000 réservations synthétiques par lots de 500 000 lignes. La distribution est déterministe et conçue pour créer trois réponses distinctes. La science-fiction arrive en tête des genres, le Cinéma du Centre en tête des établissements et le samedi en tête des jours de réservation.

## Choix de sécurité et de fonctionnement

L'application utilise l'authentification Windows et des requêtes SQL définies dans le code. La réponse du visiteur est comparée aux options proposées. Elle n'est pas insérée dans une chaîne SQL.

Le mode simulation est séparé du mode réel. Lorsqu'il est activé, l'application n'essaie pas de se connecter à SQL Server et affiche une bannière visible.

Un rôle SQL en lecture seule peut être préparé pour limiter les droits du compte utilisé lors de l'activité.

## Intérêt pédagogique

Les trois défis illustrent SELECT, JOIN, GROUP BY, COUNT_BIG, ORDER BY et DATEPART. Ils permettent de montrer comment des tables sont reliées, comment des lignes sont regroupées et comment un résultat est trié.

La correspondance avec le programme ICT et le livre SQL Server 2022 de J. Poirier doit être vérifiée avec l'enseignant. Aucun chapitre ni numéro de page n'est attribué sans consultation de l'ouvrage.

## Vérifications et limites

Les tests unitaires vérifient le comportement de l'application sans serveur SQL. Les tests d'intégration présents dans le dépôt nécessitent une instance SQL Server, une base préparée et la variable RUN_SQL_INTEGRATION=1.

Le code et le générateur ne prouvent pas que les dix millions de réservations sont déjà installées. Le temps de génération, l'espace disque, les performances, la durée du parcours et la migration sur le PC de Sébeillon restent à mesurer.

La validation du scénario par l'enseignant et les essais avec des visiteurs restent également à effectuer.

## Prochaines étapes

1. Exécuter les scripts sur une instance SQL Server de test.
2. Conserver les résultats de sql/03_verify_volume.sql.
3. Exécuter les tests d'intégration.
4. Mesurer le temps de génération et l'espace disque.
5. Tester l'activité avec plusieurs personnes et chronométrer le parcours.
6. Réaliser l'installation sur un autre PC Windows.
7. Corriger les documents après les essais et obtenir la validation pédagogique.
