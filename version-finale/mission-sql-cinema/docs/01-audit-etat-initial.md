# Audit initial du dépôt

Date de l'audit : 29 octobre 2026. Audit effectué à partir des fichiers accessibles dans la branche main. Le poste SQL Server local n'a pas été inspecté et aucun test SQL n'a été exécuté dans cet audit distant.

## Points réutilisables

- Le dépôt contient déjà des scripts SQL et Python pour un jeu de données volumineux.
- Le générateur existant prévoit plusieurs millions de parties, achats et signalements, avec des clés étrangères.
- L'application Flask actuelle se connecte à SQL Server avec pyodbc et utilise des paramètres dans les requêtes.
- Des manuels, un rapport et un cahier des charges sont présents dans le dépôt.

## Écarts identifiés

- Le README principal décrit surtout un dépôt d'exercices et présente l'activité de détection de joueurs suspects comme un projet de Portes ouvertes.
- L'interface existante demande de régler plusieurs seuils de suspicion, ce qui est peu accessible à un visiteur qui ne connaît pas SQL.
- Le générateur existant écrit les CSV dans un chemin fixe sous le Bureau, dépend de Faker et utilise les fonctions aléatoires sans graine globale reproductible.
- Le script de génération existant annonce des volumes élevés, mais cela ne prouve pas que la base cible contient effectivement ces lignes.
- Plusieurs fichiers historiques sont dupliqués dans archive et versions précédentes. Ils ne doivent pas être supprimés avant comparaison.
- La disponibilité réelle de SQL Server, les performances et la durée du parcours n'ont pas été mesurées.

## Risques techniques

- La génération de plusieurs millions de lignes peut prendre un temps important et consommer plusieurs Go.
- La connexion dépend de la configuration de l'instance SQL Server et du pilote ODBC.
- Les documents binaires existants ne sont pas tous inspectés dans le détail par cet audit.
- Le contenu du livre SQL Server 2022 de J. Poirier n'est pas fourni sous une forme permettant de vérifier les chapitres et les pages.

## Décision provisoire

Créer une nouvelle activité isolée dans `version-finale/mission-sql-cinema/` et conserver l'ancienne activité et les archives. La piste cinéma doit être présentée à l'enseignant pour validation avant de considérer le choix comme définitif.
