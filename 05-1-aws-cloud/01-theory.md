# Phase 05.5: AWS Cloud - Lý Thuyết

> **Thời gian:** 4 tuần
> **Mục tiêu:** Master AWS services cho Backend Development
> **Certification target:** AWS Certified Developer Associate

---

## 📚 BÀI 1: AWS FUNDAMENTALS

### 1.1 Cloud Computing Concepts

**IaaS vs PaaS vs SaaS:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CLOUD STACK                               │
├─────────────────────────────────────────────────────────────┤
│  SaaS (Software as a Service)                                │
│  - Gmail, Salesforce, Dropbox                                │
│  - Bạn chỉ sử dụng application                               │
├─────────────────────────────────────────────────────────────┤
│  PaaS (Platform as a Service)                                │
│  - Heroku, AWS Elastic Beanstalk, Google App Engine          │
│  - Bạn deploy code, cloud lo phần còn lại                    │
├─────────────────────────────────────────────────────────────┤
│  IaaS (Infrastructure as a Service)                          │
│  - AWS EC2, DigitalOcean, Linode                             │
│  - Bạn quản lý OS, middleware, application                   │
├─────────────────────────────────────────────────────────────┤
│  On-Premises (Traditional)                                   │
│  - Tự mua server, tự quản lý tất cả                          │
└─────────────────────────────────────────────────────────────┘
```

**Public vs Private vs Hybrid Cloud:**

| Type | Description | Use Case |
|------|-------------|----------|
| Public Cloud | AWS, GCP, Azure | Startup, web apps, cost-effective |
| Private Cloud | On-prem datacenter | Banks, gov, strict compliance |
| Hybrid Cloud | Public + Private | Burst to cloud, data residency |

---

### 1.2 AWS Global Infrastructure

```
┌─────────────────────────────────────────────────────────────┐
│                    AWS GLOBAL INFRASTRUCTURE                 │
├─────────────────────────────────────────────────────────────┤
│  Regions                                                     │
│  - Geographic areas (us-east-1, ap-southeast-1, etc.)        │
│  - Each region = multiple Availability Zones                 │
│  - Choose region based on: latency, compliance, cost         │
├─────────────────────────────────────────────────────────────┤
│  Availability Zones (AZs)                                    │
│  - Data centers within a region                              │
│  - Physically separate, connected by high-speed links        │
│  - Deploy across AZs for high availability                   │
├─────────────────────────────────────────────────────────────┤
│  Edge Locations                                              │
│  - CloudFront CDN locations                                  │
│  - Cache content closer to users                             │
│  - 200+ locations worldwide                                  │
└─────────────────────────────────────────────────────────────┘
```

**AWS Regions:**
- `us-east-1` (N. Virginia) - Cheapest, most services
- `us-west-2` (Oregon) - Popular for West Coast
- `eu-west-1` (Ireland) - Popular for Europe
- `ap-southeast-1` (Singapore) - Popular for SEA
- `ap-northeast-1` (Tokyo) - Popular for Asia

---

### 1.3 Shared Responsibility Model

```
┌─────────────────────────────────────────────────────────────┐
│            SHARED RESPONSIBILITY MODEL                       │
├─────────────────────────────────────────────────────────────┤
│  AWS RESPONSIBILITY (Security OF the Cloud)                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  - Physical infrastructure (data centers)            │    │
│  │  - Network infrastructure                            │    │
│  │  - Hypervisor (virtualization layer)                 │    │
│  │  - Managed services (RDS, Lambda, S3)                │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  CUSTOMER RESPONSIBILITY (Security IN the Cloud)             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  - EC2: OS patches, security groups                  │    │
│  │  - Data encryption (at rest & in transit)            │    │
│  │  - IAM: User access management                       │    │
│  │  - Application security                              │    │
│  │  - S3: Bucket policies                               │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 2: AWS COMPUTE SERVICES

### 2.1 EC2 (Elastic Compute Cloud)

**EC2 Instance Types:**

