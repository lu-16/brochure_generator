IMAGE_NAME=brochure-generator
PROJECT_DIR=$(shell pwd)

.PHONY: build run

run_local:
	streamlit run app.py --server.port 8501 --server.address 0.0.0.0

build:
	docker build --platform=linux/amd64 --no-cache --build-arg DEBIAN_FRONTEND=noninteractive -t $(IMAGE_NAME) .

run:
	docker run --env-file .env -p 8501:8501 -v $(PROJECT_DIR):/app $(IMAGE_NAME)

stop:
	docker stop $$(docker ps -q --filter ancestor=$(IMAGE_NAME))

clean:
	docker rmi -f $$(docker images -q $(IMAGE_NAME))
	docker volume prune -f
	docker network prune -f
	docker container prune -f
	docker image prune -f
	docker system prune -f
