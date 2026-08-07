
use role securityadmin; 
 -- Autoriser les roles a utiliser le warehouse 
 grant usage on warehouse wh_commercial_analytics
 to role role_manager_france ; 

  grant usage on warehouse wh_commercial_analytics
 to role role_manager_germany ; 

  grant usage on warehouse wh_commercial_analytics
 to role role_manager_morocco ; 

  grant usage on warehouse wh_commercial_analytics
 to role role_global_manager ; 

 -- Autoriser l'acces a la base 
  grant usage on database commercial_analytics
 to role role_manager_france ; 

  grant usage on database commercial_analytics
 to role role_manager_germany ; 

  grant usage on database commercial_analytics
 to role role_manager_morocco ;

  grant usage on database commercial_analytics
 to role role_global_manager ; 

 -- Autoriser l'accès aux schemas 
  grant usage on schema commercial_analytics.gold
 to role role_manager_france ;
 
   grant usage on schema commercial_analytics.gold
 to role role_manager_morocco ; 

   grant usage on schema commercial_analytics.gold
 to role role_manager_germany ; 

   grant usage on schema commercial_analytics.gold
 to role role_global_manager ; 

 -- Autoriser la lecture de sales_by_country
   grant select on table  commercial_analytics.gold.sales_by_country
 to role role_manager_france ; 

   grant select on table  commercial_analytics.gold.sales_by_country
 to role role_manager_germany ; 

   grant select on table  commercial_analytics.gold.sales_by_country
 to role role_manager_morocco ; 

   grant select on table  commercial_analytics.gold.sales_by_country
 to role role_global_manager; 

 --- Attribuer les roles a un utilisateur 
use role securityadmin; 
 
 grant role role_manager_france
 to user didi242 ; 

  grant role role_manager_germany
 to user didi242 ; 

  grant role role_manager_morocco
 to user didi242 ; 

  grant role role_global_manager
 to user didi242 ; 

 -- tests
 use role role_manager_france;
 use warehouse wh_commercial_analytics; 
 use database commercial_analytics; 
 use schema commercial_analytics.gold; 

select current_role() ;

-- mettre use CURRENT_SECONDARY_ROLES NONE parceque le is_role_in_session regarde tous les roles secondaires actifs 
USE SECONDARY ROLES NONE;

SELECT CURRENT_SECONDARY_ROLES();

 select * from sales_by_country
 order by country; 