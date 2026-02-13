-- models/daily_candles.sql


{{ config(materialized='table') }}

WITH raw_data AS (
    SELECT 
        epoch_ms(timestamp) as price_timestamp,
        price
    FROM raw_ethereum_prices
),

daily_prices AS (
    SELECT 
        date_trunc('day', price_timestamp) as day,
        price,
        price_timestamp,
        ROW_NUMBER() OVER (PARTITION BY date_trunc('day', price_timestamp) ORDER BY price_timestamp ASC) as row_asc,
        ROW_NUMBER() OVER (PARTITION BY date_trunc('day', price_timestamp) ORDER BY price_timestamp DESC) as row_desc
    FROM raw_data
)

SELECT 
    day,
    MAX(CASE WHEN row_asc = 1 THEN price END) as open_price,
    MAX(price) as high_price,
    MIN(price) as low_price,
    MAX(CASE WHEN row_desc = 1 THEN price END) as close_price,
FROM daily_prices
GROUP BY 1
ORDER BY 1 DESC