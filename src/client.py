import discord
from discord import Client
from discord.ext import commands
from message_parser import parse_message
from db.db import DB

class MyClient(commands.Bot):
    def __init__(self, guild_name:str, intents, command_prefix="!") -> None:
        super().__init__(intents=intents, command_prefix=command_prefix)
        # super().__init__()
        self.guild_name = guild_name
        self.db = DB()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def setup_group(self, ctx, **args):
            
        time = list(args['timestamp'].timetuple())
        sender_id = args['sender'].id
        group_name = args['group_name']
        group_collection = {
            "name": args['group_name'],
            "members": args['members'],
            "timestamp": time,
            "creator_id": sender_id,
        }
        print(group_collection)
        try:
            self.db.create_group(group_collection)
            await self.make_group(ctx, ctx.guild, group_name)
            await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=False)
            # await ctx.channel.set_permissions(ctx.guild.me, read_messages=True, send_messages=True)
            admins_id = self.get_admins_id()
            for member_id in list(set(admins_id) - set(args['members'])):
                print(member_id)
                member = await self.fetch_user(member_id)
                await self.set_channel_permissions(member, ctx.channel)

        except Exception as e:
            print(e)
            await ctx.channel.send(e.args[0])
            return
        await ctx.channel.send(f"Grupo **{args['group_name']}** criado com sucesso pelo usuário <@{sender_id}> no dia {time[2]}/{time[1]}/{time[0]}")



    async def make_group(self, ctx, guild, group_name):
        try:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            category = await guild.create_category(group_name, overwrites=overwrites, reason=None)
            await guild.create_text_channel("texto", overwrites=overwrites, category=category, reason=None)
            await guild.create_voice_channel("voz", overwrites=overwrites, category=category, reason=None)
        except Exception as e:
            print(e)
            await ctx.send("Erro ao criar grupo")

    async def list_users_from_server(self, ctx):
        server_id = ctx.guild.id
        self.server = self.get_guild(server_id)
        users = self.server.members
        await ctx.channel.send(f"{len(users)} users in the server:")
        for user in users:
            print(user.name)

    async def set_channel_permissions(self, member, channel):
        await channel.set_permissions(member, read_messages=True, send_messages=True)

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    def get_admins_id(self):
        return self.db.get_admins_id()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content.startswith('!make-group'):
            message_content = parse_message(message)
            print(message_content)
            await self.setup_group(message, **message_content)

        if message.content.startswith('!list_users'):
            await self.list_users_from_server(message)

