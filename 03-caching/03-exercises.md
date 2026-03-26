# Phase 3: Caching với Redis - Bài Tập Thực Hành

> **Thời gian:** 4-6 giờ

---

## 📝 BÀI TẬP 1: INSTALL REDIS & BASIC OPERATIONS (30 phút)

### Đề bài

**Step 1: Cài đặt Redis**

```bash
# Docker (recommended)
docker run -d -p 6379:6379 --name redis-redis redis:latest

# Hoặc install trực tiếp
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server

# macOS
brew install redis
brew services start redis
```

**Step 2: Kết nối và test**

```bash
# Connect to Redis CLI
redis-cli

# Test commands
PING  # Should return PONG
SET test "Hello Redis"
GET test
DEL test

# Check info
INFO

# Monitor commands (real-time)
MONITOR
```

**Step 3: Add dependency vào project**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

```yaml
# application.yml
spring:
  data:
    redis:
      host: localhost
      port: 6379
      # password: your-password  # If configured
```

**Step 4: Tạo config class**

```java
@Configuration
@EnableCaching
public class RedisConfig {

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.setHashKeySerializer(new StringRedisSerializer());
        template.setHashValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.afterPropertiesSet();
        return template;
    }
}
```

### Cách submit

```markdown
## Redis Installation Report

### Installation method:
- [ ] Docker
- [ ] Native install

### Test results:
```bash
$ redis-cli
127.0.0.1:6379> PING
PONG
127.0.0.1:6379> SET test "Hello"
OK
127.0.0.1:6379> GET test
"Hello"
```

### Spring Boot connection test:
- [ ] Application starts without errors
- [ ] Can inject RedisTemplate
```

---

## 📝 BÀI TẬP 2: IMPLEMENT CACHE-Aside PATTERN (2 giờ)

### Đề bài

Implement caching cho **Blog Platform** với các entities: Post, Author, Comment

**Yêu cầu:**

1. **PostService** với các methods:
   - `getPostById(Long id)` - Cache-Aside pattern
   - `getAllPosts()` - Cache list posts
   - `createPost(Post post)` - Invalidate cache sau khi create
   - `updatePost(Long id, PostUpdateDTO dto)` - Invalidate cache
   - `deletePost(Long id)` - Invalidate cache

2. **AuthorService** với các methods:
   - `getAuthorById(Long id)` - Cache author với posts
   - `getAuthorPosts(Long authorId)` - Cache list posts by author

3. **CommentService**:
   - `getCommentsForPost(Long postId)` - Cache comments
   - `addComment(Long postId, Comment comment)` - Invalidate cache

### Code template

```java
@Service
@RequiredArgsConstructor
public class PostService {

    private final PostRepository postRepository;
    private final RedisTemplate<String, Object> redisTemplate;

    private static final String POST_KEY_PREFIX = "post:";
    private static final String ALL_POSTS_KEY = "posts:all";

    public Post getPostById(Long id) {
        // TODO: Implement Cache-Aside
    }

    public List<Post> getAllPosts() {
        // TODO: Cache list posts
    }

    @Transactional
    public Post createPost(Post post) {
        Post saved = postRepository.save(post);
        // TODO: Invalidate cache
        return saved;
    }

    // Implement remaining methods...
}
```

### Cách submit

```markdown
## Cache-Aside Implementation

### PostService

#### getPostById - Cache hit scenario:
```
1. Check cache: post:123
2. Found → return cached
3. Time: 2ms (vs 50ms from DB)
```

#### getPostById - Cache miss scenario:
```
1. Check cache: post:123
2. Not found → query DB
3. Store in cache: post:123 with 30min TTL
4. Time: 52ms total
```

### Invalidation strategy:
- createPost → Delete posts:all cache
- updatePost → Delete post:{id} and posts:all
- deletePost → Delete post:{id} and posts:all

### Code submitted:
- Link GitHub: ...
```

---

## 📝 BÀI TẬP 3: REDIS DATA STRUCTURES (2 giờ)

### Đề bài

Implement các features sau sử dụng Redis data structures:

**1. Shopping Cart (Hash)**
```java
public interface ShoppingCartService {
    void addToCart(Long userId, Long productId, int quantity);
    void removeFromCart(Long userId, Long productId);
    Map<Long, Integer> getCart(Long userId);
    void clearCart(Long userId);
    int getCartSize(Long userId);
}
```

**2. Recent Views (List - LRU cache)**
```java
public interface RecentViewsService {
    void viewProduct(Long userId, Long productId);
    List<Long> getRecentViews(Long userId, int limit);
}
// Yêu cầu: Lưu 10 products xem gần nhất, remove oldest khi vượt quá
```

**3. Product Tags (Set)**
```java
public interface ProductTagService {
    void addTag(Long productId, String tag);
    void removeTag(Long productId, String tag);
    Set<String> getTags(Long productId);
    Set<Long> getProductsWithTag(String tag);
}
```

**4. Leaderboard (Sorted Set)**
```java
public interface LeaderboardService {
    void addScore(Long userId, double score);
    void incrementScore(Long userId, double increment);
    List<LeaderboardEntry> getTopUsers(int limit);
    Long getUserRank(Long userId);
    Double getUserScore(Long userId);
}
```

### Cách submit

```markdown
## Redis Data Structures Implementation

### 1. Shopping Cart (Hash)
```java
// Implementation code
```

Test:
```bash
# Redis CLI
HGETALL cart:1
```

### 2. Recent Views (List)
Implementation với LRANGE và LTRIM

### 3. Product Tags (Set)
Implementation với SADD, SMEMBERS, SINTER

### 4. Leaderboard (Sorted Set)
Implementation với ZADD, ZREVRANGE, ZREVRANK

### Test Results:
- [ ] Shopping Cart: Add, remove, get cart working
- [ ] Recent Views: LRU eviction working
- [ ] Tags: Set operations working
- [ ] Leaderboard: Ranking correct
```

---

## 📝 BÀI TẬP 4: DISTRIBUTED LOCK (1 giờ)

### Đề bài

Implement distributed lock cho **Flash Sale** scenario:

**Scenario:**
- 1000 users try to buy iPhone 15 cùng lúc
- Chỉ có 100 phones trong kho
- Prevent overselling

**Yêu cầu:**

```java
@Service
public class FlashSaleService {

    // Implement với Redisson distributed lock
    @Transactional
    public OrderResult purchaseFlashSale(Long userId, Long productId) {
        // TODO:
        // 1. Acquire distributed lock
        // 2. Check stock
        // 3. If stock > 0: decrement, create order
        // 4. If stock = 0: return sold out
        // 5. Release lock
    }
}
```

### Cách submit

```markdown
## Distributed Lock Implementation

### Implementation approach:
- Used Redisson RLock
- Lock key: "flashsale:product:{id}"
- Wait time: 5 seconds
- Lease time: 30 seconds

### Test results:

Simulated 100 concurrent requests for 10 items:
- Orders created: 10 ✅
- Stock remaining: 0 ✅
- Oversold: 0 ✅

### Code:
- GitHub link: ...
```

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 3

- [ ] Cài đặt Redis thành công
- [ ] Implement Cache-Aside pattern
- [ ] Sử dụng được Hash cho Shopping Cart
- [ ] Sử dụng được List cho Recent Views
- [ ] Sử dụng được Set cho Tags
- [ ] Sử dụng được Sorted Set cho Leaderboard
- [ ] Implement distributed lock

---

## 🔜 TIẾP THEO

Submit xong, tôi sẽ review và unlock Phase 4: Microservices!
