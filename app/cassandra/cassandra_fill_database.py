import time
import random
from cassandra.cluster import Cluster

import db

KEYSPACE = "nosql"
reg = db.records
percent = reg / 10


def main():
    cluster = Cluster(['0.0.0.0'], port=9042)
    session = cluster.connect('system_schema', wait_for_all_pools=True)

    rows = session.execute("SELECT keyspace_name FROM keyspaces")
    if KEYSPACE in [row[0] for row in rows]:
        print(f"Eliminando espacio de trabajo {KEYSPACE}...")
        session.execute("DROP KEYSPACE " + KEYSPACE)

    print(f"Creando espacio de trabajo {KEYSPACE}...")
    session.execute("""
        CREATE KEYSPACE %s
        """ % KEYSPACE)

    print(f"Estableciendo espacio de trabajo {KEYSPACE}...")
    #log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    #log.info("creating table cities...")
    print(f"Creando tabla sensores")
    session.execute("""
        CREATE TABLE sensores (
            id int,
            sensor int,
            temperatura float,
            humedad float,
            presion float,
            PRIMARY KEY(id)
            );
        """)

    prepared = session.prepare("""
        INSERT INTO sensores (id, sensor, temperatura, humedad, presion)
        VALUES (?, ?, ?, ?, ?)
        """)

    print(f'Comenzando la carga de {reg:,} de registros.')
    start_time = time.time()
    for i in range(reg):
        rand = random.random()
        sen = int(rand * 100)
        temp = rand * 60
        hum = rand * 100
        pres = 950 + (rand * 200)
        session.execute(prepared.bind((i, sen, temp, hum, pres)))
        if(i % percent == 0):
            seconds = (time.time() - start_time)
            print(f'  {i/percent*10}% en: {seconds:.6} segundos')
    seconds = (time.time() - start_time)
    print(f'{reg:,} registros en: {seconds:.6} segundos\n')


if __name__ == '__main__':
    main()
