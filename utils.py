import random
import json
from googlesearch import search

with open("./json/quotes.json", encoding="utf-8") as fh:
    quotes = json.load(fh)


def searching_google(query):
    results = search(query, lang="es")
    return results[0]


def fortune_coockie():
    quote = random.choice(quotes)
    return f"{quote.get('phrase')}"


def contar(guild_id, num):
    with open("./json/contador.json", encoding="utf-8") as fh:
        contador = json.load(fh)

    actual = contador.get(guild_id)

    if actual + 1 == num:
        contador[guild_id] = num

    with open("./json/contador.json", "w") as jsonFile:
        json.dump(contador, jsonFile)
