# Phase 06.5: Kubernetes - Bài Tập Thực Hành

> **Thời gian:** 3-4 giờ
> **Mục tiêu:** Deploy Spring Boot app lên Kubernetes cluster

---

## 📝 BÀI TẬP 1: LOCAL KUBERNETES SETUP (45 phút)

### Đề bài

Cài đặt Kubernetes local environment với Minikube hoặc Kind

### Phần 1: Cài đặt tools

```bash
# 1. Cài đặt Minikube
# macOS
brew install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 2. Cài đặt kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# 3. Cài đặt Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 4. Cài đặt k9s (optional nhưng recommended)
# https://k9scli.io/topics/install/
```

### Phần 2: Start cluster

```bash
# Start Minikube
minikube start --cpus=4 --memory=4096 --disk-size=20gb

# Enable addons
minikube addons enable metrics-server
minikube addons enable ingress
minikube addons enable dashboard

# Check cluster
kubectl cluster-info
kubectl get nodes
kubectl get pods -A

# Open dashboard
minikube dashboard
```

### Checklist hoàn thành

- [ ] Minikube/Kind đang chạy
- [ ] kubectl configured
- [ ] Helm installed
- [ ] Dashboard accessible

---

## 📝 BÀI TẬP 2: DEPLOY SPRING BOOT APP (1 giờ)

### Đề bài

Deploy ứng dụng Spring Boot lên Kubernetes

### Phần 1: Tạo Docker image

```bash
# 1. Build JAR file
./gradlew bootJar

# 2. Build Docker image
docker build -t order-service:1.0.0 .

# 3. Test locally
docker run -p 8080:8080 order-service:1.0.0

# 4. Verify health endpoint
curl http://localhost:8080/actuator/health
```

### Phần 2: Tạo Kubernetes manifests

**Yêu cầu:** Tạo các files sau trong `k8s/` folder:

```yaml
# TODO: k8s/namespace.yaml
# Tạo namespace "ecommerce"

# TODO: k8s/deployment.yaml
# Deployment với 3 replicas
# Liveness/readiness probes sử dụng /actuator/health
# Resources: requests 256Mi/100m, limits 512Mi/500m

# TODO: k8s/service.yaml
# ClusterIP service expose port 8080

# TODO: k8s/configmap.yaml
# SPRING_PROFILES_ACTIVE=kubernetes
# LOGGING_LEVEL_COM_EXAMPLE=INFO

# TODO: k8s/secret.yaml
# DB credentials (dummy values cho local)
```

### Phần 3: Deploy và verify

```bash
# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml -n ecommerce
kubectl apply -f k8s/secret.yaml -n ecommerce
kubectl apply -f k8s/deployment.yaml -n ecommerce
kubectl apply -f k8s/service.yaml -n ecommerce

# Check status
kubectl get all -n ecommerce

# Port-forward để test
kubectl port-forward svc/order-service 8080:80 -n ecommerce

# Test endpoint
curl http://localhost:8080/actuator/health
```

### Checklist hoàn thành

- [ ] Docker image build thành công
- [ ] Deployment với 3 replicas
- [ ] Pods đang Running
- [ ] Service accessible qua port-forward
- [ ] Health endpoint trả về 200

---

## 📝 BÀI TẬP 3: AUTO-SCALING (30 phút)

### Đề bài

Cấu hình Horizontal Pod Autoscaler (HPA)

### Phần 1: Tạo HPA manifest

```yaml
# TODO: k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
  namespace: ecommerce
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Phần 2: Test auto-scaling

```bash
# Apply HPA
kubectl apply -f k8s/hpa.yaml

# Check HPA status
kubectl get hpa -n ecommerce
kubectl describe hpa order-service-hpa -n ecommerce

# Generate load (terminal mới)
kubectl run -it --rm load-generator --image=busybox --restart=Never -- \
  wget -qO- http://order-service.ecommerce.svc/actuator/health

# Watch scaling events
kubectl get pods -n ecommerce -w
kubectl get events -n ecommerce --sort-by='.lastTimestamp'
```

### Checklist hoàn thành

- [ ] HPA created thành công
- [ ] minReplicas = 2, maxReplicas = 5
- [ ] Pods scale up/down dựa trên CPU

---

## 📝 BÀI TẬP 4: ROLLING UPDATE & ROLLBACK (30 phút)

### Đề bài

Thực hành zero-downtime deployment

### Phần 1: Rolling update

```bash
# 1. Build version mới
# Change version trong application.yml: 1.0.0 → 1.1.0
./gradlew bootJar
docker build -t order-service:1.1.0 .

# 2. Update image trong deployment
kubectl set image deployment/order-service \
  order-service=order-service:1.1.0 \
  -n ecommerce

