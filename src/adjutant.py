import discord

# TODO environment variable?
with open('/Users/leo/.discord/token', 'r') as infile:
    discord_token = infile.read().strip()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run(discord_token)
