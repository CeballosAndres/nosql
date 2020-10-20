import redis
import time 

# connect to redis
client = redis.Redis(
        host = 'localhost',
        port = 6379
        )

reg = 1_000

start_time = time.time()
print(f'Comenzando la carga de {reg} registros.')

whit client.pipeline() as pipe:
    for n in range(reg):
	    pipe.set('key:'+str(n), 'value:'+str(n))
    pipe.execute()

seconds = (time.time() - start_time)
print(f'{reg} registros en: {seconds} segundos\n')

