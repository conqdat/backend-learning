# Phase 0: Java Core Mastery - Ví Dụ Thực Tế

> **Mục tiêu:** Code mẫu thực tế cho từng chủ đề trong roadmap.sh/java

---

## 📁 PHẦN 1: BASICS EXAMPLES

### 1.1 Data Types & Variables

```java
public class DataTypesExample {
    public static void main(String[] args) {
        // Primitive types
        byte b = 100;
        short s = 10000;
        int i = 100000;
        long l = 10000000000L;
        float f = 3.14f;
        double d = 3.14159;
        char c = 'A';
        boolean bool = true;

        // Type casting
        double myDouble = 9.99;
        int myInt = (int) myDouble;  // 9

        // String parsing
        String strNum = "123";
        int num = Integer.parseInt(strNum);
        double dNum = Double.parseDouble(strNum);

        // Type inference (Java 10+)
        var list = new ArrayList<String>();
        var name = "John";  // Inferred as String
    }
}
```

---

### 1.2 String Operations

```java
public class StringExample {
    public static void main(String[] args) {
        // String creation
        String s1 = "Hello";  // String Pool
        String s2 = new String("Hello");  // Heap

        // Common operations
        String text = "Hello World";
        System.out.println(text.length());  // 11
        System.out.println(text.charAt(0));  // H
        System.out.println(text.substring(0, 5));  // Hello
        System.out.println(text.toUpperCase());  // HELLO WORLD
        System.out.println(text.replace("l", "L"));  // HeLLo WorLd
        System.out.println(text.contains("World"));  // true

        // String comparison
        String a = "Java";
        String b = "Java";
        String c = new String("Java");

        System.out.println(a == b);  // true (same reference in pool)
        System.out.println(a == c);  // false (different references)
        System.out.println(a.equals(c));  // true (same content)

        // String concatenation
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 100; i++) {
            sb.append(i);  // More efficient than +=
        }
        String result = sb.toString();
    }
}
```

---

### 1.3 Arrays

```java
public class ArrayExample {
    public static void main(String[] args) {
        // Single dimension
        int[] numbers = {1, 2, 3, 4, 5};
        int[] moreNumbers = new int[5];

        // Multi-dimension
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        // Common operations
        Arrays.sort(numbers);
        int index = Arrays.binarySearch(numbers, 3);
        Arrays.fill(moreNumbers, 0);
        String result = Arrays.toString(numbers);

        // Stream operations on arrays
        int sum = Arrays.stream(numbers).sum();
        int max = Arrays.stream(numbers).max().getAsInt();
        long count = Arrays.stream(numbers).count();
    }
}
```

---

## 📁 PHẦN 2: OOP EXAMPLES

### 2.1 Class Design Example

```java
// Complete class with all OOP concepts
public class BankAccount {
    // Encapsulation: private fields
    private String accountNumber;
    private String owner;
    private double balance;
    private static int accountCount = 0;  // Static field

    // Constructor
    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;
        this.accountNumber = generateAccountNumber();
        this.balance = initialBalance;
        accountCount++;
    }

    // Static method
    public static int getAccountCount() {
        return accountCount;
    }

    // Instance methods with encapsulation
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited: " + amount);
        }
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            System.out.println("Withdrew: " + amount);
            return true;
        }
        return false;
    }

    // Getter (no setter for accountNumber - immutable)
    public String getAccountNumber() { return accountNumber; }
    public String getOwner() { return owner; }
    public double getBalance() { return balance; }

    // Method overloading
    public void transfer(double amount, BankAccount target) {
        if (withdraw(amount)) {
            target.deposit(amount);
        }
    }

    public void transfer(double amount, BankAccount target, String note) {
        System.out.println("Note: " + note);
        transfer(amount, target);
    }

    // toString, equals, hashCode
    @Override
    public String toString() {
        return "BankAccount{" +
               "accountNumber='" + accountNumber + '\'' +
               ", owner='" + owner + '\'' +
               ", balance=" + balance +
               '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        BankAccount that = (BankAccount) o;
        return Objects.equals(accountNumber, that.accountNumber);
    }

    @Override
    public int hashCode() {
        return Objects.hash(accountNumber);
    }

    // Helper method
    private String generateAccountNumber() {
        return "ACC" + System.currentTimeMillis();
    }

    // finalize() - deprecated but shown for completeness
    @Deprecated
    @Override
    protected void finalize() throws Throwable {
        try {
            System.out.println("Account being closed");
        } finally {
            super.finalize();
        }
    }
}
```

