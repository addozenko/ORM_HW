import json
from session import SESSION

from models import Publisher, Shop, Book, Stock, Sale


with open('data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    SESSION.add(model(id=record.get('pk'), **record.get('fields')))