import json
import random
import time
from kafka import KafkaProducer
from kafka_producer.config import get_kafka_producer_config


class SensorProducer:
    def __init__(self, topic: str):
        self.producer = KafkaProducer(**get_kafka_producer_config())
        self.topic = topic

    def produce_sensor_data(self):
        while True:
            data = {
                'sensor_id': random.randint(1, 100),
                'temperature': round(random.uniform(15, 35), 2),
                'humidity': round(random.uniform(20, 90), 2),
                'timestamp': int(time.time())
            }
            self.producer.send(self.topic, value=json.dumps(data).encode('utf-8'))
            self.producer.flush()  # Ensure message is sent before the next iteration
            time.sleep(1)  # Simulating sensor frequency

if __name__ == "__main__":
    producer = SensorProducer(topic='sensor_data')
    try:
        producer.produce_sensor_data()
    except Exception as e:
        print(f"Error while producing data: {str(e)}")
