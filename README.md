![alt text](https://static.tildacdn.com/tild3561-6163-4531-b662-383539366166/WIS_LOGO_white_NEW.svg)

# Documentation for Hexagonal Architecture project

---

# How to start a project

* Clone project

```bash
git clone https://github.com/WISPukh/OnionRepresentation.git 
```

* Navigate to project directory

```bash
cd OnionRepresentation
```

* Copy .env parameters

```bash
cp .env.example .env
```

* Navigate to deployment directory

```bash
cd deployment
```

* The following command will start project in docker containers:

```bash
make up
```

* This command will stop containers:

```bash
make stop
```

_TIP_

* To list all possible command run this command: 

```bash
make help
```

## Swagger link:

### **http://localhost:8004/docs**


# Troubleshooting

### If you got 

### If for some reason you don't have make installed here are all commands, just copy and paste them.

* Build or rebuild services

```bash
docker-compose -f docker-compose-local.yml build
```

* Create and start containers

```bash
docker-compose -f docker-compose-local.yml up -d
```

* Restart services

```bash
docker-compose -f docker-compose-local.yml restart
```

* Stop services

```bash
docker-compose -f docker-compose-local.yml stop
```

* Stop and remove containers

```bash
docker-compose -f docker-compose-local.yml down
```

* Upgrade to latest migration
	
```bash
docker exec -it onion alembic upgrade head
```

* Show logs for container

```bash
docker logs onion -f
```

* Delete all docker data for this project

```bash
docker rm -f onion onion_db
docker image rm onionrepresentation-project
docker volume rm onionrepresentation_onion_volume
docker network rm onionrepresentation_default
docker system prune -f
```
