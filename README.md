# Flux Player

[Background](https://www.adamgrant.info/flux-player)

## How to use Flux for your custom AI application

The application must have the ability to run code such as OpenAI's custom GPT feature.
The rest is using the prompt and making a catridge.

### Use the Prompt

See `prompt.md` and copy as is.

### Make a cartridge

A cartridge is a YAML or Python file describing the state transitions and data storage.

### YAML

The file should be named `cartridge.yaml` and contain the following structure:

```yaml
START:
  role: (The role of the AI)
  prompt: (The prompt)
  events: (A list of events)
```

### Python

In python, the syntax is different but the structure is the same. The key is to assign this to the variable `cartridge`

```python
cartridge = {
  'START': {
    'role': (The role of the AI),
    'prompt': (The prompt, either a string or a function that takes the data dict as an argument),
    'events': (A list of events. See the next section)
  }
}
```

You can also "print" your Python cartridge to a YAML file using the `-x` flag:

```bash
flux -c cartridge.py -x
```

which will create a `cartridge.yaml` file in the same directory as `cartridge.py`.
This is particularly useful if you want to divide up your cartridge into many project files yet still have a single portable file to distribute.

The advantage to using Python over YAML is the flexibility of the language. You can use variables and functions to make the cartridge more dynamic. This is also important when doing interesting manipulations with `data` between states in a way that can't be done in YAML. This is done using the `before` function.

Note the `START` state is **required** and only the `START` state has the `role` property, which is maintained throughout the state transitions.

`prompt` defines the prompt the LLM will act upon after the user enters the state.

### Events

The `events` array is what determines what transitions are possible from the current state. Each event is an object with the following structure:

```yaml
- target: (Name of the state this transition will go to)
  if_the_user: (A description of what the user should say to trigger this transition assuming the sentence starts with 'if the user...')
```

See the examples folder in this repo to get ideas.

# Running

Once you've created your cartridge.py or cartridge.yaml here's how you can run it.

## Locally

Get the latest `flux` distributable from [the releases](https://github.com/adamjgrant/fluxplayer/tags)

Then in the same directory as the cartridge, run:

```bash
./flux
```

Alternatively, use `flux.py` from the base level of this repo with the `lib` directory 

```bash
$ ls
cartridge.py   flux   flux.py   lib
# OR
$ ls
cartridge.yaml   flux   flux.py   lib
```

and run

```bash
python flux.py
```

in the same directory.

## In ChatGPT

For running on OpenAI's Custom GPTs, get the `flux` binary from [the releases page](https://github.com/adamjgrant/fluxplayer/releases) and upload it with your cartridge to your custom GPT.

`prompt.md` is the prompt you'll want to use for the GPT. Note that cartridge.yaml or .python must be at the same directory as flux.

**Do not change from prompt.md** to customize for your GPT's needs! Remember that your cartridge is what makes your GPT unique. Every Flux-powered GPT should have exactly the same prompt. This prompt has been carefully tested over many iterations to "behave" across a variety of seeds, so you'll want to stick with this one.

You can also specify a custom cartridge path with `-c`

```bash
flux -c /path/to/cartridge
```

Use `-s=<STATE>` and `-t=<transition>` to define the current state and transition respectively. This will otherwise default to the `START` state.

# Testing

```bash
python -m unittest test.py
```


## Building from source

First, make sure you have docker installed and running. Then run:

```bash
./build.sh
```

you will also need an .env file with the version like this:
if it's the first time you're running this, you may need to run `poetry install` too.

```
VERSION=2.0.10
```

The file you'll need will be in dist/linux/flux