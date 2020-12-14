import time
import random
import db
from pymongo import MongoClient


if __name__ == "__main__":
    print(f"\nObteniendo datos del usuario 'kponce'")
    print("\nRealizando consulta a MySQL")
    sql = """select * from comentario as c inner join tweet as t on c.fk_tweet = t.id inner join usuario as u on t.fk_usuario = u.id where u.usuario = 'kponce';"""

    # Un registro
    conn = db.mysql_conn()
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute(sql)
    result = cursor.fetchone()
    seconds = (time.time() - start_time)
    print(f" Se obtuvo en {seconds:.5} segundos")
    print(" Nombre: ", result[13])

    print("\nRealizando consulta a MongoDB")
    client = MongoClient('localhost', port=27017, username='nosql', password='test_db')
    db = client['twitter']
    col = db['users']
    start_time = time.time()
    result = col.find_one({'usuario':'kponce'},{'tweets':0})
    seconds = (time.time() - start_time)
    print(f" Se obtuvo en {seconds:.5} segundos")
    print(" Nombre: ", result['nombre'])

    conn.close()
    client.close()
