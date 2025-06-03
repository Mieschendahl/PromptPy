# Examples

This directory contains examples that demonstrate how *PromptPy* can be used.

All of the examples use *ChatGPT* as the LLM implementation, although this can be changed by importing your own LLM implementation into the examples and replacing the imports from `gpt.py`.

## Setup

1. Install *OpenAI* and *PromptPy*.

    ```bash
    pip install --upgrade openai git+https://github.com/Mieschendahl/PromptPy.git
    ```

2. Set your [OpenAI API Key](https://platform.openai.com/api-keys).

    ```bash
    export OPENAI_API_KEY=<your_api_key>
    ```

3. Run an example.

    ```bash
    python3 example_<example_id>.py
    ```

- Alternatively, you can run the examples in a [Docker](https://www.docker.com/resources/what-container/) container.

    ```bash
    python3 docker.py
    ```