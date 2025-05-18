

```bash
# create fake data
uv sync
source .venv/bin/activate
python setup/create_tpch_data.py --sf 0.25 --output ./data/

docker compose up -d 
sleep 30 && open http://localhost:8888/doc/tree/notebooks/
```

Setup Spark tables and insert data

```bash
docker compose down
```
