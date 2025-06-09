import re

def clean_code(code: str) -> str:
    """Removes delimiteres such as ```python ... ``` from a code snippet.
    
    Args:
        code: The code snippet to clean.
    
    Returns:
        cleaned: The cleaned code.
    """
    match = re.search(r'```(?:[a-zA-Z]*\n)?(.*)```', code, re.DOTALL)

    if not match:
        return code  # No code block found

    return match.group(1).strip()