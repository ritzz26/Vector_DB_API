# Vector Database REST API (Production Ready)

A lightweight and production-ready vector database system with a REST API using FastAPI. This system supports storing libraries of documents and chunks, indexing embeddings, and performing fast k-Nearest Neighbor (kNN) searches.

Designed for ease of use, containerization, and Kubernetes deployment.

---

## Project Structure 
```
root/
├── .dockerignore
├── .python-version
├── Dockerfile
├── Makefile
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── api/
│   ├── db/
│   ├── services/
├── tests/
├── helmchart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
└── db_state.json (generated at runtime)
```


---

## Getting Started

### Install Dependencies (Recommended Python 3.11)

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
make port-forward
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

## Technical Decisions for Indexing Algorithms
1. Linear Scan (Brute Force):
    - Compare the query vector to every stored chunk vector
    - Time Complexity: O(N)
    - Space Complexity: O(N)
    - Simple and effective for small to medium datasets. Works reliably and doesn't need pre-processing which can reduce costs

2. Grid-based Index:
    - Hash vectors into buckets based on the embedding dimensions. Search is limited to the bucket and its neighbors
    - Time Complexity: O(K) (K neighbors in the bucket)
    - Space Complexity: O(N)
    - Speeds up search when vectors are evenly distributed.

3. Sorted List Index:
    - Store vectors sorted by their L2 norms. Use binary search to narrow down candidates. 
    - Time Complexity: O(log N + K)
    - Space Complexity: O(N)
    - Effective when norms correlate with similarity and reduces search space. 

---

## Developer Notes

- Python version required: 3.11.x
- `.python-version` included for pyenv users
- use `make` for all common dev and deployment tasks

## TODO for the future

- Add metadata filtering
- Add advanced index structures (KD-Tree, HNSW)
- Authentication using OAuth2 or JWT

## License

MIT License