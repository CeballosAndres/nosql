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

    # # 10 claves
    # start_time = time.time()
    # print(f"\nObteniendo 10 clave aleatorias:")
    # for n in range(10):   
    #     val = get_key()
    #     sql = "SELECT password FROM users WHERE username='"+val+"'"
    #     cursor.execute(sql)
    #     result = cursor.fetchone()
    #     print(f'  {val} - {result[0]}')
    # seconds = (time.time() - start_time)
    # print(f"En {seconds} segundos\n")


