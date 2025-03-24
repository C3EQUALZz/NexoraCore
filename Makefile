DC = docker compose
NETWORK_NAME = microservices-network

.PHONY: all network kafka user team

# 👉 Создание сети (не падать, если она уже есть)
network:
	-@docker network rm $(NETWORK_NAME)
	@docker network create $(NETWORK_NAME)

# 👉 Поднять kafka (брокер)
kafka:
	cd src/apps/kafka && $(DC) --env-file .env -f docker/production.yml up --build -d

down-kafka:
	cd src/apps/kafka && $(DC) --env-file .env -f docker/production.yml down

# 👉 Поднять user сервис
user:
	cd src/apps/user && $(DC) --env-file .env -f docker/production.yml up --build -d

down-user:
	cd src/apps/user && $(DC) --env-file .env -f docker/production.yml down

# 👉 Поднять team сервис
team:
	cd src/apps/team && $(DC) --env-file .env -f docker/production.yml up --build -d

down-team:
	cd src/apps/team && $(DC) --env-file .env -f docker/production.yml down

calendar:
	cd src/apps/calendar && $(DC) --env-file .env -f docker/production.yml up --build -d

down-calendar:
	cd src/apps/calendar && $(DC) --env-file .env -f docker/production.yml down

# 👉 Поднять всё (по порядку)
all: network kafka user team calendar

# 👉 Остановить все сервисы
down-all: down-team down-user down-kafka down-calendar
	@docker network rm $(NETWORK_NAME) || true
