import time
import random
from mysql import connector

def db():
	db_connection = connector.connect(
		host='localhost',
		user='root',
		password='nosql',
		database='test_db')
	return db_connection

def execute(sql):
	conn = db()
	cursor = conn.cursor()
	cursor.execute(sql)
	conn.commit()

if __name__ == '__main__':
	reg = 1_000
	percent = reg / 10
	
	execute("DROP TABLE IF EXISTS sensores")
	execute("""CREATE TABLE sensores (
			id int PRIMARY KEY,
			temperatura float,
			humedad float,
			presion float
			)
		""")

	sql = "INSERT INTO sensores (id, temperatura, humedad, presion) VALUES (%s, %s, %s, %s)"

	conn = db()
	cursor = conn.cursor()
	
	start_time = time.time()
	print(f'Comenzando la carga de {reg:,} de registros.')
	for i in range(reg):
		rand = random.random()
		val = (i, rand, rand, rand)
		cursor.execute(sql, val)
		if(i % percent == 0):
			seconds = (time.time() - start_time)
			print(f'  {i/percent*10}% en: {seconds:.6} segundos')
	conn.commit()

	seconds = (time.time() - start_time)
	print(f'{reg:,} registros en: {seconds:.6} segundos\n')
