# Phase 0: Java Core Mastery - Lý Thuyết

> **Thời gian:** 4 tuần
> **Mục tiêu:** Hiểu sâu Java Core - phân biệt Senior vs Mid-level
> **Quan trọng:** Đây là phần hay bị hỏi nhất khi phỏng vấn Senior!

---

## 📚 BÀI 1: COLLECTIONS FRAMEWORK - PHÂN BIỆT SENIOR VS MID

### 1.1 HashMap - "Con át chủ bài" trong phỏng vấn

**Câu hỏi kinh điển:** *"HashMap hoạt động như thế nào?"*

**Mid-level trả lời:**
```java
Map<String, String> map = new HashMap<>();
map.put("key", "value");
map.get("key");
```

**Senior phải trả lời được:**

```
HashMap = Array (bucket) + LinkedList/Tree (collision resolution)

1. put(key, value):
   - Tính hash = key.hashCode()
   - Tính index = (n-1) & hash  (n = số buckets)
   - Nếu bucket trống → tạo Node mới
   - Nếu bucket có Node → traverse linked list
     - Nếu key tồn tại → update value
     - Nếu không → add vào cuối list
   - Nếu size > threshold → resize (2x)

2. get(key):
   - Tính hash = key.hashCode()
   - Tính index = (n-1) & hash
   - Tìm trong bucket
   - Nếu collision → traverse linked list/tree

3. Collision resolution:
   - < 8 nodes: Linked List
   - >= 8 nodes: Red-Black Tree (Java 8+)
   - < 6 nodes: Convert back to Linked List
```

**Code minh họa:**

```java
// HashMap internal structure (Java 8+)
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;
    final K key;
    V value;
    Node<K,V> next;  // Linked list for collision

    // Constructor, getters...
}

// Red-Black Tree node (khi collision nhiều)
static final class TreeNode<K,V> extends LinkedHashMap.Entry<K,V> {
    TreeNode<K,V> parent;  // red-black tree links
    TreeNode<K,V> left;
    TreeNode<K,V> right;
    TreeNode<K,V> prev;    // used to remove next node
    boolean red;

    // Constructor, methods...
}
```

**Tại sao Java 8 dùng Tree?**
- Linked List: O(n) cho get/put trong worst case
- Red-Black Tree: O(log n) cho get/put
- Performance improvement khi collision cao!

---

### 1.2 HashMap vs ConcurrentHashMap

**Câu hỏi:** *"Sự khác biệt giữa HashMap và ConcurrentHashMap?"*

| Aspect | HashMap | ConcurrentHashMap |
|--------|---------|-------------------|
| Thread-safe | ❌ No | ✅ Yes |
| Null keys/values | ✅ Yes | ❌ No |
| Locking mechanism | N/A | Segment/Bucket locking |
| Performance | Fast (single thread) | Slower but thread-safe |
| Iterator | Fail-fast | Weakly consistent |

**Internal của ConcurrentHashMap (Java 8+):**

```
┌─────────────────────────────────────────────────────────────┐
│              ConcurrentHashMap                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │Bucket 0 │  │Bucket 1 │  │Bucket 2 │  │Bucket 3 │  ...   │
│  ├─────────┤  ├─────────┤  ├─────────┤  ├─────────┤        │
│  │  Node   │  │  Node   │  │  Node   │  │  Node   │        │
│  │  Node   │  │  Node   │  │  Node   │  │  Node   │        │
│  │  Tree   │  │  Tree   │  │  Tree   │  │  Tree   │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│       │            │            │            │              │
│       └────────────┴────────────┴────────────┘              │
│                         │                                    │
│              CAS (Compare-And-Swap) locking                  │
│              - Lock free cho read                            │
│              - CAS + synchronized cho write                  │
└─────────────────────────────────────────────────────────────┘
```

**Code so sánh:**

