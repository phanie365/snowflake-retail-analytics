use role role_data_engineer; 
use warehouse wh_commercial_analytics; 
use database commercial_analytics; 
use schema commercial_analytics.gold; 

CREATE OR REPLACE SECURE VIEW V_SALES_BY_COUNTRY AS

SELECT
    COUNTRY,
    TOTAL_SALES,
    NUMBER_OF_ORDERS,
    AVERAGE_ORDER_AMOUNT,
    TOTAL_QUANTITY_SOLD
FROM SALES_BY_COUNTRY;