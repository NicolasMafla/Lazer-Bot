import discord
import os
from decouple import config
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

DISCORD_TOKEN = config("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="-", description="Bot de lazer force uwu", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("-help"))
    #guild = bot.guilds[0].name
    for guild in bot.guilds:
      print(f"{bot.user} has connected to {guild.name}!")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("El comando no existe o lo escribiste mal :eyes:")

for file_name in os.listdir("./cogs"):
    if file_name.endswith(".py"):
        bot.load_extension(f"cogs.{file_name[:-3]}")

keep_alive()
bot.run(DISCORD_TOKEN)