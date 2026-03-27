# Phase 06.3: Docker - Ví Dụ Thực Tế

---

## 📁 BÀI 1: DOCKERIZE SPRING BOOT APPLICATION

### Ví dụ 1.1: Basic Dockerfile

```dockerfile
# Dockerfile
FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

# Copy JAR file
COPY target/myapp-1.0.0.jar app.jar

# Expose port
EXPOSE 8080

# Run application
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Build & Run:**
```bash
# Build JAR
./gradlew bootJar

# Build Docker image
docker build -t myapp:1.0.0 .

# Run container
docker run -d -p 8080:8080 --name myapp myapp:1.0.0

# Check logs
docker logs -f myapp

# Test endpoint
curl http://localhost:8080/actuator/health

# Stop container
docker stop myapp

# Remove container
docker rm myapp
```

---

### Ví dụ 1.2: Optimized Dockerfile (Multi-stage)

```dockerfile
# Dockerfile
# ============================================================
# BUILD STAGE
# ============================================================
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Copy gradle files first (better caching)
COPY build.gradle settings.gradle ./
COPY gradle/ ./gradle/
COPY gradlew ./

# Download dependencies (cached layer)
RUN ./gradlew downloadDependencies || true

# Copy source code
COPY src/ ./src/

# Build application
RUN ./gradlew bootJar -x test

# ============================================================
# RUNTIME STAGE
# ============================================================
FROM eclipse-temurin:17-jre-alpine

