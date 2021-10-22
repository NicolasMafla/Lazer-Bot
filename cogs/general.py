import discord
import json
from discord.ext import commands
from utils import fortune_coockie

class General(commands.Cog, description="Comandos de información general"):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Información detallada acerca del servidor",
                      brief="Información del servidor")
    async def info(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}",
                              description=f"{ctx.guild.description}",
                              color=discord.colour.Color.teal())
        embed.add_field(name="Creación", value=f"{ctx.guild.created_at.date()}")
        embed.add_field(name="Dueño", value=f"{ctx.guild.owner.name}")
        embed.add_field(name="Región", value=f"{ctx.guild.region}")
        embed.add_field(name="ID", value=f"{ctx.guild.id}")
        roles = ', '.join([r.name for r in ctx.guild.roles])
        embed.add_field(name="Roles", value=f"{roles}")
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name="Miembros", value=f"{ctx.guild.member_count}")

        await ctx.send(embed=embed)

    @commands.command(description="Información detallada acerca de un miembro",
                      brief="Información de un miembro")
    async def info_user(self, ctx, member: discord.Member=None):
      if member is None:
        await ctx.send("Debes mencionar al que quieras ver su info crack :eyes:")
      else:
        embed = discord.Embed(title=f"{member.name}",
                              color=member.color)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name="Creación", value=f"{member.created_at.date()}")
        embed.add_field(name="Se unió", value=f"{member.joined_at.date()}")
        embed.add_field(name="Id", value=f"{member.discriminator}")
        embed.add_field(name="Top role", value=f"{member.top_role.name}")
        await ctx.send(embed=embed)

    @commands.command(description="Despedida con bendición cuando un miembro se va",
                      brief="Despedida con bendición")
    async def bendicion(self, ctx, member: discord.Member=None):
      if member is None:
        await ctx.send("Debes mencionar al que quieras dar la bendición crack :eyes:")
      else:
        embed = discord.Embed()
        message = f"*Que nuestro señor panda te cuide y te proteja.* :pray::candle: {member.mention}"
        embed.add_field(name="Bendición", value=message)
        fortune_message = f"Galleta de la fortuna: {fortune_coockie()}"
        embed.set_footer(text=fortune_message)
        message = await ctx.send(embed=embed)
        await message.add_reaction("🔥")

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author == self.client.user:
          return
          
      if message.channel.name == "contar":
          ctx = await self.client.get_context(message)
          
          try:
              num = int(message.content)
              id_guild = str(message.guild.id)

              with open("./json/contador.json", encoding="utf-8") as fh:
                  contador = json.load(fh)
              
              actual = contador.get(id_guild)
              if actual + 1 == num:
                  contador[id_guild] = num
              else:
                  await ctx.channel.purge(limit=1)
                  await ctx.send("Sigue con el conteo :eye:")
              
              with open("./json/contador.json", "w") as jsonFile:
                  json.dump(contador, jsonFile)
          
          except:
              await ctx.channel.purge(limit=1)
              await ctx.send("Sigue con el conteo :eye:")
      

def setup(client):
    client.add_cog(General(client))
