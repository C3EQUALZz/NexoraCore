DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker/app.yml
STORAGES_FILE= docker/storages.yml
CACHE_FILE = docker/cache.yml
BROKER_FILE = docker/broker.yml
APP_CONTAINER = calendar-service-app-backend


.PHONY: app
app:
	$(DC) -f $(APP_FILE) $(ENV) up --build -d

.PHONY: storages
storages:
	$(DC) -f $(STORAGES_FILE) $(ENV) up --build -d

.PHONY: cache
cache:
	$(DC) -f $(CACHE_FILE) $(ENV) up --build -d

.PHONY: broker
broker:
	$(DC) -f $(BROKER_FILE) $(ENV) up --build -d

.PHONY: all
all:
	$(DC) -f $(CACHE_FILE) -f $(STORAGES_FILE) -f $(BROKER_FILE) -f $(APP_FILE) $(ENV) up --build -d

.PHONY: all-down
all-down:
	$(DC) -f $(CACHE_FILE) -f $(STORAGES_FILE) -f $(BROKER_FILE) -f $(APP_FILE) $(ENV) down

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) ${ENV} down

.PHONY: cache-down
cache-down:
	$(DC) -f $(CACHE_FILE) $(ENV) down

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGES_FILE) ${ENV} down

.PHONY: broker-down
broker-down:
	$(DC) -f $(BROKER_FILE) ${ENV} down

.PHONY: app-shell
app-shell:
	$(EXEC) $(APP_CONTAINER) bash

.PHONY: app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f