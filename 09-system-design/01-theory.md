# Phase 09: System Design - Lý Thuyết

> **Thời gian:** 4 tuần
> **Mục tiêu:** Design được scalable systems, pass senior interview
>
> **Tham khảo:** [system-design-primer](https://github.com/donnemartin/system-design-primer)

---

## 📚 BÀI 1: SYSTEM DESIGN INTERVIEW FRAMEWORK

### 6-Step Framework

```
Step 1: Requirements Clarification (5 min)
        - Functional requirements
        - Non-functional requirements
        - Scale estimation

Step 2: Back-of-the-envelope Estimation (5 min)
        - QPS, storage, bandwidth

Step 3: Data Model Design (10 min)
        - Database schema
        - Data flow

Step 4: High-level Design (15 min)
        - Services/APIs
        - Architecture diagram

Step 5: Deep Dive (15 min)
        - Bottlenecks
        - Scaling strategies

Step 6: Summary & Trade-offs (10 min)
        - What went well
        - What could be better
```

---

## 📚 BÀI 2: SCALE ESTIMATION

### 2.1 Back-of-the-envelope Calculations

**Ví dụ: Design Twitter**

```
Giả sử:
- 500M users
- 300M daily active users (DAU)
- Mỗi user tweet 2 times/day
- Mỗi tweet xem bởi 1000 people

Calculations:
- Tweets per day: 300M × 2 = 600M tweets
- Tweet reads per day: 600M × 1000 = 600B reads
- QPS (writes): 600M / 86400 ≈ 7,000 tweets/sec
- QPS (reads): 600B / 86400 ≈ 7,000,000 reads/sec

Storage:
- Mỗi tweet: 1KB
- Daily storage: 600M × 1KB = 600GB
- 5 years storage: 600GB × 365 × 5 ≈ 1PB
```

### 2.2 Power of Two Choices

```
Rule of thumb:
- 1 million users ≈ 1GB RAM
- 1 billion users ≈ 1TB RAM
- Read:Write ratio thường là 100:1 đến 1000:1
- Cache hit ratio target: 90%+
```

---

## 📚 BÀI 3: DESIGN PATTERNS

### 3.1 Load Balancer Patterns

```
Clients → Load Balancer → Servers

LB Algorithms:
- Round Robin
- Least Connections
- IP Hash (sticky sessions)
- Weighted (cho heterogeneous servers)
```

### 3.2 Database Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE SCALING                          │
├─────────────────────────────────────────────────────────────┤
│  1. Read Replicas                                           │
│     Master → Slaves (replication)                           │
│     Writes: Master, Reads: Slaves                           │
├─────────────────────────────────────────────────────────────┤
│  2. Sharding (Horizontal Partitioning)                      │
│     Users A-M → DB1, Users N-Z → DB2                        │
│     Or: Geo-based sharding                                  │
├─────────────────────────────────────────────────────────────┤
│  3. Vertical Partitioning                                   │
│     Frequently accessed columns → Fast DB                   │
│     Archive columns → Cold storage                          │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Caching Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                    CACHING STRATEGIES                        │
├─────────────────────────────────────────────────────────────┤
│  1. Cache-Aside (Lazy Loading)                              │
│     Application → Check cache → Miss → DB → Cache          │
├─────────────────────────────────────────────────────────────┤
│  2. Write-Through                                           │
│     Write cache → Cache writes to DB sync                  │
├─────────────────────────────────────────────────────────────┤
│  3. Write-Behind                                            │
│     Write cache → Async batch write to DB                  │
├─────────────────────────────────────────────────────────────┤
│  4. Refresh-Ahead                                           │
│     Proactively refresh before expiry                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 4: MESSAGE QUEUE PATTERNS

### 4.1 Queue-based Load Leveling

```
Producer → Queue → Consumer

Benefits:
- Decouple producer and consumer
- Smooth traffic spikes
- Retry failed messages
```

### 4.2 Pub-Sub Pattern

```
                ┌──────────────┐
Publisher ─────►│    Topic     │
                └──────┬───────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
    Subscriber 1  Subscriber 2  Subscriber 3
```

---

## 📚 BÀI 5: AVAILABILITY & CONSISTENCY

### 5.1 CAP Theorem

```
┌─────────────────────────────────────────────────────────────┐
│                    CAP THEOREM                               │
├─────────────────────────────────────────────────────────────┤
│  Chỉ có thể chọn 2 trong 3:                                 │
│                                                              │
│  Consistency (C): Tất cả nodes thấy cùng data tại cùng thời │
│  Availability (A): Mọi request đều có response              │
│  Partition Tolerance (P): System hoạt động dù có network    │
│                             partition                        │
│                                                              │
│  Thực tế: P là bắt buộc → chọn C hoặc A                     │
│                                                              │
│  ┌─────────────┬─────────────┬─────────────────────────┐   │
│  │  Type       │  Trade-off  │  Use Case               │   │
│  ├─────────────┼─────────────┼─────────────────────────┤   │
│  │  CP         │  Lose A     │  Banking, payments      │   │
│  │  AP         │  Lose C     │  Social media, feeds    │   │
│  │  CA         │  Lose P     │  Không tồn tại thực tế  │   │
│  └─────────────┴─────────────┴─────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Consistency Models

```
Strong Consistency:
- Read sau Write luôn trả về data mới nhất
- Dùng cho: Banking, financial systems
- Example: RDBMS với ACID transactions

Eventual Consistency:
- Read sau Write có thể trả về data cũ
- Nhưng cuối cùng sẽ converge
- Dùng cho: Social media, DNS, caches
- Example: DynamoDB, Cassandra

Causal Consistency:
- Giữ causal order của operations
- Good balance giữa C và A
```

### 5.3 Availability Numbers

```
┌─────────────────────────────────────────────────────────────┐
│              AVAILABILITY NUMBERS                            │
├─────────────────────────────────────────────────────────────┤
│  99%       = 3.65 days downtime/year                       │
│  99.9%     = 8.76 hours downtime/year                      │
│  99.99%    = 52.6 minutes downtime/year                    │
│  99.999%   = 5.26 minutes downtime/year                    │
│  99.9999%  = 31.5 seconds downtime/year                    │
└─────────────────────────────────────────────────────────────┘

Cách tính availability:
Availability = MTTF / (MTTF + MTTR)

MTTF = Mean Time To Failure
MTTR = Mean Time To Repair
```

---

## 📚 BÀI 6: ESTIMATION CHEAT SHEET

### 6.1 Power of Two

```
Latency numbers (cho 1 request):
- L1 cache: 0.5 ns
- L2 cache: 7 ns
- Main memory: 100 ns
- SSD: 150 μs
- HDD: 10 ms
- Network (DC): 0.5 ms
- Internet (US-EU): 150 ms

Rule of thumb:
- 1 million users ≈ 1TB storage/month
- 1 billion users ≈ 1PB storage/month
- Read:Write ratio = 100:1 to 1000:1
- Cache hit ratio target = 90%+
```

### 6.2 Back-of-envelope Calculations

```
Ví dụ: Design URL Shortener

QPS estimation:
- 500M users, 10% create URL/day = 50M writes/day
- 50M / 86400 ≈ 600 writes/sec
- Read 100x more = 60,000 reads/sec

Storage:
- 50M URLs/day × 30 days = 1.5B URLs/month
- Mỗi URL record: 500 bytes
- 1.5B × 500 = 750 GB/month
- 5 years: 750 × 60 = 45 TB

Bandwidth:
- Short URL: 50 bytes
- Redirect response: 500 bytes
- 60,000 reads/sec × 500 bytes = 30 MB/s
```

---

## 📚 BÀI 7: CASE STUDIES TỪ SYSTEM-DESIGN-PRIMER

### 7.1 Design URL Shortener (TinyURL/bit.ly)

**Requirements:**
- Functional: Shorten URL, redirect to original
- Non-functional: High availability, low latency, short URLs

**API Design:**
```
POST /api/v1/shorten
  Request: { "url": "https://example.com/very-long-url" }
  Response: { "shortUrl": "https://short.url/abc123" }

GET /api/v1/{shortCode}
  Response: 301 redirect to original URL
```

**Data Model:**
```sql
CREATE TABLE url_mappings (
  id BIGINT PRIMARY KEY,
  short_code VARCHAR(10) UNIQUE NOT NULL,
  original_url TEXT NOT NULL,
  user_id BIGINT,
  created_at TIMESTAMP,
  expiry_date TIMESTAMP,
  INDEX idx_short_code (short_code)
);
```

**Algorithm:**
```
1. Base62 encoding (a-z, A-Z, 0-9)
2. Input: auto-increment ID → Output: 6-char code
3. Example: ID=12345 → "abc123"

Collision handling:
- Check DB for existing short_code
- If exists, increment ID and retry
```

**Architecture:**
```
                    ┌─────────────┐
Clients ───────────►│   Load      │
                    │  Balancer   │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ Service  │     │ Service  │     │ Service  │
   │   1      │     │   2      │     │   N      │
   └────┬─────┘     └────┬─────┘     └────┬─────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                    ┌────▼─────┐
                    │ Database │
                    │  Cluster │
                    └──────────┘
```

### 7.2 Design Rate Limiter

**Requirements:**
- Limit requests per user/IP/endpoint
- Low latency (< 1ms check)
- Distributed (work across multiple servers)

**Algorithms:**

```
1. Fixed Window:
   - Count requests in fixed time window
   - Simple nhưng có boundary problem

2. Sliding Window:
   - Count requests in rolling window
   - Fair hơn, phức tạp hơn

3. Token Bucket:
   - Tokens added at fixed rate
   - Each request consumes 1 token
   - Allows bursting

4. Leaky Bucket:
   - Requests processed at fixed rate
   - Queue overflow → reject
```

**Implementation với Redis:**
```java
@Service
public class RateLimiter {

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    public boolean isAllowed(String userId, int limit, int windowSeconds) {
        String key = "rate_limit:" + userId;
        long current = redisTemplate.opsForValue().increment(key);

        if (current == 1) {
            redisTemplate.expire(key, windowSeconds, TimeUnit.SECONDS);
        }

        return current <= limit;
    }
}
```

### 7.3 Design Twitter/Instagram Feed

**Requirements:**
- Users see feed of people they follow
- Real-time updates
- Handle celebrities (millions of followers)

**Approach 1: Pull (Fan-out on read)**
```
- Khi user load feed → query DB cho tất cả followees
- Simple nhưng chậm với power users
```

**Approach 2: Push (Fan-out on write)**
```
- Khi user post → push to cache của tất cả followers
- Fast read nhưng slow write cho celebrities
```

**Hybrid Approach:**
```
- Normal users: Push model
- Celebrities (>1M followers): Pull model
- Regular users: Push model

Architecture:
- Write → Kafka → Process → Cache (Redis)
- Read → Cache → If empty → DB → Cache
```

**Data Model:**
```sql
-- User table
users (id, username, email, created_at)

-- Follow table
follows (follower_id, followee_id, created_at)
PRIMARY KEY (follower_id, followee_id)

-- Tweets table
tweets (id, user_id, content, created_at)
INDEX idx_user_created (user_id, created_at)

-- Feed cache (Redis)
Key: feed:{user_id}
Value: List of tweet IDs (sorted by time)
```

---

## 📝 TÓM TẮT PHASE 09

1. ✅ System design interview framework (6 steps)
2. ✅ Scale estimation calculations
3. ✅ Design patterns (LB, DB scaling, caching)
4. ✅ Message queue patterns
5. ✅ CAP theorem & consistency models
6. ✅ Availability numbers
7. ✅ Case studies (URL shortener, Rate limiter, Twitter feed)

---

## 🔜 TIẾP THEO

Xem `02-examples.md` để xem thêm design cases!
