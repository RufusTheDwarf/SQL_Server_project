# Manuel d'animation

## Objectif

Le visiteur aide un festival à comprendre les préférences de son public à partir de réservations d'un cinéma fictif. Il répond à trois défis qui utilisent réellement des requêtes SQL lorsque le mode simulation est désactivé.

Le parcours vise 5 à 8 minutes. La durée n'a pas encore été mesurée avec plusieurs visiteurs.

## Préparation avant l'arrivée du public

1. Démarrer SQL Server et vérifier que MissionCinema est accessible.
2. Démarrer l'application avec le manuel d'installation.
3. Vérifier que la bannière MODE SIMULATION n'est pas affichée.
4. Effectuer une partie complète.
5. Vérifier que les trois défis affichent des résultats.
6. Tester le bouton Recommencer.
7. Laisser l'application ouverte sur le premier défi.

Si SQL Server n'est pas disponible, ne pas présenter des résultats simulés comme une exécution réelle.

## Présentation au visiteur

« Un festival veut organiser sa programmation en fonction des goûts du public. Tu vas analyser les réservations d'un cinéma fictif et répondre à trois questions. Pas besoin de connaître SQL à l'avance. Observe les chiffres, compare les réponses et choisis celle qui te semble correcte. »

## Déroulement conseillé

### 0 à 30 secondes : présenter la mission

Expliquer le contexte du cinéma et les trois questions. Préciser que les données sont fictives, mais structurées comme celles d'une vraie base relationnelle.

### 30 secondes à 1 minute : expliquer l'écran

Montrer où se trouve la question, comment sélectionner une réponse et où lire les nombres. Laisser le visiteur lire lui-même.

### 1 à 4 minutes : réaliser les trois défis

Laisser le visiteur réfléchir et choisir. Intervenir seulement s'il ne comprend pas la consigne ou le vocabulaire.

### 4 à 5 minutes : expliquer les résultats

Relier les réponses aux opérations SQL visibles à l'écran. Expliquer pourquoi les données doivent être reliées et regroupées avant de pouvoir comparer les totaux.

### 5 à 6 minutes : conclure et réinitialiser

Demander au visiteur ce qu'il a appris, le remercier, puis cliquer sur Recommencer.

Ce déroulement est une proposition. Il doit être ajusté après des essais chronométrés.

## Notions SQL utilisées

### SELECT

SELECT indique les colonnes ou les expressions que la requête doit retourner.

### JOIN

Une jointure relie des informations réparties dans plusieurs tables. Une réservation référence une séance. La séance référence un film et un cinéma.

### GROUP BY

GROUP BY regroupe les lignes qui ont une même valeur, par exemple le même genre de film ou le même cinéma.

### COUNT_BIG

COUNT_BIG compte le nombre de lignes dans chaque groupe et renvoie un entier de grande capacité, adapté aux grands volumes.

### ORDER BY

ORDER BY trie le résultat. Ici, les groupes sont classés du plus grand total au plus petit.

### DATEPART

DATEPART extrait une partie d'une date. Dans le troisième défi, il permet d'obtenir le jour de la semaine de chaque réservation.

L'application configure DATEFIRST à 7 pour que SQL Server numérote les jours de 1 pour dimanche à 7 pour samedi. Sans ce réglage, la numérotation peut varier selon la session SQL.

La clause WHERE n'est pas utilisée dans les trois défis actuels. Ne pas la présenter comme une opération effectuée par l'activité.

## Les trois requêtes

### Défi 1 : genre préféré

La requête relie Reservations, Seances et Films, puis compte les réservations par genre.

\`\`\`sql
SELECT
    f.genre AS label,
    f.genre AS value,
    COUNT_BIG(*) AS total
FROM dbo.Reservations AS r
INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
INNER JOIN dbo.Films AS f ON f.film_id = s.film_id
GROUP BY f.genre
ORDER BY total DESC, f.genre;
\`\`\`

### Défi 2 : cinéma le plus fréquenté

La requête relie Reservations, Seances et Cinemas, puis compte les réservations par établissement.

\`\`\`sql
SELECT
    c.nom AS label,
    CONVERT(VARCHAR(12), c.cinema_id) AS value,
    COUNT_BIG(*) AS total
FROM dbo.Reservations AS r
INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
INNER JOIN dbo.Cinemas AS c ON c.cinema_id = s.cinema_id
GROUP BY c.nom, c.cinema_id
ORDER BY total DESC, c.nom;
\`\`\`

### Défi 3 : jour de réservation

La requête extrait le jour de la semaine, compte les réservations et trie les totaux.

\`\`\`sql
SELECT
    DATEPART(WEEKDAY, r.date_reservation) AS jour_numero,
    COUNT_BIG(*) AS total
FROM dbo.Reservations AS r
GROUP BY DATEPART(WEEKDAY, r.date_reservation)
ORDER BY total DESC, jour_numero;
\`\`\`

## Réponses attendues avec le générateur fourni

Lorsque les scripts SQL ont été exécutés correctement sur une base neuve, les résultats attendus sont :

- Genre le plus fréquent : Science-fiction.
- Cinéma le plus fréquenté : Cinéma du Centre.
- Jour de réservation le plus fréquent : samedi.

La répartition est volontairement construite pour rendre les réponses distinctes. Il s'agit de données synthétiques, pas d'une observation du marché. Vérifier les valeurs dans l'application et dans sql/03_verify_volume.sql avant une démonstration.

## Questions possibles

### À quoi sert une base de données ?

Elle permet de stocker des informations de façon structurée, de les retrouver et de les analyser.

### Pourquoi plusieurs tables ?

Pour séparer les types d'informations, éviter des répétitions inutiles et relier les éléments avec des clés.

### Pourquoi les jointures ?

Parce que les informations nécessaires à une réponse peuvent se trouver dans plusieurs tables.

### Pourquoi dix millions de réservations ?

Pour montrer que SQL peut analyser un volume important de lignes. Le volume doit être contrôlé sur le serveur avant de l'annoncer comme atteint.

### Les réservations sont-elles réelles ?

Non. Les réservations sont synthétiques et générées pour le projet. Elles ne représentent pas de vrais clients.

## Gestion des problèmes

### La page ne se charge plus

Vérifier la fenêtre PowerShell. Si nécessaire, arrêter l'application avec CTRL+C puis la relancer.

### SQL Server est indisponible

Vérifier le service, le nom de l'instance, le pilote ODBC et les droits Windows. Ne pas basculer silencieusement en mode simulation.

### Le mode simulation est affiché

Informer le visiteur que les chiffres sont des exemples. Pour une démonstration réelle, arrêter l'application, supprimer DEMO_MODE et redémarrer après vérification de la connexion SQL.

### La base n'est pas accessible

Ne pas inventer de résultats ni présenter des captures comme une exécution en direct. Utiliser seulement une activité de secours préparée et acceptée par l'enseignant.

## Fin de partie

Demander au visiteur d'expliquer avec ses mots pourquoi une jointure ou un regroupement peut être utile. Le remercier, puis utiliser Recommencer. Ce bouton remet à zéro la progression du navigateur, pas les données SQL.
