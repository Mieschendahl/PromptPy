def clean_code(code: str, last: bool = True) -> str:
    """Removes delimiteres such as ```python ... ``` from a code snippet.
    
    Args:
        code: The code snippet to clean.
        last: If the last or the first code snippet should be extracted.
    
    Returns:
        cleaned: The cleaned code.
    """
    lines = code.split("\n")
    lines = lines[::-1] if last else lines
    for i, line in enumerate(lines):
        if "```" in line:
            lines = lines[i+1:]
            break
    for i, line in enumerate(lines):
        if "```" in line:
            lines = lines[:i]
            break
    lines = lines[::-1] if last else lines
    return "\n".join(lines)