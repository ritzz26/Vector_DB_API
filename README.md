# stack-ai_take_home
Vector_DB Take Home Assignment 

## Running locally
Build the image
```bash
docker build -t vector-db-api .
```

Run the container
```bash
docker run -p 8000:8000 vector-db-api
```

## Deployment with Helm:
Build image
```bash
docker build -t vector-db-api .
```
Load image into minikube
```bash
minikube image load vector-db-api
```
Install chart
```bash
helm install vector-db-api ./helmchart
```
Forward port to access API
```bash
kubectl port-forward service/vector-db-api 8000:8000
```