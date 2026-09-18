-- Étape 1 : Signalements
SELECT j.id_joueur, j.pseudo, COUNT(s.id_signalement) AS nb_signalements
FROM Joueurs j
JOIN Signalements s ON j.id_joueur = s.id_joueur
WHERE s.motif = 'Triche'
GROUP BY j.id_joueur, j.pseudo
HAVING COUNT(s.id_signalement) >= 3
ORDER BY nb_signalements DESC;

-- Étape 2 : Vérification statistique
SELECT pseudo, heures_jeu, victoires, defaites, precision_tir, tirs_tete
FROM Joueurs
WHERE id_joueur IN (1, 2, 3);

-- Étape 3 : Croisement des indices
SELECT j.id_joueur, j.pseudo,
       COUNT(s.id_signalement) AS nb_signalements,
       j.precision_tir, j.tirs_tete, j.heures_jeu
FROM Joueurs j
JOIN Signalements s ON j.id_joueur = s.id_joueur
WHERE s.motif = 'Triche'
GROUP BY j.id_joueur, j.pseudo, j.precision_tir, j.tirs_tete, j.heures_jeu
HAVING COUNT(s.id_signalement) >= 3
   AND j.precision_tir > 95
   AND j.tirs_tete > 800
   AND j.heures_jeu < 100;

-- Étape 4 : Sanction
INSERT INTO Sanctions (id_joueur, motif, date_sanction, type_sanction)
SELECT id_joueur, 'Triche confirmée', GETDATE(), 'Bannissement permanent'
FROM Joueurs
WHERE id_joueur IN (1, 2, 3);

SELECT * FROM Sanctions WHERE motif = 'Triche confirmée';