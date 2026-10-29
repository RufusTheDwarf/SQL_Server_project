IF DB_ID(N'MissionCinema') IS NULL
BEGIN
    CREATE DATABASE [MissionCinema];
END
ELSE
BEGIN
    PRINT 'La base MissionCinema existe deja. Aucune modification effectuee.';
END;
GO
