from typing import Optional, Any
from promptpy.utils import log, random_str, pad
from promptpy.model import get_model, Message
from promptpy.option import stop, seperator, Option

_allow_injection: bool = False

def set_allow_injection(allow_injection: bool) -> None:
    """Set whether the user can manually inject a prompt before the LLM before can respond."""
    global _allow_injection
    _allow_injection = allow_injection

def get_allow_injection() -> bool:
    return _allow_injection

class ChoiceError(Exception):
    """Costum exception for LLM option selection errors."""

class Prompter:
    """A class for interacting with an LLM."""
    _last_id: Optional[str] = None

    def __init__(self, messages: Optional[list[Message]] = None):
        """
        Args:
            messages: Messages from a previous conversation.
        """
        self.messages = [] if messages is None else messages
        self._id = random_str(length=10, digits=True).upper()  # id for distinguishing prompters
    
    def copy(self) -> "Prompter":
        return Prompter(self.messages)

    def log_message(self, *messages: Message) -> None:
        """Logs the given messages, if the global verbose value is set to True.
        
        Args:
            messages: The messages that should be logged.
        """
        if Prompter._last_id != self._id:  # Visually marks the beginning of the prompter
            Prompter._last_id = self._id
            log(f"PROMPTER ID: {self._id}",)
            log()
        for message in messages:
            log(message.role.upper() + ":")
            log(pad(message.content, padding=" # "))
            log()

    def add_message(self, *messages: Message) -> "Prompter":
        """Adds multiple messages to the conversation.

        Args:
            messages: The messages that should be added.
        """
        for message in messages:
            self.messages.append(message)
            self.log_message(self.messages[-1])
        return self
    
    def add_prompt(self, *messages: str, role="user") -> "Prompter":
        """Adds multiple messages to the conversation.

        Args:
            messages: The contents of messages that should be added.
            role: The role that the messages should have.
                The default value is "user".
        """
        return self.add_message(*[Message(message, role) for message in messages])

    def add_response(self, stop: Optional[str] = None) -> "Prompter":
        """Adds a response from the LLM, based on the current conversation.
        The user can manually inject a prompt before the LLM response is generated, if allow_injection is set to true.

        Args:
            stop: Stop sequence for which the LLM should stop the response.
        """
        if _allow_injection:
            prompt = input("INJECTION (↵: continue, x: exit): ")
            print()
            if prompt == "x":
                exit(0)
            if prompt != "":
                self.add_prompt(prompt)
        response = get_model().get_response(self.messages, stop).strip()
        self.add_prompt(response, role="assistant")
        return self

    def get_response(self, stop: Optional[str] = None) -> str | Any:
        """Like add_response but returns the 

        Args:
            stop: Stop sequence for which the LLM should stop the response.
        """
        self.add_response(stop=stop)
        return self.messages[-1].content

    def get_choice(self, *options: Option, role="developer") -> tuple[str, Any]:
        """Gets a choice from an LLM and returns the label of the option that was chosen as well as any
        data which the LLM was instructed to generate if this option was chosen.
        
        Args:
            options: A list of options that the LLM can choose from.
            role: The role that the choice instructions should have.
                The default value is "developer".
        """
        description = "\n\n".join(option.describe() for option in options)
        self.add_prompt(f"Use one of the following options:\n\n{description}", role=role)
        response = self.get_response(stop=stop)
        if seperator not in response:
            raise ChoiceError(f"The model did not adhere to the selection format: \"{response}\"")
        label, data = map(str.strip, response.split(seperator, 1))
        if label not in {option.label for option in options}:
            raise ChoiceError(f"The model made an invalid choice: \"{label}\"")
        return label, data