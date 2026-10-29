# Projet SQL Server pour les Portes ouvertes de l'ETML

Ce dépôt contient des travaux SQL Server, des scripts de génération de données et des documents de projet. La refonte pédagogique est développée dans une branche distincte afin de préserver les travaux antérieurs.

## Activité en refonte

La nouvelle piste est **Mission SQL : enquête au cinéma**. Le visiteur répond à trois questions à partir de données de réservations. L'application doit montrer comment SQL relie des tables, regroupe des lignes et trie des résultats.

Statut : prototype ajouté, scénario à faire valider par l'enseignant. Le fonctionnement avec SQL Server, les dix millions de lignes et la durée de 5 à 8 minutes restent à vérifier sur le poste cible.

## Structure utile

- `version-finale/mission-sql-cinema/` : nouvelle application, scripts SQL, tests et documentation.
- `version-finale/portes-ouvertes/` : application précédente de détection de joueurs suspects.
- `version-finale/01-script-generation-bd/` : ancien générateur de données.
- `version-finale/02-scenario-enquete/` : anciens exercices d'enquête.
- `version-finale/03-manuels/` et `version-finale/04-rapport/` : documents antérieurs.
- `archive/` : versions historiques conservées pour référence.
- `E-P_DB-PréparationPO-CDC-v26.pdf` : cahier des charges fourni.

## Lancer le prototype cinéma

Consulter [le README de l'activité](version-finale/mission-sql-cinema/README.md). L'application utilise Flask et pyodbc, et fonctionne en local. SQL Server est requis pour les résultats réels. Le mode simulation est explicitement signalé et ne doit pas être utilisé pour prétendre à une exécution SQL.

## Vérifications

Les tests unitaires sont dans `version-finale/mission-sql-cinema/tests/`. Les scripts de création, génération et contrôle des volumes sont dans `version-finale/mission-sql-cinema/sql/`.

Aucune preuve d'une exécution SQL Server n'est fournie par le dépôt à ce stade. Il faut exécuter les scripts, conserver les résultats de contrôle et mesurer le temps et l'espace réellement utilisés.

## Livrables attendus

Les documents d'installation et d'animation, les documents visiteurs Word et PDF, le rapport actualisé, l'affiche et le journal de travail doivent être finalisés après validation du scénario et essais réels. Le journal ne doit contenir que des activités et durées vérifiables.

## Référence pédagogique

Le cahier des charges demande de s'appuyer sur le livre *SQL Server 2022* de J. Poirier. Les chapitres et pages ne sont pas cités ici car l'ouvrage n'a pas été consulté dans les ressources accessibles. Les notions exactes doivent être confirmées avec l'enseignant.
