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

SELECT COUNT_BIG(*) AS total_reservations
FROM dbo.Reservations;

SELECT COUNT_BIG(*) AS reservations_sans_seance
FROM dbo.Reservations AS r
LEFT JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
WHERE s.seance_id IS NULL;

SELECT
    SUM(CONVERT(BIGINT, used_page_count)) * 8 / 1024.0 AS espace_utilise_mo
FROM sys.dm_db_partition_stats
WHERE object_id IN (
    OBJECT_ID('dbo.Films'),
    OBJECT_ID('dbo.Cinemas'),
    OBJECT_ID('dbo.Seances'),
    OBJECT_ID('dbo.Reservations')
);
GO
