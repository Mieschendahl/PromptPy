from gpt import gpt_4o_mini
from promptpy import set_model, set_log_file, set_allow_injection, set_use_cache, set_cache_tag, Prompter, Option

set_model(gpt_4o_mini)  # required
set_log_file(None)  # optional (default: sys.stdout)
set_allow_injection(False)  # optional (default: False)
set_use_cache(True)  # optional (default: True)
set_cache_tag("DEMO-01")  # optional (default: #DEFAULT#)

### EXAMPLE 01 ###

def translate(message):
    return Prompter()\
        .add_prompt("You are a translator", role="developer")\
        .add_prompt("Return the user message in german and do nothing else", role="developer")\
        .add_prompt(message)\
        .get_response()

print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (generated)
print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (cached)
print()
    
### EXAMPLE 02 ###

while True:
    prompt = input("Hi, who are you? ")
    label, response = Prompter()\
        .add_prompt(prompt)\
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

### EXAMPLE 03 ###

logs = open("logs.txt", "w")
set_log_file(logs)

question = input("Any english questions? ")
response = Prompter()\
    .add_prompt("You are an english teacher", role="developer")\
    .add_prompt(question)\
    .get_response()
print(response)