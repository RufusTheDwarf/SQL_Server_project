import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('fr_FR')

NB_JOUEURS = 500_000
NB_JEUX = 5_000
NB_PLATEFORMES = 20
NB_PARTIES = 7_000_000
NB_ACHATS = 2_000_000
NB_SIGNALEMENTS = 1_000_000
NB_SANCTIONS = 500_000

print("Génération des joueurs...")
with open('data/joueurs.csv', 'w', newline='', encoding='latin-1') as f:
    writer = csv.writer(f)
    writer.writerow(['id_joueur', 'pseudo', 'pays', 'date_inscription', 'heures_jeu',
                     'victoires', 'defaites', 'precision_tir', 'tirs_tete'])
    for i in range(1, NB_JOUEURS+1):
        if i in [1, 2, 3]:
            # Suspects : stats anormales
            pseudo = fake.user_name()
            pays = fake.country()
            date_insc = fake.date_between(start_date='-5y', end_date='today')
            heures = round(random.uniform(20, 80), 2)          # < 100 h
            victoires = random.randint(400, 600)               # très haut
            defaites = random.randint(0, 10)                   # très bas
            precision = round(random.uniform(95, 99.99), 2)    # > 95 %
            tirs_tete = random.randint(800, 1200)              # > 800
        else:
            # Joueurs normaux : valeurs plausibles et bornées
            pseudo = fake.user_name()
            pays = fake.country()
            date_insc = fake.date_between(start_date='-5y', end_date='today')
            heures = round(random.uniform(100, 5000), 2)       # au moins 100 h
            victoires = random.randint(0, 400)                 # max 400
            defaites = random.randint(50, 500)                 # min 50
            precision = round(random.uniform(0, 90), 2)        # max 90 %
            tirs_tete = random.randint(0, 500)                 # max 500
        writer.writerow([i, pseudo, pays, date_insc, heures,
                         victoires, defaites, precision, tirs_tete])

print("Génération des jeux...")
genres = ['FPS', 'RPG', 'MMO', 'MOBA', 'Battle Royale', 'Sport', 'Simulation']
with open('data/jeux.csv', 'w', newline='', encoding='latin-1') as f:
    writer = csv.writer(f)
    writer.writerow(['id_jeu', 'nom_jeu', 'editeur', 'genre'])
    for i in range(1, NB_JEUX+1):
        nom = fake.catch_phrase()
        editeur = fake.company()
        genre = random.choice(genres)
        writer.writerow([i, nom, editeur, genre])

print("Génération des plateformes...")
plateformes = [
    ('PlayStation 5', 'Sony'), ('PlayStation 4', 'Sony'),
    ('Xbox Series X', 'Microsoft'), ('Xbox One', 'Microsoft'),
    ('Nintendo Switch', 'Nintendo'), ('PC (Windows)', 'Microsoft'),
    ('PC (Linux)', 'Open Source'), ('Steam Deck', 'Valve'),
    ('Oculus Quest', 'Meta'), ('iOS', 'Apple'), ('Android', 'Google')
]
with open('data/plateformes.csv', 'w', newline='', encoding='latin-1') as f:
    writer = csv.writer(f)
    writer.writerow(['id_plateforme', 'nom_plateforme', 'constructeur'])
    for i in range(1, NB_PLATEFORMES+1):
        if i <= len(plateformes):
            nom, cons = plateformes[i-1]
        else:
            nom = fake.word() + ' ' + str(i)
            cons = fake.company()
        writer.writerow([i, nom, cons])

print("Génération des parties (long)...")
with open('data/parties.csv', 'w', newline='', encoding='latin-1') as f:
    writer = csv.writer(f)
    writer.writerow(['id_partie', 'id_joueur', 'id_jeu', 'id_plateforme',
                     'date_partie', 'duree_minutes', 'score', 'resultat'])
    for i in range(1, NB_PARTIES+1):
        id_j = random.randint(1, NB_JOUEURS)
        id_jeu = random.randint(1, NB_JEUX)
        id_plat = random.randint(1, NB_PLATEFORMES)
        date_p = fake.date_time_between(start_date='-3y', end_date='now')
        duree = random.randint(5, 180)
        score = random.randint(0, 50)
        resultat = random.choice(['victoire', 'defaite', 'nul'])
        writer.writerow([i, id_j, id_jeu, id_plat, date_p, duree, score, resultat])

print("Génération des achats...")
with open('data/achats.csv', 'w', newline='', encoding='latin-1') as f:
    writer = csv.writer(f)
    writer.writerow(['id_achat', 'id_joueur', 'id_jeu', 'date_achat', 'montant'])
    for i in range(1, NB_ACHATS+1):
        id_j = random.randint(1, NB_JOUEURS)
        id_jeu = random.randint(1, NB_JEUX)
        date_a = fake.date_time_between(start_date='-2y', end_date='now')
        montant = round(random.uniform(5, 100), 2)
        writer.writerow([i, id_j, id_jeu, date_a, montant])

print("Génération des signalements...")
motifs = ['Triche', 'Insultes', 'Abandon', 'Comportement toxique', 'Harcèlement']
statuts_possibles = ['En attente', 'Traité', 'Rejeté']
with open('data/signalements.csv', 'w', newline='', encoding='latin-1') as f:
    writer = csv.writer(f)
    writer.writerow(['id_signalement', 'id_joueur', 'motif', 'date_signalement', 'statut'])
    for i in range(1, NB_SIGNALEMENTS+1):
        if i <= 9:
            # 3 signalements pour chacun des 3 suspects, motif forcé 'Triche'
            id_j = (i-1) // 3 + 1  # 1,1,1,2,2,2,3,3,3
            motif = 'Triche'
            date_s = fake.date_time_between(start_date='-1y', end_date='now')
            statut = 'En attente'
        else:
            id_j = random.randint(1, NB_JOUEURS)
            motif = random.choice(motifs)
            date_s = fake.date_time_between(start_date='-1y', end_date='now')
            statut = random.choice(statuts_possibles)
        writer.writerow([i, id_j, motif, date_s, statut])

print("Génération des sanctions...")
types_sanction = ['Avertissement', 'Suspension 1 jour', 'Suspension 7 jours',
                  'Bannissement permanent', 'Suspension 30 jours']
with open('data/sanctions.csv', 'w', newline='', encoding='latin-1') as f:
    writer = csv.writer(f)
    writer.writerow(['id_sanction', 'id_joueur', 'motif', 'date_sanction', 'type_sanction'])
    for i in range(1, NB_SANCTIONS+1):
        if i <= 3:
            id_j = i
            motif = random.choice(motifs)
            date_san = fake.date_time_between(start_date='-2y', end_date='now')
            type_san = random.choice(types_sanction)
        else:
            id_j = random.randint(1, NB_JOUEURS)
            motif = random.choice(motifs)
            date_san = fake.date_time_between(start_date='-2y', end_date='now')
            type_san = random.choice(types_sanction)
        writer.writerow([i, id_j, motif, date_san, type_san])

print("Génération terminée !")