import os
import unittest
from contextlib import closing
import pyodbc

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import get_connection


@unittest.skipUnless(os.getenv("RUN_SQL_INTEGRATION") == "1", "Définir RUN_SQL_INTEGRATION=1 sur un poste SQL Server de test.")
class SQLServerIntegrationTests(unittest.TestCase):
    def test_reservations_volume(self):
        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("SELECT COUNT_BIG(*) FROM dbo.Reservations")
                self.assertGreaterEqual(int(cursor.fetchone()[0]), 10_000_000)

    def test_relations_without_orphans(self):
        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("""
                    SELECT COUNT_BIG(*)
                    FROM dbo.Reservations AS r
                    LEFT JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
                    LEFT JOIN dbo.Clients AS c ON c.client_id = r.client_id
                    WHERE s.seance_id IS NULL OR c.client_id IS NULL
                """)
                self.assertEqual(int(cursor.fetchone()[0]), 0)

    def test_genre_query_returns_rows(self):
        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("""
                    SELECT f.genre, COUNT_BIG(*) AS total
                    FROM dbo.Reservations AS r
                    JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
                    JOIN dbo.Films AS f ON f.film_id = s.film_id
                    GROUP BY f.genre
                    ORDER BY total DESC
                """)
                self.assertGreater(len(cursor.fetchall()), 0)


if __name__ == "__main__":
    unittest.main()
