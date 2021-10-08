"""Runs the adjutant client for the MNIST example."""

import os
import logging
# TODO these imports will probably need to change if someone has pip installed adjutant
from adjutant.adjutant_client import Adjutant
from mnist_model import WANDB_PROJECT_TITLE

WANDB_ENTITY = 'kostaleonard'
DISCORD_TOKEN_ENVIRONMENT_VAR = 'DISCORD_ADJ_TOKEN'
RUN_EXPERIMENT_SCRIPT = './run_experiment.sh'


def main() -> None:
    """Runs the program."""
    logging.basicConfig(level=logging.INFO)
    adj = Adjutant(WANDB_ENTITY,
                   WANDB_PROJECT_TITLE,
                   run_experiment_script=RUN_EXPERIMENT_SCRIPT)
    adj.run(os.environ[DISCORD_TOKEN_ENVIRONMENT_VAR])


if __name__ == '__main__':
    main()
