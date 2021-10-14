"""Contains the Adjutant Discord client class."""

from typing import Optional
import logging
import json
from json.decoder import JSONDecodeError
from subprocess import Popen
import numpy as np
import wandb
from wandb.apis.public import Run
import discord
from discord.ext import tasks
from discord import TextChannel, Message

SECONDS_BETWEEN_WANDB_CHECKS = 60
COMMAND_HELLO = '$hello'
COMMAND_EXPERIMENT = '$experiment'


class Adjutant(discord.Client):
    """The Adjutant Discord client."""
    _wandb_api: wandb.Api
    _wandb_entity: str
    _wandb_project_title: str
    _run_experiment_script: Optional[str]
    channel_name: str
    channel: Optional[TextChannel]
    _reported_runs: dict[str, Run]

    def __init__(
            self,
            wandb_entity: str,
            wandb_project_title: str,
            *args,
            run_experiment_script: Optional[str] = None,
            channel_name: str = 'general',
            **kwargs) -> None:
        """Instantiates the object.

        :param wandb_entity: The WandB entity name (username or account name)
            under which exists the project.
        :param wandb_project_title: The title of the project on WandB to which
            to supply updates on Discord.
        :param run_experiment_script: The filename of an executable script that
            runs a new experiment with the given hyperparameters as a
            JSON-formatted command line argument. This script may also request
            another entity, e.g. Kubernetes, to initiate the experiment on its
            behalf rather than actually running the experiment itself.
        :param channel_name: The name of the channel in which to post updates.
        """
        super().__init__(*args, **kwargs)
        self._wandb_api = wandb.Api()
        self._wandb_entity = wandb_entity
        self._wandb_project_title = wandb_project_title
        self._run_experiment_script = run_experiment_script
        self.channel_name = channel_name
        self.channel = None
        self._reported_runs = self._get_project_runs()
        # pylint: disable=no-member
        self.check_wandb_for_new_runs.start()

    def _get_channel(self) -> Optional[TextChannel]:
        """Returns the channel whose name is self.channel_name, or None if no
        such channel exists.

        :return: The channel whose name is self.channel_name, or None if no such
            channel exists.
        """
        for channel in self.get_all_channels():
            if channel.name == self.channel_name:
                return channel
        return None

    def _get_project_runs(self) -> dict[str, Run]:
        """Returns the dict of all Runs for this project. The keys are the names
        of the runs and the values are the corresponding Run objects.

        :return: The dict of all Runs for this project.
        """
        self._wandb_api.flush()
        runs = self._wandb_api.runs(
            f'{self._wandb_entity}/{self._wandb_project_title}')
        runs = filter(lambda run: run.state == 'finished', runs)
        return {run.name: run for run in runs}

    @staticmethod
    def _get_run_with_best_val_loss(runs: dict[str, Run]) -> Run:
        """Returns the Run with the best (i.e., lowest) validation loss.

        :param runs: The dict of Runs to filter. The keys are the names of the
            runs and the values are the corresponding Run objects.
        :return: The Run with the best (i.e., lowest) validation loss.
        """
        runs = filter(lambda run: 'best_val_loss' in run.summary, runs.values())
        return min(runs, key=lambda run: run.summary['best_val_loss'])

    async def on_ready(self) -> None:
        """Runs once the client has successfully logged in. Logs the event and
        sets self.channel to the one requested by the user."""
        logging.info('Logged in as %s, %s', self.user.name, self.user.id)
        best_run_info = ''
        best_run = Adjutant._get_run_with_best_val_loss(self._reported_runs)
        if best_run:
            best_val_loss = best_run.summary.get('best_val_loss', np.inf)
            best_run_info = (
                f'Best run: {best_run.name}, best val loss: '
                f'{best_val_loss:.3f}\nLink to run: {best_run.url}')
        self.channel = self._get_channel()
        await self.channel.send(
            f'Adjutant starting! Found {len(self._reported_runs)} runs for '
            f'project {self._wandb_entity}/{self._wandb_project_title}.\n'
            f'{best_run_info}')

    @tasks.loop(seconds=SECONDS_BETWEEN_WANDB_CHECKS)
    async def check_wandb_for_new_runs(self) -> None:
        """Checks WandB for new runs for this project and posts the results of
        those runs."""
        runs = self._get_project_runs()
        new_run_names = set(runs.keys()).difference(
            set(self._reported_runs.keys()))
        for run_name in new_run_names:
            run = runs[run_name]
            self._reported_runs[run_name] = run
            best_val_loss = run.summary.get('best_val_loss', np.inf)
            await self.channel.send(
                f'Run {run.name} finished! Best val loss: {best_val_loss:.3f}\n'
                f'Link to run: {run.url}')

    @check_wandb_for_new_runs.before_loop
    async def _before_check_wandb_for_new_runs(self) -> None:
        """Prevents the check_wandb_for_new_runs loop from running before the
        client has logged in."""
        await self.wait_until_ready()

    @staticmethod
    def _get_hyperparams(text: str) -> dict:
        """Returns the hyperparameter dictionary from the text of the user's
        post. Returns the empty dict if the text contains an improperly
        formatted dictionary or no dictionary at all.

        :param text: The text of the user's message, starting with
            COMMAND_EXPERIMENT.
        :return: The hyperparameter dictionary from the text of the user's post
            (may be the empty dict).
        """
        args = text[len(COMMAND_EXPERIMENT):].strip()
        try:
            hyperparams = json.loads(args)
        except JSONDecodeError:
            hyperparams = {}
        return hyperparams

    def run_experiment(self, hyperparams: dict) -> None:
        """Runs an experiment in a subprocess.

        :param hyperparams: The hyperparameters to pass to the experiment
            function.
        """
        # We don't use the context manager because it waits for the subprocess.
        # pylint: disable=consider-using-with
        Popen([self._run_experiment_script, json.dumps(hyperparams)])

    async def on_message(self, message: Message) -> None:
        """Runs every time a message is posted (including by this bot). Responds
        to user commands to initiate new runs, etc. If the message's channel
        does not match that of this bot, the post is ignored.

        :param message: The user's post on the Discord server, in any channel.
        """
        if message.author == self.user or message.channel != self.channel:
            return
        if message.content.startswith(COMMAND_HELLO):
            await self.channel.send('Hello!')
        elif message.content.startswith(COMMAND_EXPERIMENT):
            if not self._run_experiment_script:
                await self.channel.send('No experiment script provided; '
                                        'cannot launch experiment.')
            else:
                hyperparams = Adjutant._get_hyperparams(message.content)
                await self.channel.send(
                    f'Running new experiment with the following '
                    f'hyperparameters.\n{json.dumps(hyperparams, indent=4)}')
                self.run_experiment(hyperparams)
