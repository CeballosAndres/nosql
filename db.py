import redis
from mysql import connector

records = 1_000_000 

def redis_conn():
	client = redis.Redis(
		host = 'localhost',
		port = 6379
		)
	return client

def mysql_conn():
	db_connection = connector.connect(
		host='localhost',
		user='root',
		password='nosql',
		database='test_db')
	return db_connection
