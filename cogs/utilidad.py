from discord.ext import commands
from utils import searching_google


class Utilidad(commands.Cog, description="Comandos de información general"):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Retorna el mejor resultado de búsqueda por google",
                      brief="Mejor resultado de google")
    async def buscar(self, ctx, *, query: str):
        result = searching_google(query)
        await ctx.send(result)


def setup(client):
    client.add_cog(Utilidad(client))
