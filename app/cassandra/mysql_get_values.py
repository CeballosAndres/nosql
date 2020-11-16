import time
import random
import db

def get_key():
    return str(random.randint(0, db.records))

if __name__ == "__main__":
    val = get_key()
    print("\nRealizando consultas a MySQL")
    print(f"\nObteniendo 1 registro aleatorio: {val}")
    sql = "SELECT * FROM sensores WHERE id= %s"

    # Un registro
    conn = db.mysql_conn()
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute(sql,(val,))
    result = cursor.fetchone()
    seconds = (time.time() - start_time)
    print(f"  Se obtuvo {result} en {seconds:.5} segundos")

    # 10 registros
    start_time = time.time()
    print(f"\nObteniendo 10 registros aleatorios:")
    print("Lectura-Sensor-Temperatura-Humedad-Presión")
    for n in range(10):   
        val = get_key()
        sql = "SELECT * FROM sensores WHERE id= %s"
        cursor.execute(sql, (val,))
        result = cursor.fetchone()
        print(f'  {result}')
    seconds = (time.time() - start_time)
    print(f"En {seconds:.5} segundos\n")


    # Promedios por sensor
    start_time = time.time()
    sql = "SELECT avg(temperatura) FROM sensores"
    print(f"Obtener promedio de {db.records:,} registros de temperaturas: ")
    cursor.execute(sql)
    result = cursor.fetchone()
    seconds = (time.time() - start_time)
    print(f" Promedio: {result[0]:.5} en {seconds:.5} segundos\n")

    start_time = time.time()
    sql = "SELECT avg(humedad) FROM sensores"
    print(f"Obtener promedio de {db.records:,} registros de humedad: ")
    cursor.execute(sql)
    result = cursor.fetchone()
    seconds = (time.time() - start_time)
    print(f" Promedio: {result[0]:.5} en {seconds:.5} segundos\n")

    start_time = time.time()
    sql = "SELECT avg(presion) FROM sensores"
    print(f"Obtener promedio de {db.records:,} registros de presión: ")
    cursor.execute(sql)
    result = cursor.fetchone()
    seconds = (time.time() - start_time)
    print(f" Promedio: {result[0]:.5} en {seconds:.5} segundos\n")

    conn.close()