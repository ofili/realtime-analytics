import unittest
from kafka_consumer.spark_stream_processor import process_stream
from unittest.mock import patch


class TestSparkStreamProcessor(unittest.TestCase):

    @patch('kafka_consumer.spark_stream_processor.SparkSession')
    def test_process_stream(self, mock_spark):
        """Test that Spark Structured Streaming is set up correctly."""
        mock_spark_instance = mock_spark.builder.getOrCreate.return_value

        # Call the process stream function
        process_stream()

        # Check that the Spark streaming readStream and writeStream methods were called
        self.assertTrue(mock_spark_instance.readStream.called)
        self.assertTrue(mock_spark_instance.writeStream.called)

    @patch('kafka_consumer.spark_stream_processor.SparkSession')
    def test_consumer_handles_errors(self, mock_spark):
        """Test error handling in Spark consumer."""
        mock_spark_instance = mock_spark.builder.getOrCreate.return_value
        mock_spark_instance.readStream.side_effect = Exception("Test Stream Failure")

        with self.assertRaises(Exception):
            process_stream()  # Expect error to propagate up


if __name__ == '__main__':
    unittest.main()
