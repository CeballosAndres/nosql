import redis
import time 

# connect to redis
client = redis.Redis(
        host = 'localhost',
        port = 6379
        )

reg = 1_000_000
percent = reg / 10

start_time = time.time()
print(f'Comenzando la carga de {reg} registros.')
for n in range(reg):
	client.set('key:'+str(n), 'value:'+str(n))
	if(n % percent == 0):
		seconds = (time.time() - start_time)
		print(f'  {n/percent*10}% en: {seconds} segundos')

seconds = (time.time() - start_time)
print(f'{reg} registros en: {seconds} segundos\n')

