import unittest

from app.chatbot import build_account_breakdown, is_percentage_distribution_request
from app.config import settings


class ChatbotChartTests(unittest.TestCase):
    def test_detects_percentage_distribution_request(self):
        question = "What is the percentage distribution of debits, credits, fees, and penalties in my financial account?"
        self.assertTrue(is_percentage_distribution_request(question))

    def test_builds_chart_response_for_account_breakdown(self):
        response = build_account_breakdown(
            "Show the percentage breakdown of debits, credits, fees and penalties in my account."
        )

        self.assertIsNotNone(response)
        self.assertEqual(response["category"], "account_breakdown")
        self.assertEqual(response["source_url"], "https://www.iob.bank.in/en/")
        self.assertEqual(response["chart"]["items"][0]["label"], "Debits")
        self.assertEqual(response["chart"]["items"][0]["value"], 42)

    def test_business_loan_answer_uses_official_iob_information(self):
        from app.chatbot import find_best_answer

        response = find_best_answer("What is an MSME loan?")
        self.assertIsNotNone(response)
        self.assertIn("MSME", response["answer"])
        self.assertIn("https://www.iob.bank.in/en/msme", response["source_url"])

    def test_fee_question_explains_common_account_charges(self):
        from app.chatbot import find_best_answer

        response = find_best_answer("Why am I paying fees and penalties on my account?")
        self.assertIsNotNone(response)
        self.assertIn("fees", response["answer"].lower())
        self.assertIn("penalties", response["answer"].lower())

    def test_account_breakdown_answer_includes_example_and_formula(self):
        from app.chatbot import find_best_answer

        response = find_best_answer("Explain my account breakdown.")
        self.assertIsNotNone(response)
        self.assertIn("opening balance", response["answer"].lower())
        self.assertIn("closing balance", response["answer"].lower())
        self.assertIn("authorised", response["answer"].lower())

    def test_interest_rate_question_asks_for_scheme_when_context_is_unclear(self):
        from app.chatbot import find_best_answer

        response = find_best_answer("What is the interest rate?")
        self.assertIsNotNone(response)
        self.assertEqual(response["category"], "clarification_required")
        self.assertIn("Which loan scheme", response["answer"])

    def test_allows_vite_dev_ports_for_cors(self):
        self.assertIn("http://localhost:5176", settings.CORS_ORIGINS)


if __name__ == "__main__":
    unittest.main()
