# 🛡️ POC Snowflake – Gouvernance et Sécurisation des Données

> **Une seule plateforme de données. Des accès adaptés à chaque utilisateur.**

## 📖 Contexte métier

Une entreprise internationale du secteur du retail est implantée dans plusieurs pays :

- 🇫🇷 France
- 🇩🇪 Allemagne
- 🇲🇦 Maroc

Afin de faciliter l'analyse des données et d'éviter la multiplication des plateformes, l'entreprise souhaite **centraliser l'ensemble de ses données dans Snowflake**.

Le principal défi consiste à garantir que chaque collaborateur accède uniquement aux données qui lui sont autorisées, tout en conservant une plateforme unique.

Ce Proof of Concept répond à ce besoin en mettant en œuvre les mécanismes de gouvernance et de sécurité proposés par Snowflake.

---

# 🎯 Objectifs

Ce projet a pour objectif de démontrer qu'il est possible de :

- Centraliser les données sur une plateforme unique.
- Restreindre l'accès aux données selon le rôle métier.
- Protéger les données sensibles grâce au masquage dynamique.
- Garantir un accès sécurisé sans dupliquer les données.
- Automatiser les traitements avec les fonctionnalités natives de Snowflake.

---

# 🏗️ Architecture du projet

```
                Sources

                   │

              Bronze Layer

                   │

              Silver Layer

                   │

               Gold Layer

                   │

        Gouvernance & Sécurité

       • Business Roles
       • Privileges
       • Row Access Policies
       • Masking Policies

                   │

              Utilisateurs
```

---

# 🔐 Modèle de gouvernance

La sécurité repose sur plusieurs mécanismes complémentaires.

## 👤 Business Roles

Des rôles métiers ont été créés afin de représenter les différents profils de l'entreprise.

Exemple :

- ROLE_MANAGER_FRANCE
- ROLE_MANAGER_GERMANY
- ROLE_MANAGER_MOROCCO
- ROLE_GLOBAL_MANAGER
- ROLE_DATA_ENGINEER

---

## 🔑 Gestion des privilèges

Chaque rôle reçoit uniquement les autorisations nécessaires.

Par exemple :

- accès aux bases de données
- accès aux warehouses
- lecture des tables
- exécution des traitements

Les privilèges sont attribués selon les responsabilités de chaque rôle.

---

## 🛡️ Row Access Policies

Les politiques de filtrage permettent d'afficher uniquement les lignes correspondant au pays de l'utilisateur connecté.

Exemple :

| Rôle | Données visibles |
|------|------------------|
| ROLE_MANAGER_FRANCE | France |
| ROLE_MANAGER_GERMANY | Allemagne |
| ROLE_MANAGER_MOROCCO | Maroc |
| ROLE_GLOBAL_MANAGER | Tous les pays |

---

## 🔒 Masking Policies

Les données sensibles sont automatiquement masquées selon le rôle connecté.

Exemple :

| Rôle | Adresse | Téléphone |
|------|----------|------------|
| Data Engineer | Visible | Visible |
| Managers | Masqué | Masqué |

---

# ⚙️ Fonctionnalités implémentées

✔ Création des rôles

✔ Attribution des privilèges

✔ Row Access Policies

✔ Masking Policies

✔ Secure Views

✔ Architecture Bronze / Silver / Gold

✔ Streams

✔ Tasks

✔ Interface Streamlit

✔ Versionning Git / GitHub

---

# 🧪 Démonstration

Le projet montre qu'une même requête peut produire des résultats différents selon le rôle actif.

### Exemple : Row Access Policy

**Global Manager**

- 🇫🇷 France
- 🇩🇪 Allemagne
- 🇲🇦 Maroc

**Manager Maroc**

- 🇲🇦 Maroc uniquement

---

### Exemple : Masking Policy

**Data Engineer**

```
CUSTOMER_ADDRESS

123 Main Street
```

**Manager**

```
CUSTOMER_ADDRESS

******** ADDRESS MASKED ********
```

---

# 📂 Structure du projet

```
snowflake-retail-analytics/

│

├── sql/
│   ├── 01_create_database.sql
│   ├── 02_create_schemas.sql
│   ├── 03_create_roles.sql
│   ├── 04_create_warehouse.sql
│   ├── 05_grants_data_engineer.sql
│   ├── 06_explore_sample_data.sql
│   ├── 07_create-bronze_table.sql
│   ├── 08_create_table_silver.sql
│   ├── 09_create_gold_tables.sql
│   ├── 10_create_row_access_policies.sql
│   ├── 11_apply_row_access_policies.sql
│   ├── 12_test-row_access_policies.sql
│   ├── 13_create_masking_policies.sql
│   ├── 14_apply_masking_policies.sql
│   ├── 15_test_masking_policies.sql
│   ├── 16_create_secure_views.sql
│   ├── 17_gold_tables.sql
│   ├── 18_create_streams.sql
│   └── 19_create_tasks.sql
│
├── streamlit/
│   └── app.py
│
├── images/
│
├── readme.md
│
└── .gitignore
```

---

# 🛠️ Technologies utilisées

- ❄️ Snowflake
- SQL
- Python
- Streamlit
- Git
- GitHub

---

# 💡 Ce que démontre ce POC

Ce projet montre qu'il est possible de construire une plateforme de données unique tout en garantissant un niveau de sécurité élevé.

Grâce aux rôles, aux privilèges et aux politiques de sécurité, chaque utilisateur accède uniquement aux données qui lui sont destinées.

Les données restent centralisées, les traitements sont simplifiés et les informations sensibles sont protégées sans duplication des jeux de données.

---

# 🚀 Perspectives d'évolution

Ce Proof of Concept peut facilement être étendu afin d'intégrer :

- de nouveaux pays ;
- de nouveaux rôles métiers ;
- des politiques de sécurité supplémentaires ;
- d'autres domaines fonctionnels (Finance, RH, Supply Chain, etc.).

---

# 👩🏽‍💻 À propos

Ce projet a été réalisé dans le cadre de mon portfolio Data afin de mettre en pratique les fonctionnalités avancées de gouvernance et de sécurité de Snowflake.

N'hésitez pas à parcourir le dépôt, à explorer le code SQL et à me faire part de vos retours.