```
┌─────────────────────────────────────────────────────────────┐
│                    EC2 INSTANCE FAMILIES                     │
├─────────────────────────────────────────────────────────────┤
│  General Purpose (M, T)                                      │
│  - Balanced CPU, memory, networking                          │
│  - Use case: Web servers, small databases                    │
│  - Examples: t3.micro, m5.large                              │
├─────────────────────────────────────────────────────────────┤
│  Compute Optimized (C)                                       │
│  - High performance processors                               │
│  - Use case: Batch processing, gaming servers                │
│  - Examples: c5.large, c5n.xlarge                            │
├─────────────────────────────────────────────────────────────┤
│  Memory Optimized (R, X)                                     │
│  - Large memory capacity                                     │
│  - Use case: In-memory databases, real-time analytics        │
│  - Examples: r5.large, x1e.xlarge                            │
├─────────────────────────────────────────────────────────────┤
│  Storage Optimized (I, D)                                    │
│  - High disk throughput                                      │
│  - Use case: Data warehouses, distributed file systems       │
│  - Examples: i3.large, d2.xlarge                             │
└─────────────────────────────────────────────────────────────┘
```

**Instance Naming:**
```
m5.large
│ │ └───── Size (nano, micro, small, medium, large, xlarge, etc.)
│ └─────── Generation (5 = 5th gen)
└───────── Family (m = general purpose, c = compute, r = memory)
```

**Purchasing Options:**

| Option | Discount | Commitment | Use Case |
|--------|----------|------------|----------|
| On-Demand | 0% | None | Short-term, unpredictable |
| Reserved (1yr) | Up to 40% | 1 year | Steady-state workloads |
| Reserved (3yr) | Up to 60% | 3 years | Long-term workloads |
| Spot | Up to 90% | None | Batch processing, fault-tolerant |

---

### 2.2 Auto Scaling

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTO SCALING ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Application Load Balancer               │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        │                                     │
│         ┌──────────────┼──────────────┐                      │
│         │              │              │                      │
│         ▼              ▼              ▼                      │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                 │
│  │ EC2 AZ1  │   │ EC2 AZ2  │   │ EC2 AZ3  │                 │
│  │          │   │          │   │          │                 │
│  └──────────┘   └──────────┘   └──────────┘                 │
│         ▲              ▲              ▲                      │
│         │              │              │                      │
│         └──────────────┼──────────────┘                      │
│                        │                                     │
│         ┌──────────────▼──────────────┐                      │
│         │      Auto Scaling Group      │                      │
│         │  - Min: 2, Max: 10, Desired: 3 │                   │
│         │  - Scaling Policies           │                      │
│         └───────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

**Scaling Policies:**
- **Target Tracking:** Maintain CPU at 70%
- **Simple Scaling:** Add 2 instances when CPU > 80%
- **Step Scaling:** Add 2 if CPU 70-80%, add 4 if CPU > 80%
- **Scheduled Scaling:** Scale up at 9am, scale down at 6pm

---

### 2.3 Lambda (Serverless)

**Lambda Concepts:**

```
┌─────────────────────────────────────────────────────────────┐
│                    LAMBDA ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│  Function                                                    │
│  - Code + Configuration                                      │
│  - Runtime (Node.js, Python, Java, etc.)                     │
│  - Memory (128MB - 10GB)                                     │
│  - Timeout (max 15 minutes)                                  │
├─────────────────────────────────────────────────────────────┤
│  Trigger/Event Source                                        │
│  - API Gateway (HTTP requests)                               │
│  - S3 (file uploads)                                         │
│  - DynamoDB Streams (data changes)                           │
│  - EventBridge (scheduled events)                            │
│  - SQS/SNS (messages)                                        │
├─────────────────────────────────────────────────────────────┤
│  Layers                                                      │
│  - Shared code/libraries                                     │
│  - Separate from function code                               │
│  - Version independently                                     │
├─────────────────────────────────────────────────────────────┤
│  Cold Start vs Warm Start                                    │
│  - Cold: First invocation (slow, ~1-5s)                      │
│  - Warm: Subsequent invocations (fast, ~100ms)               │
│  - Mitigation: Provisioned Concurrency                       │
└─────────────────────────────────────────────────────────────┘
```

