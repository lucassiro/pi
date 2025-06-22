First [install uv](https://docs.astral.sh/uv/getting-started/installation/)

To execute data ingestion
```bash
uv run -m data_ingestion.main
```

To execute dashboard
```bash
source .venv/bin/activate
streamlit run dashboard/Hello.py
```