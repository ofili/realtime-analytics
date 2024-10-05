import json
import logging
import random
import time
from datetime import datetime
from kafka import KafkaProducer
from faker import Faker

# Initialize the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Initialize the Faker instance for generating fake logs
fake = Faker()

# Kafka configurations
KAFKA_BROKER_URL = 'localhost:9092'  # Replace with actual broker URL
KAFKA_TOPIC = 'logs_topic'

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Log Levels and Event Types (for generating diverse logs)
LOG_LEVELS = ['INFO', 'WARNING', 'ERROR', 'DEBUG', 'CRITICAL']
EVENT_TYPES = ['user_login', 'user_logout', 'file_upload', 'file_download', 'error_event']

# Function to generate random logs
def generate_log():
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "log_level": random.choice(LOG_LEVELS),
        "event_type": random.choice(EVENT_TYPES),
        "user_id": fake.uuid4(),
        "ip_address": fake.ipv4_public(),
        "message": fake.sentence(),
        "metadata": {
            "file_name": fake.file_name(),
            "file_size": random.randint(100, 10000)
        }
    }
    return log_data

# Send logs to Kafka topic
def send_logs_to_kafka(batch_size=10, interval=2):
    try:
        while True:
            batch = []
            for _ in range(batch_size):
                log = generate_log()
                batch.append(log)
                logging.info(f"Generated log: {log}")
                producer.send(KAFKA_TOPIC, value=log)

            # Flush batch and wait for next cycle
            producer.flush()
            logging.info(f"Flushed {len(batch)} logs to Kafka topic {KAFKA_TOPIC}")
            time.sleep(interval)

    except KeyboardInterrupt:
        logging.info("Log producer stopped.")
    except Exception as e:
        logging.error(f"Error producing logs: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    logging.info(f"Starting log producer for topic '{KAFKA_TOPIC}' at {KAFKA_BROKER_URL}")
    send_logs_to_kafka(batch_size=10, interval=2)  # Customize batch size and interval as needed
