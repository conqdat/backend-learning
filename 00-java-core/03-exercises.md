# Phase 0: Java Core Mastery - Bài Tập Thực Hành

> **Thời gian:** 4-6 giờ
> **Quan trọng:** Đây là nền tảng cho Senior Java!

---

## 📝 BÀI TẬP 1: HASHMAP CUSTOM IMPLEMENTATION (2 giờ)

### Đề bài

**Implement một HashMap đơn giản** (không dùng `java.util.HashMap`)

**Yêu cầu:**
1. Array of buckets
2. Linked list cho collision
3. Auto-resize khi load factor > 0.75
4. Support put(), get(), remove()

### Code template

```java
public class MyHashMap<K, V> {

    private static final int DEFAULT_CAPACITY = 16;
    private static final float LOAD_FACTOR = 0.75f;

    private Node<K, V>[] buckets;
    private int size;

    private static class Node<K, V> {
        final K key;
        V value;
        Node<K, V> next;

        Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }

    public MyHashMap() {
        buckets = new Node[DEFAULT_CAPACITY];
    }

    public void put(K key, V value) {
        // TODO: Implement
        // 1. Tính hash
        // 2. Tính bucket index
        // 3. Nếu bucket có Node, traverse linked list
        // 4. Nếu key tồn tại → update, không → add mới
        // 5. Nếu size > threshold → resize
    }

    public V get(K key) {
        // TODO: Implement
        // 1. Tính hash và bucket index
        // 2. Traverse linked list tìm key
        // 3. Return value hoặc null
    }

    public V remove(K key) {
        // TODO: Implement
        // 1. Tìm Node trong bucket
        // 2. Remove khỏi linked list
        // 3. Return value cũ
    }

    public int size() {
        return size;
    }
}
```

### Test cases

```java
public class MyHashMapTest {

    @Test
    public void testPutAndGet() {
        MyHashMap<String, String> map = new MyHashMap<>();
        map.put("key1", "value1");
        map.put("key2", "value2");

        assertEquals("value1", map.get("key1"));
        assertEquals("value2", map.get("key2"));
        assertNull(map.get("key3"));
    }

    @Test
    public void testUpdateExistingKey() {
        MyHashMap<String, String> map = new MyHashMap<>();
        map.put("key1", "value1");
        map.put("key1", "updated_value");

        assertEquals("updated_value", map.get("key1"));
        assertEquals(1, map.size());
    }

    @Test
    public void testRemove() {
        MyHashMap<String, String> map = new MyHashMap<>();
        map.put("key1", "value1");
        map.put("key2", "value2");

        assertEquals("value1", map.remove("key1"));
        assertNull(map.get("key1"));
        assertEquals(1, map.size());
    }

    @Test
    public void testResize() {
        MyHashMap<Integer, String> map = new MyHashMap<>();

        // Thêm nhiều keys để trigger resize
        for (int i = 0; i < 100; i++) {
            map.put(i, "value" + i);
        }

        // Verify tất cả values vẫn accessible
        for (int i = 0; i < 100; i++) {
            assertEquals("value" + i, map.get(i));
        }
    }

    @Test
    public void testCollision() {
        MyHashMap<BadHashKey, String> map = new MyHashMap<>();

        // BadHashKey luôn trả về cùng hashCode
        for (int i = 0; i < 10; i++) {
            map.put(new BadHashKey(i), "value" + i);
        }

        // Verify tất cả values vẫn accessible
        for (int i = 0; i < 10; i++) {
            assertEquals("value" + i, map.get(new BadHashKey(i)));
        }
    }
}

class BadHashKey {
    private int value;

    public BadHashKey(int value) {
        this.value = value;
    }

    @Override
    public int hashCode() {
        return 42;  // ❌ Tất cả keys có cùng hash!
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof BadHashKey)) return false;
        BadHashKey other = (BadHashKey) o;
        return this.value == other.value;
    }
}
```

---

## 📝 BÀI TẬP 2: THREAD-SAFE COUNTER (1 giờ)

### Đề bài

Implement thread-safe counter với các yêu cầu:

