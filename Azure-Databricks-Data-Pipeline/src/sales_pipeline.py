from pyspark.sql import SparkSession
from pyspark.sql.functions import col, coalesce, lit, to_date, round
from pyspark.sql.types import IntegerType, DoubleType

spark = SparkSession.builder.appName("AzureDatabricksSalesPipeline").getOrCreate()

# Change these paths when running in Azure Databricks.
INPUT_PATH = "data/sales_data.csv"
OUTPUT_PATH = "output/curated_sales"

# 1. Data ingestion
raw_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(INPUT_PATH)
)

# 2. Transformation
sales_df = (
    raw_df
    .withColumn("order_date", to_date(col("order_date")))
    .withColumn("quantity", col("quantity").cast(IntegerType()))
    .withColumn("unit_price", col("unit_price").cast(DoubleType()))
    .withColumn("customer_segment", coalesce(col("customer_segment"), lit("Unknown")))
    .filter((col("quantity") > 0) & (col("unit_price") >= 0))
    .withColumn("revenue", round(col("quantity") * col("unit_price"), 2))
)

# 3. Data quality check
sales_df = sales_df.dropDuplicates(["order_id"])

# 4. Data storage / processing using Delta Lake
sales_df.write.format("delta").mode("overwrite").save(OUTPUT_PATH)

# 5. Register a temporary view for SQL analysis
sales_df.createOrReplaceTempView("sales")

# Example PySpark analysis
sales_df.groupBy("region").sum("revenue").orderBy("region").show()

# Example SQL analysis
spark.sql("""
    SELECT region, ROUND(SUM(revenue), 2) AS total_revenue
    FROM sales
    GROUP BY region
    ORDER BY total_revenue DESC
""").show()

spark.stop()
