import requests
import duckdb
import os

def extract_data():
   

   #File Creation
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_dir = os.path.join(project_root, "database")
    db_path = os.path.join(db_dir, "crypto_vault.db")    
    os.makedirs(db_dir, exist_ok=True)
    
    #API set up
    crypto = "ethereum"
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart"
    params = {"vs_currency": "eur", "days": "7"} 
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        rows = data['prices']
        
        con = duckdb.connect(db_path)
        con.execute("CREATE TABLE IF NOT EXISTS raw_ethereum_prices (timestamp BIGINT, price DOUBLE)")
        con.execute("CREATE TEMP TABLE staging_prices (timestamp BIGINT, price DOUBLE)")
        con.executemany("INSERT INTO staging_prices VALUES (?, ?)", rows)
        insertion = con.execute("""
            INSERT INTO raw_ethereum_prices 
            SELECT * FROM staging_prices 
            WHERE timestamp NOT IN (SELECT timestamp FROM raw_ethereum_prices)
        """).fetchall()

        rows_inserted = insertion[0][0]
        print(rows_inserted)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_data()