from kafka import KafkaProducer
import os

def get_kafka_producer_config():
    return {
        'bootstrap_servers': os.getenv('KAFKA_BROKER', 'localhost:9092'),
        'key_serializer': str.encode,
        'value_serializer': lambda v: v.encode('utf-8'),
        'security_protocol': 'SASL_SSL',
        'sasl_mechanism': 'PLAIN',
        'sasl_plain_username': os.getenv('KAFKA_USERNAME'),
        'sasl_plain_password': os.getenv('KAFKA_PASSWORD'),
        'retries': 5,
        'linger_ms': 5,  # Batching messages
        'acks': 'all',  # Ensure message durability
    }
