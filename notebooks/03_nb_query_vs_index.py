# Databricks notebook source
# %pip install databricks-vector-search


# COMMAND ----------

import os
from databricks.vector_search.client import VectorSearchClient

workspace_url = os.environ.get("WORKSPACE_URL")
sp_client_id = os.environ.get("SP_CLIENT_ID")
sp_client_secret = os.environ.get("SP_CLIENT_SECRET")

vsc = VectorSearchClient(
    workspace_url=workspace_url,
    service_principal_client_id=sp_client_id,
    service_principal_client_secret=sp_client_secret
)

index = vsc.get_index(endpoint_name="proj_customer_service_vs", index_name="agentic_catalog.agentic_schema.proj_customer_service_ai_search_index")

index.similarity_search(num_results=3, 
                        columns=["indexed_doc","product_id"], 
                        query_text="Tell me about the AccountEase Pro", 
                        query_type="HYBRID"
                        )