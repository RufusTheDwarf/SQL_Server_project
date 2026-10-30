# Manuels Mission SQL Cinéma

Ce dossier contient les trois manuels destinés à l'installation, à l'animation et aux visiteurs.

Chaque manuel est livré au format Word (.docx) et PDF. Les sources Markdown sont conservées dans le sous-dossier source.

## Installation

Le poste est préparé depuis la racine du dépôt en double-cliquant sur setup.bat. Le fichier lance setup.ps1, qui vérifie les prérequis, prépare la base, génère et contrôle les réservations, installe les dépendances, exécute les tests et ouvre l'interface locale.

SQL Server, sqlcmd, Python et Microsoft ODBC Driver 18 doivent être installés avant le lancement. Le setup ne les installe pas.

## Fichiers

- Manuel d'installation : L-141-Rafael_Melo-ManuelInstallation.
- Manuel d'animation : D-141-Rafael_Melo-ManuelAnimateur.
- Fiche visiteur : D-141-Rafael_Melo-ManuelVisiteur.

## Reconstruction des Word et PDF

Depuis ce dossier, exécuter :

```powershell
python build_manuals.py
```