---

### 2.2 Inheritance & Polymorphism

```java
// Base class
abstract class Shape {
    protected String color;

    public Shape(String color) {
        this.color = color;
    }

    // Abstract method
    public abstract double area();

    // Concrete method
    public void display() {
        System.out.println("Color: " + color);
    }

    // Final method (cannot be overridden)
    public final void displayInfo() {
        System.out.println("Area: " + area());
    }
}

// Subclass
class Circle extends Shape {
    private double radius;

    public Circle(String color, double radius) {
        super(color);
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }

    @Override
    public String toString() {
        return "Circle{radius=" + radius + "}";
    }
}

class Rectangle extends Shape {
    private double width, height;

    public Rectangle(String color, double width, double height) {
        super(color);
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height;
    }
}

// Usage
public class PolymorphismDemo {
    public static void main(String[] args) {
        // Polymorphism
        List<Shape> shapes = new ArrayList<>();
        shapes.add(new Circle("Red", 5));
        shapes.add(new Rectangle("Blue", 4, 6));

        // Dynamic binding
        for (Shape shape : shapes) {
            shape.display();  // Calls appropriate method
            System.out.println("Area: " + shape.area());
        }
    }
}
```

---

### 2.3 Interface Example

```java
// Multiple interfaces
interface Flyable {
    void fly();

    default void land() {
        System.out.println("Landing...");
    }

    static void honk() {
        System.out.println("Honking!");
    }
}

interface Swimmable {
    void swim();

    default void dive() {
        System.out.println("Diving...");
    }
}

// Class implementing multiple interfaces
class Duck implements Flyable, Swimmable {
    private String name;

    public Duck(String name) {
        this.name = name;
    }

    @Override
    public void fly() {
        System.out.println(name + " is flying");
    }

    @Override
    public void swim() {
        System.out.println(name + " is swimming");
    }

    // Can override default methods
    @Override
    public void land() {
        System.out.println(name + " landed gracefully");
    }
}

// Abstract class with interface
abstract class Bird implements Flyable {
    protected String name;

    public Bird(String name) {
        this.name = name;
    }

    public abstract void layEgg();

    public void chirp() {
        System.out.println(name + " is chirping");
    }
}

class Eagle extends Bird {
    public Eagle(String name) {
        super(name);
    }

    @Override
    public void fly() {
        System.out.println(name + " soars high!");
    }

    @Override
    public void layEgg() {
        System.out.println(name + " laid an egg");
    }
}
```

---

### 2.4 Enum Example

```java
enum OrderStatus {
    PENDING("Order is pending"),
    CONFIRMED("Order confirmed"),
    PROCESSING("Order is being processed"),
    SHIPPED("Order has been shipped"),
    DELIVERED("Order delivered"),
    CANCELLED("Order cancelled");

    private final String description;

    OrderStatus(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }

    // Static method
    public static List<OrderStatus> getActiveStatuses() {
        return Arrays.asList(PENDING, CONFIRMED, PROCESSING, SHIPPED);
    }
}

enum PaymentMethod {
    CREDIT_CARD {
        @Override
        public void processPayment(double amount) {
            System.out.println("Processing credit card payment: $" + amount);
        }
    },
    DEBIT_CARD {
        @Override
        public void processPayment(double amount) {
            System.out.println("Processing debit card payment: $" + amount);
        }
    },
    PAYPAL {
        @Override
        public void processPayment(double amount) {
            System.out.println("Processing PayPal payment: $" + amount);
        }
    };

    public abstract void processPayment(double amount);
}

// Usage
public class EnumExample {
    public static void main(String[] args) {
        OrderStatus status = OrderStatus.CONFIRMED;
        System.out.println(status.getDescription());

        // Switch on enum
        switch (status) {
            case PENDING, CONFIRMED -> System.out.println("Active order");
            case DELIVERED -> System.out.println("Completed");
            case CANCELLED -> System.out.println("Cancelled");
        }

        // Enum methods
        for (OrderStatus s : OrderStatus.values()) {
            System.out.println(s.name() + ": " + s.ordinal());
        }

        PaymentMethod.CREDIT_CARD.processPayment(100.0);
    }
}
```

---

## 📁 PHẦN 3: COLLECTIONS EXAMPLES

### 3.1 HashMap Deep Dive

