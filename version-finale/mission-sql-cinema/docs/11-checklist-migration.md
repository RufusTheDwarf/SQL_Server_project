# Checklist de migration

Cette liste doit être complétée avant la migration, pendant l'installation et à la fin de l'essai sur le PC de Sébeillon. La date cible communiquée pour cette installation est le 5 décembre 2026.

## Avant le déplacement

- [ ] Obtenir la validation du scénario par l'enseignant.
- [ ] Confirmer les versions Windows, SQL Server, Python et ODBC du PC cible.
- [ ] Vérifier que le matériel dispose de suffisamment d'espace disque.
- [ ] Générer les données et vérifier les 10 000 000 réservations.
- [ ] Conserver les résultats de sql/03_verify_volume.sql.
- [ ] Mesurer le temps de génération et l'espace utilisé.
- [ ] Exécuter les tests unitaires et les tests d'intégration.
- [ ] Chronométrer une partie complète.
- [ ] Préparer une sauvegarde SQL Server.
- [ ] Tester la restauration de la sauvegarde.
- [ ] Préparer une activité de secours approuvée.

## Sur le PC cible

- [ ] Installer SQL Server et SSMS si nécessaire.
- [ ] Installer Python et Microsoft ODBC Driver 18.
- [ ] Restaurer la base ou exécuter les scripts d'installation.
- [ ] Vérifier l'instance SQL Server et les droits Windows.
- [ ] Configurer SQL_SERVER, SQL_DATABASE et SQL_DRIVER.
- [ ] Installer les dépendances Python.
- [ ] Lancer l'application en mode réel.
- [ ] Vérifier que le bandeau MODE SIMULATION n'est pas affiché.
- [ ] Tester les trois défis.
- [ ] Vérifier les résultats et les nombres affichés.
- [ ] Tester le bouton Recommencer.
- [ ] Tester le clavier et la souris.
- [ ] Vérifier la lisibilité sur l'écran de démonstration.
- [ ] Vérifier l'ouverture de l'adresse locale dans le navigateur.
- [ ] Chronométrer plusieurs parties et noter les résultats.

## Après l'installation

- [ ] Noter la date, le PC et les versions logicielles.
- [ ] Enregistrer les résultats des tests.
- [ ] Noter les problèmes rencontrés et leur résolution.
- [ ] Mettre à jour le journal de travail.
- [ ] Mettre à jour la matrice de conformité selon les preuves.

## Secours

Si SQL Server est indisponible, le mode simulation peut servir à montrer l'interface. Prévenir le visiteur que les chiffres sont des exemples. Ne jamais présenter ce mode comme une démonstration SQL réelle.

N'utiliser une activité de secours que si elle a été préparée et acceptée par l'enseignant.
