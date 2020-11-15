import time
import random
import db

def get_key():
    rand = random.randint(1, db.records)
    return "KEY:"+str(rand)

if __name__ == "__main__":
    val = get_key()
    print("\nRealizando consultas a Redis")
    print(f"\nObteniendo 1 clave aleatoria: {val}")
    
    # Una clave
    conn = db.redis_conn()
    start_time = time.time()
    result = conn.get(val)

    seconds = (time.time() - start_time)
    print(f"  Se obtuvo {result} en {seconds} segundos\n")

    # 10 claves
    start_time = time.time()
    print(f"\nObteniendo 10 clave aleatorias:")
    for n in range(10):   
        val = get_key()
        result = conn.get(val)
        print(f'  {val} - {result}')
    seconds = (time.time() - start_time)
    print(f"En {seconds} segundos\n")

    values = []
    for n in range(10):
        val = get_key()
        values.append(val)

    start_time = time.time()
    result = conn.mget(values)

    seconds = (time.time() - start_time)
    print(f"Haciendo uso de mget se obtienen: {result} en {seconds} segundos\n")