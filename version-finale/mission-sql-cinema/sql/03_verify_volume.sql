USE [MissionCinema];
GO

SET NOCOUNT ON;
SET DATEFIRST 7;
GO

DECLARE @TotalReservations BIGINT = (SELECT COUNT_BIG(*) FROM dbo.Reservations);
DECLARE @OrphelinesSeance BIGINT;
DECLARE @OrphelinesClient BIGINT;

SELECT
    t.name AS table_name,
    SUM(p.rows) AS row_count
FROM sys.tables AS t
JOIN sys.partitions AS p ON p.object_id = t.object_id
WHERE p.index_id IN (0, 1)
GROUP BY t.name
ORDER BY t.name;

SELECT
    @TotalReservations AS total_reservations,
    (SELECT COUNT_BIG(*) FROM dbo.Clients) AS total_clients,
    (SELECT COUNT_BIG(*) FROM dbo.Seances) AS total_seances,
    (SELECT COUNT_BIG(*) FROM dbo.Films) AS total_films,
    (SELECT COUNT_BIG(*) FROM dbo.Cinemas) AS total_cinemas;

SELECT @OrphelinesSeance = COUNT_BIG(*)
FROM dbo.Reservations AS r
LEFT JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
WHERE s.seance_id IS NULL;

SELECT @OrphelinesClient = COUNT_BIG(*)
FROM dbo.Reservations AS r
LEFT JOIN dbo.Clients AS c ON c.client_id = r.client_id
WHERE c.client_id IS NULL;

SELECT @OrphelinesSeance AS reservations_sans_seance;
SELECT @OrphelinesClient AS reservations_sans_client;

SELECT
    f.genre,
    COUNT_BIG(*) AS total_reservations
FROM dbo.Reservations AS r
INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
INNER JOIN dbo.Films AS f ON f.film_id = s.film_id
GROUP BY f.genre
ORDER BY total_reservations DESC, f.genre;

SELECT
    c.nom AS cinema,
    COUNT_BIG(*) AS total_reservations
FROM dbo.Reservations AS r
INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
INNER JOIN dbo.Cinemas AS c ON c.cinema_id = s.cinema_id
GROUP BY c.nom, c.cinema_id
ORDER BY total_reservations DESC, c.nom;

SELECT
    DATEPART(WEEKDAY, date_reservation) AS jour_numero,
    COUNT_BIG(*) AS total_reservations
FROM dbo.Reservations
GROUP BY DATEPART(WEEKDAY, date_reservation)
ORDER BY total_reservations DESC, jour_numero;

SELECT
    SUM(CONVERT(BIGINT, used_page_count)) * 8 / 1024.0 AS espace_utilise_mo
FROM sys.dm_db_partition_stats
WHERE object_id IN (
    OBJECT_ID('dbo.Films'),
    OBJECT_ID('dbo.Cinemas'),
    OBJECT_ID('dbo.Clients'),
    OBJECT_ID('dbo.Seances'),
    OBJECT_ID('dbo.Reservations')
);

IF @TotalReservations < 10000000
    PRINT 'ATTENTION : le seuil de 10 000 000 reservations n est pas atteint.';
ELSE
    PRINT 'OK : le seuil de 10 000 000 reservations est atteint.';

IF @OrphelinesSeance <> 0 OR @OrphelinesClient <> 0
    PRINT 'ATTENTION : des reservations orphelines ont ete trouvees.';
ELSE
    PRINT 'OK : aucune reservation orpheline detectee.';
GO
