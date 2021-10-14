# adjutant

`adjutant` is a package for managing ML experiments over Discord in conjunction with WandB.

## Installation

```bash
pip install adjutant
```

### Discord bot creation

To allow `adjutant` to post to discord as a bot, first follow [these instructions](https://discordpy.readthedocs.io/en/stable/discord.html) for creating a Discord bot and adding it to your Server. You then create an `Adjutant` object with your bot token.

**Note: Be careful not to share your bot's token. Consider storing it in an environment variable or file that is not checked in to version control.**

### WandB setup

`adjutant` is designed to work with WandB for ML experiment tracking. Create a WandB account at [wandb.ai](https://wandb.ai/).

Wherever you plan to run `adjutant`, make sure you are either logged in to your WandB account, or have an API key populated in the `WAND_API_KEY` environment variable. More information is available in [the WandB docs](https://docs.wandb.ai/guides/track/public-api-guide).

## Examples

For more advanced examples, please see [examples](examples), starting with [the MNIST example](examples/mnist).

### Basic `adjutant`

The most basic formulation of `adjutant` provides updates on WandB experiments under the given project name. Your WandB entity name is your account name, and the project title is the name of the project you have created (or will create) to store experiments.

```python
from adjutant import Adjutant
client = Adjutant('my-wandb-entity', 'my-wandb-project-title')
client.run('my-discord-token')
```

### `adjutant` with experiment launching

By providing a `run_experiment_script` constructor argument, `adjutant` will be able to respond to user requests on Discord to run a new experiment. `adjutant` will execute `run_experiment_script` in a subprocess so that it can still respond to new requests. `run_experiment_script` may also request another entity, e.g. Kubernetes, to initiate the experiment on its behalf rather than actually running the experiment itself.


First, here are the contents of `run_experiment.sh`, which takes a JSON-formatted string as its command line argument. `adjutant` will pass this script the hyperparameters with which to run the experiment. In this script, `train_model.py` trains a new model with the supplied hyperparameters. For an example of what the training script might look like, see [the mnist example](examples/mnist).

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
