# Vector Database REST API (Production Ready)

A lightweight and production-ready vector database system with a REST API using FastAPI. This system supports storing libraries of documents and chunks, indexing embeddings, and performing fast k-Nearest Neighbor (kNN) searches.

Designed for ease of use, containerization, and Kubernetes deployment.

---

## Features

- CRUD operations for Libraries, Documents, and Chunks
- k-Nearest Neighbor search (cosine similarity)
- Thread-safe in-memory store
- Disk persistence (state saved and restored on restart)
- Simple API Key authentication for all endpoints
- Dockerized for easy deployment
- Kubernetes ready (Helm chart included)
- GitHub Actions CI for test automation

---

## Core Concepts

### Chunk
A piece of text with an embedding and metadata.

### Document
A collection of chunks with metadata.

### Library
A collection of documents with metadata.

---

## Getting Started

### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the API Locally

```bash
make run
```

Access the API at:

```
http://localhost:8000/docs
```

## Running Tests

```bash
make test
```

---

## Docker Usage

### Build the Image

```bash
make docker-build
```

### Run the Container

```bash
make docker-run
```

Access the API at:

```
http://localhost:8000/docs
```

---

## Kubernetes Deployment (Minikube)

### Start Minikube

```bash
minikube start
```

### Load Docker Image into Minikube

```bash
make minikube-load
```

### Deploy with Helm

```bash
make helm-install
```

### Access the API

```bash
kubectl port-forward svc/vector-db-api 8000:8000
```

> Access at `http://localhost:8000/docs`

---

## Persistence

The system saves state to `db_state.json` on every update, ensuring that data survives container or pod restarts.

- Uses atomic file saves to avoid corruption
- Automatically loads state on startup

---

## Kubernetes Readiness

The Helm chart includes:

- Liveness and Readiness probes (check `/docs` endpoint)
- Service and Deployment definitions
- Default replica count of 1

---

## CI/CD (GitHub Actions)

- Automatically runs tests on push and pull requests
- Ensures correctness before deployment

---

## API Documentation

Once running, access full API docs at:

```
http://localhost:8000/docs
```

Interactive Swagger UI provided by FastAPI.

---


## TODO for the future

- Add metadata filtering
- Add advanced index structures (KD-Tree, HNSW)
