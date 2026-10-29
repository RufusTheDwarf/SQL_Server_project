# Matrice de conformité au cahier des charges

Les statuts ci-dessous reflètent les preuves présentes dans le dépôt au moment de la dernière mise à jour. Ils ne remplacent pas une validation sur le poste cible.

| Exigence | Statut | Preuve | Vérification restante |
|---|---|---|---|
| Activité ludique pour les Portes ouvertes | Partiellement conforme | Fiche de scénario et interface | Validation enseignant et essai avec visiteurs |
| Thème accessible | Partiellement conforme | Mission cinéma | Vérifier compréhension sans aide |
| Base SQL Server relationnelle | Partiellement conforme | `sql/01_schema.sql` | Exécuter le script sur SQL Server |
| Au moins 10 millions d'enregistrements | Non vérifié | `sql/02_generate_reservations.sql` | Générer puis contrôler avec `sql/03_verify_volume.sql` |
| Activité de 5 à 8 minutes | Non vérifié | Déroulement proposé dans la fiche | Chronométrer plusieurs essais |
| Lien avec les notions ICT | Partiellement conforme | Requêtes, défis et fiche de validation | Confirmation de l'enseignant et lien avec le cours |
| Référence au livre de J. Poirier | Non vérifié | Référence déclarée dans le cahier des charges | Vérifier les notions dans l'ouvrage |
| Installation sur un autre PC | Partiellement conforme | README et variables de configuration | Test depuis un dossier propre sur le PC cible |
| Manuel d'installation | Partiellement conforme | `docs/04-manuel-installation.md` | Vérification pratique par un autre élève |
| Manuel d'animation | Partiellement conforme | `docs/05-manuel-animation.md` | Compléter les réponses attendues après exécution SQL |
| Documents visiteurs Word et PDF | Partiellement conforme | Livrables exportés dans la conversation, source HTML dans `docs/13-document-visiteur.html` | Ajouter les exports au paquet de livraison final et vérifier l'impression |
| Rapport de projet | Partiellement conforme | `docs/06-rapport-projet.md` et export de travail | Actualiser après tests réels |
| Affiche éditable et PDF | Partiellement conforme | Source HTML dans `docs/12-affiche.html`, fichiers éditables et PDF exportés séparément | Vérifier l'impression et intégrer les fichiers au paquet final |
| Journal de travail fidèle | Partiellement conforme | `docs/07-journal-travail-modele.md` | Reconstruire à partir de traces puis faire vérifier |
| Tests unitaires | Conforme pour la logique testée | Workflow GitHub Actions et `tests/test_app.py` | Ajouter d'autres cas au besoin |
| Tests SQL d'intégration | Non vérifié | `tests/test_sql_integration.py` | Exécuter sur SQL Server avec `RUN_SQL_INTEGRATION=1` |
| Sécurité et paramètres | Partiellement conforme | Formulaire à choix bornés, pas de SQL libre, secret de session configurable | Audit complet de configuration et des droits SQL |
| Mesure du temps et de l'espace | Non vérifié | Script de génération et requête de taille | Conserver les mesures réelles |
