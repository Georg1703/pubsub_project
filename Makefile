IMAGE_NAME := sensor_data_image
CONTAINER_NAME := sensor_data_container

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --name ${CONTAINER_NAME} -d --rm -p 8000:8000 ${IMAGE_NAME}

start: build run

stop:
	docker stop ${CONTAINER_NAME}

test:
	docker exec -it ${CONTAINER_NAME} pytest test.py