# Rapport de projet

## Problème initial

L'activité précédente portait sur la détection de joueurs suspects. Pour un visiteur qui découvre SQL, les critères techniques ne rendaient pas suffisamment évidents le but de l'activité ni l'intérêt des requêtes. Le scénario a donc été repensé.

## Concept retenu provisoirement

**Mission SQL : enquête au cinéma** propose trois défis : repérer le genre le plus réservé, le cinéma le plus fréquenté et le jour qui compte le plus de réservations. Le scénario doit être présenté à l'enseignant. Il n'est pas considéré comme validé avant une décision réelle.

## Architecture

L'interface locale utilise Flask. Python communique avec SQL Server via pyodbc. Les tables principales sont Films, Cinemas, Clients, Seances et Reservations. Les réservations sont des données synthétiques.

## Choix pédagogiques

Les défis utilisent des jointures, COUNT_BIG, GROUP BY, ORDER BY et DATEPART. Ces opérations servent à répondre à des questions concrètes. La correspondance exacte avec le programme de cours et le livre *SQL Server 2022* de J. Poirier doit être vérifiée avec les supports scolaires. Aucun chapitre ou numéro de page n'est inventé.

## Vérifications

Le workflow de tests unitaires GitHub Actions a réussi sur la branche de refonte. Cela ne démontre pas que SQL Server a été exécuté. La génération des dix millions de réservations, les relations, les performances, la durée de l'activité et la migration sur le PC cible restent à vérifier.

## Limites et prochaines étapes

1. Faire valider le scénario.
2. Exécuter les scripts SQL sur le poste prévu.
3. Conserver les résultats qui prouvent le volume et la cohérence des relations.
4. Mesurer le temps de génération, l'espace disque et la durée de plusieurs parties.
5. Tester l'installation sur un PC propre.
6. Compléter le journal avec les durées et activités réelles des collaborateurs.
