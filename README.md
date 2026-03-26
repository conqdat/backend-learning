# 🎯 Complete Backend Developer Learning Path

> **Mục tiêu:** Trở thành Senior Backend Developer toàn diện
> **Thời gian:** 9-12 tháng
> **Phương châm:** "Học sâu - Làm thực tế - Hiểu bản chất"
> **Mentor:** Claude Code (trực tiếp dạy, review code)

---

## 📁 CẤU TRÚC KHÓA HỌC

```
backend-learning/
│
├── README.md                          ← File này
│
├── 00-java-core/                      ← Foundation (4 tuần)
│   ├── 01-theory.md                   (Collections, Concurrency, JVM)
│   ├── 02-examples.md                 (Code samples)
│   └── 03-exercises.md                (Hands-on labs)
│
├── 01-spring-boot/                    ← Framework (2 tuần)
│   ├── 01-theory.md                   (Auto-config, Starters)
│   ├── 02-examples.md                 (Custom starter)
│   └── 03-exercises.md                (Build starter)
│
├── 02-database/                       ← Data Layer (4 tuần)
│   ├── 01-theory.md                   (SQL, NoSQL, ORM)
│   ├── 02-examples.md                 (JPA, Query optimization)
│   └── 03-exercises.md                (Schema design, indexing)
│
├── 03-caching/                        ← Performance (2 tuần)
│   ├── 01-theory.md                   (Caching patterns, Redis)
│   ├── 02-examples.md                 (Redis ops, distributed lock)
│   └── 03-exercises.md                (Cache strategies)
│
├── 04-microservices/                  ← Architecture (4 tuần)
│   ├── 01-theory.md                   (Saga, API Gateway, Events)
│   ├── 02-examples.md                 (Service design)
│   └── 03-exercises.md                (Build microservices)
│
├── 05-0-security/                       ← Security (3 tuần)
│   ├── 01-theory.md                   (AuthN, AuthZ, OAuth2)
│   ├── 02-examples.md                 (Spring Security, JWT)
│   └── 03-exercises.md                (Security implementation)
│
├── 05-1-aws-cloud/                    ← Cloud & AWS (2 tuần)
│   ├── 01-theory.md                   (EC2, Lambda, S3, VPC, IAM)
│   ├── 02-examples.md                 (AWS CLI, SDK, Terraform)
│   └── 03-exercises.md                (Hands-on AWS labs)
│
├── 06-1-docker/                       ← Container Fundamentals (2 tuần)
│   ├── 01-theory.md                   (Docker basics, Dockerfile, Compose)
│   ├── 02-examples.md                 (Spring Boot on Docker, microservices)
│   └── 03-exercises.md                (Containerize apps)
│
├── 06-2-kubernetes/                   ← Container Orchestration (3 tuần)
│   ├── 01-theory.md                   (K8s architecture, Pods, Deployments)
│   ├── 02-examples.md                 (Spring Boot on K8s, Helm)
│   └── 03-exercises.md                (Deploy to K8s)
│
├── 06-3-git-github/                   ← Version Control & CI/CD (2 tuần)
│   ├── 01-theory.md                   (Git internals, GitHub Actions)
│   ├── 02-examples.md                 (Workflows, automation)
│   └── 03-exercises.md                (Git workflow, CI pipeline)
│
├── 06-4-devops/                       ← Monitoring & Logging (2 tuần)
│   ├── 01-theory.md                   (Prometheus, ELK, Circuit Breaker)
│   ├── 02-examples.md                 (Metrics, logging, tracing)
│   └── 03-exercises.md                (Setup monitoring)
│
├── 07-testing/                        ← Quality Assurance (2 tuần)
│   ├── 01-theory.md                   (Unit, Integration, E2E)
│   ├── 02-examples.md                 (JUnit, Mockito, Testcontainers)
│   └── 03-exercises.md                (Write tests)
│
├── 08-network-os/                     ← Fundamentals (2 tuần)
│   ├── 01-theory.md                   (HTTP, TCP/IP, Linux)
│   ├── 02-examples.md                 (Network troubleshooting)
│   └── 03-exercises.md                (Linux commands, networking)
│
├── 09-system-design/                  ← Architecture (4 tuần)
│   ├── 01-theory.md                   (Design patterns, Scaling)
│   ├── 02-examples.md                 (System design cases)
│   └── 03-exercises.md                (Design interviews)
│
└── 10-capstone/                       ← Final Project (6 tuần)
    └── project-requirements.md        (E-commerce platform)
```

---

## 🗺️ ROADMAP CHI TIẾT

