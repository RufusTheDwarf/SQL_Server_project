import os
import sys
from contextlib import closing

import pyodbc
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or os.urandom(32)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

JOURS = {
    1: "Dimanche",
    2: "Lundi",
    3: "Mardi",
    4: "Mercredi",
    5: "Jeudi",
    6: "Vendredi",
    7: "Samedi",
}

SQL_REQUETES = [
    """
    SELECT
        f.genre AS label,
        f.genre AS value,
        COUNT_BIG(*) AS total
    FROM dbo.Reservations AS r
    INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
    INNER JOIN dbo.Films AS f ON f.film_id = s.film_id
    GROUP BY f.genre
    ORDER BY total DESC, f.genre;
    """,
    """
    SELECT
        c.nom AS label,
        CONVERT(VARCHAR(12), c.cinema_id) AS value,
        COUNT_BIG(*) AS total
    FROM dbo.Reservations AS r
    INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
    INNER JOIN dbo.Cinemas AS c ON c.cinema_id = s.cinema_id
    GROUP BY c.nom, c.cinema_id
    ORDER BY total DESC, c.nom;
    """,
    """
    SELECT
        DATEPART(WEEKDAY, r.date_reservation) AS jour_numero,
        COUNT_BIG(*) AS total
    FROM dbo.Reservations AS r
    GROUP BY DATEPART(WEEKDAY, r.date_reservation)
    ORDER BY total DESC, jour_numero;
    """,
]

ETAPES = [
    {
        "titre": "Quel genre attire le plus de réservations ?",
        "explication": "SQL relie les réservations aux séances et aux films, regroupe les lignes par genre, puis compte les réservations.",
        "notion": "SELECT, JOIN, GROUP BY, COUNT_BIG et ORDER BY",
        "requete": SQL_REQUETES[0],
    },
    {
        "titre": "Dans quel cinéma réserve-t-on le plus ?",
        "explication": "SQL relie chaque réservation à sa séance et au cinéma correspondant, puis compare les totaux par établissement.",
        "notion": "JOIN entre trois tables, GROUP BY et COUNT_BIG",
        "requete": SQL_REQUETES[1],
    },
    {
        "titre": "Quel jour de la semaine est le plus fréquent ?",
        "explication": "SQL extrait le jour de la semaine de chaque réservation, regroupe les lignes et classe les totaux.",
        "notion": "DATEPART, GROUP BY, COUNT_BIG et ORDER BY",
        "requete": SQL_REQUETES[2],
    },
]

DONNEES_DEMO = [
    [
        {"label": "Science-fiction", "value": "Science-fiction", "total": 1880000},
        {"label": "Action", "value": "Action", "total": 1242500},
        {"label": "Aventure", "value": "Aventure", "total": 1242500},
        {"label": "Comédie", "value": "Comédie", "total": 1255000},
        {"label": "Documentaire", "value": "Documentaire", "total": 1255000},
        {"label": "Drame", "value": "Drame", "total": 1255000},
        {"label": "Mystère", "value": "Mystère", "total": 1242500},
        {"label": "Thriller", "value": "Thriller", "total": 627500},
    ],
    [
        {"label": "Cinéma du Centre", "value": "1", "total": 3000000},
        {"label": "Le Grand Écran", "value": "2", "total": 2500000},
        {"label": "Riviera Films", "value": "3", "total": 2000000},
        {"label": "Les Arcades", "value": "4", "total": 1500000},
        {"label": "Cinéma des Alpes", "value": "5", "total": 1000000},
    ],
    [
        {"label": "Samedi", "value": "7", "total": 3500000},
        {"label": "Vendredi", "value": "6", "total": 1500000},
        {"label": "Dimanche", "value": "1", "total": 1000000},
        {"label": "Lundi", "value": "2", "total": 1000000},
        {"label": "Mardi", "value": "3", "total": 1000000},
        {"label": "Mercredi", "value": "4", "total": 1000000},
        {"label": "Jeudi", "value": "5", "total": 1000000},
    ],
]

_CACHE_OPTIONS = {}


