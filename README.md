

**Prerequisites**:

1. [uv](https://docs.astral.sh/uv/getting-started/installation/)


```bash
# create fake data
uv sync
source .venv/bin/activate
python generate_data.py --sf 0.5 --format csv
python -m ipykernel install --user --name=venv --display-name="My Virtual Environment"

jupyter lab # this opens http://localhost:8888/lab
# stop with Ctrl + c
```

