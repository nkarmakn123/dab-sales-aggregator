from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

spark = SparkSession.builder.getOrCreate()

df = spark.read.option("header", True).csv("dbfs:/FileStore/data/sales.csv")
df = df.withColumn("quantity", col("quantity").cast("int"))
df = df.withColumn("price", col("price").cast("double"))

agg_df = df.groupBy("product").agg((_sum(col("quantity") * col("price"))).alias("total_sales"))

agg_df.write.format("delta").mode("overwrite").save("/tmp/output/sales_summary")
