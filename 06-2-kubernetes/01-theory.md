# Phase 06.5: Kubernetes cho Backend Developers

> **Thời gian:** 3 tuần
> **Mục tiêu:** Deploy và quản lý Spring Boot applications trên Kubernetes

---

## 📚 BÀI 1: KUBERNETES FUNDAMENTALS

### 1.1 Kubernetes là gì?

```
Kubernetes (K8s) = Container orchestration platform

Giúp:
- Auto-deploy containers
- Auto-scaling khi tải cao
- Self-healing (restart failed containers)
- Load balancing
- Rolling updates (zero-downtime deployment)
```

### 1.2 Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CONTROL PLANE (Master Node)                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  API Server           │  Scheduler                       │   │
│  │  - Gateway to K8s     │  - Assign Pods to Nodes          │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  Controller Manager   │  etcd (Key-Value Store)          │   │
│  │  - Maintains state    │  - Cluster configuration         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ─────────────────────────────────────────────────────────────  │
│                              │                                   │
│  WORKER NODES                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │     Node 1      │  │     Node 2      │  │     Node 3      │  │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤  │
│  │  Kubelet        │  │  Kubelet        │  │  Kubelet        │  │
│  │  Kube-proxy     │  │  Kube-proxy     │  │  Kube-proxy     │  │
│  │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │  │
│  │  │   Pod     │  │  │  │   Pod     │  │  │  │   Pod     │  │  │
│  │  │ Container │  │  │  │ Container │  │  │  │ Container │  │  │
│  │  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Các thành phần chính

| Component | Description |
|-----------|-------------|
| **Pod** | Đơn vị nhỏ nhất - chứa 1+ containers |
| **Deployment** | Quản lý Pods (replicas, updates) |
| **Service** | Load balancing, service discovery |
| **ConfigMap** | Cấu hình ngoài cho ứng dụng |
| **Secret** | Lưu trữ sensitive data (passwords, keys) |
| **Ingress** | HTTP/HTTPS routing từ bên ngoài |
| **HPA** | Horizontal Pod Autoscaler |

---

## 📚 BÀI 2: PODS & DEPLOYMENTS

### 2.1 Pod - Đơn vị cơ bản

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: myapp:1.0.0
    ports:
    - containerPort: 8080
    env:
    - name: SPRING_PROFILES_ACTIVE
      value: "production"
    resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
      limits:
        memory: "1Gi"
        cpu: "500m"
```

**Tại sao không run container trực tiếp?**

```
Pod benefits:
- Multiple containers chia sẻ storage/network
- Sidecar pattern (logging, monitoring)
- Lifecycle management
- Health checks (liveness, readiness)
```

### 2.2 Deployment - Quản lý Pods

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3                    # Số lượng Pods
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp-container
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
        livenessProbe:           # Check app có sống không
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:          # Check app sẵn sàng nhận traffic
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### 2.3 Deployment Strategies

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROLLING UPDATE (Default)                      │
├─────────────────────────────────────────────────────────────────┤
│  v1: [●●●]  →  v1: [●●○]  →  v1: [●○○]  →  v1: [○○○]           │
│              v2: [○○●]     v2: [○○●●]    v2: [●●●]             │
│                                                                  │
│  Zero-downtime, gradual replacement                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    BLUE-GREEN DEPLOYMENT                         │
├─────────────────────────────────────────────────────────────────┤
│  Blue: [v1 v1 v1]  ← Active                                     │
│  Green: [    ]     ← Deploy v2, test                            │
│                                                                  │
│  Switch traffic: Blue → Green                                   │
│  Rollback: Switch lại Blue                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    CANARY DEPLOYMENT                             │
├─────────────────────────────────────────────────────────────────┤
│  v1: [●●●●●]  (95% traffic)                                     │
│  v2: [●    ]  (5% traffic - testing)                            │
│                                                                  │
│  Tăng dần traffic cho v2 nếu ổn định                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 3: SERVICES & NETWORKING

### 3.1 Service Types

```yaml
# ClusterIP - Internal only
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080

# LoadBalancer - External access (cloud provider)
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080

# NodePort - Access via node IP
apiVersion: v1
kind: Service
metadata:
  name: myapp-nodeport
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080  # 30000-32767
```

### 3.2 Service Discovery

```
┌─────────────────────────────────────────────────────────────────┐
│                    DNS-BASED DISCOVERY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Pod A → myapp-service.default.svc.cluster.local:80 → Pod B    │
│                                                                  │
│  Format: <service-name>.<namespace>.svc.cluster.local          │
│                                                                  │
│  Trong cùng namespace: <service-name>:<port>                   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Ingress - HTTP Routing

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /users
        pathType: Prefix
        backend:
          service:
            name: user-service
            port:
              number: 8080
      - path: /orders
        pathType: Prefix
        backend:
          service:
            name: order-service
            port:
              number: 8080
  tls:
  - hosts:
    - api.example.com
    secretName: tls-secret
```

---

## 📚 BÀI 4: CONFIGMAPS & SECRETS

### 4.1 ConfigMap - Cấu hình ứng dụng

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  application.yml: |
    server:
      port: 8080
    spring:
      datasource:
        url: jdbc:postgresql://db-service:5432/mydb
        username: ${DB_USERNAME}
        password: ${DB_PASSWORD}
    logging:
      level:
        com.example: INFO
    cache:
      redis:
        host: redis-service
        port: 6379
```

