import multiprocessing as mp
import redis
import time 

def redis_pro(first, last):
    client = redis.Redis()
    with client.pipeline() as pipe:
        for n in range(first, last):
            pipe.set('key:'+str(n), 'value:'+str(n))
        pipe.execute()

if __name__ == '__main__':
    reg = 1_000_000
    workers = 4
    pipe_width = 10_000
    start_time = time.time()

    print(f'Comenzando la carga de {reg:,} registros.')
    
    jobs = []
    for i in range(1, int((reg/pipe_width)+1)):
        first = ((i-1) * pipe_width) + 1
        last = (i * pipe_width) + 1
        p = mp.Process(target=redis_pro, args=(first, last))
        jobs.append(p)
        p.start()

    p.join()
    seconds = (time.time() - start_time)
    print(f'{reg:,} registros en: {seconds:.5} segundos\n')
