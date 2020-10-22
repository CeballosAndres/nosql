from mysql import connector
from mysql.connector import errorcode


db_connection = connector.connect(
		host='localhost',
		user='root', 
		password='nosql', 
		database='test_db'
	)
