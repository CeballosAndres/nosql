import redis
from mysql import connector

records = 1_000_000 

def redis_conn():
	client = redis.Redis(
		host = '192.168.1.99',
		port = 6379
		)
	return client

def mysql_conn():
	db_connection = connector.connect(
		host='192.168.1.99',
		user='root',
		password='nosql',
		database='test_db')
	return db_connection