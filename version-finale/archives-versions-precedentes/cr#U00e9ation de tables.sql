-- Joueurs
IF OBJECT_ID('dbo.Joueurs', 'U') IS NOT NULL DROP TABLE dbo.Joueurs;
CREATE TABLE dbo.Joueurs (
    id_joueur       INT PRIMARY KEY,
    pseudo          VARCHAR(50) COLLATE Latin1_General_CI_AS NOT NULL,
    pays            VARCHAR(50) COLLATE Latin1_General_CI_AS,
    date_inscription DATE,
    heures_jeu      DECIMAL(10,2) DEFAULT 0,
    victoires       INT DEFAULT 0,
    defaites        INT DEFAULT 0,
    precision_tir   DECIMAL(5,2) DEFAULT 0,
    tirs_tete       INT DEFAULT 0
);

-- Jeux
IF OBJECT_ID('dbo.Jeux', 'U') IS NOT NULL DROP TABLE dbo.Jeux;
CREATE TABLE dbo.Jeux (
    id_jeu      INT PRIMARY KEY,
    nom_jeu     VARCHAR(100) COLLATE Latin1_General_CI_AS NOT NULL,
    editeur     VARCHAR(50) COLLATE Latin1_General_CI_AS,
    genre       VARCHAR(50) COLLATE Latin1_General_CI_AS
);

-- Plateformes
IF OBJECT_ID('dbo.Plateformes', 'U') IS NOT NULL DROP TABLE dbo.Plateformes;
CREATE TABLE dbo.Plateformes (
    id_plateforme INT PRIMARY KEY,
    nom_plateforme VARCHAR(50) COLLATE Latin1_General_CI_AS NOT NULL,
    constructeur  VARCHAR(50) COLLATE Latin1_General_CI_AS
);

-- Parties
IF OBJECT_ID('dbo.Parties', 'U') IS NOT NULL DROP TABLE dbo.Parties;
CREATE TABLE dbo.Parties (
    id_partie      INT PRIMARY KEY,
    id_joueur      INT NOT NULL,
    id_jeu         INT NOT NULL,
    id_plateforme  INT NOT NULL,
    date_partie    DATETIME NOT NULL,
    duree_minutes  INT,
    score          INT,
    resultat       VARCHAR(20) COLLATE Latin1_General_CI_AS
);
ALTER TABLE dbo.Parties ADD CONSTRAINT FK_Parties_Joueurs FOREIGN KEY (id_joueur) REFERENCES dbo.Joueurs(id_joueur);
ALTER TABLE dbo.Parties ADD CONSTRAINT FK_Parties_Jeux FOREIGN KEY (id_jeu) REFERENCES dbo.Jeux(id_jeu);
ALTER TABLE dbo.Parties ADD CONSTRAINT FK_Parties_Plateformes FOREIGN KEY (id_plateforme) REFERENCES dbo.Plateformes(id_plateforme);

-- Achats
IF OBJECT_ID('dbo.Achats', 'U') IS NOT NULL DROP TABLE dbo.Achats;
CREATE TABLE dbo.Achats (
    id_achat       INT PRIMARY KEY,
    id_joueur      INT NOT NULL,
    id_jeu         INT NOT NULL,
    date_achat     DATETIME NOT NULL,
    montant        DECIMAL(10,2)
);
ALTER TABLE dbo.Achats ADD CONSTRAINT FK_Achats_Joueurs FOREIGN KEY (id_joueur) REFERENCES dbo.Joueurs(id_joueur);
ALTER TABLE dbo.Achats ADD CONSTRAINT FK_Achats_Jeux FOREIGN KEY (id_jeu) REFERENCES dbo.Jeux(id_jeu);

-- Signalements
IF OBJECT_ID('dbo.Signalements', 'U') IS NOT NULL DROP TABLE dbo.Signalements;
CREATE TABLE dbo.Signalements (
    id_signalement   INT PRIMARY KEY,
    id_joueur        INT NOT NULL,
    motif            VARCHAR(200) COLLATE Latin1_General_CI_AS,
    date_signalement DATETIME NOT NULL,
    statut           VARCHAR(20) COLLATE Latin1_General_CI_AS DEFAULT 'En attente'
);
ALTER TABLE dbo.Signalements ADD CONSTRAINT FK_Signalements_Joueurs FOREIGN KEY (id_joueur) REFERENCES dbo.Joueurs(id_joueur);

-- Sanctions (CORRIGÉ : id_sanction IDENTITY)
IF OBJECT_ID('dbo.Sanctions', 'U') IS NOT NULL DROP TABLE dbo.Sanctions;
CREATE TABLE dbo.Sanctions (
    id_sanction    INT IDENTITY(1,1) PRIMARY KEY,
    id_joueur      INT NOT NULL,
    motif          VARCHAR(200) COLLATE Latin1_General_CI_AS,
    date_sanction  DATETIME NOT NULL,
    type_sanction  VARCHAR(30) COLLATE Latin1_General_CI_AS
);
ALTER TABLE dbo.Sanctions ADD CONSTRAINT FK_Sanctions_Joueurs FOREIGN KEY (id_joueur) REFERENCES dbo.Joueurs(id_joueur);