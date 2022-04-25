all:
	docker-compose up -d

clean:
	docker-compose down -v

force_clean:
	docker stop kafka-manager kafka-manager-db kafka kafka-zk | xargs docker rm

test:
	docker exec -it kafka-manager bash -c "cd /code && coverage run --source='.' manage.py test --parallel && coverage combine && coverage report || rm -f .coverage.*"

makemigrations:
	docker exec -it kafka-manager bash -c "cd /code && python3 manage.py makemigrations kafka_manager_app"

migrate:
	docker exec -it kafka-manager bash -c "cd /code && python3 manage.py migrate"

createsuperuser:
	docker exec -it kafka-manager bash -c "cd /code && python3 manage.py createsuperuser"

clear_docker_space:
	docker volume ls -qf dangling=true | xargs docker volume rm || true
	docker images --filter "dangling=true" -q --no-trunc | xargs docker rmi || true
	docker ps -qa --no-trunc --filter "status=exited" | xargs docker rm || true
