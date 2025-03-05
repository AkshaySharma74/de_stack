# Databricks notebook source
spark.conf.set("spark.sql.ansi.enabled",False)

# COMMAND ----------

gold_table_name = "partner_summary.default.taxi_data_gold"

# COMMAND ----------

silver_table = dbutils.jobs.taskValues.get(taskKey = "Silver", key = "silver_table", debugValue = "partner_summary.default.taxi_data_silver")

taxiDataDF = spark.table(silver_table)

# COMMAND ----------

paymentTypeDF = spark.read.format('csv').options(header=True).options(inferSchema=True).load("dbfs:/databricks-datasets/nyctaxi/taxizone/taxi_payment_type.csv")

# COMMAND ----------

final_df = taxiDataDF.alias("t").join(paymentTypeDF.alias("p"), on=taxiDataDF.Payment_Type == paymentTypeDF.payment_type, how="inner").select("t.Trip_Distance", "t.Payment_Type", "p.Payment_Desc")

# COMMAND ----------

final_df.write.mode("overwrite").saveAsTable(gold_table_name)

# COMMAND ----------

spark.table(gold_table_name).display()