# Phase 06.5: Kubernetes - Ví Dụ Thực Tế

> **Mục tiêu:** Deploy Spring Boot applications lên Kubernetes

---

## 📁 BÀI 1: SPRING BOOT TRÊN KUBERNETES

### Ví dụ 1.1: Dockerize Spring Boot App

```dockerfile
# Dockerfile
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Copy build files
COPY build.gradle settings.gradle ./
COPY gradle/ ./gradle/
COPY gradlew ./

# Download dependencies (cache layer)
RUN ./gradlew downloadDependencies || true

# Copy source code
COPY src/ ./src/

# Build application
RUN ./gradlew bootJar -x test

# Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -s /bin/sh -D appuser

# Copy JAR từ builder stage
COPY --from=builder --chown=appuser:appgroup /app/build/libs/*.jar app.jar

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD wget -qO- http://localhost:8080/actuator/health || exit 1

# JVM options for Kubernetes
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

```yaml
# .dockerignore
target/
!.mvn/wrapper/maven-wrapper.jar
!**/src/main/**/target/
!**/src/test/**/target/

### STS ###
.apt_generated
.classpath
.factorypath
.project
.settings
.springBeans
.sts4-cache

### IntelliJ ###
.idea
**/*.iml
**/iws

### NetBeans ###
/nbproject/private/
/nbbuild/
/dist/
/nbdist/
/.nb-gradle/
build/
!**/src/main/**/build/
!**/src/test/**/build/

### VS Code ###
.vscode/
```

---

### Ví dụ 1.2: Kubernetes Manifests cho Spring Boot

```yaml
# k8s/base/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce
  labels:
    name: ecommerce

---
# k8s/base/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-service-config
  namespace: ecommerce
data:
  SPRING_PROFILES_ACTIVE: "kubernetes"
  LOGGING_LEVEL_COM_EXAMPLE: "INFO"
  SERVER_PORT: "8080"
  MANAGEMENT_ENDPOINTS_WEB_EXPOSURE_INCLUDE: "health,info,metrics,prometheus"

---
# k8s/base/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: order-service-secret
  namespace: ecommerce
type: Opaque
stringData:
  SPRING_DATASOURCE_URL: "jdbc:postgresql://postgres-service:5432/orders"
  SPRING_DATASOURCE_USERNAME: "order_service"
  SPRING_DATASOURCE_PASSWORD: "SecureP@ssw0rd!"
  JWT_SECRET: "your-super-secret-jwt-key-change-in-production"
  REDIS_URL: "redis://redis-service:6379"

---
# k8s/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: ecommerce
  labels:
    app: order-service
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: order-service
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/path: "/actuator/prometheus"
        prometheus.io/port: "8080"
    spec:
      serviceAccountName: order-service-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: order-service
        image: myregistry/order-service:1.0.0
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
          name: http
          protocol: TCP
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        envFrom:
        - configMapRef:
            name: order-service-config
        - secretRef:
            name: order-service-secret
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 45
          periodSeconds: 10
          failureThreshold: 3
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 5
          failureThreshold: 3
          timeoutSeconds: 3
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
        - name: app-config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: tmp-volume
        emptyDir: {}
      - name: app-config
        configMap:
          name: order-service-config
      imagePullSecrets:
      - name: registry-secret
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: order-service
              topologyKey: kubernetes.io/hostname

---
# k8s/base/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: ecommerce
  labels:
    app: order-service
  annotations:
    prometheus.io/scrape: "true"
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    app: order-service

---
# k8s/base/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: order-service-sa
  namespace: ecommerce
  labels:
    app: order-service

---
# k8s/base/hpa.yaml
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
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

---

### Ví dụ 1.3: Kustomize cho nhiều environments

