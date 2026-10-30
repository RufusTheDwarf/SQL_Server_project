# Manuel de formation et d'animation

## Avant l'arrivée du visiteur

1. Ouvrir l'application et vérifier que SQL Server répond.
2. Vérifier que le mode simulation n'est pas actif.
3. Faire un parcours de contrôle et utiliser le bouton de recommencement.
4. Garder cette fiche à portée de main.

## Présentation à dire au visiteur

« Un festival doit décider ce qui intéresse le public. Tu vas répondre à trois questions en utilisant les réservations d'un cinéma fictif. Tu n'as pas besoin de connaître SQL. Observe les résultats et choisis la réponse la plus fréquente. »

## Déroulement cible

| Temps visé | Étape |
|---|---|
| 0:00 à 0:30 | Présenter la mission |
| 0:30 à 1:30 | Lire la première question et expliquer les chiffres |
| 1:30 à 4:30 | Répondre aux trois défis |
| 4:30 à 5:30 | Expliquer le score et les notions utilisées |
| 5:30 à 6:00 | Recommencer et accueillir le visiteur suivant |

Cette grille est une cible de travail, pas une mesure validée. Adapter après plusieurs essais chronométrés.

## Explications pédagogiques

**Jointure :** une réservation indique une séance. La séance indique un film et un cinéma. Une jointure relie ces informations.

**GROUP BY :** regroupe les lignes qui ont une même valeur, par exemple le genre du film.

**COUNT :** compte les lignes de chaque groupe.

**ORDER BY :** trie les groupes pour repérer le total le plus élevé.

**DATEPART :** extrait une partie d'une date, ici le jour de la semaine.

## Réponses attendues

La bonne réponse de chaque défi est la première option issue du résultat SQL trié par total décroissant. Les totaux dépendent des données générées et doivent être observés dans la base installée. Ne mémoriser aucun chiffre avant l'exécution réelle.

## Questions possibles

**À quoi sert une base de données ?** À conserver des informations organisées et à permettre de les retrouver ou de les analyser.

**Pourquoi plusieurs tables ?** Pour séparer les informations et relier les éléments par des clés.

**Pourquoi dix millions de lignes ?** Pour montrer qu'une base peut gérer beaucoup de données et que les requêtes doivent être structurées. La présence réelle du volume doit être vérifiée avant la présentation.

**Les données sont-elles réelles ?** Non. Ce sont des données synthétiques créées pour l'exercice.

## En cas de problème

- Si la connexion échoue, vérifier la fenêtre du serveur et la configuration avant de relancer.
- Si le mode simulation apparaît, annoncer clairement que les chiffres sont des exemples. Ne pas présenter cette partie comme une requête SQL réelle.
- Si l'application ne répond plus, arrêter puis relancer `python app.py`.
- Si la base est indisponible, utiliser une activité de secours validée par l'enseignant plutôt que d'inventer un résultat.

## Fin de partie

Demander au visiteur ce que fait une jointure ou pourquoi on regroupe les lignes. Puis utiliser « Recommencer la partie ». Le bouton ne supprime aucune donnée de la base.
