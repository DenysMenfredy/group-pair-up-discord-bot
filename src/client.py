import discord
from discord import Client
from discord.ext import commands
from message_parser import parse_message
from db.db import DB

class MyClient(Client):
    def __init__(self, guild_name:str) -> None:
        super().__init__()
        self.guild_name = guild_name
        self.db = DB()

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
            group_collection = {
                "name": args['group_name'],
                "members": args['members'],
                "timestamp": time,
                "creator_id": sender_id,
            }
            try:
                self.db.create_group(group_collection)
            except Exception as e:
                print(e)
                await ctx.send(e.args[0])
                return
            await ctx.send(f"Grupo **{args['group_name']}** criado com sucesso pelo usuário <@{sender_id}> no dia {time[2]}/{time[1]}/{time[0]}")

        except Exception as e:
            print(e)
            print(f"Error creating group...: {e}")
            await ctx.send("Desculpe, houve um erro ao criar o grupo.")


    async def list_users_from_server(self, ctx):
        server_id = ctx.guild.id
        self.server = self.get_guild(server_id)
        users = self.server.members
        await ctx.channel.send(f"{len(users)} users in the server:")
        for user in users:
            print(user.name)

    async def set_channel_permissions(self, member, channel, permissions):
        await channel.set_permissions(member, **permissions)

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

        if message.content.startswith('!list_users'):
            await self.list_users_from_server(message)

        if message.content.startswith('!delete_all_channels'):
            await self.delete_all_channels(message)


    # @commands.Cog.listener()
    # async def delete_all_channels(self, ctx):
    #     for channel in ctx.guild.channels:
    #         await channel.delete()