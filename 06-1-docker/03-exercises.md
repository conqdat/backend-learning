# Phase 06.3: Docker - Bài Tập Thực Hành

> **Thời gian:** 2-3 giờ
> **Mục tiêu:** Containerize Spring Boot application, sử dụng Docker Compose

---

## 📝 BÀI TẬP 1: DOCKERIZE SPRING BOOT APP (45 phút)

### Đề bài

Tạo Dockerfile cho Spring Boot application

### Phần 1: Tạo Dockerfile cơ bản

```dockerfile
# TODO: Hoàn thiện Dockerfile
# Yêu cầu:
# 1. Sử dụng base image: eclipse-temurin:17-jdk-alpine
# 2. Set WORKDIR /app
# 3. Copy JAR file từ target/
# 4. Expose port 8080
# 5. Set ENTRYPOINT để chạy application

FROM ___________________

WORKDIR ___________________

COPY ___________________

EXPOSE ___________________

ENTRYPOINT ___________________
```

### Phần 2: Build và test

```bash
# 1. Build JAR file
./gradlew bootJar

# 2. Build Docker image
docker build -t myapp:1.0.0 .

# 3. Run container
docker run -d -p 8080:8080 --name myapp myapp:1.0.0

# 4. Test
curl http://localhost:8080/actuator/health

# 5. Xem logs
docker logs -f myapp
```

### Phần 3: Tối ưu Dockerfile

**Yêu cầu:**
- Tạo multi-stage build
- Sử dụng JRE thay vì JDK cho runtime stage
- Tạo non-root user
- Thêm HEALTHCHECK
- Set JAVA_OPTS

```dockerfile
# TODO: Hoàn thiện multi-stage Dockerfile
# Stage 1: Build
FROM eclipse-temurin:17-jdk-alpine AS builder
WORKDIR /app
# ... copy và build ...

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine
# ... tạo user, copy JAR, healthcheck ...
```

### Checklist hoàn thành

- [ ] Dockerfile cơ bản hoạt động
- [ ] Container chạy thành công
- [ ] Health endpoint trả về 200
- [ ] Multi-stage build hoàn thiện
- [ ] Application chạy với non-root user

---

## 📝 BÀI TẬP 2: DOCKER COMPOSE CHO DEVELOPMENT (45 phút)

### Đề bài

Tạo docker-compose.yml cho development environment với PostgreSQL và Redis

### Phần 1: Tạo docker-compose.yml

```yaml
# TODO: Hoàn thiện docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "___:___"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:postgresql://___:5432/mydb
      - SPRING_DATASOURCE_USERNAME=postgres
      - SPRING_DATASOURCE_PASSWORD=postgres123
      - SPRING_REDIS_HOST=___
    depends_on:
      - postgres
      - redis
    networks:
      - mynetwork

  postgres:
    image: postgres:15-alpine
    ports:
      - "___:___"
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres123
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - mynetwork

  redis:
    image: redis:7-alpine
    ports:
      - "___:___"
    networks:
      - mynetwork

networks:
  mynetwork:
    driver: ___

volumes:
  postgres-data:
```

### Phần 2: Test các lệnh docker-compose

```bash
# 1. Start tất cả services
docker-compose up -d

# 2. Xem logs
docker-compose logs -f app

# 3. Kiểm tra database
docker-compose exec postgres psql -U postgres -d mydb -c "\dt"

# 4. Kiểm tra redis
docker-compose exec redis redis-cli ping

# 5. Stop tất cả
docker-compose down

# 6. Stop và xóa volumes
docker-compose down -v
```

### Checklist hoàn thành

- [ ] docker-compose.yml hoàn thiện
- [ ] `docker-compose up -d` thành công
- [ ] App connect được đến PostgreSQL
- [ ] App connect được đến Redis
- [ ] `docker-compose down` thành công

---

## 📝 BÀI TẬP 3: .dockerignore (15 phút)

### Đề bài

Tạo .dockerignore để tối ưu build context

### Bài tập

```bash
# TODO: Tạo .dockerignore với các patterns sau:

# 1. Build outputs (target/, build/)

# 2. IDE files (.idea/, .vscode/, *.iml)

# 3. Git files (.git/, .gitignore)

# 4. Documentation (*.md, docs/)

# 5. Test files (src/test/)

# 6. Local config (.env, *.local.yml)

# 7. Docker files (Dockerfile, docker-compose*.yml)

# 8. OS files (.DS_Store, Thumbs.db)
```

### Test

```bash
# Check build context size
docker build . 2>&1 | grep "Sending build context"

# Trước khi có .dockerignore: ~100MB+
# Sau khi có .dockerignore: ~1MB
```

### Checklist hoàn thành

- [ ] .dockerignore tạo đúng các patterns
- [ ] Build context giảm đáng kể

---

## 📝 BÀI TẬP 4: DOCKER NETWORKING (30 phút)

### Đề bài

Thực hành Docker networking

### Phần 1: Tạo network và containers

