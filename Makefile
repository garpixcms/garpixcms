include .env
export

precommit:
	pre-commit install & pre-commit run --all-files

run:
	docker-compose up -d
	make precommit
	python3 backend/manage.py runserver

down:
	docker-compose down

up:
	docker-compose up -d

build:
	docker-compose build

stop:
	docker-compose stop

start:
	docker-compose start

restart:
	docker-compose restart

psql:
	docker-compose exec postgres psql -U $(POSTGRES_USER) $(POSTGRES_DATABASE)

shell:
	python3 backend/manage.py shell

qa:
	python3 backend/manage.py qa

logs:
	docker-compose logs --tail 100

ps:
	docker-compose ps

install:
	pipenv install
	pipenv shell
	docker-compose up -d
	python3 backend/manage.py makemigrations
	python3 backend/manage.py migrate
	python3 backend/manage.py createsuperuser
	make precommit
	make run

destroy:
	make down
	rm -rf ./data/

release:
	sed -i 's/^$(VERSION_NAME)=.*/$(VERSION_NAME)=$(TAG)/g' .env
	make down
	make up

createsuperuser:
	python3 backend/manage.py createsuperuser

makemigrations:
	python3 backend/manage.py makemigrations

migrate:
	python3 backend/manage.py migrate
