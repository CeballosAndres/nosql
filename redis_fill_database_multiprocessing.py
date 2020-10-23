import multiprocessing as mp
import time 
import db

def redis_pro(first, last):
    client = db.redis_conn()
    with client.pipeline() as pipe:
        for n in range(first, last):
            pipe.set('KEY:'+str(n), 'VALUE:'+str(n))
        pipe.execute()

if __name__ == '__main__':
    reg = 1_000_000
    pipe_width = 100_000
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