# Create non-root user
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -s /bin/sh -D appuser

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder --chown=appuser:appgroup \
    /app/build/libs/*.jar app.jar

# Switch to non-root user
USER appuser

# JVM optimizations for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport \
               -XX:MaxRAMPercentage=75.0 \
               -Djava.security.egd=file:/dev/./urandom"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
    CMD wget -qO- http://localhost:8080/actuator/health || exit 1

# Run application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

---

### Ví dụ 1.3: .dockerignore

```bash
# .dockerignore

# Build outputs
target/
build/
!.mvn/wrapper/maven-wrapper.jar

# IDE
.idea/
*.iml
.vscode/
.settings/
.project
.classpath

# Git
.git/
.gitignore

# Documentation
*.md
README*
docs/

# Tests
src/test/

# Local config
.env
*.local.yml
application-local.yml

# Docker
Dockerfile
docker-compose*.yml
.docker/

# OS
.DS_Store
Thumbs.db
```

---

## 📁 BÀI 2: DOCKER COMPOSE CHO DEVELOPMENT

### Ví dụ 2.1: Spring Boot + PostgreSQL + Redis

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: myapp
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=docker
      - SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/mydb
      - SPRING_DATASOURCE_USERNAME=postgres
      - SPRING_DATASOURCE_PASSWORD=postgres123
      - SPRING_REDIS_HOST=redis
      - SPRING_REDIS_PORT=6379
      - JAVA_OPTS=-Xmx256m -Xms128m
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
    networks:
      - mynetwork
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    container_name: postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres123
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - mynetwork
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - mynetwork
    restart: unless-stopped

networks:
  mynetwork:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
```

**Usage:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app
docker-compose logs -f postgres

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart specific service
docker-compose restart app

# Execute command in container
docker-compose exec app ls -la
docker-compose exec postgres psql -U postgres -d mydb
docker-compose exec redis redis-cli
```

---

### Ví dụ 2.2: Development với Hot Reload

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: myapp-dev
    ports:
      - "8080:8080"
      - "5005:5005"  # Debug port
    environment:
      - SPRING_PROFILES_ACTIVE=dev
      - SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/mydb
      - SPRING_DATASOURCE_USERNAME=dev
      - SPRING_DATASOURCE_PASSWORD=dev123
      - SPRING_REDIS_HOST=redis
      - JAVA_OPTS=-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005
    volumes:
      # Mount source code for hot reload
      - ./src:/app/src
      - ./build.gradle:/app/build.gradle
      - ./settings.gradle:/app/settings.gradle
      # Gradle cache
      - gradle-cache:/home/gradle/.gradle
    depends_on:
      - postgres
      - redis
    networks:
      - mynetwork

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=dev
      - POSTGRES_PASSWORD=dev123
    ports:
      - "5432:5432"
    volumes:
      - postgres-dev-data:/var/lib/postgresql/data
    networks:
      - mynetwork

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - mynetwork

volumes:
  postgres-dev-data:
  gradle-cache:

networks:
  mynetwork:
```

```dockerfile
# Dockerfile.dev
FROM eclipse-temurin:17-jdk-alpine

# Install watchexec for file watching
RUN apk add --no-cache watchexec

WORKDIR /app

# Install gradle
ENV GRADLE_VERSION=8.5
RUN wget https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip && \
    unzip gradle-${GRADLE_VERSION}-bin.zip -d /opt && \
    ln -s /opt/gradle-${GRADLE_VERSION}/bin/gradle /usr/local/bin/gradle && \
    rm gradle-${GRADLE_VERSION}-bin.zip

COPY build.gradle settings.gradle ./
COPY gradle/ ./gradle/

# Download dependencies
RUN gradle downloadDependencies || true

COPY src/ ./src/

# Run with watchexec for auto-reload
CMD ["watchexec", "-r", "-w", "src", "-w", "build.gradle", \
     "gradle", "bootRun", "--args='--spring.profiles.active=dev'"]
```

---

## 📁 BÀI 3: DOCKER COMPOSE CHO MICROSERVICES

### Ví dụ 3.1: E-commerce Microservices

```yaml
# docker-compose.yml
version: '3.8'

services:
  # API Gateway
  gateway:
    build:
      context: ./api-gateway
    ports:
      - "8080:8080"
    environment:
      - EUREKA_CLIENT_SERVICEURL_DEFAULTZONE=http://eureka:8761/eureka
    depends_on:
      - eureka
    networks:
      - ecommerce
    restart: always

  # Service Discovery
  eureka:
    build:
      context: ./service-discovery
    ports:
      - "8761:8761"
    networks:
      - ecommerce
    restart: always

  # User Service
  user-service:
    build:
      context: ./user-service
    environment:
      - EUREKA_CLIENT_SERVICEURL_DEFAULTZONE=http://eureka:8761/eureka
      - SPRING_DATASOURCE_URL=jdbc:postgresql://user-db:5432/users
    depends_on:
      - eureka
      - user-db
    networks:
      - ecommerce
    restart: always

  user-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=users
      - POSTGRES_USER=user_service
      - POSTGRES_PASSWORD=user_pass
    volumes:
      - user-db-data:/var/lib/postgresql/data
    networks:
      - ecommerce

  # Order Service
  order-service:
    build:
      context: ./order-service
    environment:
      - EUREKA_CLIENT_SERVICEURL_DEFAULTZONE=http://eureka:8761/eureka
      - SPRING_DATASOURCE_URL=jdbc:postgresql://order-db:5432/orders
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - eureka
      - order-db
      - kafka
    networks:
      - ecommerce
    restart: always

  order-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=orders
      - POSTGRES_USER=order_service
      - POSTGRES_PASSWORD=order_pass
    volumes:
      - order-db-data:/var/lib/postgresql/data
    networks:
      - ecommerce

  # Payment Service
  payment-service:
    build:
      context: ./payment-service
    environment:
      - EUREKA_CLIENT_SERVICEURL_DEFAULTZONE=http://eureka:8761/eureka
      - SPRING_DATASOURCE_URL=jdbc:mongodb://payment-db:27017/payments
    depends_on:
      - eureka
      - payment-db
    networks:
      - ecommerce
    restart: always

  payment-db:
    image: mongo:6
    environment:
      - MONGO_INITDB_DATABASE=payments
    volumes:
      - payment-db-data:/data/db
    networks:
      - ecommerce

  # Kafka
  kafka:
    image: confluentinc/cp-kafka:7.4.0
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
      - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
    depends_on:
      - zookeeper
    networks:
      - ecommerce

  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    environment:
      - ZOOKEEPER_CLIENT_PORT=2181
    networks:
      - ecommerce

networks:
  ecommerce:
    driver: bridge

volumes:
  user-db-data:
  order-db-data:
  payment-db-data:
```

---

## 📁 BÀI 4: DOCKER VOLUMES & BACKUP

### Ví dụ 4.1: Backup Database Volume

```bash
#!/bin/bash
# backup-postgres.sh

CONTAINER_NAME="postgres"
VOLUME_NAME="postgres-data"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup using docker exec
docker exec $CONTAINER_NAME pg_dump -U postgres mydb > "$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Compress backup
gzip "$BACKUP_DIR/backup_$TIMESTAMP.sql"

echo "Backup completed: $BACKUP_DIR/backup_$TIMESTAMP.sql.gz"
```

### Ví dụ 4.2: Restore Database

```bash
#!/bin/bash
# restore-postgres.sh

CONTAINER_NAME="postgres"
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup-file.sql.gz>"
    exit 1
fi

# Decompress if needed
if [[ $BACKUP_FILE == *.gz ]]; then
    gunzip -c "$BACKUP_FILE" | docker exec -i $CONTAINER_NAME psql -U postgres -d mydb
else
    cat "$BACKUP_FILE" | docker exec -i $CONTAINER_NAME psql -U postgres -d mydb
fi

echo "Restore completed from $BACKUP_FILE"
```

---

## 📁 BÀI 5: DOCKER HEALTH CHECK

### Ví dụ 5.1: Spring Boot Health Check

```dockerfile
# In Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD wget -qO- http://localhost:8080/actuator/health || exit 1
```

```yaml
# In docker-compose.yml
services:
  app:
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8080/actuator/health", "||", "exit", "1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

### Ví dụ 5.2: Custom Health Check Script

```bash
#!/bin/bash
# healthcheck.sh

# Check application health
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/actuator/health)

if [ "$RESPONSE" != "200" ]; then
    echo "Health check failed: HTTP $RESPONSE"
    exit 1
fi

# Check database connection
DB_STATUS=$(curl -s http://localhost:8080/actuator/health | grep -o '"db":{"status":"[^"]*"' | cut -d'"' -f4)

if [ "$DB_STATUS" != "UP" ]; then
    echo "Database health check failed"
    exit 1
fi

echo "All health checks passed"
exit 0
```

```dockerfile
# In Dockerfile
COPY healthcheck.sh /healthcheck.sh
RUN chmod +x /healthcheck.sh

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD /healthcheck.sh
```

---

## 📁 BÀI 6: DOCKER SECURITY

### Ví dụ 6.1: Running as Non-Root

```dockerfile
# ❌ Bad: Running as root
FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY app.jar app.jar
CMD ["java", "-jar", "app.jar"]

# ✅ Good: Running as non-root
FROM eclipse-temurin:17-jdk-alpine

# Create user and group
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -s /bin/sh -D appuser

WORKDIR /app

COPY --chown=appuser:appgroup app.jar app.jar

# Switch to non-root user
USER appuser

CMD ["java", "-jar", "app.jar"]
```

### Ví dụ 6.2: Docker Content Trust

```bash
# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1

# Push image with signature
docker trust sign myimage:1.0.0

# Verify image before running
docker run myimage:1.0.0
# Will fail if image not signed or tampered
```

### Ví dụ 6.3: Resource Limits

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:1.0.0
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    # Or using command line flags:
    # docker run --memory=512m --cpus=1.0 myapp
```

---

## 📁 BÀI 7: DOCKER TROUBLESHOOTING

### Ví dụ 7.1: Common Commands

```bash
# Check running containers
docker ps
docker ps -a  # Include stopped containers

# Check container logs
docker logs <container-name>
docker logs -f <container-name>  # Follow
docker logs --tail 100 <container-name>

# Inspect container
docker inspect <container-name>

# Execute command in container
docker exec -it <container-name> sh
docker exec -it <container-name> bash  # If available

# Check image layers
docker history <image-name>

# Check disk usage
docker system df

# Clean up
docker container prune    # Remove stopped containers
docker image prune        # Remove dangling images
docker volume prune       # Remove unused volumes
docker system prune -a    # Remove everything unused

# Check network
docker network ls
docker network inspect <network-name>

# Check volumes
docker volume ls
docker volume inspect <volume-name>
```

### Ví dụ 7.2: Common Issues

```bash
# Issue 1: Container exits immediately
docker logs <container-name>
docker inspect <container-name> | grep -A 20 State

# Common causes:
# - Application error
# - Missing environment variables
# - Port already in use
# - Database connection failed

# Issue 2: Cannot connect to other container
docker network inspect <network-name>
docker exec <container-name> ping <other-container>

# Check:
# - Same network?
# - Service name correct?
# - Container healthy?

# Issue 3: Volume not persisting data
docker volume inspect <volume-name>
docker exec <container-name> ls -la /path/to/volume

# Check:
# - Volume mounted correctly?
# - Writing to correct path?
# - Permissions correct?

# Issue 4: Out of memory
docker stats
docker update --memory=1g <container-name>

# Issue 5: Port already in use
docker ps --format "table {{.Ports}}"
# Find conflicting container
docker stop <container-name>
# Or change host port
docker run -p 8081:8080 myapp
```

---

## 📁 BÀI 8: DOCKER REGISTRY & IMAGE MANAGEMENT

### Ví dụ 8.1: Push to Docker Hub

```bash
# Login to Docker Hub
docker login -u username

# Tag image
docker tag myapp:1.0.0 username/myapp:1.0.0
docker tag myapp:1.0.0 username/myapp:latest

# Push image
docker push username/myapp:1.0.0
docker push username/myapp:latest

# Pull image
docker pull username/myapp:1.0.0
```

### Ví dụ 8.2: Push to Amazon ECR

```bash
# Create repository
aws ecr create-repository --repository-name myapp --region us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag myapp:1.0.0:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:1.0.0

# Push image
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:1.0.0
```

### Ví dụ 8.3: Push to GitHub Container Registry (ghcr.io)

```bash
# Login (using Personal Access Token with read:packages, write:packages scope)
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin

# Tag image
docker tag myapp:1.0.0 ghcr.io/username/myapp:1.0.0

# Push image
docker push ghcr.io/username/myapp:1.0.0
```

### Ví dụ 8.4: Image Tagging Best Practices

```bash
# Good: Semantic versioning
docker tag myapp:1.2.3 myapp:v1.2.3

# Good: Environment-specific
docker tag myapp:1.2.3 myapp:staging
docker tag myapp:1.2.3 myapp:production

# Good: Git commit reference
docker tag myapp:1.2.3 myapp:abc123def

# Bad: Using :latest in production
docker tag myapp:latest  # Avoid!

# Multi-arch images
docker buildx build --platform linux/amd64,linux/arm64 \
  -t myapp:1.0.0 --push .
```

---

## 📁 BÀI 9: DOCKER LOGGING & DEBUGGING

### Ví dụ 9.1: Logging Commands

```bash
# View logs
docker logs container_name

# Follow logs (tail -f)
docker logs -f container_name

# Show last N lines
docker logs --tail 100 container_name

# Show timestamps
docker logs -t container_name

# Show logs since time
docker logs --since 2024-01-15T10:00:00 container_name

# Show logs for last 5 minutes
docker logs --since 5m container_name

# Show logs until time
docker logs --until 2024-01-15T12:00:00 container_name
```

### Ví dụ 9.2: Debugging Commands

```bash
# Inspect container details
docker inspect container_name

# View container processes
docker top container_name

# View live resource usage
docker stats container_name
docker stats  # All containers

# Copy files from container
docker cp container_name:/app/logs/app.log ./app.log

# Copy files to container
docker cp ./config.yml container_name:/app/config.yml

# Execute command in running container
docker exec -it container_name sh
docker exec -it container_name bash  # If bash available

# Execute as specific user
docker exec -u root container_name bash

# Check container network
docker exec container_name netstat -tlnp
docker exec container_name curl -s localhost:8080/health

# Show changed files in container
docker diff container_name
```

### Ví dụ 9.3: Debug with Temporary Container

```bash
# Run container with entrypoint override
docker run -it --entrypoint /bin/bash myimage

# Run with different command
docker run --rm myimage java -version

# Run with environment override
docker run -e DEBUG=true --rm myimage

# Run with volume for log inspection
docker run --rm -v /var/log/myapp:/logs myimage ls -la /logs

# Inspect image layers
docker history myimage:1.0.0
docker history --no-trunc myimage:1.0.0  # Full commands
```

---

## 📁 BÀI 10: DOCKER IN CI/CD

### Ví dụ 10.1: GitHub Actions

```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*.*.*']
  pull_request:
    branches: [main]

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
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Ví dụ 10.2: GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - tags

test:
  stage: test
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker run --rm $DOCKER_IMAGE ./mvnw test
  only:
    - merge_requests

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/myapp myapp=$DOCKER_IMAGE
  only:
    - main
```

### Ví dụ 10.3: Docker Compose in CI

```yaml
# docker-compose.test.yml
version: '3.8'

services:
  app:
    build: .
    environment:
      - SPRING_PROFILES_ACTIVE=test
      - SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/testdb
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=testdb
      - POSTGRES_USER=test
      - POSTGRES_PASSWORD=test
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test"]
      interval: 5s
      timeout: 3s
      retries: 5
```

```yaml
# .github/workflows/test.yml
name: Run Tests with Docker Compose

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run tests with Docker Compose
        run: |
          docker-compose -f docker-compose.test.yml up \
            --abort-on-container-exit \
            --exit-code-from app

      - name: Cleanup
        if: always()
        run: docker-compose -f docker-compose.test.yml down -v
```

---

## 🔗 TÀI LIỆU THAM KHẢO

1. [Docker Documentation](https://docs.docker.com/)
2. [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
3. [roadmap.sh/docker](https://roadmap.sh/docker)
4. [Docker Scan (Trivy)](https://aquasecurity.github.io/trivy/)
5. [BuildKit Documentation](https://github.com/moby/buildkit)
