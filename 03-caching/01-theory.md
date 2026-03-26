# Phase 3: Caching với Redis - Lý Thuyết

> **Thời gian:** 2 tuần
> **Mục tiêu:** Master caching strategies, implement Redis cho production

---

## 📚 BÀI 1: TẠI SAO CẦN CACHING?

### 1.1 Bài toán performance

**Scenario:** E-commerce website bán điện thoại

```
Không có cache:
- User xem sản phẩm iPhone 15
- Backend query database: SELECT * FROM products WHERE id = 123
- Database scan index, fetch data
- Return response: 150ms

1000 users xem cùng 1 sản phẩm:
= 1000 queries × 150ms = 150,000ms CPU time
Database bị overload!
```

**Với cache:**
```
User đầu tiên:
- Cache miss → query DB: 150ms
- Lưu vào cache: iPhone 15 = {...}

999 users tiếp theo:
- Cache hit → read từ Redis: 5ms
- Total: 999 × 5ms = ~5,000ms

Performance improvement: 30x! 🚀
```

---

### 1.2 Khi nào nên dùng cache?

**NÊN cache:**
- ✅ Dữ liệu đọc nhiều, viết ít (reference data)
- ✅ Kết quả queries phức tạp
- ✅ API responses cho mobile app
- ✅ Session storage
- ✅ Rate limiting counters

**KHÔNG nên cache:**
- ❌ Dữ liệu real-time (stock prices, bidding)
- ❌ Dữ liệu thay đổi liên tục
- ❌ Dữ liệu cá nhân hóa cao
- ❌ Dữ liệu nhạy cảm (passwords, credit cards)

---

## 📚 BÀI 2: CACHING PATTERNS

### 2.1 Cache-Aside (Lazy Loading)

**Phổ biến nhất - default choice**

```
Application → Check cache → Nếu có: return
              Nếu không: query DB → lưu cache → return
```

```java
@Service
public class ProductService {

    @Autowired
    private ProductRepository repository;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    public Product getProductById(Long id) {
        String key = "product:" + id;

        // 1. Check cache
        Product cached = (Product) redisTemplate.opsForValue().get(key);
        if (cached != null) {
            System.out.println("Cache hit for product " + id);
            return cached;
        }

        // 2. Cache miss - query DB
        System.out.println("Cache miss for product " + id);
        Product product = repository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Product not found"));

        // 3. Store in cache
        redisTemplate.opsForValue().set(key, product, 30, TimeUnit.MINUTES);

        return product;
    }
}
```

**Pros:**
- ✅ Đơn giản, dễ implement
- ✅ Cache chỉ chứa data đã được request
- ✅ Tự động handle cache misses

**Cons:**
- ❌ Latency cao cho request đầu tiên (cache miss)
- ❌ Có thể stale data nếu DB update

---

### 2.2 Write-Through

**Cache và DB update cùng lúc**

```java
@Service
public class ProductService {

    @Autowired
    private ProductRepository repository;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Cacheable(value = "products", key = "#id")
    public Product getProductById(Long id) {
        return repository.findById(id).orElse(null);
    }

    @CachePut(value = "products", key = "#product.id")
    public Product updateProduct(Product product) {
        // Update DB
        Product updated = repository.save(product);
        // Cache tự động update (write-through)
        return updated;
    }
}
```

**Pros:**
- ✅ Data luôn consistent giữa cache và DB
- ✅ Không có stale data

**Cons:**
- ❌ Write latency cao (phải write cả cache và DB)
- ❌ Tốn tài nguyên cho data ít khi đọc

---

### 2.3 Write-Behind (Write-Back)

**Write cache trước, async write DB sau**

```
Application → Write cache → Return immediately
              ↓ (async)
              Write DB sau 5 giây
```

