
-- appliquer la politique sur l'adress client 
alter table sales_clean
modify column CUSTOMER_ADDRESS
set masking policy customer_address_masking_policy force; 

-- Appliquer la politique sur le téléphone du client
ALTER TABLE SALES_CLEAN
MODIFY COLUMN CUSTOMER_PHONE
SET MASKING POLICY CUSTOMER_PHONE_MASKING_POLICY;

