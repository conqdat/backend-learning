# Phase 3: Caching với Redis - Ví Dụ Thực Tế

---

## 📁 BÀI 1: CACHE-Aside PATTERN DEMO

### Ví dụ 1.1: Product Service với Cache-Aside

```java
@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository repository;
    private final RedisTemplate<String, Object> redisTemplate;

    private static final String PRODUCT_KEY_PREFIX = "product:";
    private static final long CACHE_TTL_MINUTES = 30;

    public Product getProductById(Long id) {
        String cacheKey = PRODUCT_KEY_PREFIX + id;

        // Step 1: Try to get from cache
        Product cachedProduct = (Product) redisTemplate.opsForValue().get(cacheKey);
        if (cachedProduct != null) {
            log.info("Cache hit for product id={}", id);
            return cachedProduct;
        }

        // Step 2: Cache miss - load from database
        log.info("Cache miss for product id={}", id);
        Product product = repository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));

        // Step 3: Store in cache with TTL
        redisTemplate.opsForValue().set(
            cacheKey,
            product,
            CACHE_TTL_MINUTES,
            TimeUnit.MINUTES
        );

        return product;
    }

    @Transactional
    public Product updateProduct(Long id, ProductUpdateDTO dto) {
        Product product = repository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));

        product.setName(dto.getName());
        product.setPrice(dto.getPrice());
        product.setDescription(dto.getDescription());

        Product updated = repository.save(product);

        // Invalidate cache
        String cacheKey = PRODUCT_KEY_PREFIX + id;
        redisTemplate.delete(cacheKey);
        log.info("Invalidated cache for product id={}", id);

        return updated;
    }
}
```

---

## 📁 BÀI 2: REDIS DATA STRUCTURES DEMO

### Ví dụ 2.1: String - Cache simple values

```java
@Service
@RequiredArgsConstructor
public class PageViewService {

    private final RedisTemplate<String, Object> redisTemplate;

    private static final String VIEWS_KEY = "page:views:";

    public void incrementPageView(Long productId) {
        String key = VIEWS_KEY + productId;
        redisTemplate.opsForValue().increment(key);
        redisTemplate.expire(key, 7, TimeUnit.DAYS);
    }

    public Long getPageViews(Long productId) {
        String key = VIEWS_KEY + productId;
        String views = (String) redisTemplate.opsForValue().get(key);
        return views != null ? Long.parseLong(views) : 0L;
    }

    public Map<String, Long> getTopViewedProducts(int limit) {
        // Get all view keys
        Set<String> keys = redisTemplate.keys(VIEWS_KEY + "*");
        if (keys == null) return Collections.emptyMap();

        // Get views for each product
        Map<String, Long> viewsMap = new HashMap<>();
        for (String key : keys) {
            String value = (String) redisTemplate.opsForValue().get(key);
            String productId = key.replace(VIEWS_KEY, "");
            viewsMap.put(productId, value != null ? Long.parseLong(value) : 0L);
        }

        // Sort and return top N
        return viewsMap.entrySet().stream()
            .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
            .limit(limit)
            .collect(Collectors.toMap(
                Map.Entry::getKey,
                Map.Entry::getValue,
                (e1, e2) -> e1,
                LinkedHashMap::new
            ));
    }
}
```

---

### Ví dụ 2.2: Hash - Store object fields

```java
@Service
@RequiredArgsConstructor
public class ShoppingCartService {

    private final RedisTemplate<String, Object> redisTemplate;

    private static final String CART_KEY_PREFIX = "cart:";

    public void addToCart(Long userId, Long productId, int quantity) {
        String cartKey = CART_KEY_PREFIX + userId;
        HashOperations<String, Object, Object> hashOps = redisTemplate.opsForHash();

        // Get current quantity
        Integer currentQty = (Integer) hashOps.get(cartKey, productId.toString());
        int newQty = currentQty != null ? currentQty + quantity : quantity;

        hashOps.put(cartKey, productId.toString(), newQty);

        // Set expiry: cart expires after 7 days of inactivity
        redisTemplate.expire(cartKey, 7, TimeUnit.DAYS);
    }

    public Map<Long, Integer> getCart(Long userId) {
        String cartKey = CART_KEY_PREFIX + userId;
        HashOperations<String, Object, Object> hashOps = redisTemplate.opsForHash();
        Map<Object, Object> entries = hashOps.entries(cartKey);

        Map<Long, Integer> cart = new HashMap<>();
        for (Map.Entry<Object, Object> entry : entries.entrySet()) {
            cart.put(Long.parseLong((String) entry.getKey()),
                    (Integer) entry.getValue());
        }
        return cart;
    }

    public void removeFromCart(Long userId, Long productId) {
        String cartKey = CART_KEY_PREFIX + userId;
        redisTemplate.opsForHash().delete(cartKey, productId.toString());
    }

    public void clearCart(Long userId) {
        String cartKey = CART_KEY_PREFIX + userId;
        redisTemplate.delete(cartKey);
    }
}
```

