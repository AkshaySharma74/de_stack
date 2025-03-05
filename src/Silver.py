# Databricks notebook source
from pyspark.sql.functions import expr

# COMMAND ----------

silver_table_name = "partner_summary.default.taxi_data_silver"

# COMMAND ----------

bronze_table = dbutils.jobs.taskValues.get(taskKey = "Bronze", key = "bronze_table", debugValue = "partner_summary.default.taxi_data_bronze")

rawDF = spark.table(bronze_table)

# COMMAND ----------

processedDF = rawDF.withColumn('Year', expr('cast(year(Pickup_DateTime) as int)')).withColumn('Month', expr('cast(month(Pickup_DateTime) as int)')) 

# COMMAND ----------

processedDF.filter("Year = 2019 and Month = 12").write.format('delta').mode('overwrite').partitionBy('Year','Month').saveAsTable(silver_table_name)

# COMMAND ----------

dbutils.jobs.taskValues.set(key = "silver_table", value = silver_table_name)