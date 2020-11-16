import time
import random
from cassandra.cluster import Cluster
import db

def get_key():
    return random.randint(0, db.records)

if __name__ == "__main__":
    cluster = Cluster(['0.0.0.0'], port=9042)
    session = cluster.connect('nosql', wait_for_all_pools=True)

    val = get_key()
    print("\nRealizando consultas a Cassandra")
    print(f"\nObteniendo 1 registro aleatorio: {val}")

    # Un registro
    prepared = session.prepare("""SELECT * FROM sensores WHERE id= ?""")
    start_time = time.time()
    result = session.execute(prepared.bind((val,)))
    seconds = (time.time() - start_time)
    print(f"  Se obtuvo {result[0]} en {seconds:.5} segundos")

    # 10 registros
    start_time = time.time()
    print(f"\nObteniendo 10 registros aleatorios:")
    for n in range(10):   
        val = get_key()
        prepared = session.prepare("""SELECT * FROM sensores WHERE id= ?""")
        result = session.execute(prepared.bind((val,)))
        print(" ", result[0])
    seconds = (time.time() - start_time)
    print(f"En {seconds:.5} segundos\n")


    # Promedios por sensor
    start_time = time.time()
    result = session.execute("""SELECT avg(temperatura) FROM sensores""")
    print(f"Obtener promedio de {db.records:,} registros de temperatura: ")
    seconds = (time.time() - start_time)
    print(f" Promedio: {result[0]} en {seconds:.5} segundos\n")

    start_time = time.time()
    result = session.execute("""SELECT avg(humedad) FROM sensores""")
    print(f"Obtener promedio de {db.records:,} registros de humedad: ")
    seconds = (time.time() - start_time)
    print(f" Promedio: {result[0]} en {seconds:.5} segundos\n")

    start_time = time.time()
    result = session.execute("""SELECT avg(presion) FROM sensores""")
    print(f"Obtener promedio de {db.records:,} registros de presión: ")
    seconds = (time.time() - start_time)
    print(f" Promedio: {result[0]} en {seconds:.5} segundos\n")
