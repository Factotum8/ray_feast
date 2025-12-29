SERVICE_NAME := app

setup:
	@uv sync

start:
	@serve run app:ingressed_app

stop:
	@serve shutdown
	@ray stop

feast_start:
	@docker build -t feast_demo -f feast_repo/Dockerfile feast_repo/
	@docker run --rm -it -p 8000:8000 -d --name container_feast_demo feast_demo

feast_stop:
	@docker stop container_feast_demo

start_docker:
	docker build -t image_$(SERVICE_NAME):latest .
	docker run -d --name container_$(SERVICE_NAME) image_$(SERVICE_NAME):latest

stop_docker:
	docker stop container_$(SERVICE_NAME)
	docker rm container_$(SERVICE_NAME)
