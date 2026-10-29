# Projet SQL Server pour les Portes ouvertes de l'ETML

Ce dépôt contient des travaux SQL Server, des scripts de génération et des documents de projet. La refonte est développée sur la branche `refonte-activite-etml` afin de préserver la branche principale et les ressources historiques.

## Activité en refonte

**Mission SQL : enquête au cinéma** propose trois défis autour des réservations d'un festival fictif. Le visiteur découvre comment des jointures, des regroupements et des tris permettent de répondre à des questions concrètes.

Statut : prototype fonctionnel côté application, scénario à faire valider par l'enseignant. Les tests unitaires passent dans GitHub Actions. Le volume réel de dix millions de réservations, les performances SQL Server, la durée de cinq à huit minutes et l'installation sur le PC cible restent à vérifier.

## Démarrage

Consulter [le README de l'activité](version-finale/mission-sql-cinema/README.md).

Ordre des scripts SQL :

1. `sql/00_create_database.sql`
2. `sql/01_schema.sql`
3. `sql/02_generate_reservations.sql`
4. `sql/03_verify_volume.sql`
5. Facultatif : `sql/04_role_lecture.sql` pour préparer un rôle de lecture seule.

L'application utilise Flask et pyodbc. Elle se lance localement sur `http://127.0.0.1:5000`. SQL Server est requis pour les résultats réels. Le mode simulation est clairement signalé.

## Documentation

- [Audit du dépôt](version-finale/mission-sql-cinema/docs/01-audit.md)
- [Fiche de validation du scénario](version-finale/mission-sql-cinema/docs/02-validation-scenario.md)
- [Manuel d'installation](version-finale/mission-sql-cinema/docs/03-manuel-installation.md)
- [Manuel de formation et d'animation](version-finale/mission-sql-cinema/docs/04-manuel-animation.md)
- [Rapport de projet](version-finale/mission-sql-cinema/docs/05-rapport-projet.md)
- [Modèle de journal de travail](version-finale/mission-sql-cinema/docs/06-journal-travail.md)
- [Planification sur 32 périodes](version-finale/mission-sql-cinema/docs/07-plan-32-periodes.md)
- [Matrice de conformité](version-finale/mission-sql-cinema/docs/08-matrice-conformite.md)
- [Affiche imprimable HTML](version-finale/mission-sql-cinema/docs/12-affiche.html)
- [Consignes visiteurs HTML](version-finale/mission-sql-cinema/docs/13-document-visiteur.html)

## Vérifications et limites connues

Les tests unitaires de l'application sont dans `version-finale/mission-sql-cinema/tests/`. Le workflow GitHub Actions exécute ces tests sans serveur SQL Server. Le succès de ces tests ne prouve pas que les scripts SQL ont été exécutés ni que dix millions de lignes existent.

Avant de déclarer le projet terminé, il faut exécuter les scripts sur SQL Server, conserver les résultats de `03_verify_volume.sql`, mesurer la durée de génération et l'espace disque, tester plusieurs parties chronométrées et réaliser une installation sur le PC de démonstration.

## Ressources historiques

- `version-finale/portes-ouvertes/` : application précédente de détection de joueurs suspects.
- `version-finale/01-script-generation-bd/` : ancien générateur de données.
- `version-finale/02-scenario-enquete/` : anciens exercices d'enquête.
- `version-finale/03-manuels/` et `version-finale/04-rapport/` : documents antérieurs.
- `E-P_DB-PréparationPO-CDC-v26.pdf` : cahier des charges.

## Référence pédagogique

Le cahier des charges demande de s'appuyer sur le livre *SQL Server 2022* de J. Poirier. L'ouvrage n'a pas été consulté dans les ressources accessibles à cette étape. Aucun chapitre ou numéro de page n'est inventé. Les notions exactes doivent être confirmées avec l'enseignant.