```java
public class HashMapExamples {
    public static void main(String[] args) {
        // Basic usage
        Map<String, Integer> map = new HashMap<>();
        map.put("Alice", 25);
        map.put("Bob", 30);
        map.put("Charlie", 35);

        // Get with null check
        Integer age = map.get("Alice");
        if (age != null) {
            System.out.println("Alice is " + age);
        }

        // Get with default (Java 8+)
        int unknownAge = map.getOrDefault("Unknown", 0);

        // Iterate
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }

        // Java 8+ methods
        map.putIfAbsent("David", 40);  // Only if key not present
        map.compute("Alice", (k, v) -> v + 1);  // Compute new value
        map.merge("Bob", 1, Integer::sum);  // Merge values

        // Remove
        map.remove("Charlie");
        map.remove("David", 40);  // Only if value matches

        // Custom object as key
        Map<Person, String> personMap = new HashMap<>();
        personMap.put(new Person("John", 30), "Developer");

        // IMPORTANT: Person must override hashCode() and equals()
    }
}

// Custom key class
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
```

---

### 3.2 ConcurrentHashMap Example

```java
public class ConcurrentHashMapExample {
    public static void main(String[] args) throws InterruptedException {
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

        // Thread-safe operations
        map.put("A", 1);
        map.putIfAbsent("B", 2);

        // Atomic operations
        map.compute("A", (k, v) -> v == null ? 1 : v + 1);
        map.merge("C", 1, Integer::sum);

        // Safe iteration during modification
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
            // Can safely modify map during iteration
        }

        // Parallel operations
        map.forEach(1, (k, v) -> System.out.println(k + "=" + v));

        // Search
        String result = map.search(1, (k, v) -> {
            if (v > 1) return k;
            return null;
        });

        // Reduce
        Integer sum = map.reduceValues(1, Integer::sum);

        ExecutorService executor = Executors.newFixedThreadPool(5);

        // Multiple threads can safely access
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            executor.submit(() -> {
                map.put("Thread" + threadId, threadId);
                System.out.println(map.get("Thread" + threadId));
            });
        }

        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.SECONDS);
        System.out.println("Final map: " + map);
    }
}
```

---

### 3.3 Stream API Examples

```java
public class StreamExamples {
    public static void main(String[] args) {
        List<Employee> employees = Arrays.asList(
            new Employee("John", 30, "IT", 50000),
            new Employee("Jane", 25, "HR", 45000),
            new Employee("Bob", 35, "IT", 60000),
            new Employee("Alice", 28, "Finance", 55000)
        );

        // Filter and map
        List<String> itEmployees = employees.stream()
            .filter(e -> e.getDepartment().equals("IT"))
            .map(Employee::getName)
            .collect(Collectors.toList());

        // Grouping
        Map<String, List<Employee>> byDept = employees.stream()
            .collect(Collectors.groupingBy(Employee::getDepartment));

        // Average salary by department
        Map<String, Double> avgSalaryByDept = employees.stream()
            .collect(Collectors.groupingBy(
                Employee::getDepartment,
                Collectors.averagingDouble(Employee::getSalary)
            ));

        // Find max salary employee
        Optional<Employee> highestPaid = employees.stream()
            .max(Comparator.comparingDouble(Employee::getSalary));

        // Partition
        Map<Boolean, List<Employee>> byHighSalary = employees.stream()
            .collect(Collectors.partitioningBy(e -> e.getSalary() > 50000));

        // Joining
        String allNames = employees.stream()
            .map(Employee::getName)
            .collect(Collectors.joining(", ", "[", "]"));

        // Parallel stream for large data
        List<String> result = employees.parallelStream()
            .filter(e -> e.getSalary() > 45000)
            .map(Employee::getName)
            .collect(Collectors.toList());
    }
}

class Employee {
    private String name;
    private int age;
    private String department;
    private double salary;

    public Employee(String name, int age, String department, double salary) {
        this.name = name;
        this.age = age;
        this.department = department;
        this.salary = salary;
    }

    public String getName() { return name; }
    public int getAge() { return age; }
    public String getDepartment() { return department; }
    public double getSalary() { return salary; }
}
```

---

### 3.4 Optional Examples

