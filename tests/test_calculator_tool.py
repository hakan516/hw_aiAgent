from ai_study_agent.tools import CalculatorTool


def test_calculator_evaluates_arithmetic_expression():
    result = CalculatorTool().run("2 + 3 * 4")

    assert result.success is True
    assert result.data == 14


def test_calculator_rejects_unsafe_expression():
    result = CalculatorTool().run("__import__('os').system('echo bad')")

    assert result.success is False
    assert result.data is None
    assert "unsupported" in result.message


def test_calculator_reports_zero_division():
    result = CalculatorTool().run("10 / 0")

    assert result.success is False
    assert "division" in result.message.lower()