| Phase    | Chủ đề              | Thời gian | Mức độ     | Đầu ra                                    |
| -------- | ------------------- | --------- | ---------- | ----------------------------------------- |
| **00**   | Java Core           | 4 tuần    | ⭐⭐⭐⭐⭐ | Hiểu JVM, Collections, Concurrency        |
| **01**   | Spring Boot         | 2 tuần    | ⭐⭐⭐⭐   | Custom starters, Auto-config              |
| **02**   | Database            | 4 tuần    | ⭐⭐⭐⭐⭐ | SQL, NoSQL, Query optimization            |
| **03**   | Caching             | 2 tuần    | ⭐⭐⭐⭐   | Redis, Multi-level cache                  |
| **04**   | Microservices       | 4 tuần    | ⭐⭐⭐⭐⭐ | Service design, Saga, Events              |
| **05**   | Security            | 3 tuần    | ⭐⭐⭐⭐⭐ | OAuth2, JWT, Spring Security              |
| **05.1** | AWS Cloud           | 2 tuần    | ⭐⭐⭐⭐   | EC2, Lambda, S3, VPC, RDS, DynamoDB       |
| **06.1** | Docker              | 2 tuần    | ⭐⭐⭐⭐   | Dockerfile, Compose, Networking, Volumes  |
| **06.2** | Kubernetes          | 3 tuần    | ⭐⭐⭐⭐   | Pods, Deployments, Services, Helm         |
| **06.3** | Git & GitHub        | 2 tuần    | ⭐⭐⭐     | Git workflow, GitHub Actions, Code review |
| **06.4** | DevOps (Monitoring) | 2 tuần    | ⭐⭐⭐     | Prometheus, ELK, Circuit Breaker          |
| **07**   | Testing             | 2 tuần    | ⭐⭐⭐     | Unit, Integration, E2E tests              |
| **08**   | Network & OS        | 2 tuần    | ⭐⭐⭐     | HTTP, TCP/IP, Linux commands              |
| **09**   | System Design       | 4 tuần    | ⭐⭐⭐⭐⭐ | Design scalable systems                   |
| **10**   | Capstone            | 6 tuần    | ⭐⭐⭐⭐⭐ | Production-ready project                  |

**Tổng:** 43 tuần (~10-11 tháng)

---

## 📖 CHI TIẾT TỪNG PHASE

### Phase 00: Java Core (4 tuần) ⭐⭐⭐⭐⭐

**Tại sao quan trọng:** Đây là foundation - phỏng vấn Senior hỏi nhiều nhất

**Nội dung:**

- Week 1: Collections Framework (HashMap, ConcurrentHashMap, etc.)
- Week 2: Concurrency (Thread pools, Locks, Atomic, CompletableFuture)
- Week 3: Stream API, Optional, Java 8+ features
- Week 4: JVM memory, GC, Memory leaks

**Bài tập lớn:**

- Implement HashMap từ scratch
- Thread-safe counter benchmark
- Producer-Consumer với BlockingQueue

---

### Phase 01: Spring Boot Core (2 tuần) ⭐⭐⭐⭐

**Nội dung:**

- Week 1: Auto-configuration, Starter dependencies
- Week 2: Custom starter, Actuator, Profiles

**Bài tập lớn:**

- Tạo custom logging starter
- Implement health indicators

---

### Phase 02: Database (4 tuần) ⭐⭐⭐⭐⭐

**Nội dung:**

- Week 1: SQL fundamentals, Indexing, Query optimization
- Week 2: JPA/Hibernate, Entity relationships, N+1 fix
- Week 3: NoSQL (MongoDB, Redis, Elasticsearch)
- Week 4: Database replication, Sharding, Transactions

**Bài tập lớn:**

- Design e-commerce schema
- Fix N+1 queries
- Implement read replicas

---

### Phase 03: Caching (2 tuần) ⭐⭐⭐⭐

**Nội dung:**

- Week 1: Caching patterns (Cache-Aside, Write-Through, etc.)
- Week 2: Redis data structures, Distributed lock, Multi-level cache

**Bài tập lớn:**

- Shopping cart với Redis Hash
- Leaderboard với Redis Sorted Set
- Flash sale với distributed lock

---

### Phase 04: Microservices (4 tuần) ⭐⭐⭐⭐⭐

**Nội dung:**

- Week 1: Monolith vs Microservices, Service decomposition
- Week 2: Inter-service communication (REST, Kafka)
- Week 3: Saga pattern, Distributed transactions
- Week 4: API Gateway, Service Discovery, Circuit Breaker

**Bài tập lớn:**

