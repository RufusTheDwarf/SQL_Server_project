USE [MissionCinema];
GO

SET NOCOUNT ON;

SELECT
    t.name AS table_name,
    SUM(p.rows) AS row_count
FROM sys.tables AS t
JOIN sys.partitions AS p ON p.object_id = t.object_id
WHERE p.index_id IN (0, 1)
GROUP BY t.name
ORDER BY t.name;

SELECT
    (SELECT COUNT_BIG(*) FROM dbo.Reservations) AS total_reservations,
    (SELECT COUNT_BIG(*) FROM dbo.Clients) AS total_clients,
    (SELECT COUNT_BIG(*) FROM dbo.Seances) AS total_seances,
    (SELECT COUNT_BIG(*) FROM dbo.Films) AS total_films,
    (SELECT COUNT_BIG(*) FROM dbo.Cinemas) AS total_cinemas;

SELECT COUNT_BIG(*) AS reservations_sans_seance
FROM dbo.Reservations AS r
LEFT JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
WHERE s.seance_id IS NULL;

SELECT COUNT_BIG(*) AS reservations_sans_client
FROM dbo.Reservations AS r
LEFT JOIN dbo.Clients AS c ON c.client_id = r.client_id
WHERE c.client_id IS NULL;

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
GO
