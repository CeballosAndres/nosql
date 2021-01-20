import time
import db
import random
from neo4j import GraphDatabase


if __name__ == "__main__":
    conn = db.mysql_conn()
    cursor = conn.cursor()
    cursor.execute("select name from company where id = %s",(random.randint(0, db.records),))
    result = cursor.fetchone()
    company_name = result[0]
    conn.close()
    cursor.close()

    print(f"\nObteniendo todos los empleados de la compañia '{company_name}'")
    print("\nRealizando consulta a MySQL")
    sql = """select p.name from person as p 
            inner join works_in as r 
            on p.id = r.fk_personId
            inner join company as c
            on c.id = r.fk_companyId
            where c.name = %s;
            """

    # Un registro
    # Mysql
    conn = db.mysql_conn()
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute(sql,(company_name,))
    result = cursor.fetchall()
    seconds = (time.time() - start_time)
    print(" Empleados:")
    for person in result:
        print("  ", person[0])
    print(f" Se obtuvo en {seconds:.5} segundos")

    conn.close()
    cursor.close()

    # Neo4j
    print("\nRealizando consulta a Neo4J")
    driver = GraphDatabase.driver("bolt://localhost:7687")
    session = driver.session()
    start_time = time.time()
    result = session.run("Match (p:Person)-[r:WORK_IN]->(c:Company) where c.name = $company_name Return p.name", company_name=company_name)
    seconds = (time.time() - start_time)
    print(" Empleados:")
    for person in result.values():
        print("  ", person[0])

    session.close()
    driver.close()
    print(f" Se obtuvo en {seconds:.5} segundos")
