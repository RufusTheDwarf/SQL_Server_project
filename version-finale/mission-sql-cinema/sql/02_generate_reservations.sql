USE [MissionCinema];
GO

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

DECLARE @NombreCible BIGINT = 10000000;
DECLARE @DejaPresent BIGINT = (SELECT COUNT_BIG(*) FROM dbo.Reservations);

IF @DejaPresent >= @NombreCible
BEGIN
    IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID('dbo.Reservations') AND name = 'IX_Reservations_Seance')
        CREATE INDEX IX_Reservations_Seance ON dbo.Reservations(seance_id);
    IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID('dbo.Reservations') AND name = 'IX_Reservations_Date')
        CREATE INDEX IX_Reservations_Date ON dbo.Reservations(date_reservation);
    PRINT CONCAT('Aucune insertion : ', @DejaPresent, ' réservations sont déjà présentes.');
    RETURN;
END;

IF @DejaPresent > 0
BEGIN
    THROW 51001, 'La table contient déjà des réservations mais reste sous la cible. Vérifiez les données avant de relancer le générateur.', 1;
END;

DECLARE @Debut DATETIME2(0) = SYSDATETIME();

;WITH Chiffres AS (
    SELECT n FROM (VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9)) AS V(n)
),
Numeros AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY a.n, b.n, c.n, d.n, e.n, f.n, g.n) AS n
    FROM Chiffres AS a
    CROSS JOIN Chiffres AS b
    CROSS JOIN Chiffres AS c
    CROSS JOIN Chiffres AS d
    CROSS JOIN Chiffres AS e
    CROSS JOIN Chiffres AS f
    CROSS JOIN Chiffres AS g
)
INSERT INTO dbo.Reservations WITH (TABLOCK)
    (reservation_id, seance_id, client_id, date_reservation, places, montant)
SELECT
    n,
    CONVERT(INT, ((n - 1) % 1000) + 1),
    CONVERT(INT, ((n - 1) % 100000) + 1),
    DATEADD(MINUTE, CONVERT(INT, n % 129600), CONVERT(DATETIME2(0), '2026-08-01')),
    CONVERT(TINYINT, ((n - 1) % 4) + 1),
    CONVERT(DECIMAL(7,2), (((n - 1) % 4) + 1) * (12.00 + (((n - 1) % 1000) % 5) * 1.50))
FROM Numeros
WHERE n <= @NombreCible
OPTION (MAXDOP 2);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID('dbo.Reservations') AND name = 'IX_Reservations_Seance')
    CREATE INDEX IX_Reservations_Seance ON dbo.Reservations(seance_id);
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID('dbo.Reservations') AND name = 'IX_Reservations_Date')
    CREATE INDEX IX_Reservations_Date ON dbo.Reservations(date_reservation);

DECLARE @Fin DATETIME2(0) = SYSDATETIME();
SELECT
    COUNT_BIG(*) AS reservations_generees,
    DATEDIFF(SECOND, @Debut, @Fin) AS duree_secondes,
    CAST(DATEDIFF(SECOND, @Debut, @Fin) / 60.0 AS DECIMAL(10,2)) AS duree_minutes
FROM dbo.Reservations;
GO
