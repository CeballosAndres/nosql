from mysql import connector

records = 100_000

def mysql_conn():
	db_connection = connector.connect(
		host='localhost',
		user='root',
		password='nosql',
		database='test_db')
	return db_connection
