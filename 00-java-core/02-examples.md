# Phase 0: Java Core Mastery - Ví Dụ Thực Tế

---

## 📁 BÀI 1: HASHMAP INTERNALS DEMO

### Ví dụ 1.1: Custom Object làm Key trong HashMap

```java
// ❌ WRONG: Không override hashCode() và equals()
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

Map<Person, String> map = new HashMap<>();
Person p1 = new Person("John", 30);
Person p2 = new Person("John", 30);  // Same data

map.put(p1, "Value1");
System.out.println(map.get(p2));  // ❌ null! (different object references)

// ✅ CORRECT: Override hashCode() và equals()
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && Objects.equals(name, person.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}

// Bây giờ:
map.put(p1, "Value1");
System.out.println(map.get(p2));  // ✅ "Value1"
```

---

### Ví dụ 1.2: HashMap Collision Demo

```java
public class HashMapCollisionDemo {

    // Custom class với hashCode() luôn trả về cùng value
    static class BadKey {
        private int value;

        public BadKey(int value) {
            this.value = value;
        }

        @Override
        public int hashCode() {
            return 1;  // ❌ Tất cả keys có cùng hash!
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof BadKey)) return false;
            BadKey other = (BadKey) o;
            return this.value == other.value;
        }
    }

    public static void main(String[] args) {
        Map<BadKey, String> map = new HashMap<>();

        // Thêm 100 keys
        for (int i = 0; i < 100; i++) {
            map.put(new BadKey(i), "Value" + i);
        }

        // Performance test
        long start = System.nanoTime();
        for (int i = 0; i < 100; i++) {
            map.get(new BadKey(i));
        }
        long end = System.nanoTime();

        System.out.println("Time: " + (end - start) / 1_000_000 + "ms");
        // Với collision: O(n) per get → 100 gets = O(n²)
        // Không collision: O(1) per get → 100 gets = O(n)
    }
}
```

---

## 📁 BÀI 2: CONCURRENCY DEMOS

### Ví dụ 2.1: Race Condition với volatile

```java
// ❌ WRONG: volatile không làm atomic
public class VolatileNotAtomic {
    private volatile int count = 0;

    public void increment() {
        count++;  // NOT atomic! Read-modify-write
    }

    public static void main(String[] args) throws InterruptedException {
        VolatileNotAtomic demo = new VolatileNotAtomic();
        ExecutorService executor = Executors.newFixedThreadPool(10);

        // 10 threads, mỗi thread increment 1000 lần
        List<CompletableFuture> futures = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            futures.add(CompletableFuture.runAsync(() -> {
                for (int j = 0; j < 1000; j++) {
                    demo.increment();
                }
            }, executor));
        }

        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
        System.out.println("Count: " + demo.count);
        // Expected: 10000
        // Actual: ??? (thường < 10000 do race condition)

        executor.shutdown();
    }
}

// ✅ CORRECT: AtomicInteger
public class AtomicCorrect {
    private AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        count.incrementAndGet();  // Atomic!
    }
}
```

---

### Ví dụ 2.2: synchronized vs ReentrantLock

```java
public class LockComparison {

    // synchronized
    static class SynchronizedCounter {
        private int count = 0;

        public synchronized void increment() {
            count++;
        }

        public synchronized int getCount() {
            return count;
        }
    }

    // ReentrantLock
    static class ReentrantLockCounter {
        private int count = 0;
        private final ReentrantLock lock = new ReentrantLock();

        public void increment() {
            lock.lock();
            try {
                count++;
            } finally {
                lock.unlock();
            }
        }

        public int getCount() {
            lock.lock();
            try {
                return count;
            } finally {
                lock.unlock();
            }
        }

        // Try lock với timeout
        public boolean tryIncrement(long timeout, TimeUnit unit) {
            try {
                if (lock.tryLock(timeout, unit)) {
                    try {
                        count++;
                        return true;
                    } finally {
                        lock.unlock();
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return false;
        }
    }

    public static void main(String[] args) {
        ReentrantLockCounter counter = new ReentrantLockCounter();

        // Fair lock (FIFO order)
        ReentrantLock fairLock = new ReentrantLock(true);

        // Lock với condition
        ReentrantLock lock = new ReentrantLock();
        Condition condition = lock.newCondition();

        // Producer-Consumer với condition
        // Producer
        lock.lock();
        try {
            while (!dataReady) {
                condition.await();  // Wait for data
            }
            // Process data
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            lock.unlock();
        }

        // Consumer
        lock.lock();
        try {
            dataReady = true;
            condition.signalAll();  // Notify waiting threads
        } finally {
            lock.unlock();
        }
    }
}
```

---

### Ví dụ 2.3: Thread Pool Best Practices

