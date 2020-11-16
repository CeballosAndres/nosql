import time
import random
from mysql import connector

import db


def execute(sql):
	conn = db.mysql_conn()
	cursor = conn.cursor()
	cursor.execute(sql)
	conn.commit()

if __name__ == '__main__':
	reg = db.records
	percent = reg / 10
	
	execute("DROP TABLE IF EXISTS sensores")
	execute("""CREATE TABLE sensores (
			id int PRIMARY KEY,
			sensor int,
			temperatura float,
			humedad float,
			presion float
			)
		""")

	sql = "INSERT INTO sensores (id, sensor, temperatura, humedad, presion) VALUES (%s, %s, %s, %s, %s)"

	conn = db.mysql_conn()
	cursor = conn.cursor()
	
	start_time = time.time()
	print(f'Comenzando la carga de {reg:,} de registros.')
	for i in range(reg):
		rand = random.random()
		sen = int(rand * 100)
		temp = rand * 60
		hum = rand * 100
		pres = 950 + (rand * 200)
		val = (i, sen, temp, hum, pres)
		cursor.execute(sql, val)
		conn.commit()
		if(i % percent == 0):
			seconds = (time.time() - start_time)
			print(f'  {i/percent*10}% en: {seconds:.6} segundos')

	seconds = (time.time() - start_time)
	print(f'{reg:,} registros en: {seconds:.6} segundos\n')
