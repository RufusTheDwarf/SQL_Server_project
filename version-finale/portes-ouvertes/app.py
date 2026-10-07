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

def get_connection():
    server = os.getenv("SQL_SERVER", "localhost")
    database = os.getenv("SQL_DATABASE", "SQL_Server_Project")
    driver = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string, timeout=5)

def to_float(form, name, default):
    try:
        value = float(form.get(name, default))
        return value
    except (TypeError, ValueError):
        return float(default)

def to_int(form, name, default):
    try:
        value = int(form.get(name, default))
        return value
    except (TypeError, ValueError):
        return int(default)

@app.route("/", methods=["GET", "POST"])
def index():
    values = DEFAULTS.copy()
    results = []
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
        )
        SELECT TOP 100
            j.id_joueur,
            j.pseudo,
            j.pays,
            j.heures_jeu,
            j.victoires,
            j.defaites,
            j.precision_tir,
            j.tirs_tete,
            ISNULL(s.total_signalements, 0) AS total_signalements,
            ISNULL(s.signalements_triche, 0) AS signalements_triche
        FROM dbo.Joueurs AS j
        LEFT JOIN SignalementsJoueur AS s
            ON s.id_joueur = j.id_joueur
        WHERE j.heures_jeu <= ?
          AND j.precision_tir >= ?
          AND j.tirs_tete >= ?
          AND j.victoires >= ?
          AND j.defaites <= ?
          AND ISNULL(s.signalements_triche, 0) >= ?
        ORDER BY
            ISNULL(s.signalements_triche, 0) DESC,
            j.precision_tir DESC,
            j.tirs_tete DESC,
            j.victoires DESC;
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
                )
                columns = [column[0] for column in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
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
        error=error,
        searched=searched,
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
