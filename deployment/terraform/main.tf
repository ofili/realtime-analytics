# Main configuration for deploying Spark on Kubernetes
provider "kubernetes" {
  config_path = "~/.kube/config"  # Path to Kubernetes config, change for cloud provider
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

# Kubernetes Namespace for Spark
resource "kubernetes_namespace" "spark_namespace" {
  metadata {
    name = "spark-namespace"
  }
}

# Spark Master Deployment
resource "kubernetes_deployment" "spark_master" {
  metadata {
    name      = "spark-master"
    namespace = kubernetes_namespace.spark_namespace.metadata[0].name
    labels = {
      app  = "spark"
      role = "master"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app  = "spark"
        role = "master"
      }
    }

    template {
      metadata {
        labels = {
          app  = "spark"
          role = "master"
        }
      }

      spec {
        container {
          name  = "spark-master"
          image = "bitnami/spark:latest"

          ports {
            container_port = 7077
          }
          ports {
            container_port = 8080
          }

          env {
            name  = "SPARK_MODE"
            value = "master"
          }

          resources {
            requests = {
              memory = "2Gi"
              cpu    = "500m"
            }

            limits = {
              memory = "4Gi"
              cpu    = "1"
            }
          }

          volume_mount {
            mount_path = "/opt/spark/data"
            name       = "spark-data"
          }
        }

        volume {
          name = "spark-data"
          empty_dir {}
        }
      }
    }
  }
}

# Spark Master Service
resource "kubernetes_service" "spark_master_service" {
  metadata {
    name      = "spark-master"
    namespace = kubernetes_namespace.spark_namespace.metadata[0].name
  }

  spec {
    selector = {
      app  = "spark"
      role = "master"
    }

    port {
      port        = 7077
      target_port = 7077
    }

    port {
      port        = 8080
      target_port = 8080
    }

    type = "LoadBalancer"  # You can switch this to ClusterIP or NodePort based on your cloud provider.
  }
}

# Spark Worker Deployment
resource "kubernetes_deployment" "spark_worker" {
  metadata {
    name      = "spark-worker"
    namespace = kubernetes_namespace.spark_namespace.metadata[0].name
    labels = {
      app  = "spark"
      role = "worker"
    }
  }

  spec {
    replicas = 3  # Number of workers, scalable as needed
    selector {
      match_labels = {
        app  = "spark"
        role = "worker"
      }
    }

    template {
      metadata {
        labels = {
          app  = "spark"
          role = "worker"
        }
      }

      spec {
        container {
          name  = "spark-worker"
          image = "bitnami/spark:latest"

          ports {
            container_port = 8081
          }

          env {
            name  = "SPARK_MODE"
            value = "worker"
          }

          env {
            name  = "SPARK_MASTER_URL"
            value = "spark://spark-master:7077"
          }

          resources {
            requests = {
              memory = "2Gi"
              cpu    = "500m"
            }

            limits = {
              memory = "4Gi"
              cpu    = "1"
            }
          }

          volume_mount {
            mount_path = "/opt/spark/data"
            name       = "spark-data"
          }
        }

        volume {
          name = "spark-data"
          empty_dir {}
        }
      }
    }
  }
}

# Spark Worker Service
resource "kubernetes_service" "spark_worker_service" {
  metadata {
    name      = "spark-worker"
    namespace = kubernetes_namespace.spark_namespace.metadata[0].name
  }

  spec {
    selector = {
      app  = "spark"
      role = "worker"
    }

    port {
      port        = 8081
      target_port = 8081
    }

    type = "ClusterIP"  # We can use ClusterIP for internal communication between nodes
  }
}

# Set Up Helm for Metrics (Optional, but highly recommended)
resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "prometheus"
  namespace  = kubernetes_namespace.spark_namespace.metadata[0].name

  values = [
    <<EOF
      alertmanager:
        enabled: false
      server:
        persistentVolume:
          enabled: false
    EOF
  ]
}

# Optional: IAM Roles for cloud storage access (e.g., AWS S3, GCS)
resource "aws_iam_role" "spark_iam_role" {
  name = "spark-iam-role"
  assume_role_policy = <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
            "Service": "eks.amazonaws.com"
          },
          "Effect": "Allow",
          "Sid": ""
        }
      ]
    }
  EOF
}