---

### Ví dụ 2.3: Sorted Set - Leaderboard

```java
@Service
@RequiredArgsConstructor
public class LeaderboardService {

    private final RedisTemplate<String, Object> redisTemplate;

    private static final String LEADERBOARD_KEY = "leaderboard:weekly";

    public void addScore(Long userId, double score) {
        ZSetOperations<String, Object> zSetOps = redisTemplate.opsForZSet();
        zSetOps.add(LEADERBOARD_KEY, userId.toString(), score);
    }

    public void incrementScore(Long userId, double increment) {
        ZSetOperations<String, Object> zSetOps = redisTemplate.opsForZSet();
        zSetOps.incrementScore(LEADERBOARD_KEY, userId.toString(), increment);
    }

    public List<LeaderboardEntry> getTopPlayers(int limit) {
        ZSetOperations<String, Object> zSetOps = redisTemplate.opsForZSet();
        Set<Object> topPlayers = zSetOps.reverseRange(LEADERBOARD_KEY, 0, limit - 1);

        if (topPlayers == null) return Collections.emptyList();

        List<LeaderboardEntry> result = new ArrayList<>();
        long rank = 1;
        for (Object player : topPlayers) {
            double score = zSetOps.score(LEADERBOARD_KEY, player.toString());
            result.add(new LeaderboardEntry(
                rank++,
                Long.parseLong((String) player),
                score
            ));
        }
        return result;
    }

    public Long getPlayerRank(Long userId) {
        ZSetOperations<String, Object> zSetOps = redisTemplate.opsForZSet();
        Long rank = zSetOps.reverseRank(LEADERBOARD_KEY, userId.toString());
        return rank != null ? rank + 1 : null;  // Convert 0-indexed to 1-indexed
    }

    public Double getPlayerScore(Long userId) {
        ZSetOperations<String, Object> zSetOps = redisTemplate.opsForZSet();
        return zSetOps.score(LEADERBOARD_KEY, userId.toString());
    }

    @Data
    @AllArgsConstructor
    public static class LeaderboardEntry {
        private Long rank;
        private Long userId;
        private Double score;
    }
}
```

---

## 📁 BÀI 3: DISTRIBUTED LOCK VỚI REDIS

### Ví dụ 3.1: Prevent duplicate orders

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final RedisTemplate<String, Object> redisTemplate;
    private final OrderRepository orderRepository;

    private static final String ORDER_LOCK_PREFIX = "order:lock:";

    @Transactional
    public Order createOrder(Long userId, OrderRequest request) {
        String lockKey = ORDER_LOCK_PREFIX + userId;

        // Try to acquire lock with 5 second timeout
        Boolean acquired = redisTemplate.opsForValue()
            .setIfAbsent(lockKey, "locked", 5, TimeUnit.SECONDS);

        if (Boolean.FALSE.equals(acquired)) {
            throw new OrderProcessingException("Order already being processed for user " + userId);
        }

        try {
            // Check for duplicate order within 1 minute
            String recentOrderKey = "order:recent:" + userId;
            Object recentOrder = redisTemplate.opsForValue().get(recentOrderKey);
            if (recentOrder != null) {
                throw new DuplicateOrderException("Duplicate order detected");
            }

            // Create order
            Order order = new Order();
            order.setUserId(userId);
            order.setItems(request.getItems());
            order.setTotalAmount(calculateTotal(request.getItems()));

            Order savedOrder = orderRepository.save(order);

            // Mark order as processed (prevent duplicates for 1 minute)
            redisTemplate.opsForValue().set(recentOrderKey, savedOrder.getId(), 1, TimeUnit.MINUTES);

            return savedOrder;

        } finally {
            // Release lock
            redisTemplate.delete(lockKey);
        }
    }
}
```

---

### Ví dụ 3.2: Redisson Distributed Lock (production-ready)

```xml
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson-spring-boot-starter</artifactId>
    <version>3.23.0</version>