```java
public class ThreadPoolBestPractices {

    // ❌ WRONG: Using Executors.newFixedThreadPool()
    // - Unbounded queue → OutOfMemoryError
    // - No control over rejection policy
    ExecutorService badPool = Executors.newFixedThreadPool(10);

    // ✅ CORRECT: Custom ThreadPoolExecutor
    ExecutorService goodPool = new ThreadPoolExecutor(
        5,                          // corePoolSize
        20,                         // maxPoolSize
        60L,                        // keepAliveTime
        TimeUnit.SECONDS,
        new ArrayBlockingQueue<>(1000),  // bounded queue
        new ThreadPoolExecutor.CallerRunsPolicy()  // backpressure
    );

    // ✅ Monitoring thread pool
    public void monitorPool(ThreadPoolExecutor executor) {
        ScheduledExecutorService monitor = Executors.newSingleThreadScheduledExecutor();

        monitor.scheduleAtFixedRate(() -> {
            System.out.println("=== Pool Status ===");
            System.out.println("Active threads: " + executor.getActiveCount());
            System.out.println("Pool size: " + executor.getPoolSize());
            System.out.println("Queue size: " + executor.getQueue().size());
            System.out.println("Completed tasks: " + executor.getCompletedTaskCount());
            System.out.println("Largest pool size: " + executor.getLargestPoolSize());
        }, 0, 10, TimeUnit.SECONDS);
    }

    // ✅ Graceful shutdown
    public void shutdownPool(ExecutorService executor, long timeout, TimeUnit unit) {
        executor.shutdown();  // Stop accepting new tasks

        try {
            if (!executor.awaitTermination(timeout, unit)) {
                executor.shutdownNow();  // Force shutdown

                if (!executor.awaitTermination(timeout, unit)) {
                    System.err.println("Pool did not terminate!");
                }
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

---

### Ví dụ 2.4: CompletableFuture trong thực tế

```java
@Service
public class OrderService {

    @Autowired
    private ProductService productService;

    @Autowired
    private UserService userService;

    @Autowired
    private PaymentService paymentService;

    /**
     * Async orchestration cho order placement
     */
    public CompletableFuture<OrderResult> placeOrder(OrderRequest request) {
        // Parallel calls
        CompletableFuture<Product> productFuture = CompletableFuture
            .supplyAsync(() -> productService.getProduct(request.getProductId()))
            .exceptionally(ex -> {
                log.error("Failed to get product", ex);
                return null;
            });

        CompletableFuture<User> userFuture = CompletableFuture
            .supplyAsync(() -> userService.getUser(request.getUserId()))
            .exceptionally(ex -> {
                log.error("Failed to get user", ex);
                return null;
            });

        // Combine results
        return productFuture.thenCombine(userFuture, (product, user) -> {
            if (product == null || user == null) {
                throw new OrderException("Product or user not found");
            }

            if (product.getStock() < request.getQuantity()) {
                throw new OutOfStockException("Not enough stock");
            }

            return new OrderContext(product, user, request);
        })
        .thenCompose(ctx -> {
            // Sequential: Payment after validation
            return paymentService.charge(user, product, request.getQuantity())
                .thenApply(payment -> {
                    if (!payment.isSuccess()) {
                        throw new PaymentFailedException("Payment declined");
                    }
                    return ctx;
                });
        })
        .thenApply(ctx -> {
            // Create order
            Order order = new Order();
            order.setProduct(ctx.product);
            order.setUser(ctx.user);
            order.setQuantity(ctx.request.getQuantity());
            order.setStatus("COMPLETED");

            return OrderResult.success(order);
        })
        .exceptionally(ex -> {
            log.error("Order failed", ex);
            return OrderResult.failure(ex.getMessage());
        });
    }

    @Data
    @AllArgsConstructor
    private static class OrderContext {
        Product product;
        User user;
        OrderRequest request;
    }
}
```

---

## 📁 BÀI 3: STREAM API & OPTIONAL DEMOS

### Ví dụ 3.1: Stream Best Practices

```java
public class StreamBestPractices {

    // ❌ WRONG: Stream cho simple loop
    List<String> names = Arrays.asList("John", "Jane", "Bob");
    for (String name : names) {
        System.out.println(name);  // Simple loop tốt hơn
    }

    // ✅ GOOD: Stream cho complex pipeline
    List<String> result = names.stream()
        .filter(n -> n.startsWith("J"))
        .map(String::toUpperCase)
        .sorted()
        .collect(Collectors.toList());

    // ❌ WRONG: Parallel stream cho small data
    List<String> smallList = IntStream.range(0, 100)
        .mapToObj(i -> "Item" + i)
        .collect(Collectors.toList());

    smallList.parallelStream()  // ❌ Overhead > benefit
        .map(this::process)
        .collect(Collectors.toList());

    // ✅ GOOD: Parallel stream cho large data
    List<String> largeList = IntStream.range(0, 1_000_000)
        .mapToObj(i -> "Item" + i)
        .collect(Collectors.toList());

    largeList.parallelStream()  // ✅ Worth it
        .map(this::process)
        .collect(Collectors.toList());

    // ✅ GOOD: Collectors utilities
    Map<String, List<User>> usersByCity = users.stream()
        .collect(Collectors.groupingBy(User::getCity));

    Map<String, Double> avgSalaryByCity = users.stream()
        .collect(Collectors.groupingBy(
            User::getCity,
            Collectors.averagingDouble(User::getSalary)
        ));

