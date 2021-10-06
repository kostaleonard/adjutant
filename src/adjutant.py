import discord

# TODO environment variable?
with open('/Users/leo/.discord/token', 'r') as infile:
    discord_token = infile.read().strip()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(discord_token)
