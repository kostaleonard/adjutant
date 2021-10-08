"""Runs the adjutant client for the MNIST example."""

import os
import logging
# TODO these imports will probably need to change if someone has pip installed adjutant
from adjutant.adjutant_client import Adjutant
from examples.mnist.mnist_model import WANDB_PROJECT_TITLE

WANDB_ENTITY = 'kostaleonard'
DISCORD_TOKEN_ENVIRONMENT_VAR = 'DISCORD_ADJ_TOKEN'


# TODO this should be in the model file
def run_experiment(hyperparams: dict) -> None:
    """Trains a new model with the given hyperparameters.

    :param hyperparams: The hyperparameters to use in model creation and
        training.
    """
    # TODO actually run experiment.
    import time
    print('Simulating a long running experiment')
    time.sleep(20)
    print('Experiment complete')


def main() -> None:
    """Runs the program."""
    logging.basicConfig(level=logging.INFO)
    adj = Adjutant(WANDB_ENTITY,
                   WANDB_PROJECT_TITLE,
                   run_experiment_fn=run_experiment)
    adj.run(os.environ[DISCORD_TOKEN_ENVIRONMENT_VAR])


if __name__ == '__main__':
    main()
