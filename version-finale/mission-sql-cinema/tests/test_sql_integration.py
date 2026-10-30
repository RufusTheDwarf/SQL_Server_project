import os
import sys
import unittest
from contextlib import closing

import pyodbc

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import get_connection


@unittest.skipUnless(
    os.getenv("RUN_SQL_INTEGRATION") == "1",
    "Définir RUN_SQL_INTEGRATION=1 sur un poste SQL Server de test.",
)
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

    def test_genre_distribution_has_one_leader(self):
        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("""
                    SELECT f.genre, COUNT_BIG(*) AS total
                    FROM dbo.Reservations AS r
                    INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
                    INNER JOIN dbo.Films AS f ON f.film_id = s.film_id
                    GROUP BY f.genre
                    ORDER BY total DESC, f.genre
                """)
                rows = cursor.fetchall()
                self.assertGreater(len(rows), 1)
                self.assertEqual(rows[0].genre, "Science-fiction")
                self.assertGreater(int(rows[0].total), int(rows[1].total))

    def test_cinema_distribution_has_one_leader(self):
        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("""
                    SELECT c.nom, COUNT_BIG(*) AS total
                    FROM dbo.Reservations AS r
                    INNER JOIN dbo.Seances AS s ON s.seance_id = r.seance_id
                    INNER JOIN dbo.Cinemas AS c ON c.cinema_id = s.cinema_id
                    GROUP BY c.nom, c.cinema_id
                    ORDER BY total DESC, c.nom
                """)
                rows = cursor.fetchall()
                self.assertEqual(len(rows), 5)
                self.assertEqual(rows[0].nom, "Cinéma du Centre")
                totals = [int(row.total) for row in rows]
                self.assertEqual(totals, sorted(totals, reverse=True))
                self.assertGreater(totals[0], totals[1])

    def test_saturday_is_the_most_frequent_reservation_day(self):
        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("SET DATEFIRST 7;")
                cursor.execute("""
                    SELECT DATEPART(WEEKDAY, date_reservation) AS jour_numero,
                           COUNT_BIG(*) AS total
                    FROM dbo.Reservations
                    GROUP BY DATEPART(WEEKDAY, date_reservation)
                    ORDER BY total DESC, jour_numero
                """)
                rows = cursor.fetchall()
                self.assertEqual(int(rows[0].jour_numero), 7)
                self.assertEqual(int(rows[1].jour_numero), 6)
                totals = [int(row.total) for row in rows]
                self.assertEqual(totals, sorted(totals, reverse=True))
                self.assertGreater(totals[0], totals[1])

    def test_generator_distribution_covers_ten_million_rows(self):
        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("""
                    SELECT
                        (SELECT COUNT_BIG(*) FROM dbo.Reservations) AS reservations,
                        (SELECT COUNT_BIG(*) FROM dbo.Cinemas) AS cinemas,
                        (SELECT COUNT_BIG(*) FROM dbo.Films) AS films,
                        (SELECT COUNT_BIG(*) FROM dbo.Clients) AS clients,
                        (SELECT MIN(client_id) FROM dbo.Clients) AS min_client_id,
                        (SELECT MAX(client_id) FROM dbo.Clients) AS max_client_id,
                        (SELECT MIN(seance_id) FROM dbo.Seances) AS min_seance_id,
                        (SELECT MAX(seance_id) FROM dbo.Seances) AS max_seance_id
                """)
                row = cursor.fetchone()
                self.assertGreaterEqual(int(row.reservations), 10_000_000)
                self.assertEqual(int(row.cinemas), 5)
                self.assertEqual(int(row.films), 16)
                self.assertEqual(int(row.clients), 100_000)
                self.assertEqual(int(row.min_client_id), 1)
                self.assertEqual(int(row.max_client_id), 100_000)
                self.assertEqual(int(row.min_seance_id), 1)
                self.assertEqual(int(row.max_seance_id), 1_000)


if __name__ == "__main__":
    unittest.main()
