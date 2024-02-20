build:
	docker compose -f ./local.yml up --build -d --remove-orphans

up:
	docker compose -f ./local.yml up -d

down:
	docker compose -f ./local.yml down

down-v:
	docker compose -f ./local.yml down -v

make-migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

createsuperuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser
