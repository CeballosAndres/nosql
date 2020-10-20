# Redis vs mySQL

## Install docker

```bash
# On macOS
brew cask install docker
```
Other OS [How to ](https://gist.github.com/rstacruz/297fc799f094f55d062b982f7dac9e41)

## Run docker-compose

```bash
# Create
docker-compose up -d

# Recreate
docker-compose up -d --force-recreate
```

## Access database

```bash
#MySQL
docker exec -it mysql-db mysql -p

#Redis
docker exec -it redis-db sh
```

## Set Python environment

```bash
# Initialize virtual environment
python3 -m venv env

# Select virtual environment
source env/bin/activate # on macOS
# on Windows .\env\Scripts\activate  

#Install dependencies
python -m pip install -r requirements.txt
```
## Test

```bash
# Test connections
python test_connections.py

# Run redis benchmark
docker exec -it redis-db redis-benchmark -q -n 100000


# Fill redis
python fill_redis.py
```
