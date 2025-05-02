IMAGE_NAME=vector-db-api
KUBE_NAMESPACE=default
RELEASE_NAME=vector-db-api
CHART_PATH=helmchart

VENV=venv

.PHONY: help setup run lint test docker-build docker-run docker-dev clean

help:
	@echo "Makefile commands:"
	@echo "  make setup          Set up virtualenv and install requirements"
	@echo "  make run            Run app locally with uvicorn"
	@echo "  make test           Run pytest test suite"
	@echo "  make docker-build   Build the Docker image"
	@echo "  make docker-run     Run the container locally"
	@echo "  make docker-dev     Run container with live reload (dev mode)"
	@echo "  make clean          Remove __pycache__ and .pyc files"

setup:
	pip install --upgrade pip && pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	PYTHONPATH=. pytest --cov=app --cov-report=term tests/ && make clean

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run -p 8000:8000 $(IMAGE_NAME)

docker-dev:
	docker run -v $$PWD:/app -p 8000:8000 $(IMAGE_NAME) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -delete

all: docker-build minikube-start minikube-load helm-install port-forward

minikube-start:
	@echo "Starting Minikube"
	minikube start

minikube-load:
	@echo "Loading Docker image into Minikube..."
	minikube image load $(IMAGE_NAME)

helm-install:
	@echo "Installing Helm chart..."
	helm upgrade --install $(RELEASE_NAME) $(CHART_PATH) --namespace $(KUBE_NAMESPACE) --create-namespace

port-forward:
	@echo "Port-forwarding http://localhost:8000 ..."
	@echo "Press Ctrl+C to stop."
	kubectl port-forward svc/$(RELEASE_NAME) 8000:8000