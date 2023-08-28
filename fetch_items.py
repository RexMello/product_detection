import dns.resolver
from pymongo import MongoClient
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

import os
cluster = MongoClient("mongodb+srv://kai:13579007@cluster0.wacwe.mongodb.net/?retryWrites=true&w=majority")

model_name = input('Enter model name: ')
db = cluster["product_data"]

if model_name not in db.list_collection_names():
    print('Collection not found')
    os._exit(1)

collec = db[model_name]


data = collec.find()

for d in data:
    print(d['Name'])