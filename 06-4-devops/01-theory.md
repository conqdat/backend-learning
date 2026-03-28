# Phase 06.4: DevOps - Production Ready

> **Thời gian:** 3 tuần
> **Mục tiêu:** Monitoring, logging, debugging production issues
>
> **Tham khảo:** [roadmap.sh/devops](https://roadmap.sh/devops)

---

## 📚 BÀI 1: OBSERVABILITY PILLARS

### 3 Pillars of Observability

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                             │
├─────────────────────────────────────────────────────────────┤
│  1. Metrics (Numbers over time)                             │
│     - CPU usage, memory, request count, error rate          │
│     - Tools: Prometheus, Grafana, Datadog                   │
├─────────────────────────────────────────────────────────────┤
│  2. Logs (Records of events)                                │
│     - Application logs, access logs, error logs             │
│     - Tools: ELK Stack, Splunk, Loki                        │
├─────────────────────────────────────────────────────────────┤
│  3. Traces (Request flow across services)                   │
│     - Distributed tracing                                   │
│     - Tools: Jaeger, Zipkin, Tempo                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 2: METRICS & ALERTING

### 2.1 Four Golden Signals

```
1. Latency: Time to process request
   - Target: p99 < 200ms

2. Traffic: Demand on your system
   - QPS, requests/sec

3. Errors: Rate of failed requests
   - Target: < 0.1%

4. Saturation: How full your service is
   - CPU, memory, disk usage
   - Target: < 70%
```

### 2.2 Prometheus Metrics

```java
@Configuration
public class MetricsConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> metricsCommonTags() {
        return registry -> registry.config()
            .commonTags("application", "ecommerce",
                       "environment", "production");
    }
}

@Service
public class OrderService {

    private final MeterRegistry meterRegistry;
    private final Timer orderProcessingTimer;
    private final Counter ordersCreatedCounter;
    private final Counter ordersFailedCounter;

    public OrderService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;

        this.orderProcessingTimer = meterRegistry.timer("orders.processing.time");
        this.ordersCreatedCounter = meterRegistry.counter("orders.created.total");
        this.ordersFailedCounter = meterRegistry.counter("orders.failed.total");
    }

    public Order createOrder(OrderRequest request) {
        return orderProcessingTimer.record(() -> {
            try {
                Order order = orderRepository.save(request.toOrder());
                ordersCreatedCounter.increment();
                return order;
            } catch (Exception e) {
                ordersFailedCounter.increment();
                throw e;
            }
        });
    }
}
```

---

## 📚 BÀI 3: LOGGING BEST PRACTICES

### 3.1 Structured Logging

```java
// ❌ Bad: Unstructured log
log.info("Order " + orderId + " created for user " + userId);

// ✅ Good: Structured log (JSON)
log.info("Order created",
    kv("orderId", orderId),
    kv("userId", userId),
    kv("amount", amount),
    kv("timestamp", Instant.now())
);
```

### 3.2 Log Levels

```
ERROR: Something broke, needs immediate attention
WARN:  Something might be wrong, check it out
INFO:  Normal business events (order created, user logged in)
DEBUG: Detailed technical information for debugging
TRACE: Very detailed, usually disabled in production
```

### 3.3 Correlation IDs

```java
@Component
public class LoggingFilter implements Filter {

    private static final String CORRELATION_ID_HEADER = "X-Correlation-ID";

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        String correlationId = httpRequest.getHeader(CORRELATION_ID_HEADER);
        if (correlationId == null || correlationId.isEmpty()) {
            correlationId = UUID.randomUUID().toString();
        }

        MDC.put("correlationId", correlationId);
        httpResponse.setHeader(CORRELATION_ID_HEADER, correlationId);

        try {
            chain.doFilter(request, response);
        } finally {
            MDC.clear();
        }
    }
}
```

---

## 📚 BÀI 4: CIRCUIT BREAKER PATTERN

### 4.1 Circuit Breaker States

```
┌─────────────────────────────────────────────────────────────┐
│               CIRCUIT BREAKER STATES                         │
├─────────────────────────────────────────────────────────────┤
│  CLOSED (Normal)                                            │
│  - Requests flow through normally                           │
│  - Track failures                                           │
│  - If failures > threshold → OPEN                           │
├─────────────────────────────────────────────────────────────┤
│  OPEN (Tripped)                                             │
│  - All requests fail immediately                            │
│  - No calls to downstream service                           │
│  - After timeout → HALF_OPEN                                │
├─────────────────────────────────────────────────────────────┤
│  HALF_OPEN (Testing)                                        │
│  - Allow limited requests through                           │
│  - If success → CLOSED                                      │
│  - If failure → OPEN                                        │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Resilience4j Implementation

```java
@Service
public class OrderService {

    @Autowired
    private PaymentServiceClient paymentClient;

    @CircuitBreaker(name = "paymentService", fallbackMethod = "createOrderFallback")
    @Retry(name = "paymentService", maxAttempts = 3)
    @Bulkhead(name = "paymentService", maxConcurrentCalls = 10)
    public Order createOrder(OrderRequest request) {
        // Call payment service
        PaymentResult payment = paymentClient.processPayment(request);

        if (!payment.isSuccess()) {
            throw new PaymentFailedException("Payment failed");
        }

        return orderRepository.save(request.toOrder());
    }

    // Fallback method
    public Order createOrderFallback(OrderRequest request, Throwable t) {
        log.warn("Payment service unavailable, queuing order for later processing", t);
        // Queue order for async processing
        return orderRepository.save(request.toOrder());
    }
}
```

---

## 📚 BÀI 5: INCIDENT RESPONSE

### 5.1 Runbook Template

```
# Incident: High Error Rate

## Symptoms
- Error rate > 5% for order service
- Customers reporting checkout failures

## Diagnosis Steps
1. Check Grafana dashboard: [link]
2. Check recent deployments: [link]
3. Check error logs: [query]
4. Check downstream dependencies status

## Resolution Steps
1. If recent deployment: Consider rollback
2. If database issue: Check connections, queries
3. If external service: Enable circuit breaker
4. Notify stakeholders

## Prevention
- Add alert for error rate > 1%
- Add automated rollback
```

---

## 📝 TÓM TẮT PHASE 06.4

1. ✅ 3 pillars of observability
2. ✅ Four golden signals
3. ✅ Structured logging với correlation IDs
4. ✅ Circuit breaker pattern
5. ✅ Incident response runbooks

---

## 📚 BÀI 6: CI/CD PIPELINE

### 6.1 CI/CD Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD PIPELINE                            │
├─────────────────────────────────────────────────────────────┤
│  CONTINUOUS INTEGRATION                                      │
│  - Developers commit code frequently                         │
│  - Automated build + test on each commit                     │
│  - Catch issues early                                        │
├─────────────────────────────────────────────────────────────┤
│  CONTINUOUS DELIVERY                                         │
│  - Code is always in deployable state                        │
│  - Automated deployment to staging                           │
│  - Manual approval for production                            │
├─────────────────────────────────────────────────────────────┤
│  CONTINUOUS DEPLOYMENT                                       │
│  - Every change that passes tests → production               │
│  - No manual intervention                                    │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 GitHub Actions Pipeline

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  JAVA_VERSION: '17'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
          cache: 'maven'

      - name: Build with Maven
        run: mvn -B package --file pom.xml

      - name: Run unit tests
        run: mvn test

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: target/surefire-reports/

  code-quality:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
          cache: 'maven'

      - name: Run SonarQube
        run: mvn -B sonar:sonar
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

  docker-build:
    runs-on: ubuntu-latest
    needs: [build, code-quality]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Container Registry
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
          cache-to: type=gha,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: docker-build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          kubectl rollout status deployment/app
```

---

## 📚 BÀI 7: INFRASTRUCTURE AS CODE

### 7.1 Terraform Basics

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "main-vpc"
    Environment = "production"
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1a"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

# Security Group
resource "aws_security_group" "app" {
  name        = "app-sg"
  description = "Security group for application"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  subnet_id     = aws_subnet.public.id

  vpc_security_group_ids = [aws_security_group.app.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker
              systemctl start docker
              systemctl enable docker
              EOF

  tags = {
    Name        = "app-server"
    Environment = "production"
  }
}

# Outputs
output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC ID"
}

output "instance_public_ip" {
  value       = aws_instance.app.public_ip
  description = "Public IP of the instance"
}
```

### 7.2 Terraform Commands

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Format configuration
terraform fmt

# Plan changes
terraform plan
terraform plan -out=tfplan
terraform plan -destroy

# Apply changes
terraform apply
terraform apply tfplan
terraform apply -auto-approve

# Destroy infrastructure
terraform destroy

# State management
terraform state list
terraform state show aws_instance.app
terraform import aws_instance.app i-1234567890abcdef0
terraform refresh

# Workspace (environments)
terraform workspace new dev
terraform workspace new prod
terraform workspace select dev
```

---

## 📚 BÀI 8: CONTAINER ORCHESTRATION

### 8.1 Kubernetes vs Alternatives

| Tool | Description | Use Case |
|------|-------------|----------|
| Kubernetes | Full-featured orchestration | Production, complex apps |
| Docker Swarm | Simple, Docker-native | Small teams, simple apps |
| Nomad | Flexible, HashiCorp ecosystem | Mixed workloads |
| ECS | AWS-managed | AWS-native teams |
| EKS | AWS-managed K8s | Need K8s on AWS |
| AKS | Azure-managed K8s | Need K8s on Azure |
| GKE | GCP-managed K8s | Need K8s on GCP |

### 8.2 When NOT to Use Kubernetes

```
❌ DON'T use Kubernetes if:
- You have a single application
- Your team is < 5 people
- You don't have DevOps expertise
- Your application doesn't need scaling
- You're just starting with containers
- Cost is a major concern

✅ DO use Kubernetes if:
- You have microservices architecture
- You need auto-scaling
- You have complex deployment requirements
- You need multi-cloud portability
- You have dedicated DevOps team
```

---

## 📚 BÀI 9: SECRETS MANAGEMENT

### 9.1 Secrets Management Options

| Tool | Description | Use Case |
|------|-------------|----------|
| AWS Secrets Manager | Managed AWS service | AWS-native apps |
| HashiCorp Vault | Open source, self-hosted | Multi-cloud, on-prem |
| Sealed Secrets | Kubernetes-native | K8s workloads |
| Doppler | Developer-focused | Teams wanting simplicity |
| AWS Parameter Store | Simple key-value | Non-sensitive config |

### 9.2 Spring Boot Integration

```yaml
# application.yml
spring:
  config:
    import: optional:vault://
  cloud:
    vault:
      authentication: APPROLE
      host: vault.example.com
      port: 8200
      scheme: https
      app-role:
        role-id: ${VAULT_ROLE_ID}
        secret-id: ${VAULT_SECRET_ID}
```

```java
@Configuration
public class VaultConfig {

    @Bean
    public VaultTemplate vaultTemplate() {
        VaultEndpoint vaultEndpoint = VaultEndpoint.create("vault.example.com", 8200);
        vaultEndpoint.setScheme("https");

        RestTemplate restTemplate = new RestTemplate();
        return new VaultTemplate(vaultEndpoint, restTemplate);
    }
}

@Service
public class DatabaseService {

    @Value("${database.password}")
    private String dbPassword;

    // Password injected from Vault at runtime
}
```

---

## 🔜 TIẾP THEO

Phase 8: Capstone Project - Apply tất cả kiến thức!

---

## 📝 TÓM TẮT DEVOPS ROADMAP (theo roadmap.sh/devops)

### Các chủ đề cần nắm vững:

**1. Coding Fundamentals:**
- ✅ Python (scripting, automation)
- ✅ Go (cloud-native tools)
- ✅ Bash/Shell scripting
- ✅ Ruby (optional, for Chef/Puppet)
- ✅ JavaScript/Node.js (optional)

**2. System Environments:**
- ✅ Linux (RHEL, Ubuntu, SUSE)
- ✅ Unix, FreeBSD
- ✅ Windows Server (basic knowledge)
- ✅ Package Managers (apt, yum, apk)

**3. Command Line:**
- ✅ Bash scripting
- ✅ PowerShell (for Windows environments)
- ✅ Text Editors (Vim/Nano/Emacs)
- ✅ Process/Performance Monitoring (top, htop, iostat)

**4. Version Control:**
- ✅ Git (branches, merges, rebasing)
- ✅ GitHub, GitLab, Bitbucket

**5. Networking:**
- ✅ HTTP, HTTPS
- ✅ DNS, SSH, SSL/TLS
- ✅ OSI Model (7 layers)
- ✅ Firewalls, Proxies
- ✅ SMTP, IMAP, POP3S (email protocols)

**6. Containerization:**
- ✅ Docker (images, containers, volumes, networks)
- ✅ LXC (Linux Containers)
- ✅ Container security best practices

**7. Cloud Platforms:**
- ✅ AWS (EC2, S3, Lambda, RDS, VPC)
- ✅ Azure (VMs, Blob Storage, Functions)
- ✅ Google Cloud (Compute Engine, GCS)
- ✅ Digital Ocean, Hetzner (smaller providers)
- ✅ Heroku, Vercel, Netlify (PaaS)

**8. Function-as-a-Service (Serverless):**
- ✅ AWS Lambda
- ✅ Azure Functions
- ✅ Cloudflare Workers
- ✅ Vercel Functions

**9. Infrastructure as Code:**
- ✅ Terraform (multi-cloud)
- ✅ Pulumi (code-based IaC)
- ✅ AWS CloudFormation
- ✅ AWS CDK

**10. Configuration Management:**
- ✅ Ansible (agentless)
- ✅ Chef (Ruby-based)
- ✅ Puppet (declarative)

**11. CI/CD Pipelines:**
- ✅ Jenkins (classic, highly customizable)
- ✅ GitHub Actions (modern, Git-integrated)
- ✅ GitLab CI (integrated with GitLab)
- ✅ Circle CI
- ✅ TeamCity

**12. Security:**
- ✅ HashiCorp Vault (secrets management)
- ✅ Sealed Secrets (Kubernetes)
- ✅ Cloud-specific tools (AWS Secrets Manager, etc.)
- ✅ SOPs (Standard Operating Procedures)

**13. Observability:**
- ✅ Prometheus (metrics collection)
- ✅ Grafana (visualization, dashboards)
- ✅ Zabbix (traditional monitoring)
- ✅ Datadog (commercial APM)

**14. Logging:**
- ✅ Elastic Stack (ELK: Elasticsearch, Logstash, Kibana)
- ✅ Splunk (commercial)
- ✅ Graylog
- ✅ Papertrail

**15. Orchestration:**
- ✅ GKE (Google Kubernetes Engine)
- ✅ EKS (Elastic Kubernetes Service)
- ✅ AKS (Azure Kubernetes Service)

**16. Web Servers:**
- ✅ Nginx (reverse proxy, load balancer)
- ✅ Apache HTTP Server
- ✅ Caddy (modern, auto-HTTPS)
- ✅ IIS (Windows)
- ✅ Tomcat (Java applications)
- ✅ Load Balancers (HAProxy, ALB)
- ✅ Caching Servers (Varnish, Redis)