```java
public class OptionalExamples {

    // Traditional null check
    public String getUserNameTraditional(User user) {
        if (user == null) return "Unknown";
        if (user.getName() == null) return "Unknown";
        return user.getName();
    }

    // With Optional
    public String getUserName(User user) {
        return Optional.ofNullable(user)
            .map(User::getName)
            .orElse("Unknown");
    }

    // Nested optionals
    public String getUserCity(User user) {
        return Optional.ofNullable(user)
            .map(User::getAddress)
            .flatMap(Address::getCity)
            .orElse("Unknown");
    }

    // Optional with exception
    public User findUserById(String id) {
        return Optional.ofNullable(findUser(id))
            .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
    }

    // Optional with action
    public void printUserName(User user) {
        Optional.ofNullable(user)
            .map(User::getName)
            .ifPresent(System.out::println);
    }

    // Optional with action or default
    public void printUserNameOrDefault(User user) {
        Optional.ofNullable(user)
            .map(User::getName)
            .ifPresentOrElse(
                System.out::println,
                () -> System.out.println("No name provided")
            );
    }

    // Anti-pattern: Don't do this!
    public String wrongUsage(Optional<String> opt) {
        return opt.get();  // Throws if empty!
    }

    // Correct usage
    public String correctUsage(Optional<String> opt) {
        return opt.orElse("default");
    }

    // Helper methods
    private User findUser(String id) { return null; }

    static class User {
        private String name;
        private Address address;
        public String getName() { return name; }
        public Address getAddress() { return address; }
    }

    static class Address {
        private String city;
        public Optional<String> getCity() {
            return Optional.ofNullable(city);
        }
    }

    static class UserNotFoundException extends RuntimeException {
        public UserNotFoundException(String message) {
            super(message);
        }
    }
}
```

---

## 📁 PHẦN 4: CONCURRENCY EXAMPLES

### 4.1 Thread Safety Patterns

```java
public class ThreadSafetyExamples {

    // ❌ NOT thread-safe
    static class UnsafeCounter {
        private int count = 0;

        public void increment() {
            count++;  // Race condition!
        }

        public int getCount() {
            return count;
        }
    }

    // ✅ Thread-safe with synchronized
    static class SynchronizedCounter {
        private int count = 0;

        public synchronized void increment() {
            count++;
        }

        public synchronized int getCount() {
            return count;
        }
    }

    // ✅ Thread-safe with ReentrantLock
    static class LockCounter {
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
    }

    // ✅ Thread-safe with AtomicInteger
    static class AtomicCounter {
        private AtomicInteger count = new AtomicInteger(0);

        public void increment() {
            count.incrementAndGet();
        }

        public int getCount() {
            return count.get();
        }
    }

    // Test race condition
    public static void main(String[] args) throws InterruptedException {
        UnsafeCounter unsafe = new UnsafeCounter();
        testCounter(unsafe, "Unsafe");

        SynchronizedCounter sync = new SynchronizedCounter();
        testCounter(sync, "Synchronized");

        AtomicCounter atomic = new AtomicCounter();
        testCounter(atomic, "Atomic");
    }

    private static void testCounter(Object counter, String name) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(10);
        CountDownLatch latch = new CountDownLatch(10);

        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    if (counter instanceof UnsafeCounter) {
                        ((UnsafeCounter) counter).increment();
                    } else if (counter instanceof SynchronizedCounter) {
                        ((SynchronizedCounter) counter).increment();
                    } else {
                        ((AtomicCounter) counter).increment();
                    }
                }
                latch.countDown();
            });
        }

        latch.await();
        executor.shutdown();

        int expected = 10000;
        int actual = counter instanceof UnsafeCounter ? ((UnsafeCounter) counter).getCount() :
                     counter instanceof SynchronizedCounter ? ((SynchronizedCounter) counter).getCount() :
                     ((AtomicCounter) counter).getCount();

        System.out.printf("%s: Expected %d, Got %d - %s%n",
            name, expected, actual, expected == actual ? "✅" : "❌");
    }
}
```

---

### 4.2 Producer-Consumer with BlockingQueue

```java
public class ProducerConsumerExample {

    private final BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(100);
    private static final int POISON_PILL = -1;

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
                    queue.put(value);  // Blocks if queue is full
                    System.out.println("Producer " + id + " produced: " + value);
                    Thread.sleep(10);  // Simulate work
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
                    int value = queue.take();  // Blocks if queue is empty

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
        ProducerConsumerExample demo = new ProducerConsumerExample();
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

---

### 4.3 CompletableFuture Example

```java
@Service
public class OrderProcessingService {

    @Autowired
    private ProductService productService;

    @Autowired
    private UserService userService;

    @Autowired
    private PaymentService paymentService;

    @Autowired
    private EmailService emailService;