**Lambda Pricing:**
- Pay per request: $0.20 per 1M requests
- Pay per duration: $0.0000166667 per GB-second
- Free tier: 1M requests + 400,000 GB-seconds/month

---

### 2.4 ECS/EKS (Containers)

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTAINER OPTIONS                         │
├─────────────────────────────────────────────────────────────┤
│  ECS (Elastic Container Service)                             │
│  - AWS-native container orchestration                        │
│  - Launch types: EC2 or Fargate (serverless)                 │
│  - Simple, integrated with AWS services                      │
├─────────────────────────────────────────────────────────────┤
│  EKS (Elastic Kubernetes Service)                            │
│  - Managed Kubernetes                                        │
│  - Compatible with on-prem K8s                               │
│  - More complex, more flexible                               │
├─────────────────────────────────────────────────────────────┤
│  Fargate                                                     │
│  - Serverless compute for containers                         │
│  - No EC2 management                                         │
│  - Pay per vCPU/memory per second                            │
├─────────────────────────────────────────────────────────────┤
│  ECR (Elastic Container Registry)                            │
│  - Store Docker images                                       │
│  - Integrated with ECS/EKS                                   │
│  - Version control for images                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 3: AWS STORAGE SERVICES

### 3.1 S3 (Simple Storage Service)

**S3 Storage Classes:**

| Class | Durability | Availability | Use Case | Cost |
|-------|-----------|--------------|----------|------|
| S3 Standard | 99.999999999% | 99.99% | Frequently accessed | $$$ |
| S3 Standard-IA | 99.999999999% | 99.9% | Infrequent access | $$ |
| S3 Glacier Instant | 99.999999999% | 99.9% | Archive, instant access | $ |
| S3 Glacier Flexible | 99.999999999% | 99.9% | Archive, 3-5 hour retrieval | ¢ |
| S3 Glacier Deep Archive | 99.999999999% | 99.9% | Long-term archive, 12 hour | ¢¢ |

**S3 Lifecycle Rules:**
```
Day 0: Upload → S3 Standard
Day 30: Transition → S3 Standard-IA
Day 90: Transition → S3 Glacier Instant
Day 365: Transition → S3 Glacier Deep Archive
Day 1825: Expire (delete)
```

**S3 Security:**
- Bucket Policies (resource-based)
- IAM Policies (user-based)
- ACLs (legacy, not recommended)
- Encryption (SSE-S3, SSE-KMS, SSE-C)

---

### 3.2 EBS (Elastic Block Store)

**EBS Volume Types:**

| Type | Description | Use Case | Max IOPS |
|------|-------------|----------|----------|
| gp3 (General Purpose) | Balanced | Boot volumes, small databases | 16,000 |
| gp2 (General Purpose) | Legacy | Development, testing | 16,000 |
| io2 (Provisioned IOPS) | High performance | Production databases | 256,000 |
| st1 (Throughput Optimized) | HDD, sequential | Big data, data warehouses | 500 |
| sc1 (Cold) | HDD, infrequent | Cold data, archives | 250 |

---

## 📚 BÀI 4: AWS DATABASE SERVICES

### 4.1 RDS (Relational Database Service)

**Supported Engines:**
- PostgreSQL
- MySQL
- MariaDB
- Oracle
- SQL Server
- Aurora (AWS-native)

**RDS Features:**
- Automated backups
- Point-in-time recovery
- Multi-AZ deployment (automatic failover)
- Read replicas (scale reads)
- Automated patching

**RDS Storage Types:**

| Type | Description | Use Case |
|------|-------------|----------|
| General Purpose (gp2/gp3) | SSD, balanced | Most workloads |
| Provisioned IOPS (io1/io2) | High IOPS | I/O-intensive databases |
| Magnetic | Legacy, cheap | Dev/test, infrequent access |

