import json
import discord
import pandas as pd
import time
import datetime
from dateutil.relativedelta import relativedelta
from discord.ext import tasks, commands
from utils import validate_date
from utils import fortune_coockie

class Fechas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      self.reminder.start()

    @commands.command(description="Agregar cumpleaños de un miembro. La fecha de nacimiento debe estar en formato dd/mm/aaaa.",
                      brief="Agregar un cumpleaños con la fecha de nacimiento")
    async def cumple(self, ctx, member: discord.Member = None, dob:str = None):
        if member is None:
            await ctx.send("Debes mencionar al que quieras agregar el cumpleaños crack :eyes:")
        elif dob is None:
            await ctx.send("Debes poner la fecha de nacimiento crack :eyes:")
        elif validate_date(dob) == False:
            await ctx.send("Debes una fecha de nacimiento válida crack :eyes:.\nDebe estar en formato dd/mm/aaaa por ejemplo: 12/04/2017")
        else:
          with open("./json/birthdays.json", "r", encoding="utf-8") as fh:
            birthdays = json.load(fh)
          guild_id = str(ctx.message.guild.id)
          data_dict = {"name":member.name,"mention":member.mention,"dob":dob}
          birthdays[guild_id][str(member.id)] = data_dict

          embed = discord.Embed(title=f"🎂 Cumpleaños 🎂", description = f"Creado para {member.name}",color=member.color)
          embed.set_thumbnail(url=f"{member.avatar_url}")
          embed.add_field(name="Se unió al planeta tierra el", value=dob)
          await ctx.send(embed=embed)
        
          with open("./json/birthdays.json", "w", encoding="utf-8") as jsonFile:
            json.dump(birthdays, jsonFile)

    @tasks.loop(hours=3.0)
    async def reminder(self):
        with open("./json/birthdays.json", encoding="utf-8") as fh:
          birthdays = json.load(fh)
        for guild in self.bot.guilds:
          if guild.id == 843615200061423617:
            continue
          print(f"checking for birthdays at {datetime.datetime.utcnow() - relativedelta(hours=5)} in {guild.name}")
          channel = self.bot.get_channel(746539159715315797)
          for member in guild.members:
            dob_dict = get_bd(str(guild.id), str(member.id), birthdays)
            dob = convert_date(dob_dict.get("dob"))
            now = datetime.datetime.utcnow() - relativedelta(hours=5)
            if check_is_today(dob, now):
              years = now - dob
              embed = discord.Embed(title=f"🎉🎂 *Feliz cumpleaños #{int(years.days/365)}* 🎂🎉", description = f"Larga vida a {member.mention}, que la suerte esté de tu lado, come mucho pastel y sigue manqueando!\nAtt: **{guild.name}**", color=member.color)
              embed.set_image(url=f"https://c.tenor.com/d3yoMUgo1j4AAAAC/2021party-twerk.gif")
              fortune_message = f"Galleta de la fortuna: {fortune_coockie()}"
              embed.set_footer(text=fortune_message)
              embed.set_thumbnail(url=f"{member.avatar_url}")
              message = await channel.send(embed=embed)
              await message.add_reaction("🔥")

    @reminder.before_loop
    async def before_printer(self):
      await self.bot.wait_until_ready()

def get_bd(guild_id, member_id, birthdays):
  dob_dict = birthdays.get(guild_id).get(member_id)
  if dob_dict is None:
    return {"name": None, "mention": None, "dob": None}
  else:
    return dob_dict

def convert_date(dob):
  if dob is None:
    return pd.NaT
  else:
    return datetime.datetime.strptime(dob, "%d/%m/%Y")

def check_is_today(dob, now):
  month_now = now.month
  day_now = now.day

  month_dob = dob.month
  day_dob = dob.day

  if (month_now==month_dob) and (day_now==day_dob):
    return True
  else:
    return False

def setup(client):
    client.add_cog(Fechas(client))
