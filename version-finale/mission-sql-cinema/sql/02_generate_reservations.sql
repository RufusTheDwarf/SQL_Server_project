USE [MissionCinema];
GO

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

DECLARE @NombreCible BIGINT = 10000000;
DECLARE @DejaPresent BIGINT = (SELECT COUNT_BIG(*) FROM dbo.Reservations);

IF @DejaPresent > 0
BEGIN
    IF (SELECT MIN(reservation_id) FROM dbo.Reservations) <> 1
       OR (SELECT MAX(reservation_id) FROM dbo.Reservations) <> @DejaPresent
    BEGIN
        THROW 51001, 'La table Reservations ne contient pas une suite continue de 1 a son nombre de lignes. Corrigez les donnees avant de reprendre.', 1;
    END;
END;

IF @DejaPresent >= @NombreCible
BEGIN
    PRINT CONCAT('Aucune insertion : ', @DejaPresent, ' reservations sont deja presentes.');
END
ELSE
BEGIN
    DECLARE @Debut DATETIME2(0) = SYSDATETIME();
    DECLARE @TailleLot INT = 500000;
    DECLARE @TailleCourante INT;
    DECLARE @DebutLot DATETIME2(0);

    WHILE @DejaPresent < @NombreCible
    BEGIN
        SET @TailleCourante = CONVERT(INT, CASE
            WHEN @NombreCible - @DejaPresent > @TailleLot THEN @TailleLot
            ELSE @NombreCible - @DejaPresent
        END);
        SET @DebutLot = SYSDATETIME();

        ;WITH Chiffres AS (
            SELECT n FROM (VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9)) AS V(n)
        ),
        Numeros AS (
            SELECT TOP (@TailleCourante)
                ROW_NUMBER() OVER (ORDER BY a.n, b.n, c.n, d.n, e.n, f.n) AS n
            FROM Chiffres AS a
            CROSS JOIN Chiffres AS b
            CROSS JOIN Chiffres AS c
            CROSS JOIN Chiffres AS d
            CROSS JOIN Chiffres AS e
            CROSS JOIN Chiffres AS f
        )
        INSERT INTO dbo.Reservations WITH (TABLOCK)
            (reservation_id, seance_id, client_id, date_reservation, places, montant)
        SELECT
            CONVERT(BIGINT, @DejaPresent) + n.n,
            s.seance_id,
            CONVERT(INT, (((CONVERT(BIGINT, @DejaPresent) + n.n) - 1) % 100000) + 1),
            DATEADD(
                MINUTE,
                -CONVERT(INT, (CONVERT(BIGINT, @DejaPresent) + n.n) % 43200),
                s.debut
            ),
            q.places,
            CONVERT(DECIMAL(7,2), q.places * s.prix)
        FROM Numeros AS n
        CROSS APPLY (
            SELECT
                CONVERT(INT, (((CONVERT(BIGINT, @DejaPresent) + n.n) - 1) % 1000) + 1) AS seance_id,
                CONVERT(TINYINT, (((CONVERT(BIGINT, @DejaPresent) + n.n) - 1) % 4) + 1) AS places
        ) AS q
        INNER JOIN dbo.Seances AS s ON s.seance_id = q.seance_id
        OPTION (MAXDOP 2);

        SET @DejaPresent = (SELECT COUNT_BIG(*) FROM dbo.Reservations);
        PRINT CONCAT(
            'Reservations presentes : ', @DejaPresent,
            ' ; duree du lot en secondes : ',
            DATEDIFF(SECOND, @DebutLot, SYSDATETIME())
        );
    END;

    PRINT CONCAT('Generation terminee en secondes : ', DATEDIFF(SECOND, @Debut, SYSDATETIME()));
END;
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID('dbo.Reservations') AND name = 'IX_Reservations_Seance')
    CREATE INDEX IX_Reservations_Seance ON dbo.Reservations(seance_id);
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE object_id = OBJECT_ID('dbo.Reservations') AND name = 'IX_Reservations_Date')
    CREATE INDEX IX_Reservations_Date ON dbo.Reservations(date_reservation);
GO