**Mount ConfigMap vào Pod:**

```yaml
spec:
  containers:
  - name: myapp
    image: myapp:1.0.0
    volumeMounts:
    - name: config-volume
      mountPath: /app/config
    envFrom:
    - configMapRef:
        name: myapp-config
  volumes:
  - name: config-volume
    configMap:
      name: myapp-config
```

### 4.2 Secrets - Sensitive data

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:
  DB_USERNAME: admin
  DB_PASSWORD: SuperSecret123!
```

**Tạo Secret từ CLI:**

```bash
# Tạo secret từ literal
kubectl create secret generic db-credentials \
  --from-literal=DB_USERNAME=admin \
  --from-literal=DB_PASSWORD=SuperSecret123!

# Tạo secret từ file
kubectl create secret generic tls-secret \
  --from-file=tls.crt=certificate.pem \
  --from-file=tls.key=key.pem
```

---

## 📚 BÀI 5: AUTO-SCALING & SELF-HEALING

### 5.1 Horizontal Pod Autoscaler (HPA)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-deployment
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
```

**HPA hoạt động:**

```
Traffic thấp: [●●] (2 pods)
              ↓
Traffic tăng: [●●●●●●] (6 pods) - HPA scale up
              ↓
Traffic giảm: [●●] (2 pods) - HPA scale down
```

### 5.2 Vertical Pod Autoscaler (VPA)

```yaml
# vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-deployment
  updatePolicy:
    updateMode: Auto  # Auto/Recreate/Off
  resourcePolicy:
    containerPolicies:
    - containerName: '*'
      minAllowed:
        cpu: "100m"
        memory: "256Mi"
      maxAllowed:
        cpu: "1000m"
        memory: "2Gi"
```

### 5.3 Self-Healing với Probes

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 30    # Đợi 30s sau khi start
  periodSeconds: 10          # Check mỗi 10s
  failureThreshold: 3        # 3 lần fail → restart

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3        # 3 lần fail → remove khỏi Service
```

---

## 📚 BÀI 6: STATEFULSETS & STORAGE

### 6.1 StatefulSet - Cho stateful apps

```yaml
# statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-statefulset
spec:
  serviceName: postgres
  replicas: 3
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
        image: postgres:15
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

**StatefulSet vs Deployment:**

| Feature | Deployment | StatefulSet |
|---------|-----------|-------------|
| Pod names | Random (myapp-abc123) | Predictable (postgres-0, postgres-1) |
| Storage | Ephemeral | Persistent (PVC) |
| Scaling | Any order | Ordered (0→1→2) |
| Use case | Stateless apps | Databases, queues |

### 6.2 Persistent Volumes

```yaml
# pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/data/postgres

# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

---

## 📚 BÀI 7: HELM CHARTS

### 7.1 Helm là gì?

```
Helm = Package manager for Kubernetes

Giống như:
- npm cho Node.js
- Maven cho Java
- apt cho Ubuntu

Benefits:
- Templating (values dev/prod/staging)
- Version control cho manifests
- Easy install/uninstall
```

### 7.2 Helm Chart Structure

```
myapp-chart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── values-prod.yaml    # Production overrides
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    ├── ingress.yaml
    └── _helpers.tpl    # Template helpers
```

### 7.3 Example Chart

```yaml
# Chart.yaml
apiVersion: v2
name: myapp
description: Spring Boot application
version: 1.0.0
appVersion: "1.0.0"

# values.yaml
replicaCount: 3
image:
  repository: myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
service:
  type: ClusterIP
  port: 80

# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    spec:
      containers:
      - name: {{ .Release.Name }}
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        resources: {{- toYaml .Values.resources | nindent 10 }}
```

### 7.4 Helm Commands

```bash
# Install chart
helm install myapp ./myapp-chart -f values-prod.yaml

# Upgrade release
helm upgrade myapp ./myapp-chart --set image.tag=1.1.0

# Rollback
helm rollback myapp 1

# List releases
helm list

# Uninstall
helm uninstall myapp

# Create new chart
helm create my-chart
```

---

## 📚 BÀI 8: RBAC & SECURITY

### 8.1 Service Account

```yaml
# serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: default
```

### 8.2 Role & RoleBinding

```yaml
# role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]

# rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: ServiceAccount
  name: myapp-sa
  namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### 8.3 Security Best Practices

```yaml
# Pod Security Context
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: myapp
    image: myapp:1.0.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
    resources:
      limits:
        cpu: "500m"
        memory: "1Gi"
```

---

## 📚 TÓM TẮT PHASE 06.5

1. ✅ Kubernetes architecture (Control Plane, Worker Nodes)
2. ✅ Pods & Deployments
3. ✅ Services (ClusterIP, LoadBalancer, NodePort)
4. ✅ Ingress & Service Discovery
5. ✅ ConfigMaps & Secrets
6. ✅ Auto-scaling (HPA, VPA)
7. ✅ StatefulSets & Persistent Volumes
8. ✅ Helm Charts
9. ✅ RBAC & Security best practices

---

## 🔜 TIẾP THEO

Xem `02-examples.md` để xem ví dụ thực tế!