# 3. Watch rollout
kubectl rollout status deployment/order-service -n ecommerce
kubectl get pods -n ecommerce -w

# 4. Check rollout history
kubectl rollout history deployment/order-service -n ecommerce
```

### Phần 2: Rollback

```bash
# 1. Rollback về version trước
kubectl rollout undo deployment/order-service -n ecommerce

# 2. Verify
kubectl rollout history deployment/order-service -n ecommerce
kubectl get pods -n ecommerce

# 3. Rollback to specific revision
kubectl rollout undo deployment/order-service --to-revision=1 -n ecommerce
```

### Checklist hoàn thành

- [ ] Rolling update thành công
- [ ] Zero-downtime (không có request failed)
- [ ] Rollback thành công

---

## 📝 BÀI TẬP 5: HELM CHART (1 giờ)

### Đề bài

Tạo Helm chart cho Spring Boot application

### Phần 1: Create chart structure

```bash
# Tạo chart mới
helm create order-service-chart

# Structure:
# order-service-chart/
# ├── Chart.yaml
# ├── values.yaml
# ├── values-prod.yaml
# └── templates/
#     ├── deployment.yaml
#     ├── service.yaml
#     ├── configmap.yaml
#     ├── hpa.yaml
#     └── _helpers.tpl
```

### Phần 2: Customize templates

**Yêu cầu:** Sửa các files templates để sử dụng values:

```yaml
# TODO: templates/deployment.yaml
# Sử dụng {{ .Values.replicaCount }}, {{ .Values.image.repository }}

# TODO: templates/service.yaml
# Sử dụng {{ .Values.service.type }}, {{ .Values.service.port }}

# TODO: values.yaml
replicaCount: 3
image:
  repository: order-service
  tag: "1.0.0"
service:
  type: ClusterIP
  port: 80
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# TODO: values-prod.yaml
replicaCount: 5
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

### Phần 3: Install và test

```bash
# Lint chart
helm lint ./order-service-chart

# Dry-run install
helm install order-service ./order-service-chart \
  --namespace ecommerce \
  --dry-run --debug

# Install thực tế
helm install order-service ./order-service-chart \
  --namespace ecommerce \
  --create-namespace

# Upgrade lên production values
helm upgrade order-service ./order-service-chart \
  --namespace ecommerce \
  -f values-prod.yaml

# Uninstall
helm uninstall order-service -n ecommerce
```

### Checklist hoàn thành

- [ ] Helm chart structure đúng
- [ ] templates sử dụng values
- [ ] Install thành công
- [ ] Upgrade với values-prod.yaml thành công

---

## 📝 BÀI TẬP 6: MONITORING SETUP (30 phút)

### Đề bài

Setup monitoring cho ứng dụng

### Phần 1: Install Prometheus Stack

```bash
# Add helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.service.type=NodePort \
  --set grafana.service.type=NodePort \
  --set grafana.adminPassword=admin123

# Get NodePort
kubectl get svc -n monitoring
```

### Phần 2: Configure ServiceMonitor

```yaml
# TODO: k8s/monitoring/servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: order-service-monitor
  namespace: ecommerce
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: order-service
  endpoints:
  - port: http
    path: /actuator/prometheus
    interval: 30s
```

### Phần 3: Verify

```bash
# Apply ServiceMonitor
kubectl apply -f k8s/monitoring/servicemonitor.yaml

# Access Prometheus
# http://localhost:<prometheus-nodeport>

# Access Grafana
# http://localhost:<grafana-nodeport>
# Login: admin / admin123

# Check metrics trong Prometheus
# Query: http_requests_total{namespace="ecommerce"}
```

### Checklist hoàn thành

- [ ] Prometheus stack installed
- [ ] ServiceMonitor created
- [ ] Metrics hiển thị trong Prometheus
- [ ] Grafana dashboard accessible

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 06.5

- [ ] Cài đặt được Kubernetes local (Minikube/Kind)
- [ ] Build Docker image cho Spring Boot app
- [ ] Deploy với Deployment & Service
- [ ] Cấu hình Liveness/Readiness probes
- [ ] Setup HPA auto-scaling
- [ ] Thực hành Rolling Update & Rollback
- [ ] Tạo Helm chart
- [ ] Setup monitoring với Prometheus/Grafana
- [ ] Troubleshoot được common issues

---

## 📤 CÁCH SUBMIT

1. Push code lên GitHub (Dockerfile, k8s manifests, Helm chart)
2. Tạo file `K8S_LABS.md` với:
   - Screenshots của Kubernetes dashboard
   - Output của `kubectl get all -n ecommerce`
   - Output của `helm list`
   - Grafana dashboard screenshot
   - Khó khăn gặp phải

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, unlock Phase tiếp theo!