**Part 1:** Dùng `synchronized`
**Part 2:** Dùng `ReentrantLock`
**Part 3:** Dùng `AtomicLong`
**Part 4:** So sánh performance

### Code template

```java
public class ThreadSafeCounter {

    // Part 1: synchronized
    static class SynchronizedCounter {
        private long count = 0;

        public synchronized void increment() {
            count++;
        }

        public synchronized long getCount() {
            return count;
        }
    }

    // Part 2: ReentrantLock
    static class LockCounter {
        private long count = 0;
        private final ReentrantLock lock = new ReentrantLock();

        public void increment() {
            lock.lock();
            try {
                count++;
            } finally {
                lock.unlock();
            }
        }

        public long getCount() {
            lock.lock();
            try {
                return count;
            } finally {
                lock.unlock();
            }
        }
    }

    // Part 3: AtomicLong
    static class AtomicCounter {
        private AtomicLong count = new AtomicLong(0);

        public void increment() {
            count.incrementAndGet();
        }

        public long getCount() {
            return count.get();
        }
    }

    // Part 4: Performance test
    public static void main(String[] args) throws InterruptedException {
        int numThreads = 10;
        int incrementsPerThread = 100_000;

        // Test SynchronizedCounter
        testCounter(new SynchronizedCounter(), numThreads, incrementsPerThread, "Synchronized");

        // Test LockCounter
        testCounter(new LockCounter(), numThreads, incrementsPerThread, "ReentrantLock");

        // Test AtomicCounter
        testCounter(new AtomicCounter(), numThreads, incrementsPerThread, "AtomicLong");
    }

    private static void testCounter(ThreadSafeCounter counter, int numThreads,
                                    int incrementsPerThread, String name) {
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);

        long startTime = System.nanoTime();

        for (int i = 0; i < numThreads; i++) {
            executor.submit(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.increment();
                }
                latch.countDown();
            });
        }

        try {
            latch.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        long endTime = System.nanoTime();
        long duration = (endTime - startTime) / 1_000_000;  // ms

        System.out.printf("%s: %d ms, final count = %d%n",
            name, duration, counter.getCount());

        executor.shutdown();
    }
}
```

### Cách submit

```markdown
## Kết quả Thread-Safe Counter

### Performance comparison (10 threads, 100k increments each):

| Implementation | Time (ms) | Correct? |
|---------------|-----------|----------|
| Synchronized  | XXX       | ✅ 1,000,000 |
| ReentrantLock | XXX       | ✅ 1,000,000 |
| AtomicLong    | XXX       | ✅ 1,000,000 |

### Nhận xét:
- Fastest: ...
- Slowest: ...
- Tại sao: ...
```

---

## 📝 BÀI TẬP 3: PRODUCER-CONSUMER (2 giờ)

### Đề bài

Implement Producer-Consumer pattern với:
- BlockingQueue
- Multiple producers
- Multiple consumers
- Graceful shutdown

### Code template

```java
public class ProducerConsumerDemo {

    private final BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(100);
    private final int POISON_PILL = -1;

    class Producer implements Runnable {
        private final int id;

        public Producer(int id) {
            this.id = id;
        }

        @Override
        public void run() {
            try {
                for (int i = 0; i < 100; i++) {
                    int value = id * 1000 + i;
                    queue.put(value);  // Block nếu queue đầy
                    System.out.println("Producer " + id + " produced: " + value);
                }
                // Send poison pill to signal completion
                queue.put(POISON_PILL);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    class Consumer implements Runnable {
        private final int id;

        public Consumer(int id) {
            this.id = id;
        }

        @Override
        public void run() {
            try {
                while (true) {
                    int value = queue.take();  // Block nếu queue rỗng

                    if (value == POISON_PILL) {
                        // Re-add poison pill for other consumers
                        queue.put(POISON_PILL);
                        System.out.println("Consumer " + id + " stopping");
                        break;
                    }

                    System.out.println("Consumer " + id + " consumed: " + value);
                    // Process value...
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        ProducerConsumerDemo demo = new ProducerConsumerDemo();

        ExecutorService executor = Executors.newFixedThreadPool(10);

        // Start 3 producers
        for (int i = 0; i < 3; i++) {
            executor.submit(demo.new Producer(i));
        }

        // Start 5 consumers
        for (int i = 0; i < 5; i++) {
            executor.submit(demo.new Consumer(i));
        }

        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.MINUTES);
    }
}
```

