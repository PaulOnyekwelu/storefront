build:
	docker compose -f ./local.yml up --build -d --remove-orphans

up:
	docker compose -f ./local.yml up

down:
	docker compose -f ./local.yml down

down-v:
	docker compose -f ./local.yml down -v