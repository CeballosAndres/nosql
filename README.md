## Install docker

```bash
# On macOS
brew cask install docker
```


## Run docker-compose

```bash
# Create
docker-compose up -d

## Recreate
docker-compose up -d --force-recreate
```

## Access data base

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
source env/bin/activate

#Install dependencies
python -m pip install redis PyMySql

# Test connections
python test_connections.py
```