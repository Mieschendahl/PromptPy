from typing import Optional

seperator = ":"
stop = "(end)"

class Option:
    """Represents an option that the LLM can choose."""
    
    def __init__(self, label: str, condition: str, action: Optional[str] = None, effect: Optional[str] = None):
        """Option constructor.

        Args:
            label: The label with which the LLM can select this option.
            condition: The condition in which the LLM should choose this option.
            action: The action that the LLM should do if this option is choosen.
            effect: The effects that the LLM should expect by performing the given action.
        """
        self.label = label
        self.condition = condition
        self.action = action
        self.effect = effect

    def describe(self) -> str:
        """Describes to the LLM when to use this option, how to use it, and if possible, what will happen if it uses it.
        
        Returns:
            option_description: The description.
        """
        message = f"{self.condition}"
        i = 1

        message += f"\n{i}. You will write \"{self.label + seperator}\""
        i += 1

        if self.action is not None:
            message += f"\n{i}. {self.action}"
            i += 1
        
        message += f"\n{i}. You will write \"{stop}\""
        i += 1
            
        if self.effect is not None:
            message += f"\n{i}. {self.effect}"
            i += 1

        return message