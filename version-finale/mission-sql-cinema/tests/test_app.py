import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import app as mission_app


class MissionAppTests(unittest.TestCase):
    def setUp(self):
        mission_app.app.config.update(TESTING=True, SECRET_KEY="test-secret")
        mission_app._CACHE_OPTIONS.clear()
        self.client = mission_app.app.test_client()

    def tearDown(self):
        mission_app._CACHE_OPTIONS.clear()

    def set_step(self, step=0, score=0):
        with self.client.session_transaction() as state:
            state["etape"] = step
            state["score"] = score

    def post_answer(self, choice, step=0):
        return self.client.post("/repondre", data={"choix": choice, "etape": str(step)})

    def test_challenge_options_are_cached_after_first_load(self):
        with patch.dict(os.environ, {"DEMO_MODE": ""}):
            with patch.object(mission_app, "lire_options", return_value=mission_app.DONNEES_DEMO[0]) as reader:
                first = mission_app.charger_options(0)
                second = mission_app.charger_options(0)
        self.assertEqual(first, second)
        reader.assert_called_once_with(0)

    def test_simulation_mode_does_not_attempt_sql_server(self):
        with patch.dict(os.environ, {"DEMO_MODE": "1"}):
            with patch.object(mission_app, "lire_options", side_effect=AssertionError("SQL ne doit pas etre appele")):
                options, simulation = mission_app.charger_options(0)
        self.assertTrue(simulation)
        self.assertEqual(options, mission_app.DONNEES_DEMO[0])

    def test_homepage_shows_first_challenge(self):
        with patch.dict(os.environ, {"DEMO_MODE": "1"}):
            response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Quel genre attire le plus de réservations".encode(), response.data)
        self.assertIn("MODE SIMULATION".encode(), response.data)
        self.assertIn(b"COUNT_BIG", response.data)

    def test_connection_error_is_explained(self):
        with patch.dict(os.environ, {"DEMO_MODE": ""}):
            with patch.object(mission_app, "charger_options", side_effect=mission_app.pyodbc.Error("connection failed")):
                response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Connexion à SQL Server impossible".encode(), response.data)

    def test_correct_answer_increases_score(self):
        self.set_step()
        with patch.object(mission_app, "charger_options", return_value=(mission_app.DONNEES_DEMO[0], True)):
            response = self.post_answer("Science-fiction")
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as state:
            self.assertEqual(state["score"], 1)
            self.assertEqual(state["etape"], 1)
            self.assertTrue(state["dernier_resultat"]["correct"])

    def test_wrong_answer_does_not_increase_score(self):
        self.set_step()
        with patch.object(mission_app, "charger_options", return_value=(mission_app.DONNEES_DEMO[0], True)):
            self.post_answer("Action")
        with self.client.session_transaction() as state:
            self.assertEqual(state["score"], 0)
            self.assertFalse(state["dernier_resultat"]["correct"])

    def test_invalid_answer_does_not_advance_challenge(self):
        self.set_step()
        with patch.object(mission_app, "charger_options", return_value=(mission_app.DONNEES_DEMO[0], True)):
            response = self.post_answer("valeur-inconnue")
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as state:
            self.assertEqual(state["etape"], 0)
            self.assertEqual(state["score"], 0)
            self.assertNotIn("dernier_resultat", state)

    def test_old_form_submission_is_ignored(self):
        self.set_step(step=1, score=1)
        with patch.object(mission_app, "charger_options", return_value=(mission_app.DONNEES_DEMO[1], True)):
            self.post_answer("1", step=0)
        with self.client.session_transaction() as state:
            self.assertEqual(state["etape"], 1)
            self.assertEqual(state["score"], 1)

    def test_empty_results_are_handled_without_advancing(self):
        self.set_step()
        with patch.object(mission_app, "charger_options", return_value=([], False)):
            self.post_answer("Action")
        with self.client.session_transaction() as state:
            self.assertEqual(state["etape"], 0)
            self.assertEqual(state["score"], 0)

    def test_untrusted_value_is_only_compared_to_options(self):
        self.set_step()
        payload = "'; DROP TABLE dbo.Reservations;--"
        with patch.object(mission_app, "charger_options", return_value=(mission_app.DONNEES_DEMO[0], True)):
            self.post_answer(payload)
        with self.client.session_transaction() as state:
            self.assertEqual(state["score"], 0)
            self.assertEqual(state["etape"], 0)

    def test_restart_clears_session(self):
        self.set_step(step=2, score=2)
        response = self.client.post("/recommencer")
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as state:
            self.assertNotIn("score", state)
            self.assertNotIn("etape", state)

    def test_answer_after_finish_is_ignored(self):
        self.set_step(step=3, score=3)
        response = self.post_answer("Action", step=3)
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as state:
            self.assertEqual(state["score"], 3)
            self.assertEqual(state["etape"], 3)


if __name__ == "__main__":
    unittest.main()
