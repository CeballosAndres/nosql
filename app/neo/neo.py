import time
from faker import Faker
import db
import random
from neo4j import GraphDatabase


reg = db.records
percent = reg / 10


def execute(sql):
    conn = db.mysql_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def insert_to_mysql(data):
    execute("DROP TABLE IF EXISTS works_in")
    execute("DROP TABLE IF EXISTS person")
    execute("DROP TABLE IF EXISTS company")

    execute("""CREATE TABLE company (
			id int NOT NULL PRIMARY KEY,
            name varchar(55),
			address varchar(200)
			)
		""")

    execute("""CREATE TABLE person (
			id int NOT NULL PRIMARY KEY,
			name varchar(100),
			address varchar(200),
			email varchar(55)
			)
		""")

    execute("""CREATE TABLE works_in (
			id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
			fk_personId int NOT NULL,
			fk_companyId int NOT NULL,
            since int,
            FOREIGN KEY (fk_personId) REFERENCES person(id),
            FOREIGN KEY (fk_companyId) REFERENCES company(id)
			)
		""")

    insert_company = """INSERT INTO company (
        id,
        name,
        address
        ) VALUES (%s, %s, %s)"""

    insert_person = """INSERT INTO person (
        id, 
        name,
        address,
        email
        ) VALUES (%s, %s, %s, %s)"""

    insert_works_in = """INSERT INTO works_in (
        fk_companyId,
        fk_personId,
        since
        ) VALUES (%s, %s, %s)"""

    conn = db.mysql_conn()
    cursor = conn.cursor()

    company_id = 0
    person_id = 0

    for company in data:
        val = (company_id,
               company['name'],
               company['address'],
               )
        cursor.execute(insert_company, val)

        for person in company['persons']:
            val = (person_id,
                   person['name'],
                   person['address'],
                   person['email'],
                   )
            cursor.execute(insert_person, val)

            val = (
                company_id,
                person_id,
                person['since'],
            )
            cursor.execute(insert_works_in, val)
            person_id += 1

        company_id += 1
        conn.commit()


def insert_to_neo4j(data):
    driver = GraphDatabase.driver("bolt://localhost:7687")
    session = driver.session()
    session.run("CREATE OR REPLACE DATABASE neo4j")

    for company in data:
        session.run(
            "CREATE (c:Company {name: $com_name})", com_name=company['name']
        )
        for person in company['persons']:
            session.run(
                "MATCH (c:Company) where c.name = $com_name CREATE (p:Person {name: $per_name})-[r:WORK_IN]->(c)", com_name=company['name'], per_name=person['name']
            )

    session.close()
    driver.close()


def create_data(seed=4000, persons_min=5, persons_max=15):
    fake = Faker('es_MX')
    Faker.seed(seed)

    person = []
    for _ in range(random.randint(persons_min, persons_max)):
        person.append(
            {
                'name': fake.name(),
                'address': fake.address(),
                'email': fake.email(),
                'since': fake.year()
            }
        )

    return {
        'name': fake.bs(),
        'address': fake.address(),
        'persons': person
    }


if __name__ == "__main__":
    persons_min = 5
    persons_max = 15
    registros = []

    print(f"Iniciando con la generación de {reg:,} empresas.")
    print(f"Cada empresa con entre {persons_min} y {persons_max}.")
    start_time = time.time()
    for i in range(reg):
        registros.append(create_data(
            seed=i, persons_min=persons_min, persons_max=persons_max))
    seconds = (time.time() - start_time)
    print(f' {reg:,} usuarios generados en: {seconds:.6} segundos\n')

    print(f'Neo4j: Comenzando la carga de {reg:,} de usuarios.')
    start_time = time.time()
    insert_to_neo4j(registros)
    seconds = (time.time() - start_time)
    print(f' {reg:,} registros en: {seconds:.6} segundos\n')

    print(f'MySQL: Comenzando la carga de {reg:,} de usuarios.')
    start_time = time.time()
    insert_to_mysql(registros)
    seconds = (time.time() - start_time)
    print(f' {reg:,} registros en: {seconds:.6} segundos\n')
