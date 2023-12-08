# Flux Player

[Background](https://www.adamgrant.info/flux-player)

## How to use Flux for your custom AI application

The application must have the ability to run code such as OpenAI's custom GPT feature.
The rest is using the prompt and making a catridge.

### Use the Prompt

See `prompt.md` and copy as is.

### Make a cartridge

A cartridge is a python file named `cartridge.py` that contains the following structure:

```python
cartridge = {
  "START": {
    "prompt": "(The prompt)",
    "events": []
  },
}
```

It must have a variable called `cartridge` and a state called `START`. This defines the first prompt the LLM will act upon after the user makes contact.

The `events` array is what determines what transitions are possible from the current state. Each event is an object with the following structure:

```python
{
  "method": "(Name of transition)",
  "target": "(Name of the state this transition will go to)",
  "if_the_user": "(A description of what the user should say to trigger this transition assuming the sentence starts with 'if the user...')"
}
```

See the examples folder in this repo to get ideas.