# AWS Cloud & Best Practices - Theory

> **Thời gian:** 4 tuần
> **Mục tiêu:** Master AWS services cho Backend Development, AWS Best Practices
> **Certification target:** AWS Certified Developer Associate
>
> **Tham khảo:** [roadmap.sh/aws-best-practices](https://roadmap.sh/aws-best-practices)

---

## 📚 BÀI 0: AWS BEST PRACTICES FRAMEWORK

### 0.1 Security Best Practices

**IAM & Access Control:**
```
✅ DO:
- Enable MFA for root account and IAM users
- Use IAM roles instead of access keys for EC2/Lambda
- Assign permissions to groups, not individual users
- Apply least privilege principle
- Rotate access keys regularly (90 days)
- Use policy conditions (IP, MFA, time-based)
- Use CloudTrail to keep an audit log
- Set up automated security auditing

❌ DON'T:
- Share access keys between team members
- Use root account for daily operations
- Grant overly permissive policies (*:*)
- Leave unused access keys active
```

**Data Protection:**
```
✅ DO:
- Encrypt data at rest (KMS, S3 SSE, EBS encryption)
- Encrypt data in transit (TLS/SSL everywhere)
- Use VPC endpoints for private AWS service access
- Enable S3 bucket versioning
- Use AWS Secrets Manager for sensitive credentials

❌ DON'T:
- Store secrets in code or config files
- Use HTTP for production traffic
- Leave S3 buckets publicly accessible (unless intended)
```

---

### 0.2 Development Best Practices

**Application Design:**
```
✅ DO:
- Do not store application state on servers (stateless design)
- Use external stores for sessions (ElastiCache, DynamoDB)
- Store extra information in your logs for debugging
- Use the official AWS SDKs for AWS interactions
- Have tools to view application logs in real-time
- Design for failure (retry logic, circuit breakers)
- Use environment variables for configuration

❌ DON'T:
- Rely on sticky sessions for state management
- Store sessions in local memory/filesystem
- Hardcode AWS credentials
- Ignore CloudWatch logs
```

**Logging & Monitoring:**
```
✅ DO:
- Use structured logging (JSON format)
- Include correlation IDs for request tracing
- Ship logs to CloudWatch Logs or S3
- Set up log retention policies
- Use X-Ray for distributed tracing

❌ DON'T:
- Log sensitive information (PII, credentials)
- Store logs only on local disk
- Ignore log rotation
```

---

### 0.3 Operations Best Practices

**Infrastructure Management:**
```
✅ DO:
- Automate everything (Infrastructure as Code)
- Use CloudFormation or Terraform
- Use tags for resource organization
- Use termination protection for critical instances
- Use a VPC for network isolation
- Lock down security groups (least privilege)
- Deploy across multiple AZs for redundancy

❌ DON'T:
- Manually create resources in console
- Use static/elastic IPs for servers
- Keep unassociated Elastic IPs (costs money)
- Use default security groups
- Deploy single-AZ for production
```

**Scaling & High Availability:**
```
✅ DO:
- Scale horizontally (add more instances)
- Use Auto Scaling groups
- Use ELB health checks instead of EC2 health checks
- Scale down on INSUFFICIENT_DATA as well as ALARM
- Use multiple AZs for all critical services
- Be aware of AWS service limits before deployment

❌ DON'T:
- Scale vertically only (bigger instances)
- Ignore scaling metrics
- Use single point of failure
```

---

### 0.4 Billing & Cost Optimization

**Cost Management:**
```
✅ DO:
- Set up granular billing alerts
- Use Reserved Instances for steady-state workloads (up to 60% savings)
- Use Spot Instances for batch/fault-tolerant workloads (up to 90% savings)
- Right-size instances based on actual usage
- Use S3 lifecycle policies for data tiering
- Delete unused resources (EBS volumes, snapshots, Elastic IPs)
- Use Cost Explorer to analyze spending

❌ DON'T:
- Leave resources running when not needed
- Over-provision "just in case"
- Ignore billing alerts
- Use on-demand for everything
```

---

### 0.5 S3 Best Practices

```
✅ DO:
- Use "-" instead of "." in bucket names for SSL compatibility
- Use random strings/prefixes at the start of keys for performance
- Enable versioning for important buckets
- Use lifecycle policies to transition old data to Glacier
- Enable S3 server access logging
- Use S3 Transfer Acceleration for global uploads

❌ DON'T:
- Use filesystem mounts (FUSE, etc.) for production
- Store sensitive data without encryption
- Leave buckets publicly accessible (unless intended)
```

---

### 0.6 EC2 & VPC Best Practices

```
✅ DO:
- Assign tags to everything (Name, Environment, Owner, CostCenter)
- Use termination protection for non-auto-scaling instances
- Use private subnets for application servers
- Use NAT Gateway for private subnet outbound access
- Use Security Groups (stateful) as primary firewall
- Use NACLs (stateless) as secondary defense layer

❌ DON'T:
- SSH directly from internet (use bastion host)
- Use public IPs for internal services
- Leave security groups open to 0.0.0.0/0
```

---

### 0.7 ELB (Elastic Load Balancer) Best Practices

```
✅ DO:
- Terminate SSL on the load balancer
- Pre-warm ELBs if expecting heavy traffic (contact AWS)
- Use multiple AZs for load balancer
- Enable access logs for debugging
- Use health checks with appropriate thresholds

❌ DON'T:
- Use single AZ for load balancer
- Ignore unhealthy target notifications
```

---

### 0.8 RDS Best Practices

```
✅ DO:
- Set up event subscriptions for failover notifications
- Use Multi-AZ for production databases
- Use Read Replicas for scaling read operations
- Enable automated backups with appropriate retention
- Use Parameter Groups for configuration management
- Monitor FreeStorageSpace, CPU, connections

❌ DON'T:
- Use default credentials
- Skip backup testing
- Ignore storage capacity alerts
```

---

### 0.9 ElastiCache Best Practices

```
✅ DO:
- Use configuration endpoints instead of individual node endpoints
- Use Multi-AZ for production caches
- Monitor cache hit/miss ratios
- Set appropriate TTL for cache entries

❌ DON'T:
- Use cache as primary data store
- Cache everything without strategy
```

---

### 0.10 Route53 Best Practices

```
✅ DO:
- Use ALIAS records instead of CNAME for root domains
- Use health checks with DNS failover
- Use latency-based routing for global apps
- Enable DNSSEC for domain security

❌ DON'T:
- Use CNAME for root domain (@)
- Skip health checks for critical services
```

---

### 0.11 CloudWatch Best Practices

```
✅ DO:
- Use CLI tools for automation
- Use the free metrics (basic monitoring)
- Use custom metrics for application-specific data
- Use detailed monitoring for critical instances (1-minute granularity)
- Set up composite alarms to reduce noise
- Use CloudWatch Logs Insights for querying

❌ DON'T:
- Set thresholds too low (alert fatigue)
- Ignore INSUFFICIENT_DATA state
- Log everything without retention policy
```

---

### 0.12 Naming Conventions

```
✅ DO:
- Decide on a naming convention early, and stick to it
- Include environment, service, and region in names
- Example: prod-user-service-us-east-1, dev-db-primary

Examples:
- VPC: vpc-prod-us-east-1, vpc-dev-us-east-1
- Subnet: subnet-prod-app-1a, subnet-prod-db-1b
- Security Group: sg-prod-app-servers, sg-prod-db-access
- EC2: i-prod-app-server-01, i-prod-bastion-01
- S3: mycompany-prod-assets-us-east-1
- RDS: prod-db-primary, prod-db-replica

❌ DON'T:
- Use random names without pattern
- Mix naming conventions
```

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
