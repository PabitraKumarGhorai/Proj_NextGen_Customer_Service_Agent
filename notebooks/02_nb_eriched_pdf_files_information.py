# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# COMMAND ----------

#Reading Product Table
df_product = spark.read.table("agentic_catalog.agentic_schema.products")
df_product.show(5)

# COMMAND ----------

#Reading Product_Docs Table
df_product_docs = spark.read.table("agentic_catalog.agentic_schema.product_docs")
df_product_docs.show(5)

# COMMAND ----------

#Joing Products with Product_Docs
df_combined = df_product.join(df_product_docs, df_product.product_name == df_product_docs.product_name, "inner")
df_combined.printSchema()


# COMMAND ----------

# MAGIC %md
# MAGIC ### Create Indexed Document Column

# COMMAND ----------

df_combined = df_combined.select(df_product["product_id"], df_product["product_name"], df_product["product_category"], df_product["product_sub_category"], df_product_docs["product_doc"])
df_combined.show(5)

# COMMAND ----------

indexed_df = df_combined.withColumn(
    "indexed_doc",
    concat(
        lit("<product_category>"),
        col("product_category"),
        lit("</product_category>\n"),
        lit("<product_sub_category>"),
        col("product_sub_category"),
        lit("</product_sub_category>\n"),
        lit("<product_name>"),
        col("product_name"),
        lit("</product_name>\n"),
        lit("<product_doc>"),
        col("product_doc"),
        lit("</product_doc>")
    )
)
display(indexed_df)

# COMMAND ----------

target_table = "agentic_catalog.agentic_schema.product_docs_combined"
indexed_df.write.format('delta').option('overwriteSchema', 'true').mode('overwrite').saveAsTable(target_table)

# COMMAND ----------

# MAGIC %md
# MAGIC -- Enable Change Data Feed to perform Vector Search Operation in this table

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE agentic_catalog.agentic_schema.product_docs_combined
# MAGIC SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
# MAGIC