- Design 6-8 services cho e-commerce
- Implement Saga pattern
- Setup API Gateway với Spring Cloud

---

### Phase 05.0: Security (3 tuần) ⭐⭐⭐⭐⭐

**Nội dung:**

- Week 1: Spring Security, Authentication, Authorization
- Week 2: JWT, OAuth2, OIDC
- Week 3: OWASP Top 10, Security best practices

**Bài tập lớn:**

- Implement JWT auth flow
- OAuth2 với Google/GitHub
- Security audit checklist

---

### Phase 05.1: AWS Cloud (2 tuần) ⭐⭐⭐⭐

**Nội dung:**

- Week 1: EC2, Auto Scaling, Load Balancing, Lambda
- Week 2: S3, CloudFront, RDS, DynamoDB, VPC, IAM

**Bài tập lớn:**

- Deploy Spring Boot app lên EC2 với ALB
- Build serverless API với Lambda + API Gateway
- Setup VPC với Terraform
- Configure CloudWatch alarms & SNS notifications

---

### Phase 06.1: Docker (2 tuần) ⭐⭐⭐⭐

**Nội dung:**

- Week 1: Docker fundamentals, Dockerfile, multi-stage builds
- Week 2: Docker Compose, volumes, networking, security

**Bài tập lớn:**

- Dockerize Spring Boot application
- Multi-stage build optimization
- Docker Compose cho microservices

---

### Phase 06.2: Kubernetes (3 tuần) ⭐⭐⭐⭐

**Nội dung:**

- Week 1: K8s architecture, Pods, Deployments, Services
- Week 2: ConfigMaps, Secrets, HPA, StatefulSets
- Week 3: Helm charts, monitoring

**Bài tập lớn:**

- Deploy Spring Boot app lên K8s cluster
- Setup HPA auto-scaling
- Create Helm chart

---

### Phase 06.3: Git & GitHub (2 tuần) ⭐⭐⭐

**Nội dung:**

- Week 1: Git internals, branching strategies, rebasing
- Week 2: GitHub Actions, CI/CD, code review

**Bài tập lớn:**

- Setup CI pipeline với GitHub Actions
- Git hooks automation
- Code review workflow

---

### Phase 06.4: DevOps - Monitoring & Logging (2 tuần) ⭐⭐⭐

**Nội dung:**

- Week 1: Prometheus, Grafana, metrics collection
- Week 2: ELK stack, distributed tracing, circuit breaker

**Bài tập lớn:**

- Setup Prometheus + Grafana
- Configure ELK stack cho logging
- Implement circuit breaker pattern

---

### Phase 07: Testing (2 tuần) ⭐⭐⭐

**Nội dung:**

- Week 1: Unit testing (JUnit 5, Mockito), Integration testing
- Week 2: E2E testing, Testcontainers, Contract testing

**Bài tập lớn:**

- Write unit tests (>80% coverage)
- Integration tests với Testcontainers
- E2E test suite

---

### Phase 08: Network & OS (2 tuần) ⭐⭐⭐

**Nội dung:**

- Week 1: HTTP/HTTPS, TCP/IP, DNS, Load Balancing
- Week 2: Linux commands, Process management, File system

**Bài tập lớn:**

- Network troubleshooting với tcpdump, Wireshark
- Linux shell scripting
- Performance tuning với top, htop, iostat

---

### Phase 09: System Design (4 tuần) ⭐⭐⭐⭐⭐

**Nội dung:**

- Week 1: System design interview framework
- Week 2: Scale estimation, Capacity planning
- Week 3: Design patterns (LB, DB scaling, Caching)
- Week 4: Message queues, Event-driven architecture

**Bài tập lớn:**

- Design URL shortener
- Design rate limiter
- Design Twitter/Instagram
- Mock system design interview

---

### Phase 10: Capstone Project (6 tuần) ⭐⭐⭐⭐⭐

**Đề bài:** Build complete E-commerce Platform

**Services:**

- User Service (PostgreSQL, JWT)
- Product Service (PostgreSQL, Redis cache)
- Order Service (PostgreSQL, Saga pattern)
- Payment Service (MongoDB, Stripe integration)
- Inventory Service (PostgreSQL)
- Notification Service (Kafka, Email/SMS)

**Infrastructure:**

- API Gateway (Spring Cloud Gateway)
- Service Discovery (Eureka/Consul)
- Message Broker (Kafka)
- Database (PostgreSQL, MongoDB, Redis)
- Container (Docker, Kubernetes)
- CI/CD (GitHub Actions)
- Monitoring (Prometheus, Grafana, ELK)