    /**
     * Process order with async orchestration
     */
    public CompletableFuture<OrderResult> processOrder(OrderRequest request) {
        // Parallel: Fetch product and user simultaneously
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
            return order;
        })
        .thenApplyAsync(order -> {
            // Send confirmation email (async)
            emailService.sendConfirmation(order);
            return order;
        })
        .thenApply(order -> OrderResult.success(order))
        .exceptionally(ex -> {
            log.error("Order processing failed", ex);
            return OrderResult.failure(ex.getMessage());
        });
    }

    // Helper classes
    @Data
    @AllArgsConstructor
    private static class OrderContext {
        Product product;
        User user;
        OrderRequest request;
    }
}

// Usage example
public class CompletableFutureUsage {
    public static void main(String[] args) {
        OrderProcessingService service = new OrderProcessingService();
        OrderRequest request = new OrderRequest("prod123", "user456", 2);

        service.processOrder(request)
            .thenAccept(result -> {
                if (result.isSuccess()) {
                    System.out.println("Order successful: " + result.getOrder());
                } else {
                    System.out.println("Order failed: " + result.getError());
                }
            })
            .join();  // Wait for completion
    }
}
```

---

### 4.4 ExecutorService Best Practices

```java
public class ExecutorServiceBestPractices {

    // ❌ WRONG: Using Executors factory methods
    // - Unbounded queue can cause OutOfMemoryError
    // - No control over rejection policy
    ExecutorService badPool = Executors.newFixedThreadPool(10);
    ExecutorService badCached = Executors.newCachedThreadPool();

    // ✅ CORRECT: Custom ThreadPoolExecutor
    ExecutorService goodPool = new ThreadPoolExecutor(
        5,                          // corePoolSize
        20,                         // maxPoolSize
        60L,                        // keepAliveTime
        TimeUnit.SECONDS,
        new ArrayBlockingQueue<>(1000),  // Bounded queue
        new ThreadPoolExecutor.CallerRunsPolicy()  // Backpressure
    );

    // Monitoring thread pool
    public void monitorPool(ThreadPoolExecutor executor) {
        ScheduledExecutorService monitor = Executors.newSingleThreadScheduledExecutor();

        monitor.scheduleAtFixedRate(() -> {
            System.out.println("=== Pool Status ===");
            System.out.println("Active threads: " + executor.getActiveCount());
            System.out.println("Pool size: " + executor.getPoolSize());
            System.out.println("Queue size: " + executor.getQueue().size());
            System.out.println("Completed tasks: " + executor.getCompletedTaskCount());
            System.out.println("Largest pool size: " + executor.getLargestPoolSize());
            System.out.println("Tasks rejected: " + executor.getRejectedExecutionHandler());
        }, 0, 10, TimeUnit.SECONDS);
    }

    // Graceful shutdown
    public void shutdownPool(ExecutorService executor, long timeout, TimeUnit unit) {
        executor.shutdown();  // Stop accepting new tasks

        try {
            if (!executor.awaitTermination(timeout, unit)) {
                System.out.println("Forcing shutdown...");
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

    // Submit task with timeout
    public <T> T submitWithTimeout(ExecutorService executor, Callable<T> task, long timeout, TimeUnit unit)
            throws TimeoutException, InterruptedException, ExecutionException {
        Future<T> future = executor.submit(task);
        return future.get(timeout, unit);  // Timeout if takes too long
    }

    // Batch processing with limited concurrency
    public void processBatch(List<String> items, int concurrency) {
        ExecutorService executor = Executors.newFixedThreadPool(concurrency);
        CountDownLatch latch = new CountDownLatch(items.size());

        for (String item : items) {
            executor.submit(() -> {
                try {
                    processItem(item);
                } finally {
                    latch.countDown();
                }
            });
        }

        try {
            latch.await();
        } finally {
            executor.shutdown();
        }
    }

    private void processItem(String item) {
        // Process item
    }
}
```

---

## 📁 PHẦN 5: EXCEPTION HANDLING EXAMPLES

### 5.1 Exception Handling Patterns

```java
public class ExceptionHandlingExamples {

    // Try-with-resources
    public String readFile(String path) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            return reader.readLine();
        }
        // Auto-closed, no finally needed
    }

    // Multiple resources
    public void processFiles(String inputPath, String outputPath) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(inputPath));
             BufferedWriter writer = new BufferedWriter(new FileWriter(outputPath))) {

            String line;
            while ((line = reader.readLine()) != null) {
                writer.write(line.toUpperCase());
                writer.newLine();
            }
        }
    }

    // Multi-catch
    public void handleMultipleExceptions(String type) {
        try {
            if (type.equals("io")) {
                throw new IOException("IO error");
            } else if (type.equals("sql")) {
                throw new SQLException("SQL error");
            }
        } catch (IOException | SQLException e) {
            System.out.println("Error occurred: " + e.getMessage());
            log.error("Error", e);
        }
    }

    // Custom exception
    public class InsufficientFundsException extends Exception {
        private final double amount;

        public InsufficientFundsException(double amount) {
            super("Insufficient funds: $" + amount);
            this.amount = amount;
        }

        public double getAmount() {
            return amount;
        }
    }

    // Throwing custom exception
    public class BankAccount {
        private double balance;

        public void withdraw(double amount) throws InsufficientFundsException {
            if (amount > balance) {
                throw new InsufficientFundsException(amount - balance);
            }
            balance -= amount;
        }
    }

    // Exception translation
    public void readFileWithTranslation(String path) {
        try {
            Files.readString(Paths.get(path));
        } catch (NoSuchFileException e) {
            throw new FileNotFoundException("File not found: " + path);
        } catch (IOException e) {
            throw new RuntimeException("Failed to read file", e);
        }
    }

    // Optional instead of exception
    public Optional<User> findUser(String id) {
        try {
            return Optional.ofNullable(database.findById(id));
        } catch (SQLException e) {
            log.error("Database error", e);
            return Optional.empty();
        }
    }
}
```

---

## 📁 PHẦN 6: DESIGN PATTERNS EXAMPLES

### 6.1 Singleton Pattern

```java
public class SingletonExamples {

