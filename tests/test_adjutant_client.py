"""Tests adjutant_client.py."""
# pylint: disable=protected-access

import os
import json
import pytest
from wandb.apis.public import Run
from adjutant import adjutant_client
from examples.mnist.mnist_model import WANDB_PROJECT_TITLE
from tests.apis import is_discord_config_present, is_wandb_config_present

WANDB_ENTITY = 'kostaleonard'
DISCORD_TOKEN_ENVIRONMENT_VAR = 'DISCORD_ADJ_TOKEN'
SETUP_TIMEOUT_SECONDS = 20
NUM_KNOWN_PROJECT_RUNS = 60
TEST_EXPERIMENT_SCRIPT = os.path.join('tests', 'write_arg.sh')
TEST_EXPERIMENT_OUTPUT_FILE = os.path.join('/', 'tmp', 'adj_write_arg_out.txt')
KNOWN_BEST_VAL_LOSS = 0.08257


def test_adjutant_init_sets_public_fields() -> None:
    """Tests that Adjutant.__init__ sets the object's fields correctly."""
    if not is_discord_config_present():
        return
    adj = adjutant_client.Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    assert adj.channel_name


def test_adjutant_get_project_runs_finds_project_runs() -> None:
    """Tests that Adjutant._get_project_runs finds runs from known projects."""
    if not is_discord_config_present() or not is_wandb_config_present():
        return
    adj = adjutant_client.Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    runs = adj._get_project_runs()
    assert len(runs) >= NUM_KNOWN_PROJECT_RUNS


def test_adjutant_get_run_with_best_val_loss_finds_best_run() -> None:
    """Tests that Adjutant._get_run_with_best_val_loss finds the run with the
    best validation loss."""
    if not is_discord_config_present() or not is_wandb_config_present():
        return
    adj = adjutant_client.Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    runs = adj._get_project_runs()
    best_run = adjutant_client.Adjutant._get_run_with_best_val_loss(runs)
    assert best_run.summary['best_val_loss'] <= KNOWN_BEST_VAL_LOSS


def test_adjutant_get_run_with_best_val_loss_no_val_loss_key() -> None:
    """Tests that Adjutant._get_run_with_best_val_loss still succeeds even when
    there are runs that don't have a validation loss key."""
    if not is_discord_config_present() or not is_wandb_config_present():
        return
    adj = adjutant_client.Adjutant(WANDB_ENTITY, WANDB_PROJECT_TITLE)
    runs = adj._get_project_runs()
    assert any('best_val_loss' not in run.summary for run in runs)
    best_run = adjutant_client.Adjutant._get_run_with_best_val_loss(runs)
    assert isinstance(best_run, Run)


def test_adjutant_get_run_with_best_val_loss_raises_error_empty_input() -> None:
    """Tests that Adjutant._get_run_with_best_val_loss raises an error when the
    input is empty."""
    with pytest.raises(ValueError):
        _ = adjutant_client.Adjutant._get_run_with_best_val_loss(set())


def test_adjutant_get_hyperparams_empty_str() -> None:
    """Tests Adjutant._get_hyperparams on the empty string."""
    assert adjutant_client.Adjutant._get_hyperparams('') == {}


def test_adjutant_get_hyperparams_bad_json() -> None:
    """Tests that Adjutant._get_hyperparams returns an empty dict when the input
    is improperly formatted."""
    assert adjutant_client.Adjutant._get_hyperparams(
        adjutant_client.COMMAND_EXPERIMENT +
        ' {"hello: 1}') == {}


def test_adjutant_get_hyperparams_no_command() -> None:
    """Tests that Adjutant._get_hyperparams returns an empty dict when the input
    does not contain the COMMAND_EXPERIMENT string as a start sequence."""
    assert adjutant_client.Adjutant._get_hyperparams(
        '{"hello": 1, "world": "abc"}') == {}


def test_adjutant_get_hyperparams_valid_json() -> None:
    """Tests that Adjutant._get_hyperparams returns the correct dict when the
    input represents valid JSON."""
    assert adjutant_client.Adjutant._get_hyperparams(
        adjutant_client.COMMAND_EXPERIMENT +
        ' {"hello": 1, "world": "abc"}') == {"hello": 1, "world": "abc"}


def test_adjutant_run_experiment_runs_command() -> None:
    """Tests that Adjutant.run_experiment runs the specified command with the
    hyperparameter JSON string as the argument."""
    # TODO this fails sometimes
    if not is_discord_config_present():
        return
    adj = adjutant_client.Adjutant(
        WANDB_ENTITY,
        WANDB_PROJECT_TITLE,
        run_experiment_script=TEST_EXPERIMENT_SCRIPT)
    hyperparams = {"hello": 1, "world": "abc"}
    try:
        os.remove(TEST_EXPERIMENT_OUTPUT_FILE)
    except FileNotFoundError:
        pass
    adj.run_experiment(hyperparams)
    assert os.path.exists(TEST_EXPERIMENT_OUTPUT_FILE)
    with open(TEST_EXPERIMENT_OUTPUT_FILE, 'r', encoding='utf-8') as infile:
        contents = infile.read()
    os.remove(TEST_EXPERIMENT_OUTPUT_FILE)
    assert json.loads(contents) == hyperparams
