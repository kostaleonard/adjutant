"""Contains the Adjutant Discord client class."""

from typing import Callable, Optional, Any
import wandb
from wandb.apis.public import Run
import discord
from discord.ext import tasks


class Adjutant(discord.Client):
    """The Adjutant Discord client."""
    wandb_api: wandb.Api
    wandb_entity: str
    wandb_project_title: str
    run_experiment_fn: Optional[Callable[[dict[str, Any]], None]]

    def __init__(self,
                 wandb_entity: str,
                 wandb_project_title: str,
                 run_experiment_fn: Optional[
                     Callable[[dict[str, Any]], None]] = None,
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
        """
        super().__init__(*args, **kwargs)
        self.wandb_api = wandb.Api()
        self.wandb_entity = wandb_entity
        self.wandb_project_title = wandb_project_title
        self.run_experiment_fn = run_experiment_fn

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
        # TODO this is just testing code.
        channel = self.get_channel(795713981909172246)
        runs = self._get_project_runs()
        await channel.send(f'Found {len(runs)} runs for project.')

    @tasks.loop(seconds=10)  # task runs every 60 seconds
    async def my_background_task(self):
        # TODO loop not working
        # TODO docstring
        # TODO get the channel by name, default to general
        channel = self.get_channel(795713981909172246)
        runs = self._get_project_runs()
        await channel.send(f'Found {len(runs)} runs for project.')

    @my_background_task.before_loop
    async def before_my_task(self):
        # TODO docstring
        await self.wait_until_ready()
