
Use role sysadmin

Create database COMMERCIAL_ANALYTICS ;

use database commercial_analytics; 

select 
current_role() ,
current_database() , 
current_warehouse() ; 