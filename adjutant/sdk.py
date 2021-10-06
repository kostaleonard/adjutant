"""Contains adjutant SDK functions."""

from typing import Optional


# TODO giving the token is like giving a password--need to find another way
def init(discord_token: str) -> None:
    """Initializes adjutant so that it can post updates to a given platform.
    :param discord_token: The bot user's Discord token. adjutant will use this
        to post as the bot on Discord.
    """
    # TODO


def post(text: str,
         filename: Optional[str] = None,
         channel: str = 'general') -> None:
    """Posts the given data to the channel.
    :param text: The text to post.
    :param filename: If provided, the file to send as an attachment.
    :param channel: The channel to which to post.
    """
    # TODO
