import redis
import time 

reg = 1_000_000
percent = reg / 10

# connect to redis
client = redis.Redis()

start_time = time.time()
print(f'Comenzando la carga de {reg:,} de registros.')
for n in range(reg):
	client.set('key:'+str(n), 'value:'+str(n))
	if(n % percent == 0):
		seconds = (time.time() - start_time)
		print(f'  {n/percent*10}% en: {seconds} segundos')

seconds = (time.time() - start_time)
print(f'{reg:,} registros en: {seconds:.6} segundos\n')

