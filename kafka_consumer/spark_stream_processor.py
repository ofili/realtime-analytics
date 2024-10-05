from pyspark.sql import SparkSession
from pyspark.sql.functions import window, avg
import os

def process_stream():
    spark = SparkSession.builder \
        .appName("SensorDataStreamProcessor") \
        .getOrCreate()

    # Read stream from Kafka topic
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", os.getenv('KAFKA_BROKER', 'localhost:9092')) \
        .option("subscribe", "sensor_data") \
        .option("startingOffsets", "earliest") \
        .load()

    # Convert the Kafka data into readable format
    sensor_df = kafka_df.selectExpr("CAST(value AS STRING)")

    # Perform simple processing (e.g., calculate avg temp over 10-minute windows)
    aggregated_df = sensor_df \
        .groupBy(window("timestamp", "10 minutes")) \
        .agg(avg("temperature").alias("avg_temperature"))

    # Write the output to the sink (e.g., S3 or Snowflake)
    query = aggregated_df.writeStream \
        .outputMode("append") \
        .format("parquet") \
        .option("path", "s3a://bucket-name/processed-data") \
        .option("checkpointLocation", "/path/to/checkpoints") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    process_stream()
