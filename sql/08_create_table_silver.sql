use role role_data_engineer;
use warehouse wh_commercial_analytics;
use database commercial_analytics; 
use schema commercial_analytics.silver;

CREATE OR REPLACE TABLE SALES_CLEAN AS

SELECT
    SALE_ID,
    SALE_DATE,
    COUNTRY,
    CUSTOMER_NAME,
    CUSTOMER_ADDRESS,
    CUSTOMER_PHONE,
    PRODUCT_NAME,
    PRODUCT_BRAND,
    PRODUCT_TYPE,
    QUANTITY,
    EXTENDED_PRICE,
    DISCOUNT,
    TAX,

    EXTENDED_PRICE * (1 - DISCOUNT) AS NET_AMOUNT,

    EXTENDED_PRICE
        * (1 - DISCOUNT)
        * (1 + TAX) AS TOTAL_AMOUNT

FROM BRONZE.SALES_RAW;

select * from sales_clean;

SELECT
    EXTENDED_PRICE,
    DISCOUNT,
    TAX,
    NET_AMOUNT,
    TOTAL_AMOUNT
FROM SALES_CLEAN
LIMIT 10;