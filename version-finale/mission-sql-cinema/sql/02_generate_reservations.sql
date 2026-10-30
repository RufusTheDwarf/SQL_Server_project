USE [MissionCinema];
GO

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

IF OBJECT_ID(N'dbo.Reservations', N'U') IS NULL
   OR OBJECT_ID(N'dbo.Seances', N'U') IS NULL
   OR OBJECT_ID(N'dbo.Clients', N'U') IS NULL
BEGIN
    THROW 51000, 'Le schema doit etre installe avant la generation des reservations.', 1;
END;
GO

DECLARE @NombreCible BIGINT = 10000000;
DECLARE @DejaPresent BIGINT = (SELECT COUNT_BIG(*) FROM dbo.Reservations);

IF @DejaPresent > 0
BEGIN
    DECLARE @MinimumId BIGINT = (SELECT MIN(reservation_id) FROM dbo.Reservations);
    DECLARE @MaximumId BIGINT = (SELECT MAX(reservation_id) FROM dbo.Reservations);

    IF @MinimumId <> 1 OR @MaximumId <> @DejaPresent
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
    DECLARE @LignesInserees INT;
    DECLARE @DebutLot DATETIME2(0);

    WHILE @DejaPresent < @NombreCible
    BEGIN
        SET @TailleCourante = CONVERT(INT, CASE
            WHEN @NombreCible - @DejaPresent > @TailleLot THEN @TailleLot
            ELSE @NombreCible - @DejaPresent
        END);
        SET @DebutLot = SYSDATETIME();

        BEGIN TRANSACTION;

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
            ORDER BY a.n, b.n, c.n, d.n, e.n, f.n
        )
        INSERT INTO dbo.Reservations WITH (TABLOCK)
            (reservation_id, seance_id, client_id, date_reservation, places, montant)
        SELECT
            base.reservation_id,
            s.seance_id,
            CONVERT(INT, (((base.reservation_id - 1) % 100000) + 1)),
            DATEADD(
                HOUR,
                9,
                DATEADD(
                    DAY,
                    -CASE
                        WHEN calendrier.jour_seance = distribution.jour_cible THEN 7
                        ELSE (calendrier.jour_seance - distribution.jour_cible + 7) % 7
                    END,
                    CONVERT(DATETIME2(0), CONVERT(DATE, s.debut))
                )
            ),
            cycles.places,
            CONVERT(DECIMAL(7,2), cycles.places * s.prix)
        FROM Numeros AS n
        CROSS APPLY (
            SELECT CONVERT(BIGINT, @DejaPresent) + n.n AS reservation_id
        ) AS base
        CROSS APPLY (
            SELECT
                CONVERT(INT, ((base.reservation_id - 1) * 37) % 100) + 1 AS cycle_cinema,
                CONVERT(INT, ((base.reservation_id - 1) * 73) % 100) + 1 AS cycle_jour,
                CONVERT(INT, (((base.reservation_id - 1) / 100) % 200) + 1) AS numero_seance,
                CONVERT(TINYINT, ((base.reservation_id - 1) % 4) + 1) AS places
        ) AS cycles
        CROSS APPLY (
            SELECT
                CASE
                    WHEN cycles.cycle_cinema <= 30 THEN 1
                    WHEN cycles.cycle_cinema <= 55 THEN 2
                    WHEN cycles.cycle_cinema <= 75 THEN 3
                    WHEN cycles.cycle_cinema <= 90 THEN 4
                    ELSE 5
                END AS cinema_id,
                CASE
                    WHEN cycles.cycle_jour <= 10 THEN 0
                    WHEN cycles.cycle_jour <= 20 THEN 1
                    WHEN cycles.cycle_jour <= 30 THEN 2
                    WHEN cycles.cycle_jour <= 40 THEN 3
                    WHEN cycles.cycle_jour <= 50 THEN 4
                    WHEN cycles.cycle_jour <= 65 THEN 5
                    ELSE 6
                END AS jour_cible
        ) AS distribution
        CROSS APPLY (
            SELECT ((cycles.numero_seance - 1) * 5) + distribution.cinema_id AS seance_id
        ) AS choix
        INNER JOIN dbo.Seances AS s ON s.seance_id = choix.seance_id
        CROSS APPLY (
            SELECT DATEDIFF(
                DAY,
                CONVERT(DATE, '19000107', 112),
                CONVERT(DATE, s.debut)
            ) % 7 AS jour_seance
        ) AS calendrier
        OPTION (MAXDOP 2);

        SET @LignesInserees = @@ROWCOUNT;

        IF @LignesInserees <> @TailleCourante
        BEGIN
            ROLLBACK TRANSACTION;
            THROW 51002, 'Le nombre de reservations inserees ne correspond pas a la taille du lot. Le lot a ete annule.', 1;
        END;

        COMMIT TRANSACTION;
        SET @DejaPresent = @DejaPresent + @LignesInserees;

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

PRINT 'Repartition attendue : cinemas 30 %, 25 %, 20 %, 15 % et 10 % ; reservations par jour : samedi 35 %, vendredi 15 %, autres jours 10 % chacun.';
GO
