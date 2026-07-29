use role role_data_engineer ; 
use warehouse wh_commercial_analytics; 
use database commercial_analytics; 
use schema commercial_analytics.gold ; 

alter table sales_by_country
add row access policy country_access_policy 
on (country); 