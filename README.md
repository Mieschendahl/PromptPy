# PromptPy

*PromptPy* is a python library that makes prompting LLMs easy.

```python
response = Prompter()\
    .add_prompt("Translate any user input into german", role="developer")\
    .add_prompt("Hello World!", role="user")\
    .get_response()  # LLM's response
print(response)  # prints "Hallo Welt!"
```

## Features

*PromptPy's* main features are:

* **Modular:** Use any LLM implementation.
* **Cheap & Fast:** Cache LLM responses.
* **Powerful:** Let the LLM generate conditional responses.
* **Transparent:** Log conversations in an easy to read format.

Let us look at some examples.

### Modular

`promptpy` exposes the abstract `Model` class as an interface to your costum LLM implementation.

```python
gpt_4o: Model = GPT(model="gpt-4o")  # from examples/gpt.py
set_model(gpt_4o)  # ChatGPT 4o is now globally set
```

### Cheap & Fast

The `Model` class will cache LLM responses whenever possible instead of regenerating from scratch.

```python
def translate(message):
    return Prompter()\
        .add_prompt("You are a translator", role="developer")\
        .add_prompt("Return the user message in german and do nothing else", role="developer")\
        .add_prompt(message)\
        .get_response()

print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (generated)
print(f"'Hello' in german is '{translate("Hello")}'")  # prints "Hallo" (cached)
clear_cache()  # clears cache
```

### Powerful

Use the `Option` class to make the next response of the LLM depend on the current situation.
```python
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
    if label == "name":
        print(f"Hello '{response}'!")
        break
```

### Transparent

Create readable conversation logs for debugging and interactive prompting.

```python
logs = open("logs.txt", "w")
set_log_file(logs)

question = input("Any english questions? ")
response = Prompter()\
    .add_prompt("You are an english teacher", role="developer")\
    .add_prompt(question)\
    .get_response()
print(response)
```
Contents of `logs.txt`
```
PROMPTER ID: T58DOQSVN5

DEVELOPER:
 # You are an english teacher

USER:
 # What is a group of elephants called?

ASSISTANT:
 # A group of elephants is called a "herd."
```

## Setup

Using *PromptPy* requires 3 steps 

1. Run `pip install \path\to\this\project` to install the `promptpy` library. <!-- -e for quick reloading -->
2. Implement the `Model` class and set the global model.
3. Import `promptpy` in your python code and use it.

The  `examples` directory demonstrates common use cases.