from gpt import model
from promptpy import Prompter

def translate(message: str) -> str:
    return Prompter(model)\
        .add_message("You are a translator", role="developer")\
        .add_message("Return the user message in german and do nothing else", role="developer")\
        .add_message(message)\
        .get_response()

print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (generated)
print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (cached)5