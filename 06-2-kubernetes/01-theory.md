# Phase 06.5: Kubernetes cho Backend Developers

> **Thời gian:** 3 tuần
> **Mục tiêu:** Deploy và quản lý Spring Boot applications trên Kubernetes
>
> **Tham khảo:** [roadmap.sh/kubernetes](https://roadmap.sh/kubernetes)

---

## 📚 BÀI 0: KUBERNETES OVERVIEW

### 0.1 Tại sao cần Kubernetes?

```
Vấn đề khi chạy containers thủ công:
┌─────────────────────────────────────────────────────────────┐
│  ❌ Manual Container Management                              │
│  - Làm gì khi container crash?                               │
│  - Làm gì khi server hết tài nguyên?                         │
│  - Làm sao để scale khi traffic tăng?                        │
│  - Làm sao để update không downtime?                         │
│  - Làm sao để quản lý 100+ containers?                       │
└─────────────────────────────────────────────────────────────┘

Giải pháp: Kubernetes
┌─────────────────────────────────────────────────────────────┐
│  ✅ Kubernetes Benefits                                      │
│  - Self-healing: Auto restart failed containers              │
│  - Auto-scaling: Scale up/down based on load                 │
│  - Load balancing: Distribute traffic automatically          │
│  - Rolling updates: Zero-downtime deployments                │
│  - Service discovery: DNS-based communication                │
│  - Resource optimization: Efficient cluster utilization      │
└─────────────────────────────────────────────────────────────┘
```

### 0.2 Kubernetes vs Alternatives

| Solution | Use Case | Complexity |
|----------|----------|------------|
| **Docker Swarm** | Small projects, simple setups | Low |
| **Kubernetes** | Production, microservices, multi-cloud | High |
| **Nomad** | Hashicorp stack users, flexible workloads | Medium |
| **ECS/Fargate** | AWS-only workloads | Low-Medium |
| **OpenShift** | Enterprise, need support | High |

### 0.3 Khi nào KHÔNG cần Kubernetes?

```
❌ KHÔNG dùng Kubernetes khi:
- Ứng dụng đơn giản, 1-2 services
- Team nhỏ, không có DevOps expertise
- Chạy trên single server
- Không cần auto-scaling
- Ngân sách hạn chế (K8s master node cost)

✅ Alternatives:
- Docker Compose cho development
- Heroku/Vercel/Railway cho simple apps
- AWS ECS/Fargate cho AWS-only workloads
- DigitalOcean App Platform
```

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

## 📚 BÀI 9: RESOURCE MANAGEMENT

### 9.1 Resource Requests & Limits

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: myapp
    image: myapp:1.0.0
    resources:
      requests:
        memory: "512Mi"    # Guaranteed memory
        cpu: "250m"        # 0.25 CPU core
      limits:
        memory: "1Gi"      # Max memory before OOMKilled
        cpu: "500m"        # Max CPU (throttled if exceeded)
```

**Resource Types:**

| Resource | Description | Unit |
|----------|-------------|------|
| **cpu** | CPU cores | millicores (1000m = 1 core) |
| **memory** | RAM | Mi, Gi |
| **ephemeral-storage** | Temporary storage | Mi, Gi |

**Quality of Service (QoS) Classes:**

```
┌─────────────────────────────────────────────────────────────┐
│  Guaranteed (Highest priority)                               │
│  - requests = limits for all containers                      │
│  - Last to be evicted                                        │
├─────────────────────────────────────────────────────────────┤
│  Burstable (Medium priority)                                 │
│  - requests < limits                                         │
│  - Evicted after Guaranteed pods                             │
├─────────────────────────────────────────────────────────────┤
│  BestEffort (Lowest priority)                                │
│  - No requests/limits specified                              │
│  - First to be evicted                                       │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Resource Quotas

```yaml
# Limit resources in namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: default
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "20"
    services: "10"
    secrets: "20"
    configmaps: "20"
```

---

## 📚 BÀI 10: MONITORING & OBSERVABILITY

### 10.1 Kubernetes Metrics

```bash
# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# View node metrics
kubectl top nodes

# View pod metrics
kubectl top pods

# View pod metrics with labels
kubectl top pods -l app=myapp
```

### 10.2 Health Checks & Probes

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3
  timeoutSeconds: 5

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3
  successThreshold: 1

startupProbe:  # For slow-starting applications
  httpGet:
    path: /actuator/health
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

### 10.3 Debugging Commands

```bash
# View pod status
kubectl get pods
kubectl get pods -o wide
kubectl get pods --show-labels

# Describe pod (events, conditions)
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>           # Follow
kubectl logs --previous <pod-name>   # Previous instance

# Execute in pod
kubectl exec -it <pod-name> -- bash
kubectl exec -it <pod-name> -- sh    # For Alpine

# Port forwarding
kubectl port-forward <pod-name> 8080:8080

# View events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -n <namespace>

# View all resources in namespace
kubectl get all
```

---

## 📚 BÀI 11: SCHEDULING & TAINTS

### 11.1 Node Selector

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  nodeSelector:
    disktype: ssd
    zone: us-east-1a
  containers:
  - name: myapp
    image: myapp:1.0.0
```

### 11.2 Taints and Tolerations

```bash
# Taint a node
kubectl taint nodes node1 key=value:NoSchedule

# Remove taint
kubectl taint nodes node1 key=value:NoSchedule-
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
  containers:
  - name: myapp
    image: myapp:1.0.0
```

### 11.3 Affinity Rules

```yaml
# Node Affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: zone
            operator: In
            values:
            - us-east-1a
            - us-east-1b

# Pod Affinity
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - redis
        topologyKey: kubernetes.io/hostname
```

---

## 📚 BÀI 12: DEPLOYMENT PATTERNS

### 12.1 Rolling Update (Default)

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1         # Extra pods during update
      maxUnavailable: 0   # Pods unavailable during update
```

### 12.2 Blue-Green Deployment

```yaml
# Blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0  # Old version

# Green deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:2.0.0  # New version

# Service switches from blue to green
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp-green  # Change from blue to green
```

### 12.3 Canary Deployment

```yaml
# Main deployment (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0

# Canary deployment (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:2.0.0

# Service selects both (weighted by replicas)
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp  # Both deployments have this label
```

### 12.4 GitOps with ArgoCD (optional)

```yaml
# Application manifest for ArgoCD
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/username/myapp-k8s.git
    targetRevision: HEAD
    path: manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## 📚 BÀI 13: CLUSTER MANAGEMENT

### 13.1 Multi-Cluster Management

```bash
# Configure multiple clusters
kubectl config set-cluster cluster1 --server=https://cluster1:6443
kubectl config set-cluster cluster2 --server=https://cluster2:6443

# Set contexts
kubectl config set-context ctx-cluster1 --cluster=cluster1 --user=admin
kubectl config set-context ctx-cluster2 --cluster=cluster2 --user=admin

# Switch between clusters
kubectl config use-context ctx-cluster1
kubectl config use-context ctx-cluster2
```

### 13.2 Managed Kubernetes Options

| Provider | Service | Notes |
|----------|---------|-------|
| AWS | EKS | Most popular, integrates with AWS |
| GCP | GKE | Best K8s experience (Google created K8s) |
| Azure | AKS | Good for Azure shops |
| DigitalOcean | DOKS | Simple, affordable |
| Linode | LKE | Budget-friendly |

---

## 📚 TÓM TẮT

1. ✅ Kubernetes overview & when to use
2. ✅ Kubernetes architecture (Control Plane, Worker Nodes)
3. ✅ Pods & Deployments
4. ✅ Services (ClusterIP, LoadBalancer, NodePort)
5. ✅ Ingress & Service Discovery
6. ✅ ConfigMaps & Secrets
7. ✅ Auto-scaling (HPA, VPA, Cluster Autoscaler)
8. ✅ StatefulSets & Persistent Volumes
9. ✅ Resource management (requests, limits, quotas)
10. ✅ Monitoring & debugging (metrics, logs, probes)
11. ✅ Scheduling (node selector, taints, affinity)
12. ✅ Deployment patterns (rolling, blue-green, canary)
13. ✅ Helm Charts
14. ✅ RBAC & Security best practices
15. ✅ Managed Kubernetes options

---

## 🔜 TIẾP THEO

Xem `02-examples.md` để xem ví dụ thực tế!