```yaml
# k8s/base/kustomization.yaml
apiVersion: kustomize.k8s.io/v1beta1
kind: Kustomization

resources:
  - namespace.yaml
  - configmap.yaml
  - secret.yaml
  - deployment.yaml
  - service.yaml
  - serviceaccount.yaml
  - hpa.yaml

commonLabels:
  app.kubernetes.io/managed-by: kustomize

---
# k8s/overlays/dev/kustomization.yaml
apiVersion: kustomize.k8s.io/v1beta1
kind: Kustomization

namespace: ecommerce-dev

bases:
  - ../../base

patchesStrategicMerge:
  - deployment-patch.yaml

configMapGenerator:
  - name: order-service-config
    behavior: merge
    literals:
      - SPRING_PROFILES_ACTIVE=dev
      - LOGGING_LEVEL_COM_EXAMPLE=DEBUG

---
# k8s/overlays/dev/deployment-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: order-service
        image: myregistry/order-service:dev-latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "250m"

---
# k8s/overlays/prod/kustomization.yaml
apiVersion: kustomize.k8s.io/v1beta1
kind: Kustomization

namespace: ecommerce-prod

bases:
  - ../../base

patchesStrategicMerge:
  - deployment-patch.yaml

configMapGenerator:
  - name: order-service-config
    behavior: merge
    literals:
      - SPRING_PROFILES_ACTIVE=prod
      - LOGGING_LEVEL_COM_EXAMPLE=WARN

---
# k8s/overlays/prod/deployment-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 5
  strategy:
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  template:
    spec:
      containers:
      - name: order-service
        image: myregistry/order-service:1.0.0
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

**Deploy với Kustomize:**

```bash
# Deploy to dev
kubectl apply -k k8s/overlays/dev/

# Deploy to prod
kubectl apply -k k8s/overlays/prod/

# Dry-run để xem manifests
kubectl apply -k k8s/overlays/dev/ --dry-run=client -o yaml
```

---

## 📁 BÀI 2: DATABASE TRÊN KUBERNETES

### Ví dụ 2.1: PostgreSQL với StatefulSet

```yaml
# k8s/database/postgres-statefulset.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: ecommerce
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: ecommerce
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_DB
          value: orders
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        livenessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - $(POSTGRES_USER)
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - $(POSTGRES_USER)
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: ecommerce
spec:
  type: ClusterIP
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
```

---

### Ví dụ 2.2: Redis với Helm

```bash
# Install Redis với Helm
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install Redis master-slave
helm install redis bitnami/redis \
  --namespace ecommerce \
  --set auth.enabled=true \
  --set auth.password=RedisP@ssw0rd \
  --set architecture=replication \
  --set master.replicaCount=1 \
  --set slave.replicaCount=2 \
  --set master.persistence.size=5Gi \
  --set slave.persistence.size=5Gi

# Check status
helm list -n ecommerce
helm status redis -n ecommerce

# Upgrade
helm upgrade redis bitnami/redis \
  --namespace ecommerce \
  --set image.tag=7.0

# Uninstall
helm uninstall redis -n ecommerce
```

```yaml
# values-redis.yaml (cho production)
auth:
  enabled: true
  password: RedisP@ssw0rd!

architecture: replication

master:
  replicaCount: 1
  persistence:
    enabled: true
    size: 10Gi
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1Gi"
      cpu: "500m"

slave:
  replicaCount: 2
  persistence:
    enabled: true
    size: 5Gi
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "250m"

metrics:
  enabled: true
  serviceMonitor:
    enabled: true
```

---

## 📁 BÀI 3: MONITORING & LOGGING

### Ví dụ 3.1: Prometheus Stack với Helm

```bash
# Install Prometheus Stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.service.type=LoadBalancer \
  --set grafana.service.type=LoadBalancer \
  --set grafana.adminPassword=admin123

# Access Prometheus
# http://<prometheus-lb-ip>:9090

# Access Grafana
# http://<grafana-lb-ip>:80
# Username: admin, Password: admin123
```

### Ví dụ 3.2: ServiceMonitor cho Spring Boot

```yaml
# k8s/monitoring/servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: order-service-monitor
  namespace: ecommerce
  labels:
    app: order-service
    release: prometheus
spec:
  selector:
    matchLabels:
      app: order-service
  namespaceSelector:
    matchNames:
      - ecommerce
  endpoints:
  - port: http
    path: /actuator/prometheus
    interval: 30s
    scrapeTimeout: 10s
```

```xml
<!-- pom.xml - Add Micrometer Prometheus -->
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-registry-prometheus</artifactId>
    </dependency>
</dependencies>
```

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  endpoint:
    health:
      show-details: always
  prometheus:
    metrics:
      export:
        enabled: true
  metrics:
    tags:
      application: order-service
    distribution:
      percentiles-histogram:
        http.server.requests: true
```

---

### Ví dụ 3.3: ELK Stack cho Logging