---

## 📚 TÀI NGUYÊN HỌC TẬP

### Từ 3 repos bạn đã clone:

| Chủ đề                     | Repo                      | Files                               |
| -------------------------- | ------------------------- | ----------------------------------- |
| Spring Boot best practices | claude-code-best-practice | best-practice/\*.md                 |
| Engineering skills         | claude-skills             | engineering/\*/SKILL.md             |
| Security standards         | claude-skills             | standards/security/\*.md            |
| DevOps skills              | claude-skills             | engineering/ci-cd-pipeline-builder/ |
| Agents cho code review     | everything-claude-code    | agents/\*.md                        |
| MCP configs                | everything-claude-code    | mcp-configs/                        |

### Bổ sung bên ngoài:

| Chủ đề        | Tài nguyên                    |
| ------------- | ----------------------------- |
| Java Core     | Effective Java (Joshua Bloch) |
| Spring Boot   | Spring Boot Docs, Baeldung    |
| Database      | Use The Index, Luke           |
| System Design | System Design Primer (GitHub) |
| DevOps        | Kubernetes Docs, Docker Docs  |
| Security      | OWASP Cheat Sheet Series      |

---

## ✅ CHECKLIST TỔNG QUÁT

Sau khi hoàn thành, bạn sẽ:

### Java & Framework

- [ ] Master Java Core (Collections, Concurrency, JVM)
- [ ] Spring Boot (Auto-config, Custom starters)
- [ ] REST API design best practices

### Database & Caching

- [ ] SQL (PostgreSQL/MySQL)
- [ ] NoSQL (MongoDB, Redis, Elasticsearch)
- [ ] Query optimization, Indexing
- [ ] Caching strategies (Redis, Multi-level)

### Architecture

- [ ] Microservices design
- [ ] Saga pattern, Distributed transactions
- [ ] API Gateway, Service Discovery
- [ ] Event-driven architecture (Kafka)

### Security

- [ ] Spring Security
- [ ] JWT, OAuth2, OIDC
- [ ] OWASP Top 10 prevention

### Cloud (AWS)

- [ ] EC2, Auto Scaling, Load Balancing
- [ ] Lambda, API Gateway (serverless)
- [ ] S3, CloudFront (storage & CDN)
- [ ] RDS, DynamoDB (managed databases)
- [ ] VPC, IAM (networking & security)
- [ ] CloudWatch (monitoring & alerting)

### DevOps & Containerization

- [ ] Docker (Dockerfile, Compose, networking, volumes)
- [ ] Kubernetes (Pods, Deployments, Services, Helm)
- [ ] Git & GitHub (workflow, Actions, code review)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Monitoring (Prometheus, Grafana, ELK)
- [ ] Unit, Integration, E2E tests

### Fundamentals

- [ ] HTTP/HTTPS, TCP/IP
- [ ] Linux commands, Shell scripting
- [ ] System design interview

---

## 📤 CÁCH SUBMIT BÀI TẬP

### Option 1: GitHub Repository (Recommended)

```bash
# Tạo repo
git init
git add .
git commit -m "Phase XX: Complete exercises"
git remote add origin https://github.com/yourusername/backend-learning.git
git push -u origin main
```

Gửi link GitHub cho mentor review.

### Option 2: Gửi file trực tiếp

Nếu không muốn public code, gửi file qua email/chat.

---

## 🎯 CAM KẾT

> **"Tôi sẽ không cho bạn code để copy-paste.**
>
> **Tôi sẽ GIẢNG GIẢI để bạn HIỂU SÂU bản chất.**
>
> **Mỗi phase sẽ có:**
>
> - Lý thuyết rõ ràng, dễ hiểu
> - Ví dụ thực tế, production-ready
> - Bài tập áp dụng ngay
> - Code review chi tiết
>
> **Bạn chỉ cần:**
>
> - Học đều đặn 1-2 giờ/ngày
> - Làm bài tập đầy đủ
> - Submit code để tôi review
> - Hỏi khi không hiểu
>
> **9 tháng sau, bạn sẽ tự tin ứng tuyển Senior Backend Developer."**

---

## 🚀 BẮT ĐẦU

```bash
# Bước 1: Vào folder Phase 00
cd /home/dattran/workspace/backend-learning/00-java-core

# Bước 2: Đọc lý thuyết đầu tiên
cat 01-theory.md

# Bước 3: Khi có câu hỏi, hỏi mentor (tôi)
"Em không hiểu phần HashMap internals, giải thích thêm được không?"
```

---

_Chúc bạn học tốt! 🚀_