```java
// ❌ HashMap - NOT thread-safe
Map<String, Integer> hashMap = new HashMap<>();
// Multiple threads → Race condition, infinite loop (Java 7)

// ✅ ConcurrentHashMap - Thread-safe
ConcurrentMap<String, Integer> concurrentMap = new ConcurrentHashMap<>();

// Atomic operations
concurrentMap.putIfAbsent("key", 0);
concurrentMap.compute("key", (k, v) -> v == null ? 1 : v + 1);
concurrentMap.merge("key", 1, Integer::sum);

// Performance: Không lock toàn bộ map
// Mỗi bucket có lock riêng → nhiều threads có thể write cùng lúc
```

---

### 1.3 Fail-Fast vs Fail-Safe Iterators

**Câu hỏi:** *"Sự khác biệt giữa fail-fast và fail-safe iterator?"*

**Fail-Fast:**
```java
List<String> list = new ArrayList<>(Arrays.asList("A", "B", "C"));

for (String item : list) {
    if (item.equals("B")) {
        list.remove(item);  // ❌ ConcurrentModificationException!
    }
}
```

**Tại sao?**
- Iterator lưu `expectedModCount`
- Khi list modify, `modCount` tăng
- Iterator check: `expectedModCount != modCount` → throw exception

**Fail-Safe:**
```java
ConcurrentHashMap<String, String> map = new ConcurrentHashMap<>();
map.put("A", "1");
map.put("B", "2");

for (Map.Entry<String, String> entry : map.entrySet()) {
    map.remove(entry.getKey());  // ✅ No exception!
    // Iterator làm việc trên snapshot copy
}
```

**So sánh:**

| Iterator Type | Collections | Behavior |
|--------------|-------------|----------|
| Fail-Fast | ArrayList, HashMap, HashSet | Throw ConcurrentModificationException |
| Fail-Safe | ConcurrentHashMap, CopyOnWriteArrayList | No exception, làm việc trên snapshot |

---

## 📚 BÀI 2: MULTITHREADING & CONCURRENCY

### 2.1 Thread Lifecycle

```
NEW → RUNNABLE → RUNNING → BLOCKED/WAITING/TIMED_WAITING → TERMINATED

NEW: new Thread() nhưng chưa start()
RUNNABLE: start() đã gọi, chờ CPU time
RUNNING: Đang execute
BLOCKED: Chờ monitor lock (synchronized)
WAITING: Chờ thread khác (wait(), join(), LockSupport.park())
TIMED_WAITING: Chờ có timeout (sleep(), wait(timeout))
TERMINATED: Run xong
```

---

### 2.2 synchronized vs ReentrantLock

**synchronized (Java 5-):**
```java
public synchronized void increment() {
    count++;
}

// Hoặc
public void increment() {
    synchronized(this) {
        count++;
    }
}
```

**ReentrantLock (Java 5+):**
```java
private final ReentrantLock lock = new ReentrantLock();

public void increment() {
    lock.lock();
    try {
        count++;
    } finally {
        lock.unlock();  // PHẢI có finally!
    }
}
```

**So sánh:**

| Feature | synchronized | ReentrantLock |
|---------|-------------|---------------|
| Implementation | JVM keyword | Java class |
| Fair lock | ❌ No | ✅ Yes (constructor param) |
| Try lock | ❌ No | ✅ `tryLock()` |
| Interruptible | ❌ No | ✅ `lockInterruptibly()` |
| Multiple conditions | ❌ No | ✅ `newCondition()` |
| Performance | Improved since Java 6 | Slightly better trong high contention |

---

### 2.3 volatile keyword

**Câu hỏi:** *"volatile là gì? Khi nào dùng?"*

**volatile guarantees:**
1. **Visibility:** Thay đổi của 1 thread visible cho tất cả threads
2. **Ordering:** Prevent instruction reordering
3. **NOT Atomic:** `count++` với volatile vẫn NOT thread-safe!

```java
// ❌ WRONG: volatile không làm atomic
private volatile int count = 0;

public void increment() {
    count++;  // Race condition! (read-modify-write)
}

// ✅ CORRECT: Dùng AtomicInteger
private AtomicInteger count = new AtomicInteger(0);

public void increment() {
    count.incrementAndGet();  // Atomic operation
}

// ✅ CORRECT: Dùng synchronized
private int count = 0;

public synchronized void increment() {
    count++;
}
```