---

### 4.2 DynamoDB (NoSQL)

**DynamoDB Concepts:**

```
┌─────────────────────────────────────────────────────────────┐
│                    DYNAMODB STRUCTURE                        │
├─────────────────────────────────────────────────────────────┤
│  Table                                                       │
│  - Collection of items                                       │
│  - Schema-less (each item can have different attributes)     │
├─────────────────────────────────────────────────────────────┤
│  Item                                                        │
│  - Row in the table                                          │
│  - Unique identified by Primary Key                          │
├─────────────────────────────────────────────────────────────┤
│  Attribute                                                   │
│  - Column/field in the item                                  │
│  - Types: String, Number, Binary, List, Map, Set             │
├─────────────────────────────────────────────────────────────┤
│  Primary Key                                                 │
│  - Partition Key (simple)                                    │
│  - Partition Key + Sort Key (composite)                      │
├─────────────────────────────────────────────────────────────┤
│  Secondary Indexes                                           │
│  - GSI (Global Secondary Index)                              │
│    - Different partition key, can query anytime              │
│  - LSI (Local Secondary Index)                               │
│    - Same partition key, different sort key                  │
└─────────────────────────────────────────────────────────────┘
```

**Capacity Modes:**
- **Provisioned:** Set RCU/WCU, auto-scaling available
- **On-Demand:** Pay per request, no capacity planning

**DynamoDB Streams:**
- Capture data changes (INSERT, MODIFY, REMOVE)
- Trigger Lambda functions
- Use case: Real-time analytics, replication

---

### 4.3 ElastiCache (Caching)

**Engines:**
- **Redis:** Advanced data structures, persistence, pub/sub
- **Memcached:** Simple, multi-threaded, no persistence

**Use Cases:**
- Database query caching
- Session storage
- Real-time leaderboards
- Pub/sub messaging

---

## 📚 BÀI 5: AWS NETWORKING

### 5.1 VPC (Virtual Private Cloud)

```
┌─────────────────────────────────────────────────────────────┐
│                    VPC ARCHITECTURE                          │
│  VPC: 10.0.0.0/16                                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐  ┌─────────────────────────┐   │
│  │   Public Subnet         │  │   Private Subnet        │   │
│  │   10.0.1.0/24           │  │   10.0.2.0/24           │   │
│  │                         │  │                         │   │
│  │  ┌──────────┐           │  │  ┌──────────┐           │   │
│  │  │   NAT    │           │  │  │   EC2    │           │   │
│  │  │  Gateway │           │  │  │ (App)    │           │   │
│  │  └────┬─────┘           │  │  └──────────┘           │   │
│  │       │                 │  │                         │   │
│  └───────┼─────────────────┘  └──────────┬──────────────┘   │
│          │                                │                  │
│          │    ┌──────────────────┐        │                  │
│          └───►│  Internet Gateway │◄──────┘                  │
│               └──────────────────┘                           │
│                        │                                       │
│                        ▼                                       │
│                  Internet                                      │
└─────────────────────────────────────────────────────────────┘
```

**VPC Components:**

| Component | Description |
|-----------|-------------|
| VPC | Virtual network isolated in AWS |
| Subnet | Segment of VPC (public/private) |
| Internet Gateway | Connect VPC to internet |
| NAT Gateway | Allow private subnet outbound internet |
| Route Table | Define traffic routing rules |
| Security Group | Stateful firewall for EC2 |
| NACL | Stateless firewall for subnet |

---

### 5.2 Route53 (DNS)

**Routing Policies:**

| Policy | Description | Use Case |
|--------|-------------|----------|
| Simple | Round-robin | Single resource |
| Weighted | Distribute by weight | A/B testing, blue-green |
| Latency | Route to lowest latency | Global users |
| Failover | Primary/backup | Disaster recovery |
| Geolocation | Route by location | Content localization |

---

### 5.3 CloudFront (CDN)