```java
@Service
public class ProductService {

    @Autowired
    private ScheduledExecutorService scheduler;

    private Map<Long, Product> writeBuffer = new ConcurrentHashMap<>();

    public Product updateProduct(Product product) {
        // Write to cache immediately
        writeBuffer.put(product.getId(), product);

        // Schedule async write to DB
        scheduler.schedule(() -> {
            repository.save(product);
            writeBuffer.remove(product.getId());
        }, 5, TimeUnit.SECONDS);

        return product;
    }
}
```

**Pros:**
- ✅ Write latency rất thấp
- ✅ Giảm số lượng DB writes (batching)

**Cons:**
- ❌ Có thể mất data nếu crash trước khi flush
- ❌ Complex implementation

---

### 2.4 Refresh-Ahead

**Chủ động refresh cache trước khi expire**

```java
@Service
public class ProductService {

    @Scheduled(fixedRate = 300000)  // 5 minutes
    public void refreshPopularProducts() {
        List<Long> popularIds = repository.findTop100ViewedIds();

        for (Long id : popularIds) {
            Product product = repository.findById(id).get();
            String key = "product:" + id;
            redisTemplate.opsForValue().set(key, product, 10, TimeUnit.MINUTES);
        }
    }
}
```

**Pros:**
- ✅ Không có cache miss
- ✅ Latency luôn thấp

**Cons:**
- ❌ Tốn tài nguyên cho data có thể không được request
- ❌ Complex scheduling

---

## 📚 BÀI 3: REDIS DATA STRUCTURES

### 3.1 String (phổ biến nhất)

```bash
# Set/Get
SET product:123 "{\"id\":123,\"name\":\"iPhone 15\",\"price\":999}"
GET product:123

# Set with expiry
SET product:123 "..." EX 1800  # Expire sau 30 phút

# Increment counter
INCR page:views:123
INCRBY page:views:123 10
```

```java
// Spring Data Redis
redisTemplate.opsForValue().set("product:123", product);
Product p = (Product) redisTemplate.opsForValue().get("product:123");

// With expiry
redisTemplate.opsForValue().set("product:123", product, 30, TimeUnit.MINUTES);
```

---

### 3.2 Hash (cho objects)

```bash
# Store object fields
HSET product:123 id 123
HSET product:123 name "iPhone 15"
HSET product:123 price 999

# Get all fields
HGETALL product:123

# Get specific field
HGET product:123 name
```

```java
HashOperations<String, Object, Object> hashOps = redisTemplate.opsForHash();

// Set
hashOps.put("product:123", "name", "iPhone 15");
hashOps.put("product:123", "price", 999);

// Get
String name = (String) hashOps.get("product:123", "name");

// Get all
Map<Object, Object> all = hashOps.entries("product:123");
```

---

### 3.3 List (cho queue)

```bash
# Push to list (queue)
LPUSH orders:pending "{order:1}"
LPUSH orders:pending "{order:2}"

# Pop from list
RPOP orders:pending

# Range
LRANGE orders:pending 0 -1  # All items
```

```java
ListOperations<String, Object> listOps = redisTemplate.opsForList();

// Push
listOps.leftPush("orders:pending", order1);
listOps.leftPushAll("orders:pending", orders);

// Pop
Object order = listOps.rightPop("orders:pending");

// Range
List<Object> all = listOps.range("orders:pending", 0, -1);
```

---

### 3.4 Set (cho unique items)

```bash
# Add to set
SADD users:online user1
SADD users:online user2
SADD users:online user1  # Duplicate - ignored

# Check membership
SISMEMBER users:online user1  # true

# Get all members
SMEMBERS users:online
```

```java
SetOperations<String, Object> setOps = redisTemplate.opsForSet();

// Add
setOps.add("users:online", "user1");
setOps.add("users:online", "user2");

// Check
Boolean isOnline = setOps.isMember("users:online", "user1");

// Get all
Set<Object> onlineUsers = setOps.members("users:online");
```

---

### 3.5 Sorted Set (cho leaderboard)

