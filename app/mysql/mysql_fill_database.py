import time
import db

def execute(sql):
	conn = db.mysql_conn()
	cursor = conn.cursor()
	cursor.execute(sql)
	conn.commit()

if __name__ == '__main__':
	reg = 1_000_000
	percent = reg / 10
	
	execute("DROP TABLE IF EXISTS users")
	execute("CREATE TABLE users (username VARCHAR(45) PRIMARY KEY, password VARCHAR(45))")

	sql = "INSERT INTO users (username, password) VALUES (%s, %s)"

	conn = db.mysql_conn()
	cursor = conn.cursor()
	
	start_time = time.time()
	print(f'Comenzando la carga de {reg:,} de registros.')
	for n in range(1, reg+1):
		val = ("KEY:"+str(n), "VALUE:"+str(n))
		cursor.execute(sql, val)
		if(n % percent == 0):
			seconds = (time.time() - start_time)
			print(f'  {n/percent*10}% en: {seconds:.6} segundos')
	conn.commit()

	seconds = (time.time() - start_time)
	print(f'{reg:,} registros en: {seconds:.6} segundos\n')

	cursor.execute("SELECT password FROM users WHERE username='KEY:1'")
	result = cursor.fetchone()
	print(result)