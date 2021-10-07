"""Contains the Adjutant Discord client class."""

from typing import Callable, Optional, Any
import wandb
from wandb.apis.public import Run
import discord
from discord.ext import tasks
from discord import TextChannel


class Adjutant(discord.Client):
    """The Adjutant Discord client."""
    wandb_api: wandb.Api
    wandb_entity: str
    wandb_project_title: str
    run_experiment_fn: Optional[Callable[[dict[str, Any]], None]]
    channel_name: str
    channel: Optional[TextChannel]

    def __init__(self,
                 wandb_entity: str,
                 wandb_project_title: str,
                 run_experiment_fn: Optional[
                     Callable[[dict[str, Any]], None]] = None,
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
        self.wandb_api = wandb.Api()
        self.wandb_entity = wandb_entity
        self.wandb_project_title = wandb_project_title
        self.run_experiment_fn = run_experiment_fn
        self.channel_name = channel_name
        self.channel = None
        self.my_background_task.start()

    def _get_channel(self) -> Optional[TextChannel]:
        """Returns the channel whose name is self.channel_name, or None if no
        such channel exists.

        :return: The channel whose name is self.channel_name, or None if no such
            channel exists.
        """
        for guild in self.guilds:
            for channel in guild.channels:
                if channel.name == self.channel_name:
                    return channel
        return None

    def _get_project_runs(self) -> set[Run]:
        """Returns the set of all Runs for this project.

        :return: The set of all Runs for this project.
        """
        runs = self.wandb_api.runs(
            f'{self.wandb_entity}/{self.wandb_project_title}')
        return set(runs)

    async def on_ready(self):
        # TODO docstring
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.channel = self._get_channel()

    @tasks.loop(seconds=10)
    async def my_background_task(self):
        # TODO docstring
        # TODO change name
        runs = self._get_project_runs()
        await self.channel.send(f'Found {len(runs)} runs for project.')

    @my_background_task.before_loop
    async def before_my_task(self):
        # TODO docstring
        # TODO change name
        await self.wait_until_ready()
