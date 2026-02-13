
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select day
from "crypto_vault"."main"."daily_candle"
where day is null



  
  
      
    ) dbt_internal_test