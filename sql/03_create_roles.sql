Use role securityadmin ; 

-- role technique
create role if not exists role_data_engineer ; 

-- roles metiers 
create role if not exists role_manager_france  ; 
create role if not exists role_manager_germany  ;
create role if not exists role_manager_morocco ; 
create role if not exists role_global_manager ;
create role if not exists role_finance ; 

-- role gouvernance 
create role if not exists role_auditor  ; 
