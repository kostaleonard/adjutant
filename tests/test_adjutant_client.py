"""Tests adjutant_client.py."""

import time
import pytest
from discord.channel import TextChannel
from adjutant import adjutant_client
from examples.mnist.mnist_model import WANDB_PROJECT_TITLE
from tests.apis import is_discord_config_present, is_wandb_config_present

WANDB_ENTITY = 'kostaleonard'
DISCORD_TOKEN_ENVIRONMENT_VAR = 'DISCORD_ADJ_TOKEN'
SETUP_TIMEOUT_SECONDS = 5
NUM_KNOWN_PROJECT_RUNS = 60


def test_adjutant_init_sets_public_fields() -> None:
    """Tests that Adjutant.__init__ sets the object's fields correctly."""
    adj = adjutant_client.Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    assert adj.channel_name


@pytest.mark.slowtest
def test_adjutant_get_channel_finds_discord_channel() -> None:
    """Tests that Adjutant._get_channel finds a valid channel on Discord."""
    if not is_discord_config_present():
        return
    adj = adjutant_client.Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    seconds_waited = 0
    while not adj.is_ready() and seconds_waited < SETUP_TIMEOUT_SECONDS:
        time.sleep(1)
        seconds_waited += 1
    assert adj.is_ready()
    assert isinstance(adj.channel, TextChannel)


def test_adjutant_get_project_runs_finds_project_runs() -> None:
    """Tests that Adjutant._get_project_runs finds runs from known projects."""
    if not is_wandb_config_present():
        return
    adj = adjutant_client.Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    runs = adj._get_project_runs()
    assert len(runs) >= NUM_KNOWN_PROJECT_RUNS


def test_get_hyperparams_empty_str() -> None:
    """Tests Adjutant._get_hyperparams on the empty string."""
    assert adjutant_client.Adjutant._get_hyperparams('') == {}


def test_get_hyperparams_bad_json() -> None:
    """Tests that Adjutant._get_hyperparams returns an empty dict when the input
    is improperly formatted."""
    assert adjutant_client.Adjutant._get_hyperparams('{"hello: 1}') == {}


def test_get_hyperparams_valid_json() -> None:
    """Tests that Adjutant._get_hyperparams returns the correct dict when the
    input represents valid JSON."""
    assert adjutant_client.Adjutant._get_hyperparams(
        '{"hello": 1, "world": "abc"}') == {"hello": 1, "world": "abc"}
