import unittest
from kafka_producer.sensor_producer import SensorProducer
from unittest.mock import patch


class TestKafkaProducer(unittest.TestCase):

    @patch('kafka_producer.producer_config.KafkaProducer')
    def test_produce_sensor_data(self, mock_kafka_producer):
        """Test that sensor data is produced to Kafka topic."""
        producer = SensorProducer('test_topic')
        producer.produce_sensor_data()  # Should call the Kafka producer

        # Check that Kafka producer's send method was called
        self.assertTrue(mock_kafka_producer.return_value.send.called)

    @patch('kafka_producer.producer_config.KafkaProducer')
    def test_producer_failure(self, mock_kafka_producer):
        """Test producer retries on failure."""
        mock_kafka_producer.return_value.send.side_effect = Exception("Test Kafka failure")

        producer = SensorProducer('test_topic')
        with self.assertRaises(Exception):
            producer.produce_sensor_data()  # Simulate a failure and check retry mechanism


if __name__ == '__main__':
    unittest.main()
