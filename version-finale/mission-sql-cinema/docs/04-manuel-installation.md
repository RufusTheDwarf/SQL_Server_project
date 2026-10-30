# Manuel d'installation

## Prérequis

- Windows 10 ou Windows 11.
- SQL Server installé et démarré.
- SQL Server Management Studio.
- Python 3.10 ou version compatible plus récente.
- Microsoft ODBC Driver 18 for SQL Server.
- Espace disque libre suffisant. La taille doit être mesurée pendant l'installation; prévoir une marge pour les index et les fichiers journaux.

## 1. Préparer la base

Dans SSMS, créer une base vide nommée `MissionCinema`. Ouvrir ensuite les scripts du dossier `sql` dans cet ordre :

1. `01_schema.sql`
2. `02_generate_reservations.sql`
3. `03_verify_volume.sql`

Le script de schéma refuse maintenant de supprimer des tables existantes. En cas d'erreur signalant des tables déjà présentes, vérifier la base sélectionnée et utiliser une base vide destinée au projet. Ne supprimez pas une base contenant des données utiles.

Le générateur vise dix millions de réservations. Il peut prendre un temps important. En cas d'interruption, exécuter d'abord le script de vérification. Le générateur peut reprendre une suite continue de clés déjà insérées. Ne pas lancer plusieurs générateurs simultanément.

## 2. Installer Python

Ouvrir PowerShell dans le dossier `version-finale/mission-sql-cinema` :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloque l'activation, lancer les commandes d'installation avec le chemin direct `.venv\Scripts\python.exe`.

## 3. Configurer la connexion

Exemple pour une instance locale nommée SQLEXPRESS :

```powershell
$env:SQL_SERVER = ".\SQLEXPRESS"
$env:SQL_DATABASE = "MissionCinema"
$env:SQL_DRIVER = "ODBC Driver 18 for SQL Server"
```

Le compte Windows courant doit avoir accès en lecture aux tables utilisées par l'application. Le nom d'instance doit être adapté au poste cible. Aucun mot de passe n'est requis dans le dépôt si l'authentification Windows est utilisée.

## 4. Lancer l'application

```powershell
python app.py
```

Ouvrir ensuite `http://127.0.0.1:5000`. Garder la fenêtre PowerShell ouverte pendant l'activité.

## 5. Mode simulation

Pour répéter l'interface sans SQL Server :

```powershell
$env:DEMO_MODE = "1"
python app.py
```

La bannière « MODE SIMULATION » doit rester visible. Ce mode ne prouve ni la connexion SQL ni la validité des résultats. Pour revenir au mode réel, exécuter `Remove-Item Env:DEMO_MODE` puis relancer l'application.

## 6. Compte de lecture seule\n\nSi l'application doit utiliser un compte dédié, exécuter `sql/04_role_lecture.sql` avec un compte administrateur. Ce script crée un rôle et accorde uniquement SELECT sur les tables de l'activité. Un administrateur doit ensuite créer ou sélectionner le principal Windows approprié et l'ajouter au rôle `mission_cinema_lecture`. Les commandes exactes dépendent du domaine et du nom de compte du PC cible.\n\n## 7. Contrôles avant ouverture

- Exécuter `03_verify_volume.sql` et conserver les résultats.
- Vérifier que le total des réservations atteint au moins 10 000 000.
- Vérifier que les compteurs de références orphelines valent zéro.
- Lancer l'application en mode réel et vérifier que la bannière de simulation est absente.
- Répondre aux trois défis.
- Tester le bouton de nouvelle partie.
- Chronométrer plusieurs parties.
- Tester l'installation et la connexion sur le PC utilisé à Sébeillon.

## Dépannage

**Connexion refusée :** vérifier le service SQL Server, le nom d'instance, l'authentification Windows, les permissions et le pilote ODBC.

**Le pilote est introuvable :** installer Microsoft ODBC Driver 18 for SQL Server, puis vérifier le nom exact dans la configuration.

**Volume insuffisant :** vérifier que le générateur a terminé et exécuter la requête de contrôle des volumes.

**Erreur sur des tables existantes :** le script ne les supprime pas. Sélectionner la base vide destinée à l'activité.

**Résultats simulés :** supprimer la variable `DEMO_MODE`, redémarrer l'application et vérifier la connexion SQL réelle.

## Retour à l'état initial

Le bouton de nouvelle partie efface la progression de la session du navigateur uniquement. Il ne supprime aucune donnée SQL. Pour reconstruire la base, suivre une procédure d'administration séparée et vérifier explicitement les sauvegardes avant toute opération destructive.