```
┌─────────────────────────────────────────────────────────────┐
│                    CLOUDFRONT FLOW                           │
├─────────────────────────────────────────────────────────────┤
│  User Request                                                │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────────┐                                         │
│  │ Edge Location   │ ← Cache hit → Return immediately        │
│  │ (Nearest to user)│                                        │
│  └────────┬────────┘                                         │
│           │ Cache miss                                       │
│           ▼                                                  │
│  ┌─────────────────┐                                         │
│  │ Regional Edge   │                                         │
│  └────────┬────────┘                                         │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐                                         │
│  │ Origin Server   │ (S3, EC2, ELB, custom)                  │
│  └─────────────────┘                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 6: AWS SECURITY & IAM

### 6.1 IAM (Identity and Access Management)

**IAM Components:**

```
┌─────────────────────────────────────────────────────────────┐
│                    IAM STRUCTURE                             │
├─────────────────────────────────────────────────────────────┤
│  Users                                                       │
│  - Individual people/services                                │
│  - Have credentials (password, access keys)                  │
│  - Example: alice, bob, lambda-function                      │
├─────────────────────────────────────────────────────────────┤
│  Groups                                                      │
│  - Collection of users                                       │
│  - Attach policies to groups                                 │
│  - Example: Developers, Admins                               │
├─────────────────────────────────────────────────────────────┤
│  Roles                                                       │
│  - Identity with permissions                                 │
│  - Assumed by users/services                                 │
│  - No credentials attached                                   │
│  - Example: EC2-Role, Lambda-Role                            │
├─────────────────────────────────────────────────────────────┤
│  Policies                                                    │
│  - JSON documents defining permissions                       │
│  - Identity-based (attached to users/groups/roles)           │
│  - Resource-based (attached to resources)                    │
└─────────────────────────────────────────────────────────────┘
```

**Policy Example:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": "dynamodb:Query",
      "Resource": "arn:aws:dynamodb:us-east-1:123456789:table/Users"
    }
  ]
}
```

---

### 6.2 Security Best Practices

**IAM Best Practices:**
- ✅ Enable MFA for root account
- ✅ Use IAM roles instead of access keys
- ✅ Apply least privilege principle
- ✅ Rotate access keys regularly
- ✅ Use policy conditions (IP, MFA, time)

**Data Protection:**
- ✅ Encrypt data at rest (KMS, S3 SSE)
- ✅ Encrypt data in transit (TLS/SSL)
- ✅ Use VPC endpoints for private access
- ✅ Enable CloudTrail for audit logging

---

## 📚 BÀI 7: AWS MONITORING & MANAGEMENT

### 7.1 CloudWatch

**CloudWatch Components:**

| Component | Description |
|-----------|-------------|
| Metrics | Performance data (CPU, memory, etc.) |
| Alarms | Trigger actions when threshold breached |
| Logs | Collect, monitor, analyze logs |
| Events (EventBridge) | Respond to state changes |
| Dashboards | Visualize metrics |

**Common Alarms:**
- CPU utilization > 80% for 5 minutes
- Error rate > 5% for 5 minutes
- Disk space < 10%
- Lambda duration > timeout threshold

---

### 7.2 CloudTrail

**CloudTrail captures:**
- API calls (who, what, when, where)
- Console sign-ins
- SDK/CLI commands

**Use cases:**
- Security analysis
- Compliance auditing
- Troubleshooting

---

## 📝 TÓM TẮT PHASE 05.5

1. ✅ AWS Global Infrastructure (Regions, AZs, Edge Locations)
2. ✅ EC2 (instance types, purchasing options, auto-scaling)
3. ✅ Lambda (serverless, triggers, cold start)
4. ✅ S3 (storage classes, lifecycle, security)
5. ✅ RDS & DynamoDB (managed databases)
6. ✅ VPC (subnets, routing, security groups)
7. ✅ IAM (users, roles, policies)
8. ✅ CloudWatch & CloudTrail (monitoring)

---

## 🔜 TIẾP THEO

Đọc `02-examples.md` để xem code mẫu và hands-on labs!
