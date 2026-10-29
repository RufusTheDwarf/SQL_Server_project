import os
from flask import Flask, render_template, request, session, redirect, url_for
import pyodbc

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "local-demo-change-this-key")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

ETAPES = [
    {
        "titre": "Quel genre attire le plus de réservations ?",
        "explication": "SQL regroupe les réservations par genre, compte les lignes et trie les résultats.",
        "notion": "JOIN, GROUP BY, COUNT et ORDER BY",
        "requete": "SELECT genre, COUNT(*) AS total FROM ... GROUP BY genre ORDER BY total DESC"
    },
    {
        "titre": "Dans quel cinéma réserve-t-on le plus ?",
        "explication": "La réservation est reliée à une séance, puis au cinéma. La jointure permet de compter par établissement.",
        "notion": "Jointures entre trois tables et agrégation",
        "requete": "SELECT cinema, COUNT(*) AS total FROM Reservations JOIN Seances JOIN Cinemas GROUP BY cinema"
    },
    {
        "titre": "Quel jour de la semaine est le plus fréquent ?",
        "explication": "SQL extrait le jour de la semaine de la date de réservation, puis compare les groupes.",
        "notion": "DATEPART, GROUP BY et ORDER BY",
        "requete": "SELECT DATEPART(WEEKDAY, date_reservation), COUNT(*) FROM Reservations GROUP BY DATEPART(WEEKDAY, date_reservation)"
    }
]

DONNEES_DEMO = [
    [{"label": "Action", "value": "Action", "total": 1780000},
     {"label": "Science-fiction", "value": "Science-fiction", "total": 1650000},
     {"label": "Comédie", "value": "Comédie", "total": 1510000},
     {"label": "Mystère", "value": "Mystère", "total": 1420000}],
    [{"label": "Cinéma du Centre", "value": "1", "total": 2300000},
     {"label": "Le Grand Écran", "value": "2", "total": 2180000},
     {"label": "Riviera Films", "value": "3", "total": 2050000},
     {"label": "Les Arcades", "value": "4", "total": 1900000}],
    [{"label": "Lundi", "value": "2", "total": 1510000},
     {"label": "Mardi", "value": "3", "total": 1490000},
     {"label": "Mercredi", "value": "4", "total": 1460000},
     {"label": "Jeudi", "value": "5", "total": 1430000}]
]

JOURS = {
    1: "Dimanche",
    2: "Lundi",
    3: "Mardi",
    4: "Mercredi",
    5: "Jeudi",
    6: "Vendredi",
    7: "Samedi"
}


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
    return pyodbc.connect(connection_string, timeout=5)


def lire_options(etape):
    if etape == 0:
        sql = """
            SELECT f.genre AS label, f.genre AS value, COUNT_BIG(*) AS total
            FROM dbo.Reservations AS r
            INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
            INNER JOIN dbo.Films AS f ON f.film_id = s.film_id
            GROUP BY f.genre
            ORDER BY total DESC, f.genre;
        """
    elif etape == 1:
        sql = """
            SELECT c.nom AS label, CONVERT(VARCHAR(12), c.cinema_id) AS value, COUNT_BIG(*) AS total
            FROM dbo.Reservations AS r
            INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
            INNER JOIN dbo.Cinemas AS c ON c.cinema_id = s.cinema_id
            GROUP BY c.nom, c.cinema_id
            ORDER BY total DESC, c.nom;
        """
    else:
        sql = """
            SELECT
                DATEPART(WEEKDAY, r.date_reservation) AS jour_numero,
                COUNT_BIG(*) AS total
            FROM dbo.Reservations AS r
            GROUP BY DATEPART(WEEKDAY, r.date_reservation)
            ORDER BY total DESC, jour_numero;
        """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

    options = []
    for row in rows:
        if etape == 2:
            numero = int(row.jour_numero)
            options.append({
                "label": JOURS.get(numero, f"Jour {numero}"),
                "value": str(numero),
                "total": int(row.total)
            })
        else:
            options.append({
                "label": str(row.label),
                "value": str(row.value),
                "total": int(row.total)
            })
    return options


def charger_options(etape):
    try:
        return lire_options(etape), False
    except pyodbc.Error:
        app.logger.exception("La requête de l'étape %s a échoué.", etape)
        if os.getenv("DEMO_MODE") == "1":
            return DONNEES_DEMO[etape], True
        raise


@app.route("/", methods=["GET"])
def index():
    etape = int(session.get("etape", 0))
    score = int(session.get("score", 0))
    erreur = None
    options = []
    simulation = False

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
        fini=etape >= len(ETAPES)
    )


@app.route("/repondre", methods=["POST"])
def repondre():
    try:
        etape = int(session.get("etape", 0))
    except (TypeError, ValueError):
        etape = 0

    if etape >= len(ETAPES):
        return redirect(url_for("index"))

    try:
        options, simulation = charger_options(etape)
    except pyodbc.Error:
        return redirect(url_for("index"))

    choix = request.form.get("choix", "")
    bonne_reponse = options[0]["value"] if options else None
    correct = choix == bonne_reponse
    session["score"] = int(session.get("score", 0)) + (1 if correct else 0)
    session["dernier_resultat"] = {
        "correct": correct,
        "bonne_reponse": options[0]["label"] if options else "Aucun résultat",
        "simulation": simulation
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
        dernier_resultat=resultat_partie
    )


@app.route("/recommencer", methods=["POST"])
def recommencer():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
