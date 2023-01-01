# Production
prod_run:
	docker compose -f docker-compose.prod.yml down --remove-orphans --volumes
	docker compose down --remove-orphans --volumes
	docker compose -f docker-compose.prod.yml up -d
prod_update:
	docker compose -f docker-compose.prod.yml down --remove-orphans --volumes
	docker compose down --remove-orphans --volumes
	docker compose -f docker-compose.prod.yml up -d --build
update:
	docker-compose down --remove-orphans --volumes
	docker-compose up -d --build

# Development environment
run-build:
	docker-compose up --build
run:
	docker-compose up
down:
	docker-compose down --remove-orphans --volumes
logs:
	docker-compose logs -f
seed:
	docker exec -it esus_dashboard_api bash -c "FLASK_APP=app/__init__.py && \
	flask seed"
terminal:
	docker exec -it esus_dashboard_api bash
shell:
	docker exec -it esus_dashboard_api bash -c "flask shell"
migrate:
	docker exec -it esus_dashboard_api bash -c "flask db upgrade"
makemigrations:
	docker exec -it esus_dashboard_api bash -c 'flask db migrate -m "$(m)"'