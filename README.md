# PromptPy

*PromptPy* is a python library that makes prompting LLMs easy.

```python
response = Prompter(model)\
    .add_prompt("Translate any user input into german", role="developer")\
    .add_prompt("Hello World!", role="user")\
    .get_response()  # LLM's response
print(response)  # prints "Hallo Welt!"
```

## Features

*PromptPy's* main features are:

* **Modular:** Use any LLM implementation
* **Cheap & Fast:** Cache LLM responses
* **Powerful:** Let the LLM generate conditional responses
* **Transparent:** Log conversations in an easy to read format

Let us look at some examples.

### Modular

`promptpy` provides the abstract `Model` class as an interface to your custom LLM implementation.
See `examples/gpt.py` for an example implementation for *ChatGPT*.

### Cheap & Fast

The `Model` class will cache LLM responses whenever possible instead of regenerating from scratch.

```python
def translate(message):
    return Prompter(model)\
        .add_message("You are a translator", role="developer")\
        .add_message("Return the user message in german and do nothing else", role="developer")\
        .add_message(message)\
        .get_response()

print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (generated)
print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (cached)
```

### Powerful

Use the `Option` class to make the next response of the LLM depend on the current situation.
```python
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

### Transparent

Create readable conversation logs for debugging and interactive prompting.

```python
with open("logs.txt", "w") as log_file:
    question = input("Any english questions? ")
    response = Prompter(model, log_file=log_file, id="Teacher")\
        .add_message("You are an english teacher", role="developer")\
        .add_message(question)\
        .get_response()
    print(response)
```
Contents of `logs.txt`
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

Using *PromptPy* requires three steps:

1. Run `pip install \path\to\this\project` to install the `promptpy` library <!-- -e for quick reloading -->
2. Provide a `Model` class implementation (e.g. `example/gpt.py`)
3. Import `promptpy` in your python code

The `examples` directory demonstrates this process.