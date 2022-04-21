import discord

from message_parser import parse_message
# from utils import format_date

class MyClient(discord.Client):
    def __init__(self, guild_name:str) -> None:
        super().__init__()
        self.guild_name = guild_name

    async def on_ready(self):
        print('Logged on as', self.user)

    async def setup_group(self, ctx, **args):
        try:
            guild = discord.utils.get(self.guilds, name=self.guild_name)
            category = await guild.create_category(args['group_name'], overwrites=None, reason=None)
            await guild.create_text_channel("texto", overwrites=None, category=category, reason=None)
            await guild.create_voice_channel("voz", overwrites=None, category=category, reason=None)
            time = list(args['timestamp'].timetuple())
            sender_id = args['sender'].id
            await ctx.send(f"Grupo **{args['group_name']}** criado com sucesso pelo usuário <@{sender_id}> no dia {time[2]}/{time[1]}/{time[0]}")

        except Exception as e:
            print(f"Error creating group...: {e}")
            await ctx.send("Desculpe, houve um erro ao criar o grupo.")


    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content.startswith('!pairup'):
            message_content = parse_message(message)
            print(message_content)
            await self.setup_group(message.channel, **message_content)