```yaml
# k8s/logging/filebeat-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: filebeat
  namespace: logging
spec:
  selector:
    matchLabels:
      app: filebeat
  template:
    metadata:
      labels:
        app: filebeat
    spec:
      serviceAccountName: filebeat
      containers:
      - name: filebeat
        image: docker.elastic.co/beats/filebeat:8.9.0
        args: ["-e", "-c", "/etc/filebeat.yml"]
        volumeMounts:
        - name: config
          mountPath: /etc/filebeat.yml
          subPath: filebeat.yml
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: filebeat-config
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers

---
# filebeat-config
apiVersion: v1
kind: ConfigMap
metadata:
  name: filebeat-config
  namespace: logging
data:
  filebeat.yml: |
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
      processors:
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
          matchers:
          - logs_path:
              logs_path: "/var/log/containers/"

    output.elasticsearch:
      hosts: ["http://elasticsearch:9200"]
      indices:
        - index: "logs-%{[+YYYY-MM-dd]}"
```

---

## 📁 BÀI 4: CI/CD VỚI GITHUB ACTIONS

### Ví dụ 4.1: Build & Deploy Pipeline

```yaml
# .github/workflows/deploy-k8s.yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'k8s/**'
      - 'Dockerfile'

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        cache-from: type=gha
        cache_to: type=gha,mode=max

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Setup kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.28.0'

    - name: Configure kubeconfig
      run: |
        mkdir -p ~/.kube
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > ~/.kube/config

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/order-service \
          order-service=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n ecommerce

    - name: Wait for rollout
      run: |
        kubectl rollout status deployment/order-service -n ecommerce --timeout=300s

    - name: Verify deployment
      run: |
        kubectl get pods -n ecommerce -l app=order-service
        kubectl get svc -n ecommerce order-service
```

---

## 📁 BÀI 5: TROUBLESHOOTING

### Ví dụ 5.1: Debug Commands

```bash
# Check pods status
kubectl get pods -n ecommerce
kubectl get pods -n ecommerce -o wide
kubectl get pods -n ecommerce -l app=order-service

# Describe pod (xem events, config)
kubectl describe pod order-service-abc123 -n ecommerce

# Xem logs
kubectl logs order-service-abc123 -n ecommerce
kubectl logs order-service-abc123 -n ecommerce -f  # Follow
kubectl logs order-service-abc123 -n ecommerce --previous  # Previous instance

# Exec vào container
kubectl exec -it order-service-abc123 -n ecommerce -- /bin/sh
kubectl exec -it order-service-abc123 -n ecommerce -- env  # Xem env vars

# Check resources
kubectl top pods -n ecommerce
kubectl top nodes

# Check events
kubectl get events -n ecommerce --sort-by='.lastTimestamp'

# Port-forward để test
kubectl port-forward svc/order-service 8080:80 -n ecommerce

# Check HPA status
kubectl get hpa -n ecommerce
kubectl describe hpa order-service-hpa -n ecommerce

# Check rollout status
kubectl rollout status deployment/order-service -n ecommerce
kubectl rollout history deployment/order-service -n ecommerce

# Rollback nếu có vấn đề
kubectl rollout undo deployment/order-service -n ecommerce
```

### Ví dụ 5.2: Common Issues

```bash
# Issue 1: CrashLoopBackOff
# Check logs
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous

# Check events
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# - Application error (check logs)
# - Missing config/secret
# - Liveness probe failing
# - OOMKilled (memory limit too low)

# Issue 2: ImagePullBackOff
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# - Image name wrong
# - ImagePullSecrets missing
# - Network issues

# Issue 3: Pending pods
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -n <namespace>

# Common causes:
# - No nodes with enough resources
# - PVC not bound
# - Affinity rules too restrictive

# Issue 4: Service not accessible
# Check endpoints
kubectl get endpoints <service-name> -n <namespace>

# Check pod labels match service selector
kubectl get pods -n <namespace> --show-labels
kubectl get svc <service-name> -n <namespace> -o yaml

# Test connectivity từ trong cluster
kubectl run -it --rm debug --image=busybox --restart=Never -n <namespace> -- \
  wget -qO- <service-name>:<port>
```

---

## 🔗 TÀI LIỆU THAM KHẢO

1. [Kubernetes Documentation](https://kubernetes.io/docs/)
2. [Helm Chart Repository](https://artifacthub.io/)
3. [Spring Boot on Kubernetes](https://spring.io/guides/gs/spring-boot/)
4. [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
