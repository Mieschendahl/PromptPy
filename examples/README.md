# PromptPy Examples

This directory contains examples (`example_XX.py`) that demonstrate how *PromptPy* can be used.

All of the examples use *ChatGPT* as the LLM implementation, although this can be changed by importing your own LLM implementation into the examples and removing the imports from `gpt.py`.

## Setup

Manual setup:
1. Run `pip install openai` to install the `openai` library
2. Run `pip install \path\to\this\project` to install the `promptpy` library <!-- -e for quick reloading -->
3. Run `export OPENAI_API_KEY=<your_api_key>` with a valid API key from OpenAI
4. Run `python3 example_XX.py`

Docker setup:
 1. Run `python3 docker.py` to build and run the docker container
 2. Run `export OPENAI_API_KEY=<your_api_key>` with a valid API key from OpenAI
 3. Run `python3 example_XX.py`