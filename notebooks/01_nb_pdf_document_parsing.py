# Databricks notebook source
# MAGIC %pip install PyPDF2

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest pdf files from volumne

# COMMAND ----------

import PyPDF2
import io
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

pdf_path = '/Volumes/agentic_catalog/agentic_schema/customer_service_volums/product_docs/'

files = dbutils.fs.ls(pdf_path)

pdf_files = [f for f in files if f.name.endswith('.pdf')]

print(f"found {len(pdf_files)} PDF files")
for pdf in pdf_files:
  print(" - ", pdf.name)

# COMMAND ----------

def extract_text_from_pdf(file_path):

    try:
        with open(file_path, 'rb') as f:
            pdf_bytes = f.read()

        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes.encode('latin-1') if isinstance(pdf_bytes, str) else pdf_bytes))
        
        text_content = ""

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text() + "\n"

        return text_content.strip()
    
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {str(e)}")
         

# COMMAND ----------

# MAGIC %md
# MAGIC ### Process all PDF files

# COMMAND ----------

product_data = []

for pdf_file in pdf_files:
  print(f"Processing - {pdf_file.name}")

  #Extract product name remove (.pdf) extention
  product_name = pdf_file.name.replace('.pdf', '')

  #Extract text from PDF
  full_path = f"{pdf_path}{pdf_file.name}"
  text_content = extract_text_from_pdf(full_path)

  if text_content:
      product_data.append(
          {
              'product_name':product_name,
              'product_doc': text_content
          }
      )
      print(f'Successfully extracted text from - {pdf_file.name} & character length = {len(text_content)}')

  else:
      print(f'Failed to extract text from - {pdf_file.name}')

# COMMAND ----------

columns = StructType([
    StructField('product_name', StringType(), False),
    StructField('product_doc', StringType(), True)])

target_table = 'agentic_catalog.agentic_schema.product_docs'
df = spark.createDataFrame(data = product_data, schema = columns)
print("Total data count", df.count())

df.write.format('delta').mode('overwrite').option('overwriteSchema', 'True').saveAsTable(target_table)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from agentic_catalog.agentic_schema.product_docs