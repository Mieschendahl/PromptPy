from gpt import model
from promptpy import Prompter, Option

while True:
    message = input("Hi, who are you? ")
    label, response = Prompter(model)\
        .add_message("Hi, who are you?", role="assistant")\
        .add_message(message)\
        .get_choice(
            Option(
                "give name",  # Label
                "If the users responded with his name",  # Condition
                "Write his name and nothing else"  # Action
            ),
            Option(
                "no name",  # Label
                "If the users did not respnod with his name"  # Condition
            )
        )
    if label == "give name":
        print(f"Hello '{response}'!")
        print()
        break