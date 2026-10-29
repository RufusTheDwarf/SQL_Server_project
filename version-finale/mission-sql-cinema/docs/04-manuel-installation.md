# Manuel d'installation

## Objectif

Installer l'activité sur un PC Windows pour les Portes ouvertes. Prévoir une marge de temps pour la génération des données et la vérification avant l'ouverture au public.

## Prérequis

- Windows 10 ou 11.
- SQL Server 2019 ou plus récent, édition compatible avec les besoins du projet.
- SSMS.
- Python 3.10 ou plus récent.
- Microsoft ODBC Driver 18 for SQL Server.
- Droits suffisants pour créer la base et charger les données.
- Espace disque à mesurer. Prévoir au minimum plusieurs Go libres et conserver une marge.

## Préparer la base

1. Ouvrir SSMS et se connecter à l'instance retenue.
2. Créer une base nommée `MissionCinema`.
3. Ouvrir `sql/01_schema.sql` et l'exécuter.
4. Vérifier que les tables Films, Cinemas, Seances et Reservations existent.
5. Exécuter `sql/02_generate_reservations.sql`. L'opération peut prendre du temps. Ne pas fermer SSMS avant la fin.
6. Exécuter `sql/03_verify_volume.sql`.
7. Conserver une capture ou un export des résultats. La table Reservations doit afficher au moins 10 000 000 lignes. Si ce n'est pas le cas, ne pas annoncer que l'exigence est atteinte.

## Préparer Python

Dans PowerShell, depuis le dossier `version-finale/mission-sql-cinema` :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloque l'activation, utiliser la commande Python du venv directement :
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configurer et lancer

Adapter les valeurs au serveur local :

```powershell
$env:SQL_SERVER = ".\SQLEXPRESS"
$env:SQL_DATABASE = "MissionCinema"
$env:SQL_DRIVER = "ODBC Driver 18 for SQL Server"
python app.py
```

Ouvrir `http://127.0.0.1:5000`. Garder la fenêtre PowerShell ouverte pendant l'activité.

## Contrôle avant public

- Recharger la page et confirmer qu'aucune bannière de simulation n'apparaît.
- Répondre aux trois défis et vérifier le score.
- Cliquer sur recommencer et vérifier que le score revient à zéro.
- Débrancher ou arrêter SQL Server uniquement lors d'un test hors public, puis confirmer le message d'erreur.
- Ne pas utiliser `DEMO_MODE=1` pendant une démonstration présentée comme une exécution réelle.
- Chronométrer une partie complète.
- Noter la taille réelle des fichiers de base et la durée de génération.

## Dépannage

**Connexion impossible :** vérifier que le service SQL Server fonctionne, que le nom d'instance est exact, que l'authentification Windows est autorisée et que le pilote ODBC configuré est installé.

**Erreur de droits :** demander à l'administrateur de configurer l'accès. Ne pas donner de droits administrateur SQL au compte de l'application sans nécessité.

**Résultats vides :** vérifier que les dix millions de réservations ont été chargées et que le script de vérification confirme le volume.

**Installation sur un autre PC :** refaire la configuration à partir des prérequis, ne pas copier de chemins absolus de l'ancien poste.

## Retour à l'état propre

L'application ne modifie pas les tables pendant une partie. Le bouton de redémarrage efface uniquement la session du navigateur. Ne supprimer ou recréer la base que si une personne responsable a validé l'opération.
