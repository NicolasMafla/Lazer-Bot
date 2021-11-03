import json
import discord
from discord.ext import tasks, commands
from utils import validate_date

class Fechas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@commands.Cog.listener()
    #async def on_ready(self):
    #    self.reminder.start()

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

    #@tasks.loop(seconds=10.0)
    #async def reminder(self):
        #with open("./json/birthdays.json", encoding="utf-8") as fh:
        #  birthdays = json.load(fh)
        #print(birthdays)
        #for guild in self.bot.guilds:
        #  if guild.id == 843615200061423617:
        #    message_channel = self.bot.get_channel(899327174258073610)
        #    print(f"Got channel {message_channel}")
        #    await message_channel.send("Your message")

    #@reminder.before_loop
    #async def before_printer(self):
    #    await self.bot.wait_until_ready()

def setup(client):
    client.add_cog(Fechas(client))
