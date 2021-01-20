from mysql import connector

records = 10

def mysql_conn():
	db_connection = connector.connect(
		host='localhost',
		user='root',
		password='nosql',
		database='test_db')
	return db_connection
