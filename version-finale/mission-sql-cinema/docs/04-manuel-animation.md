# Manuel de formation et d'animation

## Présentation orale

« Un festival doit décider ce qui intéresse le public. Tu vas répondre à trois questions à partir des réservations d'un cinéma fictif. Observe les résultats, choisis une réponse et découvre comment la base a trouvé le résultat. »

## Déroulement cible

| Temps cible | Animation |
| --- | --- |
| 0:00 à 0:30 | Présenter le scénario et l'objectif |
| 0:30 à 1:30 | Lire le premier défi et montrer les résultats |
| 1:30 à 4:30 | Accompagner les trois choix |
| 4:30 à 5:30 | Expliquer le score et les notions SQL |
| 5:30 à 6:00 | Recommencer la partie |

Cette chronologie est un objectif, pas une mesure. Chronométrer des personnes qui ne connaissent pas SQL.

## Notions à expliquer

- **Jointure :** relie une réservation à sa séance, puis au film ou au cinéma concerné.
- **COUNT_BIG :** compte les lignes et convient aux grands volumes.
- **GROUP BY :** rassemble les lignes qui partagent une valeur, par exemple le genre.
- **ORDER BY :** classe les résultats pour identifier le total le plus élevé.
- **DATEPART :** extrait le jour de la semaine à partir d'une date.

## Défis

1. Genre le plus réservé. La requête relie les réservations, les séances et les films, puis compte les réservations par genre.
2. Cinéma le plus fréquenté. La requête relie les réservations, les séances et les cinémas, puis compte les réservations par cinéma.
3. Jour le plus fréquent. La requête groupe les réservations par jour de la semaine.

Les réponses correctes dépendent des données réellement présentes. Elles ne doivent pas être annoncées avant d'avoir exécuté les requêtes sur la base de démonstration.

## Questions possibles

**Pourquoi faut-il plusieurs tables ?** Pour éviter de recopier toutes les informations du film et du cinéma dans chaque réservation et pour garder les relations cohérentes.

**Pourquoi SQL peut-il aider ?** Il peut compter, filtrer et comparer beaucoup de lignes plus rapidement qu'une personne qui le ferait manuellement.

**Les données sont-elles réelles ?** Non. Elles sont synthétiques, créées pour la démonstration.

**Qu'est-ce qu'une jointure ?** Une opération qui rassemble des informations de plusieurs tables à partir de clés liées.

## En cas de problème

- Si la base est indisponible, vérifier la connexion avec l'élève responsable.
- Si le mode simulation est actif, le signaler explicitement au visiteur.
- Si une requête échoue, ne pas inventer la réponse. Interrompre le mode réel et utiliser la procédure de secours.
- Le bouton de nouvelle partie remet le score et la progression à zéro sans supprimer les données.
