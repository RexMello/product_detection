import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']


from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://kai:13579007@cluster0.wacwe.mongodb.net/?retryWrites=true&w=majority")

db = cluster["product_data"]
collec = db['model_data']

data_list = []
model = input('Enter model name: ')

for i in range(22):
    
    i = str(i)
    name = input('Enter value for '+i+': ')

    dataa = {'detection_id':i,'name':name,'value':i,'ModelName':model}
    data_list.append(dataa)

if data_list != []:
    collec.insert_many(data_list)