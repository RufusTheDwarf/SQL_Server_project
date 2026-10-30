USE [MissionCinema];
GO

SET NOCOUNT ON;
GO

IF EXISTS (SELECT 1 FROM sys.tables WHERE schema_id = SCHEMA_ID('dbo'))
BEGIN
    THROW 51000, 'La base MissionCinema contient deja des tables. Utilisez une base vide pour installer le schema. Aucune table existante ne sera supprimee.', 1;
END;
GO

CREATE TABLE dbo.Films (
    film_id INT NOT NULL CONSTRAINT PK_Films PRIMARY KEY,
    titre NVARCHAR(100) NOT NULL,
    genre NVARCHAR(30) NOT NULL,
    duree_minutes SMALLINT NOT NULL,
    age_minimum TINYINT NOT NULL,
    CONSTRAINT CK_Films_Duree CHECK (duree_minutes BETWEEN 40 AND 240),
    CONSTRAINT CK_Films_Age CHECK (age_minimum IN (0, 6, 10, 12, 16, 18))
);
GO

CREATE TABLE dbo.Cinemas (
    cinema_id INT NOT NULL CONSTRAINT PK_Cinemas PRIMARY KEY,
    nom NVARCHAR(80) NOT NULL,
    ville NVARCHAR(80) NOT NULL
);
GO

CREATE TABLE dbo.Clients (
    client_id INT NOT NULL CONSTRAINT PK_Clients PRIMARY KEY,
    pseudo NVARCHAR(40) NOT NULL,
    ville NVARCHAR(80) NOT NULL
);
GO

CREATE TABLE dbo.Seances (
    seance_id INT NOT NULL CONSTRAINT PK_Seances PRIMARY KEY,
    film_id INT NOT NULL,
    cinema_id INT NOT NULL,
    debut DATETIME2(0) NOT NULL,
    prix DECIMAL(5,2) NOT NULL,
    CONSTRAINT FK_Seances_Films FOREIGN KEY (film_id) REFERENCES dbo.Films(film_id),
    CONSTRAINT FK_Seances_Cinemas FOREIGN KEY (cinema_id) REFERENCES dbo.Cinemas(cinema_id),
    CONSTRAINT CK_Seances_Prix CHECK (prix BETWEEN 0 AND 100)
);
GO

CREATE TABLE dbo.Reservations (
    reservation_id BIGINT NOT NULL CONSTRAINT PK_Reservations PRIMARY KEY,
    seance_id INT NOT NULL,
    client_id INT NOT NULL,
    date_reservation DATETIME2(0) NOT NULL,
    places TINYINT NOT NULL,
    montant DECIMAL(7,2) NOT NULL,
    CONSTRAINT FK_Reservations_Seances FOREIGN KEY (seance_id) REFERENCES dbo.Seances(seance_id),
    CONSTRAINT FK_Reservations_Clients FOREIGN KEY (client_id) REFERENCES dbo.Clients(client_id),
    CONSTRAINT CK_Reservations_Places CHECK (places BETWEEN 1 AND 8),
    CONSTRAINT CK_Reservations_Montant CHECK (montant >= 0)
);
GO

INSERT INTO dbo.Films (film_id, titre, genre, duree_minutes, age_minimum)
VALUES
(1, N'Le Dernier Signal', N'Science-fiction', 118, 12),
(2, N'Mystère au Lac', N'Mystère', 104, 10),
(3, N'Course contre la Nuit', N'Action', 126, 12),
(4, N'Les Jours de Papier', N'Drame', 112, 10),
(5, N'Planète Océan', N'Documentaire', 92, 6),
(6, N'Rires en Retard', N'Comédie', 98, 6),
(7, N'La Porte Secrète', N'Aventure', 109, 6),
(8, N'Au-delà des Étoiles', N'Science-fiction', 131, 10),
(9, N'Le Témoin Invisible', N'Mystère', 115, 12),
(10, N'La Dernière Manche', N'Action', 101, 10),
(11, N'Un Été à Vevey', N'Drame', 107, 6),
(12, N'La Terre en Partage', N'Documentaire', 88, 0),
(13, N'Le Club du Dimanche', N'Comédie', 95, 6),
(14, N'La Carte Perdue', N'Aventure', 121, 10),
(15, N'Les Machines Rêvent', N'Science-fiction', 123, 10),
(16, N'Le Dossier Oublié', N'Thriller', 108, 10);
GO

INSERT INTO dbo.Cinemas (cinema_id, nom, ville)
VALUES
(1, N'Cinéma du Centre', N'Lausanne'),
(2, N'Le Grand Écran', N'Vevey'),
(3, N'Riviera Films', N'Montreux'),
(4, N'Les Arcades', N'Aigle'),
(5, N'Cinéma des Alpes', N'Yverdon-les-Bains');
GO

;WITH Chiffres AS (
    SELECT n FROM (VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9)) AS V(n)
),
Numeros AS (
    SELECT TOP (100000)
        ROW_NUMBER() OVER (ORDER BY a.n, b.n, c.n, d.n, e.n) AS n
    FROM Chiffres AS a
    CROSS JOIN Chiffres AS b
    CROSS JOIN Chiffres AS c
    CROSS JOIN Chiffres AS d
    CROSS JOIN Chiffres AS e
    ORDER BY a.n, b.n, c.n, d.n, e.n
)
INSERT INTO dbo.Clients (client_id, pseudo, ville)
SELECT
    CONVERT(INT, n),
    CONCAT(N'Visiteur-', RIGHT(CONCAT('000000', n), 6)),
    CASE (n - 1) % 5
        WHEN 0 THEN N'Lausanne'
        WHEN 1 THEN N'Vevey'
        WHEN 2 THEN N'Montreux'
        WHEN 3 THEN N'Aigle'
        ELSE N'Yverdon-les-Bains'
    END
FROM Numeros;
GO

;WITH Chiffres AS (
    SELECT n FROM (VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9)) AS V(n)
),
Numeros AS (
    SELECT TOP (1000)
        ROW_NUMBER() OVER (ORDER BY a.n, b.n, c.n) AS n
    FROM Chiffres AS a
    CROSS JOIN Chiffres AS b
    CROSS JOIN Chiffres AS c
)
INSERT INTO dbo.Seances (seance_id, film_id, cinema_id, debut, prix)
SELECT
    CONVERT(INT, n),
    CONVERT(INT, ((n - 1) % 16) + 1),
    CONVERT(INT, ((n - 1) % 5) + 1),
    DATEADD(HOUR, CONVERT(INT, n % 12) + 10, DATEADD(DAY, CONVERT(INT, n % 90), CONVERT(DATETIME2(0), '2026-09-01'))),
    CONVERT(DECIMAL(5,2), 12.00 + (n % 5) * 1.50)
FROM Numeros;
GO

CREATE INDEX IX_Seances_Film ON dbo.Seances(film_id);
CREATE INDEX IX_Seances_Cinema ON dbo.Seances(cinema_id);
GO
