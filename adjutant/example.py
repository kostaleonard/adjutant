# TODO remove this file

import logging

logging.basicConfig(level=logging.INFO)

# TODO environment variable?
with open('/Users/leo/.discord/token', 'r') as infile:
    discord_token = infile.read().strip()

'''
client = discord.Client()


@client.event
async def on_ready() -> None:
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$pic'):
        await message.channel.send(
            'Here\'s that picture you wanted.',
            file=discord.File('/tmp/my_image.png'))
'''

from adjutant.adjutant_client import Adjutant
adj = Adjutant('kostaleonard', 'mnist')
adj.run(discord_token)
