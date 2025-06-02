# PromptPy

*PromptPy* is a Python library that makes prompting LLMs easy.

```python
# examples/example_hello_world.py
response = Prompter(model)\
    .add_message("Translate any user input into german", role="developer")\
    .add_message("Hello World!", role="user")\
    .get_response()  # get LLM's response
print(response)  # prints "Hallo Welt!"
```

## Features

### Modular

*PromptPy* provides the abstract `Model` class as an interface to your custom LLM implementation.
See `examples/gpt.py` for an example implementation for *ChatGPT*.

### Cheap & Fast

The `Model` class will cache LLM responses whenever possible, which saves the time and money needed for regenerating responses from scratch.

```python
# examples/example_translate.py
def translate(message: str) -> str:
    return Prompter(model)\
        .add_message("You are a translator", role="developer")\
        .add_message("Return the user message in german and do nothing else", role="developer")\
        .add_message(message)\
        .get_response()

print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (generated)
print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (cached)
```

### Powerful

You can use the `Option` class to make the next response of the LLM depend on the current situation, giving you a powerful way to control the flow of your program and let the LLM use tools.
```python
# examples/example_user_name.py
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
```

### Debugabble

You can easily create readable conversation logs for debugging.

```python
# examples/example_english_teacher.py
with open("logs.txt", "w") as log_file:
    question = input("Any english questions? ")
    response = Prompter(model, log_file=log_file, id="Teacher")\
        .add_message("You are an english teacher", role="developer")\
        .add_message(question)\
        .get_response()
    print(response)
```
Contents of `logs.txt`:
```
PROMPTER ID: Teacher

DEVELOPER:
 # You are an english teacher

USER:
 # What is a group of elephants called?

ASSISTANT:
 # A group of elephants is called a "herd."
```

## Setup

- First install *PromptPy*.

    ```bash
    pip install --upgrade git+https://github.com/Mieschendahl/PromptPy.git
    ```

- Then provide a `Model` class implementation (e.g. `examples/gpt.py`).

The `examples` directory contains some examples.