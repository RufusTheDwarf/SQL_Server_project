USE [MissionCinema];
GO

IF DATABASE_PRINCIPAL_ID(N'mission_cinema_lecture') IS NULL
BEGIN
    CREATE ROLE [mission_cinema_lecture];
END;
GO

GRANT SELECT ON dbo.Films TO [mission_cinema_lecture];
GRANT SELECT ON dbo.Cinemas TO [mission_cinema_lecture];
GRANT SELECT ON dbo.Clients TO [mission_cinema_lecture];
GRANT SELECT ON dbo.Seances TO [mission_cinema_lecture];
GRANT SELECT ON dbo.Reservations TO [mission_cinema_lecture];
GO

PRINT 'Role de lecture cree. Un administrateur doit ajouter le compte Windows du poste a ce role.';
GO
