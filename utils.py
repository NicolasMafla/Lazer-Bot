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
