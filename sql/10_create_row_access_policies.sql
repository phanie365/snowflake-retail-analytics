use role role_data_engineer ;
use warehouse wh_commercial_analytics;
use database commercial_analytics; 
use schema commercial_analytics.gold ; 

CREATE OR REPLACE ROW ACCESS POLICY COUNTRY_ACCESS_POLICY

AS (ROW_COUNTRY VARCHAR)

RETURNS BOOLEAN ->

    IS_ROLE_IN_SESSION('ROLE_GLOBAL_MANAGER')

    OR IS_ROLE_IN_SESSION('ROLE_DATA_ENGINEER')

    OR (
        IS_ROLE_IN_SESSION('ROLE_MANAGER_FRANCE')
        AND ROW_COUNTRY = 'FRANCE'
    )

    OR (
        IS_ROLE_IN_SESSION('ROLE_MANAGER_GERMANY')
        AND ROW_COUNTRY = 'GERMANY'
    )

    OR (
        IS_ROLE_IN_SESSION('ROLE_MANAGER_MOROCCO')
        AND ROW_COUNTRY = 'MOROCCO'
    );