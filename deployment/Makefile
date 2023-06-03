help:			## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------- #

build:			## Build or rebuild services
	docker-compose -f docker-compose-local.yml build

up:				## Create and start containers
	docker-compose -f docker-compose-local.yml up -d

restart:		## Restart services
	docker-compose -f docker-compose-local.yml restart

stop:			## Stop services
	docker-compose -f docker-compose-local.yml stop

down:			## Stop and remove containers
	docker-compose -f docker-compose-local.yml down

upgrade:		## upgrade to latest migration
	docker exec -it onion alembic upgrade head

logs:			## Show logs for container
	docker logs onion -f

clear_docker:   ## Delete all docker data for this project
	docker rm -f onion onion_db
	docker image rm deployment-project
	docker volume rm deployment_onion_volume
	docker network rm deployment_default
	docker system prune -f
