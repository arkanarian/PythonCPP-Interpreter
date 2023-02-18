ERROR_CLASSIFICATION = "Syntax Error: "
STANDARD_ERROR = "Invalid construction"


def NOT_EXPECTED_TOKEN(expected_token: str, current_token: str, line: int = -1, column: int = -1):
    return f"Expected token {expected_token} but found {current_token}:{line}:{column}"
