from django.test import TestCase
from .api import Api

import pandas

# Create you tests here
class APITestCase(TestCase):

    def setUp(self) -> None:
        pass

    def test_unresolved_api_command(self):
        result = Api().resolve_command("unkown_command", None)

        self.assertJSONEqual(
            result.content.decode("utf-8"),
            {"result": False, "error": "Command is not defined!"}
        )