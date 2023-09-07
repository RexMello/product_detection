from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://rex:13579007@cluster0.kku4atv.mongodb.net/?retryWrites=true&w=majority")

db = cluster["product_data"]
collec = db['model_data']

# data_list = []
# model = input('Enter model name: ')

# for i in range(22):
    
#     i = str(i)
#     name = input('Enter value for '+i+': ')

#     dataa = {'detection_id':i,'name':name,'value':i,'ModelName':model}
#     data_list.append(dataa)

# if data_list != []:
#     collec.insert_many(data_list)

collec.insert_one({'detection_id':'24','name':'test','value':'24','ModelName':'CakeShop'})