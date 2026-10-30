# Rapport de projet : Mission SQL au cinéma

## Problème initial

Le dépôt contenait une activité d'analyse de joueurs suspects. Le scénario demandait au visiteur de régler plusieurs critères techniques et ne rendait pas immédiatement visible l'intérêt des opérations SQL. L'enseignant a jugé l'activité précédente non pertinente. La nouvelle piste doit donc être validée avant d'être considérée comme le choix final.

## Concepts envisagés

La détection de joueurs suspects a été conservée comme référence historique. La piste cinéma a été retenue provisoirement parce que les films, séances, cinémas et réservations sont compréhensibles pour un public sans connaissance informatique. Une validation pédagogique reste nécessaire.

## Choix et architecture

L'application utilise Flask pour l'interface locale et pyodbc pour communiquer avec SQL Server. Les requêtes de l'activité sont des SELECT avec jointures et agrégations. Les réponses sont tirées du résultat réel de la requête. Un mode de simulation facultatif est signalé à l'écran.

Le schéma contient Films, Cinemas, Seances et Reservations. La génération prévue utilise des données synthétiques et vise dix millions de réservations.

## Pertinence pédagogique

Les défis sont conçus pour expliquer les jointures, COUNT, GROUP BY, ORDER BY et DATEPART. Ces notions doivent être confirmées avec l'enseignant et reliées aux éléments réellement enseignés, ainsi qu'au livre SQL Server 2022 de J. Poirier. Aucun chapitre ou numéro de page n'est indiqué sans consultation de l'ouvrage.

## Tests et limites

Des tests unitaires de la logique applicative sont présents. Leur exécution doit être confirmée avec les dépendances installées. Les scripts SQL, la génération des dix millions de lignes, la durée, l'espace disque et la migration doivent être vérifiés sur un serveur SQL Server réel.

Le rapport ne déclare donc pas le projet terminé. Les prochaines étapes sont la validation du scénario, les tests réels, la production des documents visiteurs Word et PDF, l'affiche et le journal de travail vérifié.
