import csv
import random
import os
from faker import Faker

# ============================================================
# CONFIGURATION DES CHEMINS (tout sur le Bureau)
# ============================================================
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
base_dir = os.path.join(desktop, "ProjetBD_PortesOuvertes")
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

print(f"Dossier de travail : {base_dir}")
print(f"Dossier des données : {data_dir}")

# ============================================================
# GÉNÉRATEUR DE DONNÉES
# ============================================================
fake = Faker('fr_FR')

NB_JOUEURS = 500_000
NB_JEUX = 5_000
NB_PLATEFORMES = 20
NB_PARTIES = 7_000_000
NB_ACHATS = 2_000_000
NB_SIGNALEMENTS = 1_000_000
NB_SANCTIONS = 500_000

# UTF-8 sans BOM : évite les erreurs sur les caractères accentués/spéciaux
# (pays, noms de société, pseudos) et correspond à CODEPAGE = '65001' côté SQL.
ENCODING = 'utf-8'

# ---------- Joueurs ----------
print("Génération des joueurs...")
with open(os.path.join(data_dir, 'joueurs.csv'), 'w', newline='', encoding=ENCODING) as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['id_joueur', 'pseudo', 'pays', 'date_inscription', 'heures_jeu',
                     'victoires', 'defaites', 'precision_tir', 'tirs_tete'])
    for i in range(1, NB_JOUEURS + 1):
        if i in [1, 2, 3]:
            # Suspects : statistiques impossibles (pour la démo de détection)
            pseudo = fake.user_name()
            pays = fake.country()
            date_insc = fake.date_between(start_date='-5y', end_date='today')
            heures = round(random.uniform(20, 80), 2)
            victoires = random.randint(400, 600)
            defaites = random.randint(0, 10)
            precision = round(random.uniform(95, 99.99), 2)
            tirs_tete = random.randint(800, 1200)
        else:
            pseudo = fake.user_name()
            pays = fake.country()
            date_insc = fake.date_between(start_date='-5y', end_date='today')
            heures = round(random.uniform(100, 5000), 2)
            victoires = random.randint(0, 400)
            defaites = random.randint(50, 500)
            precision = round(random.uniform(0, 90), 2)
            tirs_tete = random.randint(0, 500)
        writer.writerow([i, pseudo, pays, date_insc, heures,
                         victoires, defaites, precision, tirs_tete])

# ---------- Jeux ----------
print("Génération des jeux...")
genres = ['FPS', 'RPG', 'MMO', 'MOBA', 'Battle Royale', 'Sport', 'Simulation']
with open(os.path.join(data_dir, 'jeux.csv'), 'w', newline='', encoding=ENCODING) as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['id_jeu', 'nom_jeu', 'editeur', 'genre'])
    for i in range(1, NB_JEUX + 1):
        nom = fake.catch_phrase()
        editeur = fake.company()
        genre = random.choice(genres)
        writer.writerow([i, nom, editeur, genre])

# ---------- Plateformes ----------
print("Génération des plateformes...")
plateformes = [
    ('PlayStation 5', 'Sony'), ('PlayStation 4', 'Sony'),
    ('Xbox Series X', 'Microsoft'), ('Xbox One', 'Microsoft'),
    ('Nintendo Switch', 'Nintendo'), ('PC (Windows)', 'Microsoft'),
    ('PC (Linux)', 'Open Source'), ('Steam Deck', 'Valve'),
    ('Oculus Quest', 'Meta'), ('iOS', 'Apple'), ('Android', 'Google')
]
with open(os.path.join(data_dir, 'plateformes.csv'), 'w', newline='', encoding=ENCODING) as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['id_plateforme', 'nom_plateforme', 'constructeur'])
    for i in range(1, NB_PLATEFORMES + 1):
        if i <= len(plateformes):
            nom, cons = plateformes[i - 1]
        else:
            nom = fake.word() + ' ' + str(i)
            cons = fake.company()
        writer.writerow([i, nom, cons])

# ---------- Parties ----------
print("Génération des parties (long)...")
with open(os.path.join(data_dir, 'parties.csv'), 'w', newline='', encoding=ENCODING) as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['id_partie', 'id_joueur', 'id_jeu', 'id_plateforme',
                     'date_partie', 'duree_minutes', 'score', 'resultat'])
    for i in range(1, NB_PARTIES + 1):
        id_j = random.randint(1, NB_JOUEURS)
        id_jeu = random.randint(1, NB_JEUX)
        id_plat = random.randint(1, NB_PLATEFORMES)
        date_p = fake.date_time_between(start_date='-3y', end_date='now')
        duree = random.randint(5, 180)
        score = random.randint(0, 50)
        resultat = random.choice(['victoire', 'defaite', 'nul'])
        writer.writerow([i, id_j, id_jeu, id_plat, date_p, duree, score, resultat])

