# Real-Time Data Pipeline with Apache Spark and Kafka

This project implements a real-time data pipeline that collects, processes, and analyzes streaming log data using **Kafka** and **Apache Spark**. The infrastructure is deployed on a **Kubernetes** cluster using **Terraform** for infrastructure provisioning. The pipeline demonstrates scalable log generation, stream processing, and eventual integration with data storage or machine learning systems.

## Project Architecture

- **Log Producer (Python)**: Simulates real-time log generation and sends logs to a Kafka topic.
- **Kafka**: Message broker that ingests and stores the generated logs in a streaming fashion.
- **Apache Spark**: Processes logs in real time, applying transformations and actions for downstream systems.
- **Kubernetes**: The Apache Spark cluster and other services are deployed in a containerized environment.
- **Terraform**: Automates the deployment of Kubernetes resources, including Spark and Kafka.

## Features

- **Real-time log ingestion**: Logs are produced and consumed in real-time, simulating a high-throughput environment.
- **Scalable Spark Cluster**: Deployed on Kubernetes with horizontal scaling enabled for both master and worker nodes.
- **Kafka Integration**: Seamless connection between the Kafka broker and Spark Streaming.
- **Kubernetes Deployment**: Automated provisioning of Spark clusters and Kafka using Terraform for reproducibility and scalability.
- **Batching and Stream Processing**: The logs are processed in batches for efficient handling and monitoring.
- **Monitoring (Optional)**: Prometheus can be configured via Helm charts for monitoring and alerting.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Kubernetes Cluster](https://kubernetes.io/) (e.g., GKE, EKS, AKS, or Minikube for local testing)
- [Kafka](https://kafka.apache.org/) Broker running in the Kubernetes cluster or as a standalone service
- [Terraform](https://www.terraform.io/)
- Python 3.8+
- Kafka Python Client: `kafka-python`
- Faker: `faker`

### Folder Structure

```
real-time-data-pipeline/
│
├── terraform/
│   ├── main.tf            # Kubernetes + Spark deployment with Terraform
│   ├── spark-deployment.yaml # YAML for Spark master/worker deployment
│   └── variables.tf       # Configurable Terraform variables
│
├── producer/
│   └── log_producer.py     # Log generator script that sends messages to Kafka
│
├── spark/
│   └── spark_streaming.py  # Spark Streaming application for consuming logs from Kafka
│
└── README.md               # Project documentation
```

### Setup and Installation

#### Step 1: Set Up Kubernetes Cluster

- If using a managed service like GKE, EKS, or AKS, ensure the Kubernetes cluster is running and accessible via `kubectl`.
- Alternatively, you can use **Minikube** for local testing:
  ```bash
  minikube start
  ```

#### Step 2: Deploy Kafka on Kubernetes

You can use **Helm** to deploy Kafka on your Kubernetes cluster.

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install kafka bitnami/kafka
```

Once deployed, note the broker URL and port for connecting Kafka to the log producer.

#### Step 3: Configure Terraform

- Navigate to the `terraform/` directory.
- Initialize Terraform and apply the infrastructure configuration:

```bash
cd terraform/
terraform init
terraform apply
```

Terraform will deploy:
- **Spark Cluster**: 1 master and 3 worker nodes.
- **Services**: Load balancers and cluster IPs for accessing Spark components.

#### Step 4: Set Up Python Environment for Log Producer

In the `producer/` directory, install the necessary Python packages:

```bash
pip install kafka-python faker
```

#### Step 5: Start the Log Producer

The `log_producer.py` script generates logs and sends them to the Kafka topic:

```bash
cd producer/
python log_producer.py
```

Make sure the Kafka broker URL in `log_producer.py` matches your cluster setup.

#### Step 6: Run the Spark Streaming Application

In the `spark/` directory, start the Spark Streaming job to consume logs from Kafka:

```bash
spark-submit --master k8s://<your-k8s-master-url> \
    --deploy-mode cluster \
    --conf spark.kubernetes.namespace=spark-namespace \
    --conf spark.executor.instances=3 \
    spark_streaming.py
```

This job will continuously consume logs from Kafka and apply any transformations or actions defined in `spark_streaming.py`.

### Configuration

#### Kafka Configuration

Edit `log_producer.py` to configure Kafka broker URL, topic names, and batch sizes.

#### Spark Configuration

- Adjust `main.tf` for the Spark cluster size (number of workers, resources).
- Edit `spark_streaming.py` for custom transformations or stream processing logic.

### Monitoring

For production environments, it's essential to monitor both Kafka and Spark.

#### Prometheus (Optional)

Use the **Helm** chart included in `main.tf` to install **Prometheus** for monitoring. You can visualize metrics from Kafka and Spark, such as resource usage and throughput.

```bash
helm install prometheus prometheus-community/prometheus
```

### Project Structure Overview

1. **log_producer.py**: Generates logs and sends them to Kafka in batches. Simulates real-time log data in JSON format.
2. **spark_streaming.py**: Consumes logs from Kafka, processes them using Spark Streaming, and performs any data transformations.
3. **Terraform**: Manages infrastructure provisioning, including the Spark cluster and services on Kubernetes.

### Scalability and Optimization

- **Kafka**: Can be scaled horizontally by increasing the number of partitions and replicas.
- **Spark Workers**: The Spark cluster can be horizontally scaled by increasing the number of worker nodes via `main.tf`.
- **Batching**: The `log_producer.py` script can be modified to send larger batches of logs for high-throughput environments.
- **Monitoring**: Use **Prometheus** to track performance and health metrics of both Kafka and Spark components.

### Future Enhancements

- Integrate with **S3** or **HDFS** for storing processed data.
- Add more sophisticated log processing and aggregations in the Spark Streaming application.
- Introduce **Alerting** mechanisms via Prometheus or custom tools for monitoring log anomalies.

## Contributing

Feel free to open issues or contribute to improving the pipeline by submitting a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