**Khi nào dùng volatile:**
- ✅ Flag status (running, stopped)
- ✅ Single writer, multiple readers
- ✅ Reference assignment (không phải compound operation)

```java
// ✅ Valid use case
private volatile boolean running = true;

public void stop() {
    running = false;  // Simple assignment
}

public void run() {
    while (running) {  // Read từ main memory
        // do work
    }
}
```

---

### 2.4 ExecutorService & Thread Pools

**Câu hỏi:** *"Các loại Thread Pool và khi nào dùng?"*

```java
// 1. Fixed Thread Pool - Số thread cố định
ExecutorService fixedPool = Executors.newFixedThreadPool(10);
// Dùng khi: Biết trước workload, cần giới hạn resource

// 2. Cached Thread Pool - Tạo thread khi cần
ExecutorService cachedPool = Executors.newCachedThreadPool();
// Dùng khi: Nhiều short-lived tasks, workload thay đổi

// 3. Single Thread Executor - 1 thread duy nhất
ExecutorService singleThread = Executors.newSingleThreadExecutor();
// Dùng khi: Tasks cần execute tuần tự

// 4. Scheduled Thread Pool - Chạy theo lịch
ScheduledExecutorService scheduledPool = Executors.newScheduledThreadPool(5);
scheduledPool.scheduleAtFixedRate(task, 0, 1, TimeUnit.MINUTES);
// Dùng khi: Cron jobs, periodic tasks

// 5. Work Queue (Recommended for production)
ExecutorService customPool = new ThreadPoolExecutor(
    5,              // corePoolSize
    20,             // maxPoolSize
    60L,            // keepAliveTime
    TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(1000),  // queue capacity
    new ThreadPoolExecutor.CallerRunsPolicy()  // rejection policy
);
```

**Rejection Policies:**
- `AbortPolicy`: Throw RejectedExecutionException (default)
- `CallerRunsPolicy`: Caller thread execute task
- `DiscardPolicy`: Silent discard
- `DiscardOldestPolicy`: Discard oldest task, retry new

---

### 2.5 CompletableFuture - Async Programming

```java
// Sync (chạy tuần tự)
String result = fetchData()
    .thenApply(this::process)
    .thenApply(this::transform)
    .join();

// Async (chạy song song)
CompletableFuture<String> future1 = CompletableFuture
    .supplyAsync(() -> fetchData(1))
    .thenApply(this::process);

CompletableFuture<String> future2 = CompletableFuture
    .supplyAsync(() -> fetchData(2))
    .thenApply(this::process);

// Wait for all
CompletableFuture.allOf(future1, future2).join();

// Combine results
CompletableFuture<String> combined = future1
    .thenCombine(future2, (r1, r2) -> r1 + r2);

// Exception handling
future.exceptionally(ex -> {
    log.error("Error", ex);
    return "default value";
});
```

---

## 📚 BÀI 3: JAVA 8+ FEATURES

### 3.1 Stream API - Internal Iteration

```java
// ❌ Old way (external iteration)
List<String> result = new ArrayList<>();
for (String s : list) {
    if (s.startsWith("A")) {
        result.add(s.toUpperCase());
    }
}

// ✅ Stream API (internal iteration)
List<String> result = list.stream()
    .filter(s -> s.startsWith("A"))
    .map(String::toUpperCase)
    .collect(Collectors.toList());

// Parallel stream (cho large data)
List<String> result = list.parallelStream()
    .filter(s -> s.startsWith("A"))
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

**Stream operations classification:**

| Intermediate (Lazy) | Terminal (Eager) |
|--------------------|------------------|
| filter() | collect() |
| map() | forEach() |
| sorted() | reduce() |
| distinct() | count() |
| limit() | min()/max() |
| skip() | anyMatch()/allMatch() |

---

### 3.2 Optional - Avoid NullPointerException

```java
// ❌ Traditional
String getValue() {
    if (user == null) return null;
    if (user.getAddress() == null) return null;
    return user.getAddress().getCity();
}

