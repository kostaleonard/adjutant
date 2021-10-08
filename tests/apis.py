"""Contains functions to check the connection to external APIs. These are used
to prevent integration tests from running when there is no connection."""

import os
import pathlib

WANDB_KEY_FILE = os.path.join(str(pathlib.Path.home()), '.netrc')
WANDB_KEY_VAR = 'WANDB_API_KEY'
DISCORD_TOKEN_ENVIRONMENT_VAR = 'DISCORD_ADJ_TOKEN'


def is_wandb_config_present() -> bool:
    """Returns True if wandb configuration files and environment variables are
    present, False otherwise.

    :return: True if wandb configuration files and environment variables are
        present, False otherwise.
    """
    if not os.path.exists(WANDB_KEY_FILE) and WANDB_KEY_VAR not in os.environ:
        # No API key file.
        return False
    with open(WANDB_KEY_FILE, 'r') as infile:
        if 'api.wandb.ai' not in infile.read():
            # No wandb entry found in key file.
            return False
    return True


def is_discord_config_present() -> bool:
    """Returns True if Discord configuration files and environment variables are
    present, False otherwise.

    :return: True if Discord configuration files and environment variables are
        present, False otherwise.
    """
    return DISCORD_TOKEN_ENVIRONMENT_VAR in os.environ
