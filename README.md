# adjutant

`adjutant` is a package for managing ML experiments over Discord.

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

By providing a `run_experiment_fn` constructor argument, `adjutant` will be able to respond to user requests on Discord to run a new experiment. By default, `adjutant` will execute `run_experiment_fn` in a subprocess so that it can still respond to new requests. `run_experiment_fn` may also request another entity, e.g. Kubernetes, to initiate the experiment on its behalf rather than actually running the experiment itself.

```python
from adjutant import Adjutant


def run_experiment_fn(hyperparams: dict[str, Any]) -> None:
    """Runs a new experiment with the given hyperparameters.
    
    :param hyperparams: The hyperparameters to use for the experiment.
    """
    src

client = Adjutant('my-wandb-entity',
                  'my-wandb-project-title',
                  run_experiment_fn=run_experiment_fn)
client.run('my-discord-token')
```