</dependency>
```

```java
@Configuration
public class RedissonConfig {

    @Bean
    public RedissonClient redissonClient() {
        Config config = new Config();
        config.useSingleServer()
            .setAddress("redis://localhost:6379");
        return Redisson.create(config);
    }
}
```

```java
@Service
@RequiredArgsConstructor
public class InventoryService {

    private final RedissonClient redissonClient;
    private final ProductRepository repository;

    @Transactional
    public boolean reserveStock(Long productId, int quantity) {
        RLock lock = redissonClient.getLock("inventory:lock:" + productId);

        // Try to acquire lock with 10 second wait time, 30 second lease time
        try {
            boolean locked = lock.tryLock(10, 30, TimeUnit.SECONDS);
            if (!locked) {
                log.warn("Could not acquire lock for product {}", productId);
                return false;
            }

            try {
                Product product = repository.findById(productId)
                    .orElseThrow(() -> new ProductNotFoundException(productId));

                if (product.getStock() < quantity) {
                    return false;
                }

                product.setStock(product.getStock() - quantity);
                repository.save(product);

                return true;

            } finally {
                if (lock.isHeldByCurrentThread()) {
                    lock.unlock();
                }
            }

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Lock acquisition interrupted", e);
        }
    }
}
```

---

## 📁 BÀI 4: MULTI-LEVEL CACHING DEMO

### Ví dụ 4.1: Caffeine (L1) + Redis (L2)

```java
@Configuration
@EnableCaching
public class MultiLevelCacheConfig {

    @Bean("localCacheManager")
    @Primary
    public CacheManager localCacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager();
        cacheManager.setCaffeine(Caffeine.newBuilder()
            .maximumSize(500)
            .expireAfterWrite(5, TimeUnit.MINUTES)
            .recordStats());
        return cacheManager;
    }

    @Bean("redisCacheManager")
    public CacheManager redisCacheManager(RedisConnectionFactory factory) {
        RedisCacheManager cacheManager = RedisCacheManager.builder(factory)
            .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(30))
                .serializeValuesWith(RedisSerializationContext.SerializationPair
                    .fromSerializer(new GenericJackson2JsonRedisSerializer())))
            .transactionAware()
            .build();
        return cacheManager;
    }
}
```

```java
@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository repository;

    // L1 Cache - Hot data (frequently accessed)
    @Cacheable(value = "hot-products", key = "'top10'", cacheManager = "localCacheManager")
    public List<Product> getTop10Products() {
        log.info("L1 Cache miss - loading from DB");
        return repository.findTop10ByOrderByViewCountDesc();
    }

    // L2 Cache - General product data
    @Cacheable(value = "products", key = "#id", cacheManager = "redisCacheManager")
    public Product getProduct(Long id) {
        log.info("L2 Cache miss - loading from DB");
        return repository.findById(id).orElse(null);
    }

    // Invalidate both caches
    @CacheEvict(value = {"hot-products", "products"}, allEntries = true,
                cacheManager = "localCacheManager")
    @CacheEvict(value = "products", allEntries = true, cacheManager = "redisCacheManager")
    public void clearAllCaches() {
        log.info("Cleared all caches");
    }
}
```

---

## 📁 BÀI 5: CACHE PATTERNS SO SÁNH

### Benchmark code

```java
@Service
@RequiredArgsConstructor
public class CachePatternDemo {

    private final ProductRepository repository;
    private final RedisTemplate<String, Object> redisTemplate;

    // Pattern 1: Cache-Aside
    public Product cacheAside(Long id) {
        String key = "product:" + id;
        Product cached = (Product) redisTemplate.opsForValue().get(key);
        if (cached != null) return cached;

        Product product = repository.findById(id).orElse(null);
        if (product != null) {
            redisTemplate.opsForValue().set(key, product, 30, TimeUnit.MINUTES);
        }
        return product;
    }

    // Pattern 2: Read-Through (Spring Cache abstraction)
    @Cacheable(value = "products", key = "#id")
    public Product readThrough(Long id) {
        return repository.findById(id).orElse(null);
    }

    // Pattern 3: Write-Through
    @CachePut(value = "products", key = "#product.id")
    @Transactional
    public Product writeThrough(Product product) {
        return repository.save(product);
    }
}
```

---

## 📝 BÀI TẬP THỰC HÀNH

Xem `03-exercises.md` để làm bài tập!
