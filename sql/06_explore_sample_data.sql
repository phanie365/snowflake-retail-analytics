show databases;

use database snowflake_sample_data;
show schemas ;

use schema tpch_sf1 ;
show tables ; 

select * from customer limit 10 ; 
select * from orders limit 10 ;
select * from lineitem limit 10 ;

select * from snowflake_sample_data.tpch_sf1.nation limit 10 ; 
select * from part limit 10 ;
