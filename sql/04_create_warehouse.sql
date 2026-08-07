use role sysadmin;

-- creer un warehouse 
create warehouse if not exists wh_commercial_analytics
with 
warehouse_size='xsmall'
auto_resume=true
auto_suspend=60
initially_suspended=true;

use warehouse wh_commercial_analytics;

show warehouses like 'wh_commercial_analytics';
