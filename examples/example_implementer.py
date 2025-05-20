import sys
import importlib
import inspect
import traceback
from typing import Callable
from pathlib import Path
from functools import wraps
from gpt import gpt_4o_mini
from promptpy import set_model, set_log_file, set_allow_injection, set_use_cache, set_cache_tag, Prompter, Option
from utils import clean_code

set_model(gpt_4o_mini)  # required
set_log_file(sys.stdout)  # optional (default: sys.stdout)
set_allow_injection(False)  # optional (default: False)
set_use_cache(True)  # optional (default: True)
set_cache_tag("DEMO-01")  # optional (default: #DEFAULT#)

module_name = "__implementation__"
file_path = Path(f"{module_name}.py")

class ImplementationError(Exception):
    pass

def load(code: str, name: str) -> Callable | str:
    """Dynamically loads a python function from a given code piece.
    
    Args:
        code: The code that contains the function definition.
        name: The name of the function.
        
    Returns:
        The function object if the loading process was successful, else an error trace of the
        exception that occurred while loading.
    """

    file_path.write_text(clean_code(code))
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)  # type:ignore
        module = importlib.util.module_from_spec(spec)  # type:ignore
        spec.loader.exec_module(module)
        return getattr(module, name)
    except Exception as e:
        return "".join(traceback.format_exception(type(e), e, e.__traceback__))
    finally:
        if file_path.is_file():
            file_path.unlink()

def implement(function: Callable) -> Callable:
    """A decorator for automatically implementing functions using their doc-strings
    and signatures.
    
    Args:
        function: The function to implement via an LLM.
    """
    name = function.__name__
    signature = f"{name}{inspect.signature(function)}"
    specification = "\n".join(line.strip() for line in function.__doc__.strip().split("\n"))
    
    prompter = Prompter()\
        .add_prompt(
            "You are a python expert who should help the user implement a python function."
            "\nNever use libraries outside of python's standard library!",
            role="developer"
        )\
        .add_prompt(
            f"Please implement the function \"{name}\" for me:"
            f"\nSignature: {signature}"
            f"\nSpecification: {specification}"
        )

    while True:
        choice = prompter\
            .add_prompt("Think step by step about the correct implementation, if one exists.")\
            .add_response()\
            .get_choice(
                Option(
                    "implement",  # label
                    "If you have found an implementation",  # condition
                    "Write your implementation and nothing else, not even examples",  # action
                    "I will give you feedback on whether your implementation is correct" # effect
                ),
                Option(
                    "impossible",  # label
                    "If you have found a reason why the function can not be implemented",  # condition
                    "Write your reason",  # action
                    "I will give you feedback on whether your reasoning is correct"  # effect
                )
            )
        match choice:
            case "impossible", reason:
                raise ImplementationError(
                    f"The LLM determined that the function specification is impossible to implement because: {reason}"
                )
            case "implement", code:
                obj = load(code, name)
                if isinstance(obj, str):
                    prompter.add_prompt(f"Your implementation caused an error:\n{obj}")
                else:
                    return wraps(function)(obj)

@implement
def tribonacci(n: int) -> int:
    """Calculates the n-th entry in the tribonacci sequence, starting with the 0-th entry being 0"""

print("The tribonacci sequence is ", end="")
print(", ".join(str(tribonacci(n)) for n in range(15)))
print()