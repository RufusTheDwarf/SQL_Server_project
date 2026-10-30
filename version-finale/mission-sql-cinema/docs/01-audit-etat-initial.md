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

## Revue technique complémentaire du 30 octobre 2026

La relecture de l'application, du schéma et du générateur a révélé trois problèmes qui n'étaient pas visibles dans les seuls tests unitaires initiaux :

- Les cinq cinémas recevaient exactement le même nombre de réservations. Le deuxième défi ne possédait donc pas de gagnant réel.
- Les genres Science-fiction et Mystère avaient chacun trois films de référence. Leur total était identique, ce qui pouvait créer une égalité au premier défi.
- Les CTE de génération utilisaient TOP avec ROW_NUMBER sans ordre externe explicite. L'ordre de sélection devait être garanti pour assurer des identifiants continus.

Les corrections ont été préparées sur la branche audit-corrections-cinema-2026-10, sans modifier main. La distribution synthétique est maintenant pondérée et déterministe. Les tests d'intégration vérifient les totaux attendus des trois défis, le volume, les identifiants des tables de référence et les relations.

L'application a également été renforcée : le mode simulation n'ouvre pas de connexion SQL, une réponse hors liste est refusée et une ancienne soumission de formulaire ne peut pas faire avancer la partie.

Le workflow GitHub Actions a exécuté avec succès les tests applicatifs sur la branche de correction. Les tests d'intégration SQL Server restent ignorés tant qu'une instance réelle n'est pas configurée. Aucun résultat n'est donc encore disponible sur l'exécution du générateur, les 10 millions de lignes, les performances ou l'installation Windows.

## État à conserver

La branche de correction est une proposition technique à relire. Elle ne doit pas être fusionnée dans main avant l'exécution des scripts sur un SQL Server de test, la réussite des tests d'intégration et la validation des documents et du scénario par l'enseignant.

## Automatisation de l'installation

Un script \`setup.ps1\` et un lanceur par double clic \`setup.bat\` ont été ajoutés à la racine du dépôt. Le setup vérifie SQL Server, sqlcmd, Python, ODBC Driver 18 et les droits SELECT ; il prépare la base vide, reprend une génération interrompue lorsque les identifiants sont continus, contrôle les dix millions de lignes, exécute les tests et démarre Flask sur le port local demandé.

Le setup ne télécharge pas et n'installe pas le moteur SQL Server, Python ou le pilote ODBC. Ces composants doivent être préinstallés. Le moteur SQL Server et sqlcmd doivent être accessibles au compte Windows courant. Le script s'arrête si la base présente un schéma partiel et ne supprime aucune base ni table existante.

La syntaxe PowerShell a été contrôlée dans GitHub Actions. L'exécution complète du setup reste à tester sur un poste Windows équipé de SQL Server.
