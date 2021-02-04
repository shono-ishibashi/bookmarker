# development環境
.PHONY: setup
setup:
	docker-compose -f docker/docker-compose.yml build --no-cache

.PHONY: start
start:
	docker-compose -f docker/docker-compose.yml up --remove-orphans

.PHONY: start.background
start.background:
	docker-compose -f docker/docker-compose.yml up -d --remove-orphans

.PHONY: status
status:
	docker-compose -f docker/docker-compose.yml ps

.PHONY: stop
stop:
	docker-compose -f docker/docker-compose.yml down

