use role securityadmin ; 

-- donner l'acces au warehouse 
grant usage 
on warehouse wh_commercial_analytics
to role role_data_engineer ; 

-- donner l'acces ala database 
grant usage 
on database commercial_analytics
to role role_data_engineer; 

-- donner l'acces aux schemas 
grant usage 
on schema commercial_analytics.bronze
to role role_data_engineer ;

grant usage 
on schema commercial_analytics.silver
to role role_data_engineer ; 

grant usage 
on schema commercial_analytics.gold
to role role_data_engineer ; 

-- Autoriser la creation des objets dans les schemas 
grant create table , create view , create stage 
on schema commercial_analytics.bronze
to role role_data_engineer ; 

grant create table , create view  
on schema commercial_analytics.silver
to role role_data_engineer ; 

grant create table , create view 
on schema commercial_analytics.gold
to role role_data_engineer ; 

-- faire heriter kes acces du data enge au sysadmin , donc le role data peut creer des tables , des vues  etc mais comme sysadmin est au dessus il herite automatiquement de ces capacités
grant role role_data_engineer to role sysadmin ; 

