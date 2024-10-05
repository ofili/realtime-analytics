from prometheus_client import start_http_server, Gauge
import random
import time

# Define Prometheus metrics
g_kafka_lag = Gauge('kafka_consumer_lag', 'Kafka Consumer Lag')
g_stream_processing_time = Gauge('stream_processing_time', 'Time taken to process stream data')

def collect_metrics():
    while True:
        # Simulate metric collection (Replace with actual monitoring code)
        g_kafka_lag.set(random.randint(0, 100))
        g_stream_processing_time.set(random.uniform(0.1, 5.0))
        time.sleep(10)

if __name__ == "__main__":
    start_http_server(8000)  # Start Prometheus metrics server on port 8000
    collect_metrics()
