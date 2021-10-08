"""Contains the Adjutant Discord client class."""

from typing import Callable, Optional
import json
from json.decoder import JSONDecodeError
import logging
from logging import INFO
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
    run_experiment_fn: Optional[Callable[[dict], None]]
    channel_name: str
    channel: Optional[TextChannel]
    seconds_between_wandb_checks: int
    _reported_runs: set[Run]

    def __init__(
            self,
            wandb_entity: str,
            wandb_project_title: str,
            run_experiment_fn: Optional[
                Callable[[dict], None]] = None,
            channel_name: str = 'general',
            *args,
            **kwargs) -> None:
        """Instantiates the object.

        :param wandb_entity: The WandB entity name (username or account name)
            under which exists the project.
        :param wandb_project_title: The title of the project on WandB to which
            to supply updates on Discord.
        :param run_experiment_fn: Runs a new experiment with the given
            hyperparameters. This function may also request another entity, e.g.
            Kubernetes, to initiate the experiment on its behalf rather than
            actually running the experiment itself.
        :param channel_name: The name of the channel in which to post updates.
        """
        super().__init__(*args, **kwargs)
        self._wandb_api = wandb.Api()
        self._wandb_entity = wandb_entity
        self._wandb_project_title = wandb_project_title
        self.run_experiment_fn = run_experiment_fn
        self.channel_name = channel_name
        self.channel = None
        self._reported_runs = self._get_project_runs()
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

    def _get_project_runs(self) -> set[Run]:
        """Returns the set of all Runs for this project.

        :return: The set of all Runs for this project.
        """
        self._wandb_api.flush()
        runs = self._wandb_api.runs(
            f'{self._wandb_entity}/{self._wandb_project_title}')
        return set(runs)

    async def on_ready(self) -> None:
        """Runs once the client has successfully logged in. Logs the event and
        sets self.channel to the one requested by the user."""
        logging.log(INFO, f'Logged in as {self.user.name}, {self.user.id}')
        self.channel = self._get_channel()
        await self.channel.send(
            f'Adjutant starting! Found {len(self._reported_runs)} runs for '
            f'project {self._wandb_entity}/{self._wandb_project_title}.')
        # TODO report run with best validation loss

    @tasks.loop(seconds=SECONDS_BETWEEN_WANDB_CHECKS)
    async def check_wandb_for_new_runs(self) -> None:
        """Checks WandB for new runs for this project and posts the results of
        those runs."""
        runs = self._get_project_runs()
        # TODO only report new runs
        await self.channel.send(f'Found {len(runs)} runs for project '
                                f'{self._wandb_entity}/'
                                f'{self._wandb_project_title}.')

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
            hyperparams = Adjutant._get_hyperparams(message.content)
            await self.channel.send(
                f'Running new experiment with the following hyperparameters.\n'
                f'{json.dumps(hyperparams, indent=4)}')
