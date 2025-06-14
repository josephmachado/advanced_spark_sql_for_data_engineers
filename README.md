
## Setup

### Codespaces

### Local with Docker

**Prerequisites**:

1. [docker](https://docs.docker.com/engine/install/) & [docker compose](https://docs.docker.com/compose/)

Start the container with 

```bash
docker compose up -d
sleep 30
```

Open Jupyter lab at **[http://localhost:8888/lab/tree/notebooks](http://localhost:8888/lab/tree/notebooks)**.

Spark UI is available at **[http://localhost:8080](http://localhost:8080)**.

Stop container with

```bash
docker compose down
```
