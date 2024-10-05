import unittest
from kafka_producer.sensor_producer import SensorProducer
from kafka_consumer.spark_stream_processor import process_stream
from storage.s3_sink import S3Sink
from unittest.mock import patch

class TestIntegration(unittest.TestCase):

    @patch('kafka_producer.producer_config.KafkaProducer')
    @patch('kafka_consumer.spark_stream_processor.SparkSession')
    @patch('storage.s3_sink.boto3.client')
    def test_end_to_end_pipeline(self, mock_producer, mock_spark, mock_boto3):
        """Test the full pipeline: producing, consuming, and storing data."""
        # Simulate producer producing sensor data
        producer = SensorProducer('test_topic')
        producer.produce_sensor_data()
        self.assertTrue(mock_producer.return_value.send.called)

        # Simulate Spark consumer processing the stream
        process_stream()
        self.assertTrue(mock_spark.builder.getOrCreate.return_value.readStream.called)

        # Simulate S3 upload
        sink = S3Sink()
        sink.upload_file('test_file.parquet', 'processed/test_file.parquet')
        self.assertTrue(mock_boto3.return_value.upload_file.called)

if __name__ == '__main__':
    unittest.main()
