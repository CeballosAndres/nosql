from mysql.connector import errorcode
import db

# connect to redis
client = db.redis_conn()
# set a key
client.set('test-redis', 'Redis OK')
# get a value
value = client.get('test-redis')
print(value)

# Test connection with mysql
try:
	db_connection = db.mysql_conn()
	print("Database connection made!")
except connector.Error as error:
	if error.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database doesn't exist")
	elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("User name or password is wrong")
	else:
		print(error)
else:
	db_connection.close()

# Test connection with cassandra cluster
session = db.cassandra_conn()
#session.execute('USE CityInfo')
rows = session.execute('SELECT * FROM users')
for row in rows:
	print(row.age, row.name, row.username)