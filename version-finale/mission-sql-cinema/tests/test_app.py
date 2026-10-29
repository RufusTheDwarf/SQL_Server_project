import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import app as mission_app


class MissionAppTests(unittest.TestCase):
    def setUp(self):
        mission_app.app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.client = mission_app.app.test_client()

    def test_homepage_shows_first_challenge(self):
        with patch.object(mission_app, "charger_options", return_value=(mission_app.DONNEES_DEMO[0], True)):
            response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Quel genre attire le plus de réservations".encode(), response.data)
        self.assertIn("MODE SIMULATION".encode(), response.data)

    def test_correct_answer_increases_score(self):
        with self.client.session_transaction() as state:
            state["etape"] = 0
            state["score"] = 0
        with patch.object(mission_app, "charger_options", return_value=(mission_app.DONNEES_DEMO[0], True)):
            response = self.client.post("/repondre", data={"choix": "Action"})
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as state:
            self.assertEqual(state["score"], 1)
            self.assertEqual(state["etape"], 1)
            self.assertTrue(state["dernier_resultat"]["correct"])

    def test_wrong_answer_does_not_increase_score(self):
        with self.client.session_transaction() as state:
            state["etape"] = 0
            state["score"] = 0
        with patch.object(mission_app, "charger_options", return_value=(mission_app.DONNEES_DEMO[0], True)):
            self.client.post("/repondre", data={"choix": "Mystère"})
        with self.client.session_transaction() as state:
            self.assertEqual(state["score"], 0)
            self.assertFalse(state["dernier_resultat"]["correct"])

    def test_untrusted_value_is_only_compared_to_options(self):
        payload = "'; DROP TABLE dbo.Reservations;--"
        with self.client.session_transaction() as state:
            state["etape"] = 0
            state["score"] = 0
        with patch.object(mission_app, "charger_options", return_value=(mission_app.DONNEES_DEMO[0], True)):
            self.client.post("/repondre", data={"choix": payload})
        with self.client.session_transaction() as state:
            self.assertEqual(state["score"], 0)
            self.assertFalse(state["dernier_resultat"]["correct"])

    def test_restart_clears_session(self):
        with self.client.session_transaction() as state:
            state["etape"] = 2
            state["score"] = 2
        response = self.client.post("/recommencer")
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as state:
            self.assertNotIn("score", state)
            self.assertNotIn("etape", state)

    def test_answer_after_finish_is_ignored(self):
        with self.client.session_transaction() as state:
            state["etape"] = 3
            state["score"] = 3
        response = self.client.post("/repondre", data={"choix": "Action"})
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as state:
            self.assertEqual(state["score"], 3)


if __name__ == "__main__":
    unittest.main()
