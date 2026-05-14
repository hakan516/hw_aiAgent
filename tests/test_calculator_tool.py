import unittest

from ai_study_agent.tools import CalculatorTool


class CalculatorToolTest(unittest.TestCase):
    def test_calculator_evaluates_arithmetic_expression(self):
        result = CalculatorTool().run("2 + 3 * 4")

        self.assertTrue(result.success)
        self.assertEqual(result.data, 14)

    def test_calculator_rejects_unsafe_expression(self):
        result = CalculatorTool().run("__import__('os').system('echo bad')")

        self.assertFalse(result.success)
        self.assertIsNone(result.data)
        self.assertIn("unsupported", result.message)

    def test_calculator_reports_zero_division(self):
        result = CalculatorTool().run("10 / 0")

        self.assertFalse(result.success)
        self.assertIn("division", result.message.lower())


if __name__ == "__main__":
    unittest.main()
