import os

def get_kafka_consumer_config():
    return {
        'bootstrap_servers': os.getenv('KAFKA_BROKER', 'localhost:9092'),
        'group_id': 'sensor_data_group',
        'enable_auto_commit': False,
        'auto_offset_reset': 'earliest',
        'security_protocol': 'SASL_SSL',
        'sasl_mechanism': 'PLAIN',
        'sasl_plain_username': os.getenv('KAFKA_USERNAME'),
        'sasl_plain_password': os.getenv('KAFKA_PASSWORD'),
    }
