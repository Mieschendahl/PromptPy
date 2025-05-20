class Message:
    """Represents a message in a conversation between a Prompter and an LLM."""
    
    def __init__(self, content: str, role: str = "user"):
        """Message constructor.
        
        Args:
            content: The content of the message.
            role: The role of the message owner (can be "developer", "user", or "assistant")
        """
        assert role in ("developer", "user", "assistant"), "Invalid role was given."
        self.content = content
        self.role = role

    def __str__(self) -> str:
        return f"{self.role.upper()}:\n{self.content}"
    
    def __repr__(self) -> str:
        return f"Message(content={repr(self.content)}, role={repr(self.role)})"