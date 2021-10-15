# MNIST

## Files

* [`mnist_adjutant.py`](mnist_adjutant.py): Runs the adjutant Discord client. When run, the script will post to Discord to notify the user of a successful connection.
* [`mnist_model.py`](mnist_model.py): Trains a new machine learning model on the MNIST dataset, syncing with WandB. Takes at most 1 argument: either a JSON-formatted string representing the hyperparameters, or nothing for the default hyperparameters.
* [`run_experiment.sh`](run_experiment.sh): Runs `mnist_model.py` with the given hyperparameters. Takes at most 1 argument in the same format as `mnist_model.py`. This script is provided to the adjutant client on creation (see `mnist_adjutant.py`).

## Usage

### Discord and WandB profile configuration

First, make the following edits to `mnist_adjutant.py`:

* Change `WANDB_ENTITY = 'kostaleonard'` to `WANDB_ENTITY = '<my-wandb-entity>'`. Remember that your WandB entity is your username.
* Change `DISCORD_TOKEN_ENVIRONMENT_VAR = 'DISCORD_ADJ_TOKEN'` to the name of the environment variable containing your Discord bot's API token. Alternatively, you can paste your token directly into the line `adj.run(os.environ[DISCORD_TOKEN_ENVIRONMENT_VAR])` with `adj.run('<my-token>')`. Just be careful that your token doesn't end up in your version control if you paste it directly in the code.

Second, make the following edits to `mnist_model.py`:

* Change `WANDB_PROJECT_TITLE = 'mnist'` to `WANDB_PROJECT_TITLE = '<my-wandb-project-title>'`.

### Running

Now that you have completed configuration for your WandB and Discord profiles, run the `adjutant` client.

```bash
python mnist_adjutant.py
```

You will see it log in to Discord. It is now waiting for new experiments to appear in WandB. You can initiate one with the training script.

```bash
python mnist_model.py
```

When your run finishes, you'll see `adjutant` post summary statistics and a link to the run on [wandb.ai](https://wandb.ai).