```bash
# Add with score
ZADD leaderboard 1000 "player1"
ZADD leaderboard 850 "player2"
ZADD leaderboard 1200 "player3"

# Get top N (by score)
ZREVRANGE leaderboard 0 9  # Top 10

# Get rank
ZREVRANK leaderboard "player1"
```

```java
ZSetOperations<String, Object> zSetOps = redisTemplate.opsForZSet();

// Add
zSetOps.add("leaderboard", "player1", 1000);
zSetOps.add("leaderboard", "player2", 850);

// Top 10
Set<Object> top10 = zSetOps.reverseRange("leaderboard", 0, 9);

// Get rank
Long rank = zSetOps.reverseRank("leaderboard", "player1");
```

---

## 📚 BÀI 4: CACHE INVALIDATION STRATEGIES

### 4.1 Time-based (TTL)

**Đơn giản nhất - set expiry time**

```java
// Tự động expire sau 30 phút
redisTemplate.opsForValue().set("product:123", product, 30, TimeUnit.MINUTES);
```

**Khi nào dùng:**
- ✅ Data không cần real-time
- ✅ Data có thể stale trong thời gian ngắn
- ✅ Muốn đơn giản, không muốn manage invalidation

---

### 4.2 Event-based

**Invalidate khi data thay đổi**

```java
@Service
public class ProductService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Autowired
    private ProductRepository repository;

    @CacheEvict(value = "products", key = "#id")
    @Transactional
    public void deleteProduct(Long id) {
        repository.deleteById(id);
        // Cache tự động clear
    }

    @CacheEvict(value = "products", key = "#product.id")
    @Transactional
    public Product updateProduct(Product product) {
        Product updated = repository.save(product);
        // Cache clear, next read sẽ load từ DB
        return updated;
    }
}
```

---

### 4.3 Pattern-based invalidation

**Xóa nhiều keys cùng pattern**

```java
public void invalidateProductCache(Long productId) {
    // Xóa cache product
    redisTemplate.delete("product:" + productId);

    // Xóa cache list products
    Set<String> keys = redisTemplate.keys("products:*");
    if (keys != null) {
        redisTemplate.delete(keys);
    }
}
```

**⚠️ Lưu ý:** `keys()` command block Redis, không dùng trong production!

**Alternative:** Dùng SCAN thay vì KEYS

```java
public void invalidateProductCache() {
    Cursor<byte[]> cursor = redisTemplate.execute(
        (RedisCallback<Cursor<byte[]>>) connection ->
            connection.scan(new ScanOptions.ScanOptionsBuilder().pattern("products:*").count(100).build())
    );

    List<String> keysToDelete = new ArrayList<>();
    while (cursor.hasNext()) {
        keysToDelete.add(new String(cursor.next()));
    }

    if (!keysToDelete.isEmpty()) {
        redisTemplate.delete(keysToDelete);
    }
}
```

---

### 4.4 Cache-Aside với invalidation

**Best practice cho most scenarios:**

```java
@Service
public class ProductService {

    @Autowired
    private ProductRepository repository;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    // READ - Cache-Aside
    public Product getProduct(Long id) {
        String key = "product:" + id;
        Product cached = (Product) redisTemplate.opsForValue().get(key);

        if (cached != null) {
            return cached;
        }

        Product product = repository.findById(id).orElse(null);
        if (product != null) {
            redisTemplate.opsForValue().set(key, product, 30, TimeUnit.MINUTES);
        }
        return product;
    }

    // UPDATE - Invalidate cache
    @Transactional
    public Product updateProduct(Long id, ProductUpdateDTO dto) {
        Product product = repository.findById(id).orElse(null);
        if (product == null) return null;

        // Update fields
        product.setName(dto.getName());
        product.setPrice(dto.getPrice());

        Product updated = repository.save(product);

        // Invalidate cache
        redisTemplate.delete("product:" + id);

        return updated;
    }

    // DELETE - Invalidate cache
    @Transactional
    public void deleteProduct(Long id) {
        repository.deleteById(id);
        redisTemplate.delete("product:" + id);
    }
}
```

