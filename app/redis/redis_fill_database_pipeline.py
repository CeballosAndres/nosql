import time 
import db

reg = 1_000_000

# Connect to redis
client = db.redis_conn()

start_time = time.time()

print(f'Comenzando la carga de {reg:,} registros.')

with client.pipeline() as pipe:
    for n in range(reg):
        pipe.set('KEY:'+str(n), 'VALUE:'+str(n))
    pipe.execute()

seconds = (time.time() - start_time)
print(f'{reg:,} registros en: {seconds:.5} segundos\n')


