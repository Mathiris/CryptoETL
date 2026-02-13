
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select low_price
from "crypto_vault"."main"."daily_candle"
where low_price is null



  
  
      
    ) dbt_internal_test