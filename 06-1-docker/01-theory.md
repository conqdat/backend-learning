# Docker Fundamentals

> **Thời gian:** 2 tuần
> **Mục tiêu:** Master Docker, containerize Spring Boot applications, Docker Compose
>
> **Tham khảo:** [roadmap.sh/docker](https://roadmap.sh/docker)

---

## 📚 BÀI 0: PREREQUISITES & LINUX FUNDAMENTALS

### 0.1 Linux Fundamentals for Docker

**Shell Commands cần biết:**

```bash
# File operations
ls, cd, pwd, cp, mv, rm, mkdir, touch, cat, less, tail, head

# Process management
ps, top, kill, pkill, systemctl, service

# Network
netstat, ss, curl, wget, ping, nslookup, dig

# Permissions
chmod, chown, chgrp

# Package managers
apt-get, yum, dnf, apk (Alpine)
```

**Shell Scripting cơ bản:**

```bash
#!/bin/bash
# Variables
NAME="Docker"
echo "Hello $NAME"

# Conditionals
if [ -f "/path/to/file" ]; then
    echo "File exists"
fi

# Loops
for i in 1 2 3; do
    echo "Number $i"
done

# Functions
my_function() {
    echo "This is a function"
}
```

**Users & Groups:**

```bash
# Create user
useradd -m appuser

# Set password
passwd appuser

# Switch user
su - appuser

# Run as user (in Dockerfile)
USER appuser
```

---

### 0.2 Container Underlying Technologies

**Namespaces (Process Isolation):**

```bash
# PID Namespace - Process isolation
unshare --pid --fork bash

# NET Namespace - Network isolation
unshare --net bash

# MNT Namespace - Filesystem isolation
unshare --mount bash

# UTS Namespace - Hostname isolation
unshare --uts bash

# IPC Namespace - Inter-process communication
unshare --ipc bash

# USER Namespace - User/group isolation
unshare --user bash
```

**cgroups (Resource Limits):**

```bash
# Memory limit
echo 536870912 > /sys/fs/cgroup/memory/mygroup/memory.limit_in_bytes

# CPU limit
echo 50000 > /sys/fs/cgroup/cpu/mygroup/cpu.cfs_quota_us

# Docker does this automatically:
docker run --memory=512m --cpus=1.0 myimage
```

**Union Filesystems (Layered Filesystem):**

```
┌─────────────────────────────────────────┐
│  Container Layer (Read-Write)           │
├─────────────────────────────────────────┤
│  Image Layer 3 (Read-Only)              │
├─────────────────────────────────────────┤
│  Image Layer 2 (Read-Only)              │
├─────────────────────────────────────────┤
│  Image Layer 1 (Read-Only)              │
├─────────────────────────────────────────┤
│  Bootfs (Boot Filesystem)               │
└─────────────────────────────────────────┘
```

---

---

## 📚 BÀI 1: DOCKER FUNDAMENTALS

### 1.1 Containers vs Virtual Machines

```
┌─────────────────────────────────────────────────────────────────┐
│              VIRTUAL MACHINES vs CONTAINERS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VIRTUAL MACHINES:                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  App A  │  App B  │  App C                              │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  Guest OS │  Guest OS │  Guest OS                       │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │           Hypervisor (VM Manager)                       │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                Host OS                                  │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                Hardware                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  - Heavy (GBs per VM)                                           │
│  - Slow boot (minutes)                                          │
│  - Full isolation                                                │
│                                                                  │
│  CONTAINERS:                                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Container A │ Container B │ Container C                │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │           Container Engine (Docker)                     │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                Host OS                                  │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                Hardware                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  - Lightweight (MBs per container)                              │
│  - Fast boot (seconds)                                          │
│  - Process-level isolation                                       │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Docker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Client (docker CLI)                                            │
│       │                                                          │
│       │ docker run/build/push                                   │
│       ▼                                                          │
│  Docker Daemon (dockerd)                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  REST API                                                │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  Core Components:                                        │   │
│  │  - Image Builder                                         │   │
│  │  - Container Manager                                     │   │
│  │  - Registry Client                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                          │
│       ├──────────────┬──────────────┬──────────────┐           │
│       ▼              ▼              ▼              ▼           │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────┐   │
│  │ Images  │   │Containers│   │ Networks │   │  Volumes    │   │
│  │  (RO)   │   │ (RW)    │   │          │   │  (Persist)  │   │
│  └─────────┘   └─────────┘   └─────────┘   └─────────────┘   │
│                                                                  │
│  Registry (Docker Hub, ECR, GCR)                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  docker.io/library/ubuntu                               │   │
│  │  amazoncorretto:17                                      │   │
│  │  postgres:15                                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Docker Objects

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER OBJECTS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  IMAGE:                                                         │
│  - Read-only template with application + dependencies           │
│  - Built from Dockerfile                                        │
│  - Layers (union filesystem)                                    │
│  Example: myapp:1.0.0                                           │
│                                                                  │
│  CONTAINER:                                                     │
│  - Runnable instance of an image                                │
│  - Has writable layer on top                                    │
│  - Can be started/stopped/deleted                               │
│  Example: docker run myapp:1.0.0                                │
│                                                                  │
│  VOLUME:                                                        │
│  - Persistent data storage                                      │
│  - Survives container deletion                                  │
│  - Share data between containers                                │
│  Example: docker volume create mydata                           │
│                                                                  │
│  NETWORK:                                                       │
│  - Connect containers                                             │
│  - Types: bridge, host, overlay, none                           │
│  Example: docker network create mynet                           │
│                                                                  │
│  DOCKERFILE:                                                    │
│  - Text file with build instructions                            │
│  - Docker builds image from this                                │
│  Example: See section 2.1                                       │
│                                                                  │
│  DOCKER COMPOSE:                                                │
│  - Define multi-container applications                          │
│  - YAML format                                                  │
│  Example: docker-compose.yml                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 2: DOCKERFILE & IMAGE BUILDING

### 2.1 Dockerfile Instructions

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKERFILE INSTRUCTIONS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FROM <image>[:tag]                                             │
│  - Base image to build upon                                     │
│  - Should be first instruction (usually)                        │
│                                                                  │
│  WORKDIR /path                                                  │
│  - Set working directory for subsequent instructions            │
│                                                                  │
│  COPY <src> <dest>                                              │
│  - Copy files from build context to image                       │
│                                                                  │
│  ADD <src> <dest>                                               │
│  - Like COPY but also extracts tarballs, supports URLs          │
│                                                                  │
│  RUN <command>                                                  │
│  - Execute command during build (creates new layer)             │
│                                                                  │
│  ENV KEY=value                                                  │
│  - Set environment variables                                    │
│                                                                  │
│  ARG name=default                                               │
│  - Build-time variable (not in final image)                     │
│                                                                  │
│  EXPOSE <port>                                                  │
│  - Document which port container listens on                     │
│                                                                  │
│  CMD ["executable", "param1", "param2"]                         │
│  - Default command when container starts                        │
│  - Can be overridden at runtime                                 │
│                                                                  │
│  ENTRYPOINT ["executable"]                                      │
│  - Configure container to run as executable                     │
│  - CMD args passed as parameters                                │
│                                                                  │
│  USER <username>                                                │
│  - Switch to non-root user (security)                           │
│                                                                  │
│  HEALTHCHECK --interval=30s --timeout=3s CMD <command>          │
│  - Check if container is healthy                                │
│                                                                  │
│  LABEL key=value                                                │
│  - Add metadata to image                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Image Layers & Caching

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER IMAGE LAYERS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Dockerfile:                                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  FROM amazoncorretto:17        ← Layer 1 (Base Image)   │   │
│  │  WORKDIR /app                  ← Layer 2                │   │
│  │  COPY build.gradle ./          ← Layer 3                │   │
│  │  RUN gradle dependencies       ← Layer 4 (expensive!)   │   │
│  │  COPY src/ ./src/              ← Layer 5                │   │
│  │  RUN gradle build              ← Layer 6                │   │
│  │  CMD ["java", "-jar", "app.jar"] ← Layer 7              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Build Cache Behavior:                                          │
│  - Docker caches each layer                                     │
│  - If layer unchanged, use cached version                       │
│  - Cache invalidated when instruction changes                   │
│                                                                  │
│  Best Practice:                                                 │
│  1. Order instructions: least changed → most changed            │
│  2. COPY dependencies first, then source code                   │
│  3. Combine RUN commands (reduce layers)                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 3: DOCKER COMPOSE

### 3.1 Docker Compose File Structure

```yaml
version: '3.8'

services:
  service-name:
    image: image-name:tag
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "host:container"
    volumes:
      - source:destination
    environment:
      - KEY=value
    env_file:
      - .env
    depends_on:
      - other-service
    networks:
      - network-name
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  network-name:
    driver: bridge

volumes:
  volume-name:
```

### 3.2 Service Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│              DOCKER COMPOSE DEPENDENCIES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  depends_on (short form):                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  services:                                               │   │
│  │    web:                                                  │   │
│  │      depends_on:                                         │   │
│  │        - db                                              │   │
│  │        - redis                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│  - Starts services in order                                    │
│  - Does NOT wait for service to be ready                       │
│                                                                  │
│  depends_on (long form with condition):                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  services:                                               │   │
│  │    web:                                                  │   │
│  │      depends_on:                                         │   │
│  │        db:                                               │   │
│  │          condition: service_healthy                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│  - Waits until health check passes                             │
│  - Requires healthcheck in dependent service                   │
│                                                                  │
│  wait_for_it.sh script:                                        │
│  - Custom script to wait for port/database                     │
│  - More control over timeout, retries                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 4: DOCKER VOLUMES & DATA PERSISTENCE

### 4.1 Storage Options

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER STORAGE OPTIONS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VOLUMES:                                                       │
│  - Managed by Docker (/var/lib/docker/volumes/)                 │
│  - Best for persistence, backup, sharing                        │
│  - Can mount to multiple containers                             │
│  Example: docker volume create mydata                           │
│           docker run -v mydata:/data myimage                    │
│                                                                  │
│  BIND MOUNTS:                                                   │
│  - Mount host filesystem path                                   │
│  - Good for development (code sync)                             │
│  - Path-dependent (not portable)                                │
│  Example: docker run -v /host/path:/container/path myimage      │
│                                                                  │
│  TMPFS:                                                         │
│  - In-memory storage (Linux only)                               │
│  - Not persisted, fast                                          │
│  - For sensitive data                                           │
│  Example: docker run --tmpfs /app myimage                       │
│                                                                  │
│  ANONYMOUS VOLUMES:                                             │
│  - No name, auto-generated                                      │
│  - Used when you don't need to share/reuse                      │
│  Example: docker run -v /var/lib/mysql myimage                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Volume Use Cases

```
Database Persistence:
┌─────────────────────────────────────────────────────────────┐
│  volumes:                                                   │
│    - postgres-data:/var/lib/postgresql/data                 │
│                                                             │
│  volumes:                                                   │
│    postgres-data:                                           │
└─────────────────────────────────────────────────────────────┘

Development (Bind Mount):
┌─────────────────────────────────────────────────────────────┐
│  volumes:                                                   │
│    - ./src:/app/src       # Code sync                       │
│    - ./config:/app/config # Config sync                     │
└─────────────────────────────────────────────────────────────┘

Shared Data (Multiple Containers):
┌─────────────────────────────────────────────────────────────┐
│  services:                                                  │
│    app1:                                                    │
│      volumes:                                               │
│        - shared-data:/shared                                │
│    app2:                                                    │
│      volumes:                                               │
│        - shared-data:/shared                                │
│                                                             │
│  volumes:                                                   │
│    shared-data:                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 5: DOCKER NETWORKING

### 5.1 Network Types

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER NETWORK TYPES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BRIDGE (default):                                              │
│  - Private network on host                                      │
│  - Containers communicate via IP/name                           │
│  - Port mapping for external access                             │
│  Example: docker network create mynet                           │
│                                                                  │
│  HOST:                                                          │
│  - Container shares host's network                              │
│  - No port mapping needed                                        │
│  - No network isolation                                         │
│  Example: docker run --network host myimage                     │
│                                                                  │
│  OVERLAY:                                                       │
│  - Connect multiple Docker daemons (Swarm)                      │
│  - Cross-host communication                                     │
│  Example: docker network create -d overlay mynet                │
│                                                                  │
│  NONE:                                                          │
│  - No networking                                                │
│  - For isolated containers                                      │
│  Example: docker run --network none myimage                     │
│                                                                  │
│  BRIDGE (default):                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Container A (172.18.0.2)                               │   │
│  │       │                                                  │   │
│  │       ▼                                                  │   │
│  │  ┌─────────────┐     ┌─────────────┐                    │   │
│  │  │   bridge    │◄────┤   docker0   │                    │   │
│  │  │   network   │     │   (bridge)  │                    │   │
│  │  └─────────────┘     └─────────────┘                    │   │
│  │       │                                                  │   │
│  │       ▼                                                  │   │
│  │  Container B (172.18.0.3)                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Service Discovery

```
Within same network:
┌─────────────────────────────────────────────────────────────┐
│  services:                                                  │
│    web:                                                     │
│      # Can reach db by service name                         │
│      environment:                                           │
│        - DB_HOST=db       # ← Service name!                │
│    db:                                                      │
│      image: postgres:15                                     │
│                                                             │
│  # From web container:                                      │
│  psql -h db -U postgres  # ← 'db' resolves automatically   │
└─────────────────────────────────────────────────────────────┘

DNS Resolution:
- Docker provides embedded DNS server
- Service name → Container IP
- Works within same network
```

---

## 📚 BÀI 6: MULTI-STAGE BUILDS

### 6.1 What & Why

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULTI-STAGE BUILDS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Problem:                                                       │
│  - Build tools increase image size                              │
│  - Development dependencies not needed in production            │
│  - Security concerns (build tools = attack surface)             │
│                                                                  │
│  Solution: Multi-stage builds                                   │
│  - Stage 1: Build with full toolchain                           │
│  - Stage 2: Copy only artifacts to minimal runtime image        │
│  - Result: Small, secure production image                       │
│                                                                  │
│  Before (Single-stage):                                         │
│  FROM maven:3.9-amazoncorretto-17  ← 500MB+                    │
│  ... build ...                                                   │
│  CMD ["java", "-jar", "app.jar"]                                │
│  Final size: ~550MB                                             │
│                                                                  │
│  After (Multi-stage):                                           │
│  FROM maven:3.9-amazoncorretto-17 AS builder  # Build stage    │
│  ... build ...                                                   │
│                                                                  │
│  FROM amazoncorretto:17-alpine  # Runtime stage (~50MB)        │
│  COPY --from=builder app.jar ./                                 │
│  CMD ["java", "-jar", "app.jar"]                                │
│  Final size: ~100MB (80% smaller!)                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 7: DOCKER SECURITY BEST PRACTICES

### 7.1 Security Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│              DOCKER SECURITY BEST PRACTICES                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. USE OFFICIAL/VERIFIED IMAGES                                │
│     ✅ FROM amazoncorretto:17                                   │
│     ✅ FROM eclipse-temurin:17-jre-alpine                       │
│     ❌ FROM random-user/mystery-image:latest                    │
│                                                                  │
│  2. SCAN IMAGES FOR VULNERABILITIES                             │
│     docker scan myimage                                         │
│     trivy image myimage                                         │
│     grype myimage                                               │
│                                                                  │
│  3. RUN AS NON-ROOT USER                                        │
│     RUN adduser -D appuser                                      │
│     USER appuser                                                │
│     CMD ["java", "-jar", "app.jar"]                             │
│                                                                  │
│  4. USE SPECIFIC TAGS (NOT :latest)                             │
│     ✅ FROM postgres:15.3-alpine                                │
│     ❌ FROM postgres:latest                                     │
│                                                                  │
│  5. MINIMIZE LAYERS & COMBINE COMMANDS                          │
│     RUN apt-get update && apt-get install -y \                  │
│         package1 \                                              │
│         package2 \                                              │
│         && rm -rf /var/lib/apt/lists/*                          │
│                                                                  │
│  6. USE .dockerignore                                           │
│     target/                                                     │
│     .git/                                                       │
│     .env                                                        │
│     *.md                                                        │
│                                                                  │
│  7. SET RESOURCE LIMITS                                         │
│     docker run --memory=512m --cpus=1.0 myimage                 │
│     # Or in docker-compose.yml:                                 │
│     deploy:                                                     │
│       resources:                                                │
│         limits:                                                 │
│           cpus: '1.0'                                           │
│           memory: 512M                                          │
│                                                                  │
│  8. REMOVE UNNECESSARY TOOLS                                    │
│     Use -alpine or -slim variants                               │
│     Don't install curl, wget, ssh in production                 │
│                                                                  │
│  9. USE READ-ONLY FILESYSTEM                                    │
│     docker run --read-only myimage                              │
│     # Mount writable volumes for needed paths                   │
│     -v /tmp                                                      │
│                                                                  │
│  10. SECRETS MANAGEMENT                                         │
│      ❌ ENV DB_PASSWORD=secret123  # In image!                  │
│      ✅ docker run -e DB_PASSWORD=$(cat .env)                   │
│      ✅ docker secret create db_pass .env                       │
│      ✅ Use Docker Swarm/K8s secrets                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 8: DOCKER REGISTRY & IMAGE MANAGEMENT

### 8.1 Container Registries

**Public Registries:**

```bash
# Docker Hub (default)
docker pull nginx:latest
docker push myusername/myimage:latest

# Amazon ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
docker tag myimage:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/myimage:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/myimage:latest

# Google Container Registry (GCR)
docker tag myimage:latest gcr.io/my-project/myimage:latest
docker push gcr.io/my-project/myimage:latest

# GitHub Container Registry (ghcr)
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
docker tag myimage:latest ghcr.io/username/myimage:latest
docker push ghcr.io/username/myimage:latest
```

### 8.2 Image Tagging Best Practices

```bash
# ✅ GOOD: Specific version tags
docker tag myapp:1.0.0
docker tag myapp:1.0
docker tag myapp:1

# ✅ GOOD: Semantic versioning
docker tag myapp:1.2.3

# ✅ GOOD: Environment-specific
docker tag myapp:1.2.3-staging
docker tag myapp:1.2.3-production

# ❌ BAD: Using :latest in production
docker tag myapp:latest  # Avoid in production!

# ✅ GOOD: Multi-platform tags
docker tag myapp:1.2.3-linux-amd64
docker tag myapp:1.2.3-linux-arm64
```

### 8.3 Image Management Commands

```bash
# List images
docker images
docker image ls

# Inspect image
docker image inspect myimage:1.0

# View image history
docker image history myimage:1.0

# Remove image
docker image rm myimage:1.0
docker rmi myimage:1.0

# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a

# Save image to tarball
docker save -o myimage.tar myimage:1.0

# Load image from tarball
docker load -i myimage.tar

# Export container filesystem
docker export -o container.tar container_id

# Import from tarball
docker import container.tar newimage:1.0
```

---

## 📚 BÀI 9: DOCKER LOGGING & DEBUGGING

### 9.1 Logging

```bash
# View container logs
docker logs container_name

# Follow logs (like tail -f)
docker logs -f container_name

# Show last N lines
docker logs --tail 100 container_name

# Show timestamps
docker logs -t container_name

# Show logs since time
docker logs --since 2024-01-15T10:00:00 container_name

# Show logs for last 5 minutes
docker logs --since 5m container_name

# View logs from specific container
docker logs --details container_name
```

**Logging Drivers:**

```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  # Other drivers:
  # - syslog
  # - journald
  # - gelf (Graylog)
  # - fluentd
  # - awslogs
  # - splunk
```

### 9.2 Debugging Containers

```bash
# Inspect container
docker inspect container_name

# View container processes
docker top container_name

# View live resource usage
docker stats container_name

# Copy files from container
docker cp container_name:/path/to/file ./local_file

# Copy files to container
docker cp ./local_file container_name:/path/

# Execute command in running container
docker exec -it container_name bash
docker exec -it container_name sh  # For Alpine

# Execute as specific user
docker exec -u root container_name bash

# Check container network
docker exec container_name netstat -tlnp
docker exec container_name curl localhost:8080

# Inspect container filesystem
docker diff container_name  # Show changed files
```

**Debug with temporary container:**

```bash
# Run container with entrypoint override
docker run -it --entrypoint /bin/bash myimage

# Run with different command
docker run myimage java -version

# Run with environment override
docker run -e DEBUG=true myimage

# Run with volume for log inspection
docker run -v /var/log/myapp:/logs myimage
```

---

## 📚 BÀI 10: DOCKER IN CI/CD

### 10.1 Docker in Continuous Integration

```yaml
# GitHub Actions example
name: Build and Push Docker Image

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            user/app:${{ github.sha }}
            user/app:latest
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max

      - name: Run tests
        run: docker run user/app:${{ github.sha }} ./mvnw test
```

### 10.2 Docker Build Best Practices for CI/CD

```dockerfile
# Use BuildKit for better performance
# syntax=docker/dockerfile:1

# Build arguments for CI
ARG VERSION=unknown
ARG BUILD_DATE=unknown
ARG GIT_COMMIT=unknown

LABEL version=$VERSION
LABEL build-date=$BUILD_DATE
LABEL git-commit=$GIT_COMMIT

# Multi-stage for testing
FROM maven:3.9-amazoncorretto-17 AS test
WORKDIR /app
COPY . .
RUN ./mvnw test

# Build stage
FROM maven:3.9-amazoncorretto-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN ./mvnw dependency:go-offline
COPY src ./src
RUN ./mvnw package -DskipTests

# Runtime stage
FROM amazoncorretto:17-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## 📚 TÓM TẮT

1. ✅ Linux fundamentals & shell commands
2. ✅ Container underlying technologies (namespaces, cgroups, union filesystems)
3. ✅ Docker fundamentals (containers vs VMs, architecture)
4. ✅ Dockerfile instructions & best practices
5. ✅ Image layers & caching strategies
6. ✅ Docker Compose for multi-container apps
7. ✅ Volumes for data persistence (volumes, bind mounts, tmpfs)
8. ✅ Docker networking (bridge, host, overlay, none)
9. ✅ Multi-stage builds for smaller images
10. ✅ Security best practices
11. ✅ Container registries (Docker Hub, ECR, GCR, ghcr)
12. ✅ Image tagging best practices
13. ✅ Logging & debugging
14. ✅ Docker in CI/CD

---

## 🔜 TIẾP THEO

Xem `02-examples.md` để xem ví dụ thực tế!