    // Eager initialization (thread-safe)
    static class EagerSingleton {
        private static final EagerSingleton INSTANCE = new EagerSingleton();

        private EagerSingleton() {}

        public static EagerSingleton getInstance() {
            return INSTANCE;
        }
    }

    // Lazy initialization with synchronization
    static class LazySingleton {
        private static LazySingleton instance;

        private LazySingleton() {}

        public static synchronized LazySingleton getInstance() {
            if (instance == null) {
                instance = new LazySingleton();
            }
            return instance;
        }
    }

    // Double-checked locking (best lazy)
    static class DoubleCheckedSingleton {
        private static volatile DoubleCheckedSingleton instance;

        private DoubleCheckedSingleton() {}

        public static DoubleCheckedSingleton getInstance() {
            if (instance == null) {
                synchronized (DoubleCheckedSingleton.class) {
                    if (instance == null) {
                        instance = new DoubleCheckedSingleton();
                    }
                }
            }
            return instance;
        }
    }

    // Bill Pugh Singleton (recommended)
    static class BillPughSingleton {
        private BillPughSingleton() {}

        private static class SingletonHelper {
            private static final BillPughSingleton INSTANCE = new BillPughSingleton();
        }

        public static BillPughSingleton getInstance() {
            return SingletonHelper.INSTANCE;
        }
    }

    // Enum Singleton (effective Java recommendation)
    enum EnumSingleton {
        INSTANCE;

        public void doSomething() {
            System.out.println("Doing something");
        }
    }
}
```

---

### 6.2 Builder Pattern

```java
// Traditional Builder Pattern
public class User {
    private final String firstName;
    private final String lastName;
    private final int age;
    private final String email;

    private User(Builder builder) {
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.age = builder.age;
        this.email = builder.email;
    }

    // Getters

    public static class Builder {
        private final String firstName;  // Required
        private final String lastName;   // Required
        private int age = 0;             // Optional
        private String email = "";       // Optional

        public Builder(String firstName, String lastName) {
            this.firstName = firstName;
            this.lastName = lastName;
        }

        public Builder age(int age) {
            this.age = age;
            return this;
        }

        public Builder email(String email) {
            this.email = email;
            return this;
        }

        public User build() {
            // Validation
            if (firstName == null || lastName == null) {
                throw new IllegalStateException("First and last name are required");
            }
            if (age < 0 || age > 150) {
                throw new IllegalStateException("Invalid age");
            }
            return new User(this);
        }
    }
}

// Usage
User user = new User.Builder("John", "Doe")
    .age(30)
    .email("john@example.com")
    .build();
```

---

## 📝 BÀI TẬP THỰC HÀNH

Xem `03-exercises.md` để làm bài tập thực hành!

---

## 🔗 TÀI LIỆU THAM KHẢO

- [Official Java Documentation](https://docs.oracle.com/en/java/)
- [Effective Java by Joshua Bloch](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/)
- [Java Roadmap](https://roadmap.sh/java)