### Bonus: Custom implementation với wait/notify

```java
public class CustomBlockingQueue<T> {

    private final Queue<T> queue = new LinkedList<>();
    private final int capacity;

    public CustomBlockingQueue(int capacity) {
        this.capacity = capacity;
    }

    public synchronized void put(T item) throws InterruptedException {
        while (queue.size() == capacity) {
            wait();  // Chờ cho đến khi queue không đầy
        }

        queue.add(item);
        notifyAll();  // Notify consumers
    }

    public synchronized T take() throws InterruptedException {
        while (queue.isEmpty()) {
            wait();  // Chờ cho đến khi queue không rỗng
        }

        T item = queue.poll();
        notifyAll();  // Notify producers
        return item;
    }
}
```

---

## 📝 BÀI TẬP 4: STREAM API PRACTICE (1 giờ)

### Đề bài

Cho list employees:

```java
class Employee {
    String name;
    int age;
    String department;
    double salary;
    LocalDate joinDate;

    // Constructor, getters
}

List<Employee> employees = Arrays.asList(
    new Employee("John", 30, "IT", 50000, LocalDate.of(2020, 1, 1)),
    new Employee("Jane", 25, "HR", 45000, LocalDate.of(2021, 6, 1)),
    new Employee("Bob", 35, "IT", 60000, LocalDate.of(2019, 3, 15)),
    new Employee("Alice", 28, "Finance", 55000, LocalDate.of(2022, 2, 1)),
    // ... thêm employees
);
```

**Yêu cầu:**

```java
// 1. Tìm employees trong IT department
List<Employee> itEmployees = employees.stream()
    .filter(e -> e.getDepartment().equals("IT"))
    .collect(Collectors.toList());

// 2. Tính average salary của tất cả employees
double avgSalary = employees.stream()
    .collect(Collectors.averagingDouble(Employee::getSalary));

// 3. Group employees by department
Map<String, List<Employee>> byDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDepartment));

// 4. Tìm employee có salary cao nhất mỗi department
Map<String, Optional<Employee>> maxSalaryByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.maxBy(Comparator.comparingDouble(Employee::getSalary))
    ));

// 5. Tính total salary cost mỗi department
Map<String, Double> totalSalaryByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.summingDouble(Employee::getSalary)
    ));

// 6. Tìm 3 employees có salary cao nhất
List<Employee> top3Earners = employees.stream()
    .sorted(Comparator.comparingDouble(Employee::getSalary).reversed())
    .limit(3)
    .collect(Collectors.toList());

// 7. Kiểm tra tất cả employees có age >= 18 không
boolean allAdults = employees.stream()
    .allMatch(e -> e.getAge() >= 18);

// 8. Tìm employee trẻ nhất
Optional<Employee> youngest = employees.stream()
    .min(Comparator.comparingInt(Employee::getAge));

// 9. Partition employees thành 2 groups: salary > 50000 và <= 50000
Map<Boolean, List<Employee>> byHighSalary = employees.stream()
    .collect(Collectors.partitioningBy(e -> e.getSalary() > 50000));

// 10. Join tất cả employee names với comma
String allNames = employees.stream()
    .map(Employee::getName)
    .collect(Collectors.joining(", "));
```

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 0

- [ ] Implement được HashMap từ scratch
- [ ] Hiểu hashCode() và equals() contract
- [ ] Phân biệt được các thread-safe collections
- [ ] Implement được Producer-Consumer
- [ ] Thành thạo Stream API operations
- [ ] Dùng đúng Optional patterns
- [ ] Hiểu JVM memory structure
- [ ] Nhận diện được memory leaks

---

## 📤 CÁCH SUBMIT

1. Push code lên GitHub
2. Tạo file `PHASE0_REPORT.md` với:
   - Link GitHub
   - Kết quả performance test
   - Những gì học được
   - Khó khăn gặp phải

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, tôi sẽ review và unlock Phase 1: Spring Boot Core!
