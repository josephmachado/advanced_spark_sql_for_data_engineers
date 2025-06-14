
## Setup

### Codespaces

**Note** Please remember to switch off your code spaces.


### Local with Docker

**Prerequisites**:

1. [docker](https://docs.docker.com/engine/install/) & [docker compose](https://docs.docker.com/compose/)

Start the container by cloning the repo and starting the containers (note you will have to stop other containers that you mayh have runnign on port 8888 & 8080) 

```bash
git clone https://github.com/josephmachado/advanced_spark_sql_for_data_engineers.git
cd advanced_spark_sql_for_data_engineers
docker compose up -d
sleep 30
```

Open Jupyter lab at **[http://localhost:8888/lab/tree/notebooks](http://localhost:8888/lab/tree/notebooks)**.

Spark UI is available at **[http://localhost:8080](http://localhost:8080)**.

Stop container with

```bash
docker compose down
```
