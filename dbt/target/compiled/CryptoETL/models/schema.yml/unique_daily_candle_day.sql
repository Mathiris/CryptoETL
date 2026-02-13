
    
    

select
    day as unique_field,
    count(*) as n_records

from "crypto_vault"."main"."daily_candle"
where day is not null
group by day
having count(*) > 1


