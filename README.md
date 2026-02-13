CryptoETL: Ethereum Daily Analysis Pipeline
===========================================

**An End-to-End ETL (Extract, Transform, Load) orchestrated by Apache Airflow.**

Acknowledgments
------------------

A special thank you to **Camille Omnes** and **Gabriel Baker** for this challenging and interesting project. I truly enjoyed building this solution!

Get Started
--------------

Place yourself in the CryptoETL directory and run the following commands:

*   make install : Initializes the Python environment and synchronizes dependencies using **uv**.
    
*   make run-ingestion : Executes the Python extraction script and populates the **DuckDB** database.
    
*   make run-dbt : Runs the dbt transformation models and executes data quality tests.
    
*   make run-viz : Launches the **Streamlit** dashboard to visualize the processed data.
    
*   make run-airflow : Starts Airflow in **standalone** mode to monitor the eth\_daily\_pipeline DAG.
    

Design Decisions & Approach
-------------------------------

### Architecture Choices

*   **Dependency Management (**uv**)**: I chose uv for its extreme speed (Rust-based) and its ability to provide a perfectly reproducible environment with a single uv sync command.
    
*   **Orchestrator (**Airflow**)**: Leveraging my experience with **Google Cloud Composer**, Airflow was the natural choice. It is the industry standard for "Pipeline as Code," offering robust monitoring and scalability.
    
*   **Storage (**DuckDB**)**: I used DuckDB as an in-process OLAP database. It’s lightweight, serverless, and incredibly fast for analytical SQL queries.
    
*   **Visualization (**Plotly/Streamlit**)**: Chosen for their ability to transform raw data into interactive insights with minimal overhead.

My goal was to provide a professional-grade financial output based on the Open-High-Low-Close (OHLC) chart standard.

This type of data modeling is essential for technical analysis as it captures the market's volatility and price action over a specific timeframe (daily, in this case). By structuring the data this way, I ensure that the output is ready for any professional charting tool or financial analyst to consume, providing more depth than a simple average price.

https://en.wikipedia.org/wiki/Open-high-low-close_chart

ETL Process
---------------

### 1\. Extract & Load

The initial goal was to use **Airbyte** via the PyAirbyte connector. However, during implementation, I encountered significant schema and date-parsing issues with the CoinGecko connector despite following the documentation.

To ensure project delivery and focus on the transformation logic, I switched to a custom Python extraction script using the CoinGecko API.

*   **Incremental Strategy**: I implemented a logic to insert only new records based on the latest timestamp to ensure a clean, duplicate-free history in DuckDB.
    

### 2\. Transform (dbt)

I implemented a dbt model to generate **Daily OHLC candles** (Open, High, Low, Close) for Ethereum,

*   **Key Logic**: Used Window Functions (ROW\_NUMBER) to accurately identify opening and closing prices within a daily window.
    
*   **Business Metric**: Added a daily\_change\_pct column to calculate the percentage difference between the start and end of the day.
    
*   **Data Quality**: Integrated dbt tests (unique, not\_null) to ensure the reliability of the final table.
    

### 3\. Orchestration (Airflow)

I configured a DAG (eth\_daily\_pipeline) scheduled to run @daily. To keep the local setup simple yet powerful, I used **Airflow Standalone**.The workflow is divided into three distinct tasks:

1.  **Ingestion**: Fetching raw data from the API.
    
2.  **Transformation**: Running dbt models.
    
3.  **Validation**: Running dbt tests to confirm data integrity.
    


