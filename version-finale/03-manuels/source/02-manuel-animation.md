# Manuel d'animation
Mission SQL Cinéma
ETML - Journées Portes Ouvertes
Version du 30 octobre 2026

## 1. Objectif de l'activité

Le visiteur aide un festival à comprendre les préférences du public à partir des réservations d'un cinéma fictif. Il répond à trois défis à choix multiples. Les résultats proviennent de requêtes SQL Server lorsque le mode simulation est désactivé.

Le parcours vise cinq à huit minutes. Cette durée reste à mesurer avec plusieurs visiteurs. Ne pas annoncer qu'elle a été chronométrée tant que des essais réels n'ont pas été réalisés.

## 2. Préparation avant l'arrivée du public

1. Vérifier que SQL Server est démarré.
2. Vérifier que la base MissionCinema est accessible.
3. Lancer setup.bat ou démarrer l'application avec le manuel d'installation.
4. Vérifier que la bannière MODE SIMULATION n'est pas affichée.
5. Effectuer une partie complète et vérifier les trois résultats.
6. Vérifier que le bouton Recommencer remet la partie à zéro.
7. Laisser l'application ouverte sur le premier défi.

Si le mode simulation est activé, prévenir clairement le visiteur que les chiffres sont des exemples. Ne pas les présenter comme des résultats venant de SQL Server.

## 3. Présentation à dire au visiteur

« Un festival veut organiser sa programmation en fonction des goûts du public. Tu vas analyser les réservations d'un cinéma fictif et répondre à trois questions. Pas besoin de connaître SQL à l'avance. Observe les chiffres, compare les réponses et choisis celle qui te semble correcte. »

## 4. Déroulement conseillé

### Accueil et contexte

Durée indicative : 30 secondes.

Présenter la mission et préciser que les données sont fictives, mais organisées comme dans une vraie base de données relationnelle.

### Lecture de l'écran

Durée indicative : 30 secondes.

Montrer la question, les propositions et le nombre de réservations affiché pour chacune. Laisser le visiteur lire la consigne.

### Les trois défis

Durée indicative : 3 à 4 minutes.

Laisser le visiteur comparer les nombres et choisir une réponse. Intervenir seulement s'il ne comprend pas le vocabulaire ou la consigne. Après validation, lire avec lui l'explication affichée.

### Bilan et réinitialisation

Durée indicative : 1 minute.

Présenter le score, expliquer une notion SQL observée et demander au visiteur ce qu'il a compris. Cliquer sur Recommencer pour préparer la session suivante.

Ce déroulement est une proposition. Ajuster les temps après des essais chronométrés.

## 5. Les trois défis

### Défi 1 : le genre préféré

Question posée : « Quel genre attire le plus de réservations ? »

La requête relie les réservations aux séances et aux films. Elle compte les réservations par genre et trie les groupes du total le plus élevé au plus faible.

```sql
SELECT
    f.genre AS label,
    f.genre AS value,
    COUNT_BIG(*) AS total
FROM dbo.Reservations AS r
INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
INNER JOIN dbo.Films AS f ON f.film_id = s.film_id
GROUP BY f.genre
ORDER BY total DESC, f.genre;
```

Réponse attendue avec les données générées : Science-fiction, avec 1 880 000 réservations.

### Défi 2 : le cinéma le plus fréquenté

Question posée : « Dans quel cinéma réserve-t-on le plus ? »

La requête relie les réservations aux séances et aux cinémas, puis compte les réservations par établissement.

```sql
SELECT
    c.nom AS label,
    CONVERT(VARCHAR(12), c.cinema_id) AS value,
    COUNT_BIG(*) AS total
FROM dbo.Reservations AS r
INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
INNER JOIN dbo.Cinemas AS c ON c.cinema_id = s.cinema_id
GROUP BY c.nom, c.cinema_id
ORDER BY total DESC, c.nom;
```

Réponse attendue avec les données générées : Cinéma du Centre, avec 3 000 000 réservations.

### Défi 3 : le jour le plus fréquent

Question posée : « Quel jour de la semaine est le plus fréquent ? »

La requête extrait le jour de la semaine de chaque réservation, compte les lignes et trie les totaux.

```sql
SELECT
    DATEPART(WEEKDAY, r.date_reservation) AS jour_numero,
    COUNT_BIG(*) AS total
FROM dbo.Reservations AS r
GROUP BY DATEPART(WEEKDAY, r.date_reservation)
ORDER BY total DESC, jour_numero;
```

