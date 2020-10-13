import redis
from mysql import connector
from mysql.connector import errorcode

# connect to redis
client = redis.Redis(
        host = 'localhost',
        port = 6379
        )

# set a key
client.set('test-redis', 'Redis OK')

# get a value
value = client.get('test-redis')
print(value)


try:
	db_connection = connector.connect(host='localhost', user='root', password='nosql', database='test_db')
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
