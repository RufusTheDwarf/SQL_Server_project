# Manuel de formation et d'animation

## Objectif de l'activité

Le visiteur aide un festival à comprendre les préférences du public à partir des réservations d'un cinéma fictif. Il répond à trois défis en observant des résultats calculés par SQL Server.

Le parcours est conçu pour durer entre cinq et huit minutes. Cette durée est un objectif qui doit encore être confirmé par des essais chronométrés avec plusieurs personnes.

## Préparation avant l'arrivée du public

1. Démarrer SQL Server et vérifier que la base `MissionCinema` est accessible.
2. Démarrer l'application avec la procédure du manuel d'installation.
3. Vérifier que la bannière « MODE SIMULATION » n'est pas affichée.
4. Effectuer une partie complète de contrôle.
5. Vérifier que les trois défis affichent des résultats cohérents.
6. Tester le bouton « Recommencer ».
7. Laisser l'application ouverte sur l'écran de départ.

Si SQL Server n'est pas disponible, ne pas présenter les résultats simulés comme des résultats calculés par une vraie base de données.

## Présentation à dire au visiteur

« Un festival veut organiser sa programmation en fonction des goûts du public. Tu vas analyser les réservations d'un cinéma fictif et répondre à trois questions. Pas besoin de connaître SQL à l'avance : observe les résultats, compare les chiffres et choisis la réponse qui correspond le mieux. »

## Déroulement conseillé

### 0 à 30 secondes : présenter la mission

Expliquer le contexte du cinéma et le but de l'enquête. Préciser que les données sont fictives, mais structurées comme dans une vraie base de données.

### 30 secondes à 1 minute 30 : expliquer le fonctionnement

Montrer comment lire une question, les réponses possibles et les nombres affichés. Laisser le visiteur prendre connaissance de l'écran.

### 1 minute 30 à 4 minutes 30 : réaliser les trois défis

Laisser le visiteur choisir ses réponses. Intervenir uniquement s'il ne comprend pas la consigne ou le vocabulaire.

### 4 minutes 30 à 5 minutes 30 : expliquer le résultat

Présenter le score et relier les défis aux notions SQL utilisées. Demander au visiteur ce qu'il a observé.

### 5 minutes 30 à 6 minutes : terminer

Utiliser le bouton « Recommencer » et préparer l'écran pour la personne suivante.

Ce déroulement est une proposition d'animation. Il doit être ajusté après plusieurs tests réels.

## Notions SQL à expliquer

### SELECT

La commande SELECT permet de choisir les informations que l'on souhaite lire dans une base de données.

### WHERE

La clause WHERE filtre les lignes pour ne conserver que celles qui correspondent à une condition.

### JOIN

Une jointure relie des informations réparties dans plusieurs tables. Par exemple, une réservation peut être reliée à une séance, puis à un film et à un cinéma.

### GROUP BY

La clause GROUP BY rassemble les lignes qui possèdent une même valeur, par exemple les films appartenant au même genre.

### COUNT

La fonction COUNT compte le nombre de lignes dans un groupe.

### ORDER BY

La clause ORDER BY trie les résultats, par exemple du total le plus élevé au plus faible.

### DATEPART

La fonction DATEPART extrait une partie d'une date. Dans cette activité, elle sert notamment à analyser les jours de la semaine.

## Réponses attendues

Les choix proposés sont issus des résultats SQL triés par total décroissant. La première option correspond au total le plus élevé pour le défi concerné.

Les chiffres exacts dépendent des données générées sur le serveur utilisé. Ils doivent être consultés dans l'application après l'installation. Ne pas apprendre ou annoncer des valeurs avant d'avoir exécuté les scripts et contrôlé la base.

## Questions possibles des visiteurs

### À quoi sert une base de données ?

Elle permet de stocker des informations de manière organisée, de les retrouver et de les analyser.

### Pourquoi utiliser plusieurs tables ?

Pour organiser les informations, éviter les répétitions inutiles et relier les éléments grâce à des clés.

### Pourquoi utiliser des jointures ?

Parce que les informations nécessaires à une analyse sont souvent réparties dans plusieurs tables.

### Pourquoi générer dix millions de réservations ?

Pour travailler sur un volume important et montrer l'intérêt de requêtes bien structurées. Le volume réel doit être confirmé avec le script de vérification avant la démonstration.

### Les réservations sont-elles réelles ?

Non. Les réservations sont des données synthétiques générées pour l'activité. Elles ne représentent pas des clients réels.

## Gestion des problèmes

### La page ne se charge plus

Vérifier la fenêtre PowerShell. Si nécessaire, arrêter l'application avec CTRL+C puis la relancer avec `python app.py`.

### La connexion à SQL Server échoue

Vérifier le service SQL Server, le nom de l'instance, les paramètres de connexion et les droits du compte Windows. Ne pas basculer silencieusement en mode simulation.

### Le mode simulation est affiché

Informer clairement le visiteur que les résultats sont simulés. Pour une démonstration réelle, rétablir la connexion SQL Server et redémarrer l'application sans la variable `DEMO_MODE`.

### La base de données est indisponible

Utiliser uniquement une activité de secours préparée et validée à l'avance. Ne pas inventer de résultats ni présenter des captures d'écran comme une exécution en direct.

## Fin de partie

Demander au visiteur d'expliquer avec ses mots ce qu'est une jointure ou pourquoi on regroupe les lignes. Le remercier pour sa participation, puis utiliser « Recommencer » pour préparer l'activité suivante.

Le bouton de nouvelle partie réinitialise la progression du navigateur. Il ne supprime aucune donnée de la base SQL.