    String namesJoined = users.stream()
        .map(User::getName)
        .collect(Collectors.joining(", ", "[", "]"));

    Set<String> uniqueCities = users.stream()
        .map(User::getCity)
        .collect(Collectors.toSet());

    // Custom collector
    Map<Boolean, List<User>> partitioned = users.stream()
        .collect(Collectors.partitioningBy(u -> u.getSalary() > 10000));
}
```

---

### Ví dụ 3.2: Optional Best Practices

```java
public class OptionalBestPractices {

    // ❌ WRONG: Optional.get() without check
    public String getUserName(User user) {
        Optional<String> name = Optional.ofNullable(user.getName());
        return name.get();  // NullPointerException if null!
    }

    // ❌ WRONG: Check isEmpty() then get()
    public String getUserName2(User user) {
        Optional<String> name = Optional.ofNullable(user.getName());
        if (name.isEmpty()) {
            return "Unknown";
        }
        return name.get();
    }

    // ✅ CORRECT: orElse()
    public String getUserName3(User user) {
        return Optional.ofNullable(user.getName())
            .orElse("Unknown");
    }

    // ✅ CORRECT: orElseGet() (lazy evaluation)
    public String getUserName4(User user) {
        return Optional.ofNullable(user.getName())
            .orElseGet(() -> generateDefaultName());  // Only called if null
    }

    // ✅ CORRECT: orElseThrow()
    public String getUserName5(User user) {
        return Optional.ofNullable(user.getName())
            .orElseThrow(() -> new UserNotFoundException(user.getId()));
    }

    // ✅ CORRECT: map() + flatMap()
    public String getUserCity(User user) {
        return Optional.ofNullable(user)
            .map(User::getAddress)      // Optional<Address>
            .flatMap(Address::getCity)  // Optional<String>
            .orElse("Unknown");
    }

    // ✅ CORRECT: ifPresent()
    public void printUserName(User user) {
        Optional.ofNullable(user.getName())
            .ifPresent(System.out::println);
    }

    // ✅ CORRECT: ifPresentOrElse() (Java 9+)
    public void printUserName2(User user) {
        Optional.ofNullable(user.getName())
            .ifPresentOrElse(
                System.out::println,
                () -> System.out.println("Name is null")
            );
    }

    // ✅ CORRECT: filter()
    public Optional<String> getValidEmail(User user) {
        return Optional.ofNullable(user.getEmail())
            .filter(email -> email.contains("@"))
            .filter(email -> email.length() > 5);
    }

    private String generateDefaultName() {
        return "User_" + System.currentTimeMillis();
    }
}
```

---

## 📁 BÀI 4: MEMORY LEAK DEMOS

### Ví dụ 4.1: Common Memory Leaks

```java
public class MemoryLeakDemos {

    // Leak 1: Static collection grows indefinitely
    static class LeakyCache {
        private static Map<String, Object> cache = new HashMap<>();

        public static void put(String key, Object value) {
            cache.put(key, value);  // Never cleaned!
        }

        // ✅ FIX: Use WeakHashMap or bounded cache
        private static Map<String, Object> fixedCache = new WeakHashMap<>();

        // Or use Caffeine/Guava cache
        private static Cache<String, Object> caffeineCache = Caffeine.newBuilder()
            .maximumSize(1000)
            .expireAfterWrite(10, TimeUnit.MINUTES)
            .build();
    }

    // Leak 2: Unclosed resources
    public String readFileWrong(String path) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(path));
        String line = reader.readLine();
        // reader.close() missing!
        return line;
    }

    public String readFileCorrect(String path) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            return reader.readLine();
        }
    }

    // Leak 3: Listeners without unregister
    static class EventPublisher {
        private List<EventListener> listeners = new ArrayList<>();

        public void addListener(EventListener listener) {
            listeners.add(listener);
        }

        public void removeListener(EventListener listener) {
            listeners.remove(listener);  // Must call this!
        }

        // ✅ FIX: Use WeakReference
        private List<WeakReference<EventListener>> weakListeners = new ArrayList<>();

        public void addWeakListener(EventListener listener) {
            weakListeners.add(new WeakReference<>(listener));
        }

        public void notifyListeners(String event) {
            weakListeners.removeIf(ref -> {
                EventListener listener = ref.get();
                if (listener == null) {
                    return true;  // GC'd, remove reference
                }
                listener.onEvent(event);
                return false;
            });
        }
    }

    // Leak 4: ThreadLocal without remove()
    static class UserContext {
        private static ThreadLocal<User> currentUser = new ThreadLocal<>();

        public static void set(User user) {
            currentUser.set(user);
        }

        public static User get() {
            return currentUser.get();
        }

        // ❌ Missing: currentUser.remove()
        // Thread pool reuse → old User object stays in memory!

        // ✅ FIX: Always call remove()
        public static void clear() {
            currentUser.remove();
        }
    }

    interface EventListener {
        void onEvent(String event);
    }
}
```

---

## 📝 BÀI TẬP THỰC HÀNH

Xem `03-exercises.md` để làm bài tập!
