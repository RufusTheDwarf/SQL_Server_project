# Matrice de conformité au cahier des charges

Les statuts ci-dessous reflètent les preuves présentes dans le dépôt au moment de l'ajout de cette matrice. Ils ne remplacent pas une validation sur le poste cible.

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
| Manuel d'installation | Partiellement conforme | README de l'activité | Vérification pratique par un autre élève |
| Manuel d'animation | Partiellement conforme | Fiche de validation | Compléter les réponses attendues et le dépannage |
| Documents visiteurs DOCX et PDF | Non conforme à ce stade | Pas encore fournis dans ce dossier | Produire et vérifier les deux formats |
| Rapport de projet actualisé | Partiellement conforme | Audit initial | Compléter après les tests réels |
| Affiche éditable et PDF | Non conforme à ce stade | Pas encore fournie | Produire les fichiers |
| Journal de travail fidèle | Non conforme à ce stade | Modèle à créer | Reconstruire à partir de traces puis faire vérifier |
| Tests unitaires | Partiellement conforme | `tests/test_app.py` | Installer dépendances et exécuter |
| Tests SQL d'intégration | Non vérifié | Scripts de vérification disponibles | Exécuter sur SQL Server |
| Sécurité et paramètres | Partiellement conforme | Configuration par variables et formulaire à choix bornés | Audit complet, gestion de secret de session |
| Mesure du temps et de l'espace | Non vérifié | Script SQL affiche la durée de génération et espace de base | Conserver les mesures réelles |
