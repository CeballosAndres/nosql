from mysql import connector
import time

def get_connector():
	db = connector.connect(
		host='localhost',
		user='root', 
		password='nosql', 
		database='test_db'
	)
	return db

def execute(sql):
	db = get_connector()
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit()


if __name__ == '__main__':
	reg = 1_000
	percent = reg / 10
	
	execute("DROP TABLE IF EXISTS users")
	execute("CREATE TABLE users (username VARCHAR(45) PRIMARY KEY, password VARCHAR(45))")

	sql = "INSERT INTO users (username, password) VALUES (%s, %s)"

	db = get_connector()
	cursor = db.cursor()
	
	start_time = time.time()
	print(f'Comenzando la carga de {reg:,} de registros.')
	for n in range(reg):
		val = ("KEY:"+str(n), "VALUE:"+str(n))
		cursor.execute(sql, val)
		if(n % percent == 0):
			seconds = (time.time() - start_time)
			print(f'  {n/percent*10}% en: {seconds} segundos')
	db.commit()

	seconds = (time.time() - start_time)
	print(f'{reg:,} registros en: {seconds:.6} segundos\n')

	cursor.execute("SELECT password FROM users WHERE username='KEY:0'")
	result = cursor.fetchone()
	print(result)