Réponse attendue avec les données générées : samedi, avec 3 500 000 réservations.

L'application configure DATEFIRST à 7 sur chaque connexion SQL. La numérotation est donc dimanche = 1, lundi = 2, jusqu'à samedi = 7.

## 6. Répartition attendue des données

Ces totaux décrivent le jeu de données synthétique prévu par le générateur. Ils ne représentent pas des statistiques de vrais cinémas. Les confirmer sur le serveur avec sql/03_verify_volume.sql après la génération.

### Par genre

- Science-fiction : 1 880 000.
- Comédie : 1 255 000.
- Documentaire : 1 255 000.
- Drame : 1 255 000.
- Action : 1 242 500.
- Aventure : 1 242 500.
- Mystère : 1 242 500.
- Thriller : 627 500.

### Par cinéma

- Cinéma du Centre : 3 000 000.
- Le Grand Écran : 2 500 000.
- Riviera Films : 2 000 000.
- Les Arcades : 1 500 000.
- Cinéma des Alpes : 1 000 000.

### Par jour de réservation

- Samedi : 3 500 000.
- Vendredi : 1 500 000.
- Dimanche : 1 000 000.
- Lundi : 1 000 000.
- Mardi : 1 000 000.
- Mercredi : 1 000 000.
- Jeudi : 1 000 000.

## 7. Notions SQL à expliquer

### SELECT

SELECT indique les informations que la requête doit retourner.

### JOIN

Une jointure relie les informations de plusieurs tables. Une réservation fait référence à une séance. La séance fait référence à un film et à un cinéma.

### GROUP BY

GROUP BY rassemble les lignes qui ont la même valeur, par exemple le même genre ou le même cinéma.

### COUNT_BIG

COUNT_BIG compte le nombre de lignes dans chaque groupe. Cette fonction renvoie un entier de grande capacité adapté aux grands volumes.

### ORDER BY

ORDER BY trie les résultats. Dans les défis, les totaux sont classés du plus grand au plus petit.

### DATEPART

DATEPART extrait une partie d'une date. Dans le troisième défi, elle permet de compter les réservations par jour de la semaine.

La clause WHERE n'est pas utilisée dans les trois requêtes de l'activité. Ne pas la présenter comme une opération effectuée par les défis.

## 8. Questions possibles des visiteurs

### À quoi sert une base de données ?

Elle sert à stocker des informations de manière organisée, à les retrouver et à les analyser.

### Pourquoi séparer les informations dans plusieurs tables ?

Pour organiser les données et éviter de répéter inutilement les mêmes informations.

### Pourquoi les jointures sont-elles utiles ?

Parce que les informations nécessaires à une réponse se trouvent souvent dans plusieurs tables.

### Les réservations sont-elles réelles ?

Non. Elles sont générées pour l'activité et ne représentent pas de vrais clients.

### Pourquoi dix millions de réservations ?

Pour montrer que SQL peut traiter et analyser un grand nombre de lignes. Le volume doit être contrôlé sur le serveur avant de l'annoncer comme atteint.

## 9. Gestion des problèmes

### La page ne se charge plus

Consulter la fenêtre de lancement et les journaux dans version-finale/mission-sql-cinema/logs/. Si nécessaire, redémarrer l'application avec setup.bat.

### La connexion SQL Server échoue

Vérifier le service SQL Server, le nom de l'instance, ODBC Driver 18 et les droits du compte Windows.

### Le mode simulation apparaît

Informer le visiteur que les chiffres sont des exemples. Pour une démonstration réelle, fermer l'application, supprimer la variable DEMO_MODE si elle est définie, puis relancer setup.bat.

### Le serveur Flask doit être arrêté

Utiliser le PID affiché par setup.bat et exécuter Stop-Process -Id PID dans PowerShell. Remplacer PID par le nombre réel.

### La base est indisponible

Ne pas inventer de résultats et ne pas présenter des captures comme une exécution en direct. Utiliser uniquement une activité de secours préparée et acceptée par l'enseignant.

## 10. Fin de partie

Demander au visiteur d'expliquer avec ses mots pourquoi une jointure ou un regroupement est utile. Le remercier, puis cliquer sur Recommencer.

Le bouton Recommencer remet à zéro la progression de la session du navigateur. Il ne supprime aucune donnée SQL.
