use role role_data_engineer;
use warehouse wh_commercial_analytics;
use database commercial_analytics; 
use schema commercial_analytics.bronze; 

CREATE OR REPLACE STREAM SALES_RAW_STREAM
ON TABLE SALES_RAW;