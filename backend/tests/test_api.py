import unittest
import json
from app import app, init_db

class FeedbackTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        init_db()

    def test_healthz(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_submit_feedback_success(self):
        payload = {"name": "Alice", "comment": "Great app!"}
        response = self.client.post("/submit", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Feedback submitted", response.get_json()["message"])

    def test_submit_feedback_missing_data(self):
        payload = {"name": ""}
        response = self.client.post("/submit", json=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()