# ---------- Achats ----------
print("Génération des achats...")
with open(os.path.join(data_dir, 'achats.csv'), 'w', newline='', encoding=ENCODING) as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['id_achat', 'id_joueur', 'id_jeu', 'date_achat', 'montant'])
    for i in range(1, NB_ACHATS + 1):
        id_j = random.randint(1, NB_JOUEURS)
        id_jeu = random.randint(1, NB_JEUX)
        date_a = fake.date_time_between(start_date='-2y', end_date='now')
        montant = round(random.uniform(5, 100), 2)
        writer.writerow([i, id_j, id_jeu, date_a, montant])

# ---------- Signalements ----------
print("Génération des signalements...")
motifs = ['Triche', 'Insultes', 'Abandon', 'Comportement toxique', 'Harcèlement']
statuts_possibles = ['En attente', 'Traité', 'Rejeté']
with open(os.path.join(data_dir, 'signalements.csv'), 'w', newline='', encoding=ENCODING) as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['id_signalement', 'id_joueur', 'motif', 'date_signalement', 'statut'])
    for i in range(1, NB_SIGNALEMENTS + 1):
        if i <= 9:
            # 3 signalements pour chacun des 3 suspects, motif forcé 'Triche'
            id_j = (i - 1) // 3 + 1
            motif = 'Triche'
            date_s = fake.date_time_between(start_date='-1y', end_date='now')
            statut = 'En attente'
        else:
            id_j = random.randint(1, NB_JOUEURS)
            motif = random.choice(motifs)
            date_s = fake.date_time_between(start_date='-1y', end_date='now')
            statut = random.choice(statuts_possibles)
        writer.writerow([i, id_j, motif, date_s, statut])

# ---------- Sanctions ----------
print("Génération des sanctions...")
types_sanction = ['Avertissement', 'Suspension 1 jour', 'Suspension 7 jours',
                  'Bannissement permanent', 'Suspension 30 jours']
with open(os.path.join(data_dir, 'sanctions.csv'), 'w', newline='', encoding=ENCODING) as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['id_sanction', 'id_joueur', 'motif', 'date_sanction', 'type_sanction'])
    for i in range(1, NB_SANCTIONS + 1):
        if i <= 3:
            id_j = i
            motif = random.choice(motifs)
            date_san = fake.date_time_between(start_date='-2y', end_date='now')
            type_san = random.choice(types_sanction)
        else:
            id_j = random.randint(1, NB_JOUEURS)
            motif = random.choice(motifs)
            date_san = fake.date_time_between(start_date='-2y', end_date='now')
            type_san = random.choice(types_sanction)
        writer.writerow([i, id_j, motif, date_san, type_san])

print("Génération des CSV terminée !")

# ============================================================
# ÉCRITURE DU SCRIPT SQL (création tables + BULK INSERT + FK)
# ============================================================
# Ordre logique :
#   1. CREATE TABLE (PK seule, pas de FK) -> pas de vérification de contrainte
#      pendant le chargement des grosses tables (Parties = 7M lignes).
#   2. BULK INSERT de toutes les tables (FORMAT='CSV' + FIELDQUOTE gère
#      correctement les champs texte contenant une virgule, ex. noms de société).
#   3. ALTER TABLE ... ADD CONSTRAINT (FK) une fois les données en place :
#      un seul contrôle d'intégrité global, beaucoup plus rapide que
#      7 millions de contrôles ligne par ligne.
#   4. Index sur les colonnes de clé étrangère pour les jointures de reporting.

