# Fiche de validation du scénario

**Statut : à présenter à l'enseignant. Aucune validation n'est présumée.**

## Thème

Mission SQL : enquête au cinéma.

## Public cible

Parents et adolescents visitant les Portes ouvertes de l'ETML, sans connaissance SQL préalable.

## Histoire en moins de 30 secondes

Un festival doit préparer sa programmation. Le visiteur analyse des réservations fictives pour découvrir les genres les plus demandés, le cinéma le plus fréquenté et le jour où les réservations sont les plus nombreuses.

## Objectifs pédagogiques

À la fin de l'activité, le visiteur doit pouvoir expliquer simplement qu'une base de données stocke des informations liées, que SQL peut compter et regrouper de nombreuses lignes, et qu'une jointure relie des informations réparties dans plusieurs tables.

## Déroulement prévu

| Temps cible | Action |
| --- | --- |
| 0:00 à 0:30 | Présentation de la mission |
| 0:30 à 1:30 | Première question et découverte des résultats |
| 1:30 à 4:30 | Trois défis guidés |
| 4:30 à 5:30 | Résultat et explication des notions |
| 5:30 à 6:00 | Remise à zéro et passage au visiteur suivant |

Cette durée est une estimation de conception, pas une mesure. Des essais chronométrés sont requis.

## Notions SQL proposées

- `JOIN` pour relier les réservations, séances, films et cinémas.
- `COUNT_BIG` pour compter un grand nombre de réservations.
- `GROUP BY` pour comparer des groupes.
- `ORDER BY` pour classer les résultats.
- `DATEPART` pour regrouper les réservations selon le jour de la semaine.

## Pertinence pour les cours ICT

L'activité montre une utilisation concrète des bases relationnelles et des requêtes pour répondre à une question. Elle ne se limite pas à insérer des lignes. L'élève doit toutefois confirmer que les notions correspondent au cours réellement suivi et au livre *SQL Server 2022* de J. Poirier.

## Données

Les données sont synthétiques et reproductibles. Le script vise dix millions de réservations. Le volume réel n'est confirmé qu'après exécution de `sql/03_verify_volume.sql`.

## Questions de validation

- Le scénario est-il pertinent et assez interactif ?
- Les notions choisies correspondent-elles au cours ?
- Le niveau de difficulté est-il adapté au public ?
- Le volume et la méthode de génération conviennent-ils au matériel disponible ?
- L'enseignant souhaite-t-il une modification du scénario avant développement final ?

## Décision de l'enseignant

À compléter après la présentation.

- Date :
- Décision : accepté / accepté avec modifications / refusé
- Modifications demandées :
- Nom ou signature de validation :
