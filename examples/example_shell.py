from gpt import gpt_4o_mini
from promptpy import set_model, set_log_file, set_allow_injection, set_use_cache, set_cache_tag, Prompter, Option
from utils import clean_code, Shell

set_model(gpt_4o_mini)  # required
set_log_file(open("logs.txt", "w"))  # optional (default: sys.stdout)
set_allow_injection(False)  # optional (default: False)
set_use_cache(True)  # optional (default: True)
set_cache_tag("DEMO-01")  # optional (default: #DEFAULT#)

prompter = Prompter().add_prompt("You are an assistant who will follow the instructions of the user", role="developer")

with Shell() as shell:
    print("Shell assistant:")
    while True:
        message = input("User (x: quit): ")
        if message == "x":
            exit(0)
        choice = prompter\
            .copy()\
            .add_prompt(message)\
            .get_choice(
                Option(
                    "shell",  # label
                    "If the user asks you to perform a shell action",  # condition
                    "Write the appropriate shell command and nothing else",  # action
                    "I will handle the execution of the command for you"  # effect
                ),
                Option(
                    "talk",  # label
                    "In any other case",  # condition
                    "Respond appropriatly to what the user said or asked"  # action
                )
            )
        match choice:
            case "talk", response:
                print(f"Assistant: {response}")
            case "shell", command:
                shell.send(clean_code(command), 60)