def get_connection():
    server = os.getenv("SQL_SERVER", r".\SQLEXPRESS")
    database = os.getenv("SQL_DATABASE", "MissionCinema")
    driver = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    connection = pyodbc.connect(connection_string, timeout=5)
    with closing(connection.cursor()) as cursor:
        cursor.execute("SET DATEFIRST 7;")
    return connection


def lire_options(etape):
    if etape not in range(len(SQL_REQUETES)):
        raise ValueError("Numéro de défi invalide.")

    with closing(get_connection()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(SQL_REQUETES[etape])
            rows = cursor.fetchall()

    options = []
    for row in rows:
        if etape == 2:
            numero = int(row.jour_numero)
            options.append({
                "label": JOURS.get(numero, f"Jour {numero}"),
                "value": str(numero),
                "total": int(row.total),
            })
        else:
            options.append({
                "label": str(row.label),
                "value": str(row.value),
                "total": int(row.total),
            })
    return options


def charger_options(etape):
    # Le mode simulation doit pouvoir fonctionner sans tenter une connexion SQL.
    if os.getenv("DEMO_MODE") == "1":
        return DONNEES_DEMO[etape], True

    if etape in _CACHE_OPTIONS:
        return _CACHE_OPTIONS[etape]

    try:
        resultat = (lire_options(etape), False)
    except pyodbc.Error:
        app.logger.exception("La requête de l'étape %s a échoué.", etape)
        raise

    _CACHE_OPTIONS[etape] = resultat
    return resultat


@app.route("/", methods=["GET"])
def index():
    etape = int(session.get("etape", 0))
    score = int(session.get("score", 0))
    erreur = None
    options = []
    simulation = os.getenv("DEMO_MODE") == "1"

    if etape < len(ETAPES):
        try:
            options, simulation = charger_options(etape)
        except pyodbc.Error:
            erreur = (
                "Connexion à SQL Server impossible. Vérifie le service, le nom de l'instance "
                "et la configuration ODBC. Le mode simulation est désactivé."
            )

    return render_template(
        "index.html",
        etapes=ETAPES,
        etape=etape,
        score=score,
        options=options,
        erreur=erreur,
        simulation=simulation,
        fini=etape >= len(ETAPES),
    )


@app.route("/repondre", methods=["POST"])
def repondre():
    try:
        etape = int(session.get("etape", 0))
        etape_formulaire = int(request.form.get("etape", "-1"))
    except (TypeError, ValueError):
        return redirect(url_for("index"))

    # Une ancienne soumission ne doit pas faire sauter un défi.
    if etape_formulaire != etape or etape >= len(ETAPES):
        return redirect(url_for("index"))

    try:
        options, simulation = charger_options(etape)
    except pyodbc.Error:
        return redirect(url_for("index"))

    if not options:
        return redirect(url_for("index"))

    choix = request.form.get("choix", "")
    valeurs_autorisees = {option["value"] for option in options}
    if choix not in valeurs_autorisees:
        return redirect(url_for("index"))

    bonne_reponse = options[0]["value"]
    correct = choix == bonne_reponse
    session["score"] = int(session.get("score", 0)) + (1 if correct else 0)
    session["dernier_resultat"] = {
        "correct": correct,
        "bonne_reponse": options[0]["label"],
        "simulation": simulation,
    }
    session["etape"] = etape + 1
    return redirect(url_for("resultat"))


@app.route("/resultat", methods=["GET"])
def resultat():
    resultat_partie = session.get("dernier_resultat")
    if not resultat_partie:
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        etapes=ETAPES,
        etape=int(session.get("etape", 0)),
        score=int(session.get("score", 0)),
        options=[],
        erreur=None,
        simulation=resultat_partie.get("simulation", False),
        fini=int(session.get("etape", 0)) >= len(ETAPES),
        dernier_resultat=resultat_partie,
    )


@app.route("/recommencer", methods=["POST"])
def recommencer():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    try:
        port = int(os.getenv("APP_PORT", "5000"))
    except ValueError as exc:
        raise SystemExit("APP_PORT doit etre un numero de port valide.") from exc

    if not 1 <= port <= 65535:
        raise SystemExit("APP_PORT doit etre compris entre 1 et 65535.")

    app.run(host="127.0.0.1", port=port, debug=False)
