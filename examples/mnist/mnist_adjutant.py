"""Runs the adjutant client for the MNIST example."""

import os
import logging
from adjutant.adjutant_client import Adjutant
from examples.mnist.mnist_model import WANDB_PROJECT_TITLE

WANDB_ENTITY = 'kostaleonard'
DISCORD_TOKEN_ENVIRONMENT_VAR = 'DISCORD_ADJ_TOKEN'


def main() -> None:
    """Runs the program."""
    logging.basicConfig(level=logging.INFO)
    adj = Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    adj.run(os.environ[DISCORD_TOKEN_ENVIRONMENT_VAR])


if __name__ == '__main__':
    main()
