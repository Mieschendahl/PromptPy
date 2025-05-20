# PromptPy Examples

⚠️ **Warning:** Some of the examples allow the LLM to run arbitrary **bash** and **python** code, so please be careful and make sure to only run the examples in a **secure environment**!

## Content

This directory contains examples that demonstrate how *PromptPy* can be used.

* `example_basics.py`: Presents the basic functionality of the `promptpy` library.
* `example_shell.py`: Shows how to let the LLM conditionally use tools, in this case a shell tool.
* `example_implementer.py`: Shows how to implement an automatic python function code generator for easy to implement python functions.

All of the examples use ChatGPT as the LLM implementation, although this can be changed by providing and setting your own LLM implementation.

## Setup

If you want to setup everything manually using the ChatGPT LLM implementation:
1. Run `pip install openai` to install the `openai` library.
2. Run `export OPENAI_API_KEY=<your_api_key>` with a valid API key from OpenAI.
3. Run `pip install \path\to\this\project` to install the `promptpy` library. <!-- -e for quick reloading -->

Alternatively, we provide a docker container that handles the necessary installation steps for you and provides a minimum level of security. Run `python3 docker.py` to build and run the docker container.