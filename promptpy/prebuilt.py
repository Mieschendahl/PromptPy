def clean_code(code: str) -> str:
    """Removes delimiteres such as ```python ... ``` from a code snippet.
    
    Args:
        code: The code snippet to clean.
    
    Returns:
        cleaned: The cleaned code.
    """
    lines = code.split("\n")
    start = None
    for i, line in enumerate(lines):
        if "```" in line:
            if start is not None:
                return "\n".join(lines[start+1:i])
            start = i
    if start is not None:
        lines = lines[:start] + lines[start+1:]
    return "\n".join(lines)