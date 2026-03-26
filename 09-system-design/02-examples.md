# Phase 09: System Design - Ví Dụ Thực Tế

> **Tham khảo chính:** [system-design-primer](https://github.com/donnemartin/system-design-primer)

---

## 📁 BÀI 1: DESIGN URL SHORTENER (TinyURL/bit.ly)

### 1.1 Requirements

**Functional:**
- Given a long URL, return shortened URL
- Redirect user to original URL when accessing short URL
- Optional: Custom alias, expiration, analytics

**Non-functional:**
- High availability (redirects must be fast)
- Low latency (< 100ms)
- Short URLs should be easy to type/share
- Scale: 100M URLs/month, 10B redirects/month

### 1.2 Capacity Estimation

```
Assumptions:
- 100M new URLs/month
- 10B redirects/month
- Read:Write ratio = 100:1

Traffic:
- New URLs: 100M / (30 × 24 × 3600) ≈ 40 URLs/sec
- Redirects: 10B / (30 × 24 × 3600) ≈ 4,000 redirects/sec

Storage (5 years):
- 100M URLs/month × 60 months = 6B URLs
- Each URL record: 500 bytes
- Total: 6B × 500B = 3TB

Bandwidth:
- Redirect response: 500 bytes
- 4,000 redirects/sec × 500B = 2 MB/s
```

### 1.3 API Design

```java
// REST API
POST /api/v1/shorten
Content-Type: application/json
{
    "url": "https://example.com/very-long-path/with-many-params?id=123&ref=abc",
    "customAlias": "my-custom",  // optional
    "expiryDays": 30              // optional
}

Response: 201 Created
{
    "shortUrl": "https://short.url/abc123",
    "expiryDate": "2024-12-31T23:59:59Z"
}

---

GET /api/v1/{shortCode}
Response: 301 Moved Permanently
Location: https://example.com/very-long-path/...

---

GET /api/v1/{shortCode}/stats
Response: 200 OK
{
    "originalUrl": "https://example.com/...",
    "clicks": 1234,
    "createdAt": "2024-01-01T00:00:00Z",
    "lastAccessedAt": "2024-01-15T12:30:00Z"
}
```

### 1.4 Database Schema

```sql
-- URL mappings table
CREATE TABLE url_mappings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    user_id BIGNULL,                    -- NULL for anonymous
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP NULL,
    click_count BIGINT DEFAULT 0,
    last_accessed_at TIMESTAMP NULL,

    INDEX idx_short_code (short_code),
    INDEX idx_user (user_id),
    INDEX idx_expiry (expiry_date)
);

-- Analytics table (optional, for detailed stats)
CREATE TABLE url_analytics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    short_code VARCHAR(10) NOT NULL,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    referrer VARCHAR(500),
    country VARCHAR(50),

    INDEX idx_short_code_time (short_code, accessed_at),
    INDEX idx_country (country)
);
```

### 1.5 Algorithm Design

**Base62 Encoding:**

```java
@Service
public class UrlShortener {

    private static final String BASE62 =
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

    @Autowired
    private UrlMappingRepository repository;

    public String shorten(String url) {
        // Generate unique ID (auto-increment or UUID)
        long id = generateUniqueId();

        // Convert to Base62
        String shortCode = encode(id);

        // Check collision, retry if needed
        while (repository.existsByShortCode(shortCode)) {
            id = generateUniqueId();
            shortCode = encode(id);
        }

        // Save to database
        UrlMapping mapping = new UrlMapping();
        mapping.setShortCode(shortCode);
        mapping.setOriginalUrl(url);
        repository.save(mapping);

        return shortCode;
    }

    private String encode(long num) {
        StringBuilder sb = new StringBuilder();
        while (num > 0) {
            sb.append(BASE62.charAt((int)(num % 62)));
            num /= 62;
        }
        return sb.reverse().toString();
    }

    private long decode(String shortCode) {
        long num = 0;
        for (char c : shortCode.toCharArray()) {
            num = num * 62 + BASE62.indexOf(c);
        }
        return num;
    }
}
```

### 1.6 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    URL SHORTENER ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Clients (Browser, Mobile)                                      │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────┐                                                │
│  │   Load      │                                                │
│  │  Balancer   │                                                │
│  └──────┬──────┘                                                │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Application Servers                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │    │
│  │  │ Service  │  │ Service  │  │ Service  │              │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘              │    │
│  └───────┼─────────────┼─────────────┼────────────────────┘    │
│          │             │             │                          │
│          ▼             ▼             ▼                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Redis     │  │  MySQL      │  │   Kafka     │            │
│  │   Cache     │  │  Cluster    │  │  (Analytics)│            │
│  │             │  │             │  │             │            │
│  │  - Short →  │  │  - URL      │  │  - Click    │            │
│  │  Original   │  │  mappings   │  │  events     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Flow:**

```
Shorten URL:
1. Client → POST /shorten → API Server
2. Generate short code (Base62 encode)
3. Check cache for collision
4. Save to MySQL
5. Update cache
6. Return short URL

Redirect:
1. Client → GET /{shortCode} → API Server
2. Check cache first (99% hit rate)
3. If miss → query MySQL → update cache
4. Log click event to Kafka (async)
5. Return 301 redirect
```

---

## 📁 BÀI 2: DESIGN RATE LIMITER

### 2.1 Requirements

**Functional:**
- Limit requests per user/IP/API key
- Configurable limits (requests per second/minute/hour)
- Return 429 Too Many Requests when exceeded

**Non-functional:**
- Low latency (< 1ms for rate limit check)
- Distributed (work across multiple servers)
- High availability

### 2.2 Algorithms

**Fixed Window Counter:**

```java
@Service
public class FixedWindowRateLimiter {

    private final ConcurrentHashMap<String, AtomicLong> counters = new ConcurrentHashMap<>();
    private final ConcurrentHashMap<String, Long> windows = new ConcurrentHashMap<>();

    public boolean isAllowed(String userId, int limit, long windowMs) {
        long now = System.currentTimeMillis();
        long windowStart = now / windowMs * windowMs;

        long userWindow = windows.getOrDefault(userId, 0L);
        if (userWindow != windowStart) {
            // New window, reset counter
            counters.put(userId, new AtomicLong(1));
            windows.put(userId, windowStart);
            return true;
        }

        long count = counters.get(userId).incrementAndGet();
        return count <= limit;
    }
}
```

**Sliding Window Log:**

```java
@Service
public class SlidingWindowRateLimiter {

    private final ConcurrentHashMap<String, Queue<Long>> logs = new ConcurrentHashMap<>();

    public boolean isAllowed(String userId, int limit, long windowMs) {
        long now = System.currentTimeMillis();
        long windowStart = now - windowMs;

        Queue<Long> userLog = logs.computeIfAbsent(userId, k -> new ConcurrentLinkedQueue<>());

        // Remove old entries
        while (!userLog.isEmpty() && userLog.peek() < windowStart) {
            userLog.poll();
        }

        if (userLog.size() >= limit) {
            return false;
        }

        userLog.offer(now);
        return true;
    }
}
```

**Token Bucket:**

```java
@Service
public class TokenBucketRateLimiter {

    private final ConcurrentHashMap<String, TokenBucket> buckets = new ConcurrentHashMap<>();

    static class TokenBucket {
        int capacity;
        int tokens;
        long lastRefillTime;
        int refillRate; // tokens per second

        public TokenBucket(int capacity, int refillRate) {
            this.capacity = capacity;
            this.tokens = capacity;
            this.refillRate = refillRate;
            this.lastRefillTime = System.currentTimeMillis();
        }

        public synchronized boolean consume() {
            refill();
            if (tokens > 0) {
                tokens--;
                return true;
            }
            return false;
        }

        private void refill() {
            long now = System.currentTimeMillis();
            long elapsed = now - lastRefillTime;
            int newTokens = (int)(elapsed * refillRate / 1000);
            tokens = Math.min(capacity, tokens + newTokens);
            lastRefillTime = now;
        }
    }

    public boolean isAllowed(String userId, int capacity, int refillRate) {
        TokenBucket bucket = buckets.computeIfAbsent(
            userId,
            k -> new TokenBucket(capacity, refillRate)
        );
        return bucket.consume();
    }
}
```

### 2.3 Redis Implementation (Distributed)

```java
@Service
public class RedisRateLimiter {

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    private static final String SCRIPT = """
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        local current = redis.call('GET', key)
        if current == false then
            redis.call('SET', key, 1, 'EX', window)
            return 1
        end

        local count = tonumber(current)
        if count >= limit then
            return 0
        end

        redis.call('INCR', key)
        return 1
        """;

    public boolean isAllowed(String userId, int limit, int windowSeconds) {
        String key = "ratelimit:" + userId;
        long now = System.currentTimeMillis() / 1000;

        Long result = redisTemplate.execute(
            new DefaultRedisScript<>(SCRIPT, Long.class),
            Collections.singletonList(key),
            String.valueOf(limit),
            String.valueOf(windowSeconds),
            String.valueOf(now)
        );

        return result != null && result == 1;
    }
}
```

### 2.4 Spring Boot Integration

```java
@Configuration
public class RateLimitConfig {

    @Bean
    public FilterRegistrationBean<RateLimitFilter> rateLimitFilter() {
        FilterRegistrationBean<RateLimitFilter> registration =
            new FilterRegistrationBean<>();
        registration.setFilter(new RateLimitFilter());
        registration.addUrlPatterns("/api/*");
        registration.setOrder(1);
        return registration;
    }
}

@Component
public class RateLimitFilter implements Filter {

    @Autowired
    private RedisRateLimiter rateLimiter;

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        // Get user identifier (IP, API key, or user ID)
        String userId = getClientIdentifier(httpRequest);

        if (!rateLimiter.isAllowed(userId, 100, 60)) {
            httpResponse.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
            httpResponse.setHeader("X-RateLimit-Limit", "100");
            httpResponse.setHeader("X-RateLimit-Remaining", "0");
            httpResponse.setHeader("Retry-After", "60");
            httpResponse.getWriter().write("Rate limit exceeded");
            return;
        }

        chain.doFilter(request, response);
    }

    private String getClientIdentifier(HttpServletRequest request) {
        // Option 1: IP address
        // return request.getRemoteAddr();

        // Option 2: API key from header
        String apiKey = request.getHeader("X-API-Key");
        if (apiKey != null) {
            return "api:" + apiKey;
        }

        // Option 3: User ID from JWT
        // return "user:" + getUserIdFromToken(request);

        // Default: IP address
        return "ip:" + request.getRemoteAddr();
    }
}
```

---

## 📁 BÀI 3: DESIGN TWITTER/INSTAGRAM FEED

### 3.1 Requirements

**Functional:**
- Users see feed of posts from people they follow
- Users can post tweets/photos
- Users can follow/unfollow others
- Like, comment, share functionality

**Non-functional:**
- Feed should load in < 200ms
- Support 500M users, 300M DAU
- Handle celebrities (millions of followers)
- High read:write ratio (1000:1)

### 3.2 Capacity Estimation

```
Assumptions:
- 300M DAU
- Each user posts 2 tweets/day
- Each user follows 200 people
- Read:Write ratio = 1000:1

Traffic:
- New tweets: 300M × 2 = 600M tweets/day
- Tweet reads: 600M × 1000 = 600B reads/day
- QPS writes: 600M / 86400 ≈ 7,000 tweets/sec
- QPS reads: 600B / 86400 ≈ 7M reads/sec

Storage (5 years):
- 600M tweets/day × 365 × 5 = 1.1T tweets
- Each tweet: 1KB
- Total: 1.1PB
```

### 3.3 Data Model

```sql
-- Users table
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Follows table
CREATE TABLE follows (
    follower_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id),
    INDEX idx_followee (followee_id)
);

-- Tweets table
CREATE TABLE tweets (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content TEXT,
    media_urls JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    like_count INT DEFAULT 0,
    retweet_count INT DEFAULT 0,
    INDEX idx_user_time (user_id, created_at),
    INDEX idx_created (created_at)
);

-- Likes table
CREATE TABLE likes (
    user_id BIGINT NOT NULL,
    tweet_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, tweet_id)
);
```

### 3.4 Feed Generation Approaches

**Approach 1: Pull (Fan-out on read)**

```
How it works:
- When user loads feed → Query DB for all followees' tweets
- Merge and sort by timestamp

Pros:
- Simple implementation
- No duplicate storage
- Real-time (always fresh)

Cons:
- Slow for users following many people
- DB load on every feed request

SQL:
SELECT t.* FROM tweets t
JOIN follows f ON t.user_id = f.followee_id
WHERE f.follower_id = ?
ORDER BY t.created_at DESC
LIMIT 20;
```

**Approach 2: Push (Fan-out on write)**

```
How it works:
- When user posts → Push to cache of all followers
- Feed = Pre-computed cache

Pros:
- Fast feed reads (cache lookup)
- Consistent read latency

Cons:
- Slow write for celebrities
- Storage duplication
- Delayed delivery

Pseudo-code:
def post_tweet(user_id, content):
    tweet = save_tweet(user_id, content)
    followers = get_followers(user_id)

    for follower in followers:
        cache.push(f"feed:{follower}", tweet)
```

**Approach 3: Hybrid (Recommended)**

```
How it works:
- Normal users (< 10K followers): Push model
- Celebrities (>= 10K followers): Pull model
- Feed = Merge of push cache + pull for celebrities

Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    TWITTER FEED ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Write Path:                                                 │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌─────────────┐ │
│  │  Post  │───►│ Kafka  │───►│Worker  │───►│   Redis     │ │
│  │        │    │ Queue  │    │ Pool   │    │   Cache     │ │
│  └────────┘    └────────┘    └────────┘    └─────────────┘ │
│                                                              │
│  Read Path:                                                  │
│  ┌────────┐    ┌─────────────────────────────────────────┐  │
│  │  Feed  │───►│ 1. Check Redis cache (push tweets)      │  │
│  │ Request│    │ 2. Query DB for celebrity tweets (pull) │  │
│  └────────┘    │ 3. Merge, sort, return                  │  │
│                └─────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3.5 Implementation

```java
@Service
public class FeedService {

    @Autowired
    private TweetRepository tweetRepository;

    @Autowired
    private FollowRepository followRepository;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Autowired
    private KafkaTemplate<String, TweetEvent> kafkaTemplate;

    private static final int CELEBRITY_THRESHOLD = 10000;

    // Post tweet
    @Transactional
    public Tweet postTweet(Long userId, String content) {
        Tweet tweet = tweetRepository.save(
            Tweet.builder()
                .userId(userId)
                .content(content)
                .build()
        );

        // Send to Kafka for async processing
        kafkaTemplate.send("tweet-events", new TweetEvent(tweet.getId(), userId));

        return tweet;
    }

    // Get feed
    public List<Tweet> getFeed(Long userId, int limit) {
        // Get followees
        List<Long> followees = followRepository.findFolloweeIds(userId);

        // Split into normal and celebrity
        List<Long> normalFollowees = new ArrayList<>();
        List<Long> celebrityFollowees = new ArrayList<>();

        for (Long followee : followees) {
            int followerCount = followRepository.countFollowers(followee);
            if (followerCount >= CELEBRITY_THRESHOLD) {
                celebrityFollowees.add(followee);
            } else {
                normalFollowees.add(followee);
            }
        }

        // Get cached tweets for normal followees (push)
        List<Tweet> cachedTweets = getCachedTweets(normalFollowees, limit);

        // Get tweets for celebrities (pull)
        List<Tweet> celebrityTweets = tweetRepository
            .findByUserIdsOrderByCreatedAtDesc(celebrityFollowees, PageRequest.of(0, limit));

        // Merge and sort
        List<Tweet> allTweets = Stream.concat(cachedTweets.stream(), celebrityTweets.stream())
            .sorted(Comparator.comparing(Tweet::getCreatedAt).reversed())
            .limit(limit)
            .collect(Collectors.toList());

        return allTweets;
    }

    private List<Tweet> getCachedTweets(List<Long> userIds, int limit) {
        List<Tweet> tweets = new ArrayList<>();
        for (Long userId : userIds) {
            String key = "feed:" + userId;
            List<Tweet> userTweets = (List<Tweet>) redisTemplate
                .opsForList().range(key, 0, limit - 1);
            if (userTweets != null) {
                tweets.addAll(userTweets);
            }
        }
        return tweets;
    }
}

// Kafka consumer for processing tweet events
@Component
public class TweetEventConsumer {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Autowired
    private FollowRepository followRepository;

    @KafkaListener(topics = "tweet-events")
    public void consume(TweetEvent event) {
        Tweet tweet = tweetRepository.findById(event.getTweetId()).orElse(null);
        if (tweet == null) return;

        // Get followers
        List<Long> followers = followRepository.findFollowerIds(event.getUserId());

        // Push to each follower's feed cache
        for (Long follower : followers) {
            String key = "feed:" + follower;
            redisTemplate.opsForList().leftPush(key, tweet);
            redisTemplate.opsForList().trim(key, 0, 999); // Keep last 1000
        }
    }
}
```

---

## 📝 BÀI TẬP THỰC HÀNH

Xem `03-exercises.md` để làm bài tập!

---

## 🔗 TÀI LIỆU THAM KHẢO

1. [system-design-primer](https://github.com/donnemartin/system-design-primer)
2. [System Design Interview Book](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMFM3NF)
3. [High Scalability Blog](http://highscalability.com/)