sql_script = f"""
-- ============================================================
-- 1) CRÉATION DES TABLES (clé primaire uniquement)
-- ============================================================

IF OBJECT_ID('dbo.Sanctions', 'U') IS NOT NULL DROP TABLE dbo.Sanctions;
IF OBJECT_ID('dbo.Signalements', 'U') IS NOT NULL DROP TABLE dbo.Signalements;
IF OBJECT_ID('dbo.Achats', 'U') IS NOT NULL DROP TABLE dbo.Achats;
IF OBJECT_ID('dbo.Parties', 'U') IS NOT NULL DROP TABLE dbo.Parties;
IF OBJECT_ID('dbo.Jeux', 'U') IS NOT NULL DROP TABLE dbo.Jeux;
IF OBJECT_ID('dbo.Plateformes', 'U') IS NOT NULL DROP TABLE dbo.Plateformes;
IF OBJECT_ID('dbo.Joueurs', 'U') IS NOT NULL DROP TABLE dbo.Joueurs;

CREATE TABLE dbo.Joueurs (
    id_joueur        INT PRIMARY KEY,
    pseudo           VARCHAR(50)  COLLATE Latin1_General_CI_AS NOT NULL,
    pays             VARCHAR(50)  COLLATE Latin1_General_CI_AS,
    date_inscription DATE,
    heures_jeu       DECIMAL(10,2) DEFAULT 0,
    victoires        INT DEFAULT 0,
    defaites         INT DEFAULT 0,
    precision_tir    DECIMAL(5,2) DEFAULT 0,
    tirs_tete        INT DEFAULT 0
);

CREATE TABLE dbo.Jeux (
    id_jeu   INT PRIMARY KEY,
    nom_jeu  VARCHAR(150) COLLATE Latin1_General_CI_AS NOT NULL,
    editeur  VARCHAR(100) COLLATE Latin1_General_CI_AS,
    genre    VARCHAR(50)  COLLATE Latin1_General_CI_AS
);

CREATE TABLE dbo.Plateformes (
    id_plateforme  INT PRIMARY KEY,
    nom_plateforme VARCHAR(50) COLLATE Latin1_General_CI_AS NOT NULL,
    constructeur   VARCHAR(50) COLLATE Latin1_General_CI_AS
);

CREATE TABLE dbo.Parties (
    id_partie     INT PRIMARY KEY,
    id_joueur     INT NOT NULL,
    id_jeu        INT NOT NULL,
    id_plateforme INT NOT NULL,
    date_partie   DATETIME NOT NULL,
    duree_minutes INT,
    score         INT,
    resultat      VARCHAR(20) COLLATE Latin1_General_CI_AS
);

CREATE TABLE dbo.Achats (
    id_achat   INT PRIMARY KEY,
    id_joueur  INT NOT NULL,
    id_jeu     INT NOT NULL,
    date_achat DATETIME NOT NULL,
    montant    DECIMAL(10,2)
);

CREATE TABLE dbo.Signalements (
    id_signalement   INT PRIMARY KEY,
    id_joueur        INT NOT NULL,
    motif            VARCHAR(200) COLLATE Latin1_General_CI_AS,
    date_signalement DATETIME NOT NULL,
    statut           VARCHAR(20) COLLATE Latin1_General_CI_AS DEFAULT 'En attente'
);

-- id_sanction : clé simple comme les autres tables (les CSV fournissent déjà
-- des identifiants séquentiels) -> plus d'IDENTITY/KEEPIDENTITY incohérents.
CREATE TABLE dbo.Sanctions (
    id_sanction   INT PRIMARY KEY,
    id_joueur     INT NOT NULL,
    motif         VARCHAR(200) COLLATE Latin1_General_CI_AS,
    date_sanction DATETIME NOT NULL,
    type_sanction VARCHAR(30) COLLATE Latin1_General_CI_AS
);

-- ============================================================
-- 2) BULK INSERT
--    FORMAT = 'CSV' + FIELDQUOTE = '"' : gère les champs contenant une
--    virgule (ex. raisons sociales générées par Faker) sans décaler les
--    colonnes. ROWTERMINATOR = 0x0a correspond au lineterminator='\\n'
--    utilisé côté Python. TABLOCK/BATCHSIZE accélèrent le chargement des
--    grosses tables.
-- ============================================================

BULK INSERT dbo.Joueurs
FROM '{os.path.join(data_dir, 'joueurs.csv')}'
WITH (FORMAT = 'CSV', FIELDQUOTE = '"', FIRSTROW = 2,
      FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a',
      CODEPAGE = '65001', TABLOCK, BATCHSIZE = 100000);

BULK INSERT dbo.Jeux
FROM '{os.path.join(data_dir, 'jeux.csv')}'
WITH (FORMAT = 'CSV', FIELDQUOTE = '"', FIRSTROW = 2,
      FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a',
      CODEPAGE = '65001', TABLOCK);

BULK INSERT dbo.Plateformes
FROM '{os.path.join(data_dir, 'plateformes.csv')}'
WITH (FORMAT = 'CSV', FIELDQUOTE = '"', FIRSTROW = 2,
      FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a',
      CODEPAGE = '65001', TABLOCK);

BULK INSERT dbo.Parties
FROM '{os.path.join(data_dir, 'parties.csv')}'
WITH (FORMAT = 'CSV', FIELDQUOTE = '"', FIRSTROW = 2,
      FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a',
      CODEPAGE = '65001', TABLOCK, BATCHSIZE = 100000);

BULK INSERT dbo.Achats
FROM '{os.path.join(data_dir, 'achats.csv')}'
WITH (FORMAT = 'CSV', FIELDQUOTE = '"', FIRSTROW = 2,
      FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a',
      CODEPAGE = '65001', TABLOCK, BATCHSIZE = 100000);

BULK INSERT dbo.Signalements
FROM '{os.path.join(data_dir, 'signalements.csv')}'
WITH (FORMAT = 'CSV', FIELDQUOTE = '"', FIRSTROW = 2,
      FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a',
      CODEPAGE = '65001', TABLOCK, BATCHSIZE = 100000);

BULK INSERT dbo.Sanctions
FROM '{os.path.join(data_dir, 'sanctions.csv')}'
WITH (FORMAT = 'CSV', FIELDQUOTE = '"', FIRSTROW = 2,
      FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a',
      CODEPAGE = '65001', TABLOCK, BATCHSIZE = 100000);

-- ============================================================
-- 3) CLÉS ÉTRANGÈRES (ajoutées après le chargement)
-- ============================================================

ALTER TABLE dbo.Parties  ADD CONSTRAINT FK_Parties_Joueurs     FOREIGN KEY (id_joueur)     REFERENCES dbo.Joueurs(id_joueur);
ALTER TABLE dbo.Parties  ADD CONSTRAINT FK_Parties_Jeux        FOREIGN KEY (id_jeu)        REFERENCES dbo.Jeux(id_jeu);
ALTER TABLE dbo.Parties  ADD CONSTRAINT FK_Parties_Plateformes FOREIGN KEY (id_plateforme) REFERENCES dbo.Plateformes(id_plateforme);

ALTER TABLE dbo.Achats   ADD CONSTRAINT FK_Achats_Joueurs FOREIGN KEY (id_joueur) REFERENCES dbo.Joueurs(id_joueur);
ALTER TABLE dbo.Achats   ADD CONSTRAINT FK_Achats_Jeux    FOREIGN KEY (id_jeu)    REFERENCES dbo.Jeux(id_jeu);

ALTER TABLE dbo.Signalements ADD CONSTRAINT FK_Signalements_Joueurs FOREIGN KEY (id_joueur) REFERENCES dbo.Joueurs(id_joueur);

ALTER TABLE dbo.Sanctions    ADD CONSTRAINT FK_Sanctions_Joueurs    FOREIGN KEY (id_joueur) REFERENCES dbo.Joueurs(id_joueur);

-- ============================================================
-- 4) INDEX SUR LES CLÉS ÉTRANGÈRES (accélère les jointures de reporting)
-- ============================================================

CREATE INDEX IX_Parties_Joueur      ON dbo.Parties(id_joueur);
CREATE INDEX IX_Parties_Jeu         ON dbo.Parties(id_jeu);
CREATE INDEX IX_Parties_Plateforme  ON dbo.Parties(id_plateforme);
CREATE INDEX IX_Achats_Joueur       ON dbo.Achats(id_joueur);
CREATE INDEX IX_Achats_Jeu          ON dbo.Achats(id_jeu);
CREATE INDEX IX_Signalements_Joueur ON dbo.Signalements(id_joueur);
CREATE INDEX IX_Sanctions_Joueur    ON dbo.Sanctions(id_joueur);

-- ============================================================
-- 5) VÉRIFICATION RAPIDE
-- ============================================================
SELECT 'Joueurs' AS TableName, COUNT(*) AS NbLignes FROM dbo.Joueurs
UNION ALL SELECT 'Jeux', COUNT(*) FROM dbo.Jeux
UNION ALL SELECT 'Plateformes', COUNT(*) FROM dbo.Plateformes
UNION ALL SELECT 'Parties', COUNT(*) FROM dbo.Parties
UNION ALL SELECT 'Achats', COUNT(*) FROM dbo.Achats
UNION ALL SELECT 'Signalements', COUNT(*) FROM dbo.Signalements
UNION ALL SELECT 'Sanctions', COUNT(*) FROM dbo.Sanctions;
"""

sql_path = os.path.join(base_dir, 'creation_et_import.sql')
with open(sql_path, 'w', encoding='utf-8') as f:
    f.write(sql_script)

print(f"\nScript SQL généré : {sql_path}")
print("Ouvre ce fichier dans SSMS et exécute-le pour créer les tables et importer les données.")
print("Assure-toi que le compte du service SQL Server a les droits de lecture sur le dossier data.")
