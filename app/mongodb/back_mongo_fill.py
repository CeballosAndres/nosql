from pymongo import MongoClient
import pandas as pd

import db

reg = db.records
percent = reg / 10

client = MongoClient('localhost', port=27017,
                     username='nosql', password='test_db')

db = client['peliculas']
db.drop_collection('titulos')
col_tit = db['titulos']
datos = pd.read_csv('title.basics.tsv', sep='\t', nrows=reg)

print(datos.info())

for index, row in datos.iterrows():
    col_tit.insert_one({
        'tconst': row['tconst'],
        'titleType': row['titleType'],
        'primaryTitle': row['primaryTitle'],
        'originalTitle': row['originalTitle'],
        'isAdult': row['isAdult'],
        'startYear': row['startYear'],
        'endYear': row['endYear'],
        'runtimeMinutes': row['runtimeMinutes'],
        'genres': row['genres']
    })
print(col_tit.find_one({}))


