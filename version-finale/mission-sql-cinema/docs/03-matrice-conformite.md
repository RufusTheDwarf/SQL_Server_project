# Matrice de conformité au cahier des charges

Les statuts ci-dessous décrivent les preuves présentes dans la branche de travail. Ils ne remplacent pas les vérifications sur un SQL Server réel ni la validation de l'enseignant.

| Exigence | Statut | Preuve ou vérification restante |
| --- | --- | --- |
| Activité ludique sur un thème connu | Partiellement conforme | `docs/02-validation-scenario.md`; validation enseignant à obtenir |
| Lien avec les cours ICT | Partiellement conforme | Notions décrites dans la fiche de scénario; correspondance avec le cours et le livre à confirmer |
| Dix millions d'enregistrements réels | Non vérifié | `sql/02_generate_reservations.sql` et `sql/03_verify_volume.sql`; exécuter et conserver les résultats SQL |
| Durée de cinq à huit minutes | Non vérifié | Chronométrer plusieurs visiteurs, animateur et remise à zéro compris |
| Requêtes SQL réelles | Partiellement conforme | `app.py`; tester les trois requêtes avec SQL Server installé |
| Installation sur un autre PC | Non vérifié | Suivre le manuel et réaliser un essai sur un poste propre |
| Manuel d'installation | Partiellement conforme | `docs/04-manuel-installation.md`; vérifier les étapes sur le PC cible |
| Manuel d'animation | Partiellement conforme | `docs/05-manuel-animation.md`; faire relire et tester |
| Documents visiteurs Word et PDF | Partiellement conforme | Fichiers de livraison générés séparément; vérifier leur intégration à la livraison finale |
| Rapport de raisonnement | Partiellement conforme | `docs/06-rapport-projet.md`; actualiser après mesures réelles |
| Affiche promotionnelle | Partiellement conforme | `docs/12-affiche.html`; ouvrir et imprimer en PDF, vérifier sur imprimante |
| Journal quotidien honnête | Partiellement conforme | `docs/07-journal-travail-modele.md`; les lignes réelles doivent être complétées par les collaborateurs |
| Planification de 32 périodes | Conforme comme plan | `docs/08-plan-32-periodes.md`; ne prouve pas que les périodes ont été réalisées |
| Tests unitaires | Conforme pour le périmètre CI | Workflow GitHub Actions réussi sur le commit observé |
| Tests SQL Server et performances | Non vérifié | Aucun serveur SQL Server n'a été exécuté dans cet environnement |
| Sécurité des requêtes et secrets | Partiellement conforme | Les choix de réponses sont comparés aux options retournées; revue locale et configuration du poste restent nécessaires |
| Mode simulation clairement identifié | Partiellement conforme | Bannière visible; vérifier les consignes aux animateurs |
| Validation par l'enseignant | Non vérifié | Décision écrite à ajouter après validation réelle |

## Preuves à conserver avant de déclarer le projet terminé

1. Capture ou export des résultats de `03_verify_volume.sql`.
2. Temps de génération et espace disque mesurés.
3. Résultats des tests d'intégration avec SQL Server.
4. Mesures chronométrées du parcours.
5. Résultat de l'installation sur le PC cible.
6. Décision de validation du scénario par l'enseignant.
