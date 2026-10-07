import os
from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

DEFAULTS = {
    "max_hours": 100,
    "min_accuracy": 95,
    "min_headshots": 800,
    "min_wins": 400,
    "max_losses": 10,
    "min_cheat_reports": 3,
}

MIN_SUSPICION_SCORE = 3

def get_connection():
    server = os.getenv("SQL_SERVER", r".\SQLEXPRESS")
    database = os.getenv("SQL_DATABASE", "SQL_Server_Project")
    driver = os.getenv("SQL_DRIVER", "ODBC Driver 17 for SQL Server")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string, timeout=5)

def to_float(form, name, default):
    try:
        return float(form.get(name, default))
    except (TypeError, ValueError):
        return float(default)

def to_int(form, name, default):
    try:
        return int(form.get(name, default))
    except (TypeError, ValueError):
        return int(default)

@app.route("/", methods=["GET", "POST"])
def index():
    values = DEFAULTS.copy()
    results = []
    total_suspects = 0
    error = None
    searched = request.method == "POST"

    if searched:
        values = {
            "max_hours": to_float(request.form, "max_hours", DEFAULTS["max_hours"]),
            "min_accuracy": to_float(request.form, "min_accuracy", DEFAULTS["min_accuracy"]),
            "min_headshots": to_int(request.form, "min_headshots", DEFAULTS["min_headshots"]),
            "min_wins": to_int(request.form, "min_wins", DEFAULTS["min_wins"]),
            "max_losses": to_int(request.form, "max_losses", DEFAULTS["max_losses"]),
            "min_cheat_reports": to_int(request.form, "min_cheat_reports", DEFAULTS["min_cheat_reports"]),
        }

        query = """
        WITH SignalementsJoueur AS (
            SELECT
                id_joueur,
                COUNT(*) AS total_signalements,
                SUM(CASE WHEN motif = 'Triche' THEN 1 ELSE 0 END) AS signalements_triche
            FROM dbo.Signalements
            GROUP BY id_joueur
        ),
        Scores AS (
            SELECT
                j.id_joueur,
                j.pseudo,
                j.pays,
                j.heures_jeu,
                j.victoires,
                j.defaites,
                j.precision_tir,
                j.tirs_tete,
                ISNULL(s.total_signalements, 0) AS total_signalements,
                ISNULL(s.signalements_triche, 0) AS signalements_triche,
                (
                    CASE WHEN j.heures_jeu <= ? THEN 1 ELSE 0 END +
                    CASE WHEN j.precision_tir >= ? THEN 1 ELSE 0 END +
                    CASE WHEN j.tirs_tete >= ? THEN 1 ELSE 0 END +
                    CASE WHEN j.victoires >= ? THEN 1 ELSE 0 END +
                    CASE WHEN j.defaites <= ? THEN 1 ELSE 0 END +
                    CASE WHEN ISNULL(s.signalements_triche, 0) >= ? THEN 2 ELSE 0 END
                ) AS score_suspicion
            FROM dbo.Joueurs AS j
            LEFT JOIN SignalementsJoueur AS s
                ON s.id_joueur = j.id_joueur
        ),
        Suspicious AS (
            SELECT
                *,
                COUNT(*) OVER() AS total_suspects
            FROM Scores
            WHERE score_suspicion >= ?
        )
        SELECT TOP 100
            id_joueur,
            pseudo,
            pays,
            heures_jeu,
            victoires,
            defaites,
            precision_tir,
            tirs_tete,
            total_signalements,
            signalements_triche,
            score_suspicion,
            total_suspects
        FROM Suspicious
        ORDER BY
            score_suspicion DESC,
            signalements_triche DESC,
            precision_tir DESC,
            tirs_tete DESC,
            victoires DESC;
        """

        try:
            with get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    query,
                    values["max_hours"],
                    values["min_accuracy"],
                    values["min_headshots"],
                    values["min_wins"],
                    values["max_losses"],
                    values["min_cheat_reports"],
                    MIN_SUSPICION_SCORE,
                )
                columns = [column[0] for column in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                if results:
                    total_suspects = results[0]["total_suspects"]
        except pyodbc.Error as exc:
            error = (
                "Impossible de se connecter à SQL Server. "
                "Vérifie que SQL Server est démarré et que SQL_SERVER / SQL_DATABASE "
                "correspondent à ton installation."
            )
            app.logger.exception("SQL Server error: %s", exc)

    return render_template(
        "index.html",
        values=values,
        results=results,
        total_suspects=total_suspects,
        min_suspicion_score=MIN_SUSPICION_SCORE,
        error=error,
        searched=searched,
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
