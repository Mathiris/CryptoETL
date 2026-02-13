#Install uv 
install: 
	uv sync

#run python code, that extract data 
run-ingestion: 
	uv run python scripts/extract.py

#run dbt pipeline and tests
run-dbt: 
	uv run dbt run --project-dir dbt --profiles-dir dbt
	uv run dbt test --project-dir dbt --profiles-dir dbt

#run python file with streamlit for dataviz
run-viz: 
	uv run streamlit run scripts/app.py

#run Airflow in standalone mode
run-airflow: 
	export AIRFLOW_HOME=$(PWD)/airflow && uv run airflow standalone