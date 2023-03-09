#!make

env_arg := --env-file ./api/.env

compose := docker compose

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "    up           Run docker containers"
	@echo "    stop         Stop docker containers"
	@echo "    rm           Stop and remove docker containers"
	@echo "    rmi          Stop and remove docker containers with their images and volumes"
	@echo "    logs         Stdout logs from docker containers"
	@echo "    sh SERVICE   Run the command line in the selected SERVICE docker container"

up:
	@$(compose) $(env_arg) up -d

stop:
	@$(compose) $(env_arg) stop

rm:
	@$(compose) $(env_arg) down

rmi:
	@$(compose) $(env_arg) down --rmi all -v

logs:
	@$(compose) logs -f

sh:
	@docker exec -it $(firstword $(filter-out $@,$(MAKEOVERRIDES) $(MAKECMDGOALS))) sh
