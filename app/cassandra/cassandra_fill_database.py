#!/usr/bin/env python

# import logging

# log = logging.getLogger()
# log.setLevel('DEBUG')
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
# log.addHandler(handler)

import time
import random
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "nosql"
reg = 10_000
percent = reg / 10


def main():
    cluster = Cluster(['0.0.0.0'], port=9042)
    session = cluster.connect('system_schema', wait_for_all_pools=True)

    rows = session.execute("SELECT keyspace_name FROM keyspaces")
    if KEYSPACE in [row[0] for row in rows]:
        #log.info("dropping existing keyspace...")
        print(f"Eliminando espacio de trabajo {KEYSPACE}...")
        session.execute("DROP KEYSPACE " + KEYSPACE)

    #log.info("creating keyspace...")
    print(f"Creando espacio de trabajo {KEYSPACE}...")
    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE)

    print(f"Estableciendo espacio de trabajo {KEYSPACE}...")
    #log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    #log.info("creating table cities...")
    print(f"Creando tabla sensores")
    session.execute("""
        CREATE TABLE sensores (
            id int,
            temperatura float,
            humedad float,
            presion float,
            PRIMARY KEY(id)
            );
        """)

    prepared = session.prepare("""
        INSERT INTO sensores (id, temperatura, humedad, presion)
        VALUES (?, ?, ?, ?)
        """)

    print(f'Comenzando la carga de {reg:,} de registros.')
    start_time = time.time()
    for i in range(reg):
        #log.info("inserting row %d" % i)
        #session.execute(query, dict(key="key%d" % i, a='a', b='b'))
        rand = random.random()
        session.execute(prepared.bind((i, rand, rand, rand)))
        if(i % percent == 0):
            seconds = (time.time() - start_time)
            print(f'  {i/percent*10}% en: {seconds:.6} segundos')
    seconds = (time.time() - start_time)
    print(f'{reg:,} registros en: {seconds:.6} segundos\n')


	# for n in range(1, reg+1):
	# 	val = ("KEY:"+str(n), "VALUE:"+str(n))
	# 	cursor.execute(sql, val)
	# conn.commit()


    # query = SimpleStatement("""
    #     INSERT INTO mytable (thekey, col1, col2)
    #     VALUES (%(key)s, %(a)s, %(b)s)
    #     """, consistency_level=ConsistencyLevel.ONE)


	


if __name__ == '__main__':
    main()
