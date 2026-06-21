import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True
# members: privileged — wymagany do rozsyłania przypomnień dla całej roli
# (scheduler iteruje po role.members). Trzeba go włączyć w portalu Discord.
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
