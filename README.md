# Adjutant

Adjutant is a package for managing ML experiments over Discord in conjunction with WandB.

## Installation

```bash
pip install adjutant-discord
```

### Discord bot creation

To allow adjutant to post to discord as a bot, first follow [these instructions](https://discordpy.readthedocs.io/en/stable/discord.html) for creating a Discord bot and adding it to your Server. You then create an `Adjutant` object with your bot token.

**Note: Be careful not to share your bot's token. Consider storing it in an environment variable or file that is not checked in to version control.**

### WandB setup

Adjutant is designed to work with WandB for ML experiment tracking. Create a WandB account at [wandb.ai](https://wandb.ai/).

Wherever you plan to run Adjutant, make sure you are either logged in to your WandB account, or have an API key populated in the `WANDB_API_KEY` environment variable. More information is available in [the WandB docs](https://docs.wandb.ai/guides/track/public-api-guide).

## Adjutant commands

Once Adjutant is running and has connected to Discord (see [the Basic Adjutant example below](#basic-adjutant) to get started), you can send it the following commands by posting in the chat.

| Command | Effect | Example |
| - | - | - |
| $hello | Get a response from the bot | $hello |
| $experiment {hyperparams} | Launch a new experiment with the given hyperparameters (must provide `run_experiment_script` in constructor) | $experiment {"epochs": 10, "batch_size": 32} |

## Quickstart

For more advanced examples, please see [examples](examples), starting with [the MNIST example](examples/mnist).

### Basic Adjutant

The most basic formulation of Adjutant provides updates on WandB experiments under the given project name. Your WandB entity name is your account name, and the project title is the name of the project you have created (or will create) to store experiments.

```python
from adjutant import Adjutant
client = Adjutant('my-wandb-entity', 'my-wandb-project-title')
client.run('my-discord-token')
```

When you run the script, you will see your bot post to your Discord chat with information on the WandB runs it found for the project.

### Adjutant with experiment launching

By providing a `run_experiment_script` constructor argument, Adjutant will be able to respond to user requests on Discord to run a new experiment. Adjutant will execute `run_experiment_script` in a subprocess so that it can still respond to new requests. `run_experiment_script` may also request another entity, e.g. Kubernetes, to initiate the experiment on its behalf rather than actually running the experiment itself.


First, here are the contents of `run_experiment.sh`, which takes a JSON-formatted string as its command line argument. Adjutant will pass this script the hyperparameters with which to run the experiment. In this script, `train_model.py` trains a new model with the supplied hyperparameters. For an example of what the training script might look like, see [the MNIST example](examples/mnist).

```bash
#!/bin/bash
python train_model.py "$1"
```

Now we can create a client that references `run_experiment.sh`.

```python
from adjutant import Adjutant
client = Adjutant('my-wandb-entity',
                  'my-wandb-project-title',
                  run_experiment_script='run_experiment.sh')
client.run('my-discord-token')
```
