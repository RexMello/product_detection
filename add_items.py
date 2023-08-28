import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']


from pymongo import MongoClient
import os
cluster = MongoClient("mongodb+srv://kai:13579007@cluster0.wacwe.mongodb.net/?retryWrites=true&w=majority")

model_name = input('Enter model name: ')
db = cluster["product_data"]

if model_name not in db.list_collection_names():
    print('Collection not found')
    os._exit(1)

collec = db[model_name]

data_list = []

while True:
    item = input('Enter item name: ')
    if item == 'q':
        break
    value = input('Enter item value: ')

    dataa = {'detection_id':item,'name':item,'value':value}
    data_list.append(dataa)

if data_list != []:
    collec.insert_many(data_list)