import redis
from mysql import connector
from cassandra.cluster import Cluster

records = 10

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

def cassandra_conn():
	cluster = Cluster(['0.0.0.0'], port=9042)
	return cluster.connect('CityInfo', wait_for_all_pools=True)
