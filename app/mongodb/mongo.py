import time
import datetime
from pymongo import MongoClient
from faker import Faker
from mysql import connector
import db

reg = db.records
percent = reg / 10


def execute(sql):
    conn = db.mysql_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def insert_to_mysql(data):
    execute("DROP TABLE IF EXISTS comentario")
    execute("DROP TABLE IF EXISTS tweet")
    execute("DROP TABLE IF EXISTS usuario")

    execute("""CREATE TABLE usuario (
			id int NOT NULL PRIMARY KEY,
			usuario varchar(45),
			nombre varchar(100),
			direccion varchar(200),
			email varchar(55),
			descripcion varchar(55),
			foto_perfil varchar(45)
			)
		""")

    execute("""CREATE TABLE tweet (
			id int NOT NULL PRIMARY KEY,
			fk_usuario int NOT NULL,
            fecha_publicacion datetime,
            contenido varchar(55),
            likes int,
            retwits int,
            FOREIGN KEY (fk_usuario) REFERENCES usuario(id)
			)
		""")

    execute("""CREATE TABLE comentario (
			id int NOT NULL PRIMARY KEY,
			fk_tweet int NOT NULL,
            contenido varchar(55),
            autor varchar(55),
            fecha_comentario datetime,
            FOREIGN KEY (fk_tweet) REFERENCES tweet(id)
			)
		""")

    insert_user = """INSERT INTO usuario (
        id, 
        usuario,
        nombre,
        direccion,
        email,
        descripcion,
        foto_perfil
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    insert_tweet = """INSERT INTO tweet (
        id,
        fk_usuario,
        fecha_publicacion,
        contenido,
        likes,
        retwits
        ) VALUES (%s, %s, %s, %s, %s, %s)"""

    insert_comentario = """INSERT INTO comentario (
        id,
        fk_tweet,
        contenido,
        autor,
        fecha_comentario
        ) VALUES (%s, %s, %s, %s, %s)"""

    conn = db.mysql_conn()
    cursor = conn.cursor()

    user_id = 0
    tweet_id = 0
    comment_id = 0

    for user in data:
        val = (user_id,
               user['usuario'],
               user['nombre'],
               user['direccion'],
               user['email'],
               user['descripcion'],
               user['foto_perfil'],
               )
        cursor.execute(insert_user, val)

        for tweet in user['tweets']:
            val = (tweet_id,
                   user_id,
                   tweet['fecha_publicacion'],
                   tweet['contenido'],
                   tweet['likes'],
                   tweet['retwits'],
                   )
            cursor.execute(insert_tweet, val)

            for comment in tweet['comentarios']:
                val = (comment_id,
                       tweet_id,
                       comment['contenido'],
                       comment['autor'],
                       comment['fecha_comentario'],
                       )
                cursor.execute(insert_comentario, val)
                comment_id += 1
            tweet_id += 1
        user_id += 1

        conn.commit()


def create_data(seed=4000, tweets=10, comments=10):
    fake = Faker('es_MX')
    Faker.seed(seed)
    tweets_dic = []
    for _ in range(tweets):
        comments_dic = []
        for _ in range(comments):
            comments_dic.append(
                {
                    'contenido': fake.text(50),
                    'autor': fake.user_name(),
                    'fecha_comentario': fake.date_time()
                }
            )
        tweets_dic.append(
            {
                'fecha_publicacion': fake.date_time(),
                'contenido': fake.text(50),
                'likes': fake.random_int(max=100),
                'retwits': fake.random_int(max=100),
                'comentarios': comments_dic
            }
        )

    return {
        'usuario': fake.user_name(),
        'nombre': fake.name(),
        'direccion': fake.address(),
        'email': fake.email(),
        'descripcion': fake.text(50),
        'foto_perfil': fake.file_name(extension='jpg'),
        'tweets': tweets_dic
    }


def insert_to_mongo(registros):
    client = MongoClient('localhost', port=27017,
                         username='nosql', password='test_db')
    db = client['twitter']
    db.drop_collection('users')
    col = db['users']
    col.insert_many(registros)


if __name__ == "__main__":
    registros = []

    print(f"Iniciando con la generación de {reg:,} usuarios.")
    print("Cada usuario con 10 tweets, y cada tweet con 10 comentarios.")
    start_time = time.time()
    for i in range(reg):
        registros.append(create_data(seed=i, tweets=10, comments=10))
    seconds = (time.time() - start_time)
    print(f' {reg:,} usuarios generados en: {seconds:.6} segundos\n')

    print(f'MONGO: Comenzando la carga de {reg:,} de usuarios.')
    start_time = time.time()
    insert_to_mongo(registros)
    seconds = (time.time() - start_time)
    print(f' {reg:,} registros en: {seconds:.6} segundos\n')

    print(f'MySQL: Comenzando la carga de {reg:,} de usuarios.')
    start_time = time.time()
    insert_to_mysql(registros)
    seconds = (time.time() - start_time)
    print(f' {reg:,} registros en: {seconds:.6} segundos\n')