```bash
# 1. Tạo network mới
docker network create mynet

# 2. Chạy 2 containers trong cùng network
docker run -d --name container1 --network mynet alpine sleep 3600
docker run -d --name container2 --network mynet alpine sleep 3600

# 3. Test connectivity
docker exec container1 ping -c 3 container2

# 4. Inspect network
docker network inspect mynet
```

### Phần 2: Port mapping

```bash
# 1. Chạy container với port mapping
docker run -d -p 8080:8080 --name myapp myapp:1.0.0

# 2. Kiểm tra ports
docker port myapp

# 3. Test từ host
curl http://localhost:8080/actuator/health

# 4. Test từ container khác
docker run --rm --network host busybox wget -qO- http://localhost:8080/actuator/health
```

### Phần 3: Service discovery

```yaml
# TODO: Tạo docker-compose với 2 services có thể communicate
version: '3.8'

services:
  web:
    image: nginx:alpine
    # TODO: Configure để web có thể gọi api service

  api:
    build: .
    # TODO: Configure environment để connect database

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=secret
```

### Checklist hoàn thành

- [ ] Tạo network thành công
- [ ] Containers ping được nhau
- [ ] Port mapping hoạt động
- [ ] Service discovery bằng tên hoạt động

---

## 📝 BÀI TẬP 5: DOCKER VOLUMES (30 phút)

### Đề bài

Thực hành Docker volumes cho data persistence

### Phần 1: Tạo và sử dụng volume

```bash
# 1. Tạo volume
docker volume create mydata

# 2. Chạy container với volume
docker run -d -v mydata:/data --name mycontainer alpine sh -c "while true; do echo \$(date) >> /data/log.txt; sleep 5; done"

# 3. Xem nội dung
docker exec mycontainer cat /data/log.txt

# 4. Stop và xóa container
docker stop mycontainer
docker rm mycontainer

# 5. Chạy container mới với cùng volume
docker run -it -v mydata:/data alpine cat /data/log.txt
# Log vẫn còn!
```

### Phần 2: Bind mount cho development

```yaml
# TODO: Thêm bind mount vào docker-compose.yml
services:
  app:
    build: .
    volumes:
      # Mount source code cho hot reload
      - ./src:/app/src
      # Mount config
      - ./config:/app/config
      # Named volume cho data
      - app-data:/app/data

volumes:
  app-data:
```

### Phần 3: Backup volume

```bash
# TODO: Viết script backup volume

# 1. Tạo backup
docker run --rm -v mydata:/source -v $(pwd):/backup alpine \
  tar czf /backup/mydata-backup.tar.gz -C /source .

# 2. Restore backup
docker run --rm -v mydata:/dest -v $(pwd):/backup alpine \
  tar xzf /backup/mydata-backup.tar.gz -C /dest
```

### Checklist hoàn thành

- [ ] Tạo và sử dụng volume thành công
- [ ] Data persist sau khi xóa container
- [ ] Bind mount hoạt động
- [ ] Backup/restore volume thành công

---

## 📝 BÀI TẬP 6: DOCKER SECURITY (15 phút)

### Đề bài

Áp dụng security best practices

### Phần 1: Scan image

```bash
# Install trivy (nếu chưa có)
# https://aquasecurity.github.io/trivy/latest/getting-started/installation/

# Scan image
trivy image myapp:1.0.0

# Xem kết quả
# TODO: Có bao nhiêu vulnerabilities?
# TODO: Level nào cao nhất (CRITICAL/HIGH/MEDIUM/LOW)?
```

### Phần 2: Fix vulnerabilities

```dockerfile
# TODO: Cải thiện Dockerfile để giảm vulnerabilities

# Before:
FROM eclipse-temurin:17-jdk

# After:
FROM eclipse-temurin:17-jdk-alpine
# Or use specific version
FROM eclipse-temurin:17.0.8_7-jdk-alpine
```

### Phần 3: Run as non-root

```bash
# Test chạy với root (không tốt)
docker run myapp:1.0.0 whoami
# Output: root

# Test chạy với non-root (tốt)
docker run --user 1000:1000 myapp:1.0.0 whoami
# Output: appuser
```

### Checklist hoàn thành

- [ ] Scan image với trivy
- [ ] Sử dụng specific tag (không dùng :latest)
- [ ] Chạy với non-root user
- [ ] Giảm số vulnerabilities

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 06.3

- [ ] Dockerize Spring Boot application
- [ ] Multi-stage build thành công
- [ ] Docker Compose cho development
- [ ] .dockerignore đúng cách
- [ ] Docker networking (bridge, service discovery)
- [ ] Docker volumes (persistent data, bind mount)
- [ ] Security best practices (non-root, scan, specific tags)
- [ ] Troubleshoot common issues

---

## 📤 CÁCH SUBMIT

1. Push code lên GitHub với:
   - Dockerfile (multi-stage)
   - docker-compose.yml
   - .dockerignore
   - Scripts (backup, healthcheck)

2. Tạo file `DOCKER_LABS.md` với:
   - Screenshots của `docker ps`, `docker images`
   - Output của `trivy image`
   - Build context size trước/sau khi có .dockerignore
   - Khó khăn gặp phải

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, unlock Phase tiếp theo!
