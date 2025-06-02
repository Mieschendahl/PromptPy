from typing import Callable
import inspect
from gpt import model
from promptpy import Prompter, Option

def halting(function: Callable) -> bool:
    code = inspect.getsource(function)
    label, _ = Prompter(model)\
        .add_message("You are theoretical computer scientist and python expert", role="developer")\
        .add_message(f"Will the following python function return a value when called?\n\n{code}")\
        .add_message(
            "Think step by step about whether it stops or not."
            "\nAnnotate each line of the function with what it does before you come to a conclusion."
        )\
        .add_response()\
        .get_choice(
            Option(
                "will return",  # Label
                "If the function returns a value after enough time has passed",  # Condition
                "Name your guess to which value will be returned"  # Action
            ),
            Option(
                "will not return",  # Label
                "If the function will never return a value",  # Condition
                "Explain why the function will forever continue running"  # Action
            )
        )
    return label == "will return"
    
def func_01() -> int:
    x = 0
    y = 10
    while x < y:
        x += 1
        y += 1
    return x

def func_02() -> int:
    x = 0
    y = 10
    while x < y:
        x += 2
        y += 1
    return x

print(halting(func_01))  # prints False
print(halting(func_02))  # prints True