import streamlit as st
import duckdb
import os


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_path, 'database', 'crypto_vault.db')
con = duckdb.connect(db_path, read_only=True)

st.set_page_config(page_title="ETH Dashboard", layout="wide")

st.title("Ethereum Price")

df = con.execute("""
    SELECT day, close_price 
    FROM daily_candle 
    ORDER BY day ASC
""").df()

st.line_chart(df, x="day", y="close_price")
st.dataframe(df.tail(7), use_container_width=True)