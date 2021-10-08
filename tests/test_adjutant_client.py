"""Tests adjutant_client.py."""

import time
from discord.channel import TextChannel
from adjutant import adjutant_client
from examples.mnist.mnist_model import WANDB_PROJECT_TITLE
from tests.apis import is_discord_config_present, is_wandb_config_present

WANDB_ENTITY = 'kostaleonard'
DISCORD_TOKEN_ENVIRONMENT_VAR = 'DISCORD_ADJ_TOKEN'
SETUP_TIMEOUT_SECONDS = 5


def test_adjutant_init_sets_public_fields() -> None:
    """Tests that Adjutant.__init__ sets the object's fields correctly."""
    adj = adjutant_client.Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    assert adj.channel_name


def test_adjutant_get_channel_finds_discord_channel() -> None:
    """Tests that Adjutant._get_channel finds a valid channel on Discord."""
    # TODO slowtest?
    if not is_discord_config_present():
        return
    adj = adjutant_client.Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    seconds_waited = 0
    while not adj.is_ready() and seconds_waited < SETUP_TIMEOUT_SECONDS:
        time.sleep(1)
        seconds_waited += 1
    assert adj.is_ready()
    assert isinstance(adj.channel, TextChannel)
