import os
from typing import Optional, Any
from openai import OpenAI
from promptpy import Message, Model

api_key = os.getenv("OPENAI_API_KEY", None)
client = OpenAI(api_key=api_key)

class GPT(Model):
    """ChatGPT implementation of an LLM."""
    
    def __init__(self, **kwargs: Any):
        """
        Args:
            kwargs: Configuration that is passed to OpenAI's chat completion creation method.
        """
        self.kwargs = kwargs

    def get_completion(self, messages: list[Message], stop: Optional[str] = None) -> Optional[str]:
        openai_messages = [{"role": message.role, "content": message.content} for message in messages]
        return client.chat.completions.create(
                messages=openai_messages,  # type:ignore
                stop=stop,
                **self.kwargs
            ).choices[0].message.content

    def __repr__(self) -> str:
        kwargs = ", ".join(sorted(f"{key}={repr(value)}" for key, value in self.kwargs.items()))
        return f"GPT({kwargs})"

gpt_4o = GPT(model="gpt-4o", temperature=0)
gpt_4o_mini = GPT(model="gpt-4o-mini", temperature=0)