String city = getValue();
if (city != null) {
    System.out.println(city);
}

// ✅ With Optional
Optional<User> user = getUser();
String city = user
    .map(User::getAddress)
    .flatMap(Address::getCity)
    .orElse("Unknown");

// Or
user.map(User::getAddress)
    .flatMap(Address::getCity)
    .ifPresent(System.out::println);
```

**⚠️ Optional anti-patterns:**

```java
// ❌ WRONG: Optional.get() without check
Optional<String> opt = getValue();
String value = opt.get();  // NoSuchElementException if empty!

// ✅ CORRECT
Optional<String> opt = getValue();
String value = opt.orElse("default");
```

---

## 📚 BÀI 4: JVM MEMORY MANAGEMENT

### 4.1 JVM Memory Structure

```
┌─────────────────────────────────────────────────────────────┐
│                        JVM MEMORY                            │
├─────────────────────────────────────────────────────────────┤
│                      HEAP (Runtime Data)                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   Young Generation                   │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │    │
│  │  │   Eden      │  │  Survivor   │  │  Survivor   │  │    │
│  │  │   Space     │  │    S0       │  │    S1       │  │    │
│  │  │             │  │             │  │             │  │    │
│  │  │ New objects │  │ After minor │  │ After copy  │  │    │
│  │  │ allocated   │  │ GC (alive)  │  │ from S0     │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │                   Old Generation                     │    │
│  │                   (Tenured)                          │    │
│  │                                                      │    │
│  │  Long-lived objects (survived multiple GCs)          │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                    METASPACE (Java 8+)                       │
│                    (PermGen before Java 8)                   │
│  - Class metadata                                            │
│  - Static variables                                          │
├─────────────────────────────────────────────────────────────┤
│                       Stack (Per Thread)                     │
│  - Local variables                                           │
│  - Method call stack                                         │
│  - Primitive types                                           │
│  - Object references                                         │
└─────────────────────────────────────────────────────────────┘
```

---

### 4.2 Garbage Collection Algorithms

**G1 GC (Default since Java 9):**
```
- Divide heap into regions
- Collect regions with most garbage first (Garbage First)
- Low pause time (< 200ms)
- Good for large heaps (> 4GB)
```

**Parallel GC (Throughput GC):**
```
- Multiple threads for GC
- Maximize throughput
- Higher pause time
- Good for batch processing
```

**ZGC (Low Latency, Java 11+):**
```
- Pause time < 10ms
- Heap size up to 16TB
- Good for low-latency applications
```

---

### 4.3 Memory Leaks trong Java

```java
// Leak 1: Static collections
public class Cache {
    private static Map<String, Object> cache = new HashMap<>();

    public static void add(String key, Object value) {
        cache.put(key, value);  // Never removed!
    }
}

// Leak 2: Unclosed resources
public String readFile(String path) throws IOException {
    BufferedReader reader = new BufferedReader(new FileReader(path));
    String content = reader.readLine();
    // reader.close() missing!
    return content;
}

// ✅ CORRECT: Try-with-resources
public String readFile(String path) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        return reader.readLine();
    }
}

// Leak 3: Listeners without unregister
public class EventSource {
    private List<Listener> listeners = new ArrayList<>();

    public void addListener(Listener listener) {
        listeners.add(listener);  // Never removed!
    }
}
```

---

## 📝 TÓM TẮT PHASE 0

Sau phase này, bạn cần nắm được:

1. ✅ HashMap internals (hash, buckets, collision resolution)
2. ✅ ConcurrentHashMap vs HashMap
3. ✅ Fail-fast vs fail-safe iterators
4. ✅ synchronized vs ReentrantLock
5. ✅ volatile keyword (visibility, not atomicity)
6. ✅ ExecutorService & thread pools
7. ✅ CompletableFuture for async programming
7. ✅ Stream API & Optional
8. ✅ JVM memory structure
9. ✅ Garbage collection algorithms
10. ✅ Common memory leaks

---

## 🔜 TIẾP THEO

Đọc `02-examples.md` để xem code mẫu thực tế!
