
use role role_data_engineer ; 
use warehouse wh_commercial_analytics; 
use database commercial_analytics; 
use schema commercial_analytics.silver ; 


-- Politique pour masquer l'adresse des clients
CREATE OR REPLACE MASKING POLICY CUSTOMER_ADDRESS_MASKING_POLICY
AS (VALUE VARCHAR) RETURNS VARCHAR ->
    CASE
        WHEN IS_ROLE_IN_SESSION('ROLE_DATA_ENGINEER')
            THEN VALUE
        ELSE '******** ADDRESS MASKED ********'
    END;

-- Politique pour masquer le numero de telephone des clients 
CREATE OR REPLACE MASKING POLICY CUSTOMER_PHONE_MASKING_POLICY
AS (VALUE VARCHAR)
RETURNS VARCHAR ->
    CASE
        WHEN IS_ROLE_IN_SESSION('ROLE_DATA_ENGINEER')
            THEN VALUE
        ELSE '***-***-****'
    END;