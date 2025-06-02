from gpt import model
from promptpy import Prompter

response = Prompter(model)\
    .add_message("Translate any user input into german", role="developer")\
    .add_message("Hello World!", role="user")\
    .get_response()  # get LLM's response
print(response)  # prints "Hallo Welt!"