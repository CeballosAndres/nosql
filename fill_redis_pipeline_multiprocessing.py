import multiprocessing as mp
import redis
import time 

def redis_pro(ran):
    client = redis.Redis()
    with client.pipeline() as pipe:
        for n in range(ran):
            pipe.set('key:'+str(n), 'value:'+str(n))
        pipe.execute()

if __name__ == '__main__':
    reg = 100_000
    workers = 4
    pipe_width = 10_000
    start_time = time.time()

    print(f'Comenzando la carga de {reg:,} registros.')
    
    jobs = []
    for i in range(1):
        p = mp.Process(target=redis_pro, args=(100,))
        jobs.append(p)
        p.start()

    seconds = (time.time() - start_time)
    print(f'{reg:,} registros en: {seconds:.5} segundos\n')
