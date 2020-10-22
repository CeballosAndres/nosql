import multiprocessing as mp
import redis
import time 

def redis_pro():
    client = redis.Redis()
    with client.pipeline() as pipe:
        for n in range(10000):
            pipe.set('key:'+str(n), 'value:'+str(n))
        pipe.execute()

if __name__ == '__main__':
    reg = 100_000
    workers = 4
    pipe_width = 10_000
    start_time = time.time()

    print(f'Comenzando la carga de {reg:,} registros.')
    
    jobs = []
    for i in range(100):
        p = mp.Process(target=redis_pro)
        jobs.append(p)
        p.start()

    seconds = (time.time() - start_time)
    print(f'{reg:,} registros en: {seconds:.5} segundos\n')