First [install uv](https://docs.astral.sh/uv/getting-started/installation/)

To execute data ingestion
```bash
uv run -m data_ingestion.main
```

To execute dashboard
```bash
uv tool install streamlit
uvx streamlit run dashboard/Hello.py
```