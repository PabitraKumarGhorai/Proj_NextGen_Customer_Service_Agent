# Databricks notebook source
# MAGIC %sql
# MAGIC create or replace function agentic_catalog.agentic_schema.get_types_of_policies(
# MAGIC
# MAGIC )
# MAGIC returns table (
# MAGIC     policy string,
# MAGIC     policy_details string,
# MAGIC     last_updated date
# MAGIC )
# MAGIC language sql
# MAGIC return
# MAGIC (
# MAGIC     select policy,
# MAGIC     policy_details,
# MAGIC     last_updated from agentic_catalog.agentic_schema.policies
# MAGIC )
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION agentic_catalog.agentic_schema.get_return_policy(
# MAGIC     policy_name string
# MAGIC )
# MAGIC
# MAGIC RETURNS TABLE (
# MAGIC     policy string,
# MAGIC     policy_details string,
# MAGIC     last_updated date
# MAGIC )
# MAGIC COMMENT 'Return the details of a return policy'
# MAGIC LANGUAGE SQL
# MAGIC RETURN
# MAGIC (
# MAGIC     SELECT policy,
# MAGIC     policy_details,
# MAGIC     last_updated
# MAGIC     from agentic_catalog.agentic_schema.policies
# MAGIC     where lower(policy) LIKE concat('%', lower(policy_name), '%')
# MAGIC     limit 1
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from agentic_catalog.agentic_schema.get_types_of_policies()

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from agentic_catalog.agentic_schema.policies

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from agentic_catalog.agentic_schema.get_return_policy("Exchange")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION agentic_catalog.agentic_schema.get_service_history(
# MAGIC     user_email STRING COMMENT "user email to retrive order history", user_name STRING COMMENT "user name to retrive order history"
# MAGIC )
# MAGIC RETURNS TABLE
# MAGIC (   
# MAGIC     name STRING,
# MAGIC     return_last_12_months int,
# MAGIC     issue_category string,
# MAGIC     issue_description string,
# MAGIC     product_name string,
# MAGIC     todays_date date
# MAGIC )
# MAGIC LANGUAGE SQL
# MAGIC RETURN (
# MAGIC     SELECT name, COUNT(*) AS return_last_12_months, issue_category, issue_description, product_name, now() as todays_date
# MAGIC     from agentic_catalog.agentic_schema.cust_service_data
# MAGIC     where email = lower(user_email) or name = lower(user_name)
# MAGIC     group by issue_category, name,issue_description, product_name
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from agentic_catalog.agentic_schema.cust_service_data
# MAGIC where email = 'grantstacy@example.org'

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from agentic_catalog.agentic_schema.get_service_history('grantstacy@example.org')

# COMMAND ----------

# MAGIC %sql
# MAGIC select distinct name from agentic_catalog.agentic_schema.cust_service_data

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from agentic_catalog.agentic_schema.cust_service_data where name = 'Susmita Das'

# COMMAND ----------

# MAGIC %sql
# MAGIC update agentic_catalog.agentic_schema.cust_service_data
# MAGIC set name = 'Pabitra Kumar Ghorai'
# MAGIC where customer_id = 'pppaa-gh123-456789'

# COMMAND ----------

# %sql
# insert into agentic_catalog.agentic_schema.cust_service_data
# values('susm-das123-456789', 'Susmita Das', 'susd@example.com', '+91 9051714744', '15 Thakurpukur, Kolkata -63', '123456789-9988-99877-ssdd', '2026-08-01T03:57:13.650+00:00', 'Technical Support','I want to know the how to use this product', 1004, '67d5f2af-0f13-40b8-bf7b-d4d5da874ab9', 'CoolTech SmartChill Pro 500'),
# ('susm-das123-456789', 'Susmita Das', 'susd@example.com', '+91 9051714744', '15 Thakurpukur, Kolkata -63', '123456789-9988-99877-ttyyu', '2026-07-20T03:57:13.650+00:00', 'Product Damage','Damage obsereved in this product', 1005, '16e3bff4-17b1-408b-9cdb-0b587cecc16c', 'EcoClean 4000')