---

## 📚 BÀI 5: MULTI-LEVEL CACHING

### 5.1 3-Level Cache Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    L1: In-Memory (Caffeine)                 │
│   - Fastest (nanoseconds)                                   │
│   - Per-instance (mỗi server có cache riêng)                │
│   - TTL: 1-5 phút                                           │
│   - Size limit: 1000 entries                                │
├─────────────────────────────────────────────────────────────┤
│                    L2: Redis (Distributed)                  │
│   - Fast (microseconds)                                     │
│   - Shared across all servers                               │
│   - TTL: 10-30 phút                                         │
│   - Size limit: 100,000 entries                             │
├─────────────────────────────────────────────────────────────┤
│                    L3: Database (PostgreSQL)                │
│   - Slowest (milliseconds)                                  │
│   - Persistent storage                                      │
│   - No TTL                                                  │
│   - Unlimited                                               │
└─────────────────────────────────────────────────────────────┘
```

---

### 5.2 Implement với Spring Cache

```xml
<dependencies>
    <!-- L1: Caffeine -->
    <dependency>
        <groupId>com.github.ben-manes.caffeine</groupId>
        <artifactId>caffeine</artifactId>
    </dependency>

    <!-- L2: Redis -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis</artifactId>
    </dependency>

    <!-- Spring Cache -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-cache</artifactId>
    </dependency>
</dependencies>
```

```yaml
# application.yml
spring:
  cache:
    type: caffeine
    cache-names: local-cache
    caffeine:
      spec: maximumSize=1000,expireAfterWrite=5m
  data:
    redis:
      host: localhost
      port: 6379
```

```java
@Configuration
@EnableCaching
public class CacheConfig {

    // L1 Cache: Caffeine
    @Bean
    @Primary
    public CacheManager localCacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager();
        cacheManager.setCaffeine(Caffeine.newBuilder()
            .maximumSize(1000)
            .expireAfterWrite(5, TimeUnit.MINUTES));
        return cacheManager;
    }

    // L2 Cache: Redis
    @Bean
    public CacheManager redisCacheManager(RedisConnectionFactory factory) {
        RedisCacheManager cacheManager = RedisCacheManager.builder(factory)
            .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(30))
                .serializeValuesWith(
                    RedisSerializationContext.SerializationPair
                        .fromSerializer(new GenericJackson2JsonRedisSerializer())))
            .build();
        return cacheManager;
    }
}
```

```java
@Service
public class ProductService {

    @Autowired
    private ProductRepository repository;

    // L1 Cache - cho data access thường xuyên
    @Cacheable(value = "local-cache", key = "'hot-products'")
    public List<Product> getHotProducts() {
        return repository.findTop10ByOrderByViewCountDesc();
    }

    // L2 Cache - cho general data
    @Cacheable(value = "products", key = "#id", cacheManager = "redisCacheManager")
    public Product getProduct(Long id) {
        return repository.findById(id).orElse(null);
    }

    // Invalidate cả 2 levels
    @CacheEvict(value = {"local-cache", "products"}, allEntries = true)
    public void clearAllCaches() {
        // Clear cả L1 và L2
    }
}
```

---

## 📝 TÓM TẮT PHASE 3

Sau phase này, bạn cần nắm được:

1. ✅ Khi nào nên/không nên dùng cache
2. ✅ Cache-Aside, Write-Through, Write-Behind patterns
3. ✅ Redis data structures: String, Hash, List, Set, Sorted Set
4. ✅ Cache invalidation strategies
5. ✅ Multi-level caching với Caffeine + Redis

---

## 🔜 TIẾP THEO

Đọc `02-examples.md` để xem code mẫu thực tế!
