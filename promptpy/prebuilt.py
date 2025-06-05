def clean_code(code: str, last: bool = True) -> str:
    """Removes delimiteres such as ```python ... ``` from a code snippet.
    
    Args:
        code: The code snippet to clean.
    
    Returns:
        cleaned: The cleaned code.
    """
    lines = code.split("\n")
    for i, line in enumerate(lines):
        if "```" in line:
            lines = lines[i+1:]
            break
    for i, line in enumerate(lines):
        if "```" in line:
            lines = lines[:i]
            break
    return "\n".join(lines)