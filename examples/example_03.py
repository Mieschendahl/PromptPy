from gpt import model
from promptpy import Prompter

with open("logs.txt", "w") as log_file:
    question = input("Any english questions? ")
    response = Prompter(model, log_file=log_file, id="Teacher")\
        .add_message("You are an english teacher", role="developer")\
        .add_message(question)\
        .get_response()
    print(response)