# Flux Player

[Background](https://www.adamgrant.info/flux-player)

## How to use Flux for your custom AI application

The application must have the ability to run code such as OpenAI's custom GPT feature.
The rest is using the prompt and making a catridge.

### Use the Prompt

See `prompt.md` and copy as is.

### Make a cartridge

A cartridge is a python file named `cartridge.yaml` that contains the following structure:

```yaml
START:
  role: (The role of the AI)
  prompt: (The prompt)
  events: (A list of events. See the next section)
```

Note the `START` state is **required** and only the `START` state has the `role` property, which is maintained throughout the state transitions.

`prompt` defines the prompt the LLM will act upon after the user enters the state.

The `events` array is what determines what transitions are possible from the current state. Each event is an object with the following structure:

```yaml
- method: (Name of transition)
  target: (Name of the state this transition will go to)
  if_the_user: (A description of what the user should say to trigger this transition assuming the sentence starts with 'if the user...')
```

See the examples folder in this repo to get ideas.