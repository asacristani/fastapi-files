# Write your tests here
import unittest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestAPI(unittest.TestCase):
    """
    TestAPI class for testing the FastAPI application.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize TestClient once for all tests in this class.
        """
        cls.client = TestClient(app)

    def test_foo(self):
        """
        Test if 'foo'.upper() correctly converts to 'FOO'. (legacy code)
        """
        self.assertEqual('foo'.upper(), 'FOO')

    def test_read_root(self):
        """
        Test the root endpoint for a successful response.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    def test_upload_pdf_healthinc(self):
        """
        Test uploading a valid PDF (healthinc.pdf) and check for discrepancies.
        """
        with open("assets/healthinc.pdf", "rb") as file:
            response = self.client.post("/upload_pdf/", files={"file": ("healthinc.pdf", file, "application/pdf")})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # self.assertEqual("hola", data["database_data"])
        self.assertEqual(data["database_data"]["Company Name"], "HealthInc")
        
        self.assertGreater(len(data["discrepancies"]), 0)

    def test_upload_nonexistent_pdf(self):
        """
        Test uploading a nonexistent PDF and expect a 404 response.
        """
        response = self.client.post("/upload_pdf/", files={"file": ("nonexistent.pdf", b"fake content", "application/pdf")})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "File not found"})


if __name__ == '__main__':
    unittest.main()
