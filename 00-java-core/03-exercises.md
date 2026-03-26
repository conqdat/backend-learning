# Phase 0: Java Core Mastery - Bài Tập Thực Hành

> **Thời gian:** 2-3 tuần
> **Mục tiêu:** Thực hành toàn bộ Java Core theo roadmap.sh/java
> **Quan trọng:** Hoàn thành các bài tập này để solidify kiến thức!

---

## 📝 BÀI TẬP 1: JAVA BASICS (2-3 giờ)

### 1.1 String Manipulation

**Đề bài:** Implement các utility methods cho String

```java
public class StringUtilities {

    // 1. Reverse a string without using StringBuilder.reverse()
    public static String reverse(String input) {
        // TODO: Implement
        // Example: "Hello" -> "olleH"
    }

    // 2. Check if string is palindrome
    public static boolean isPalindrome(String input) {
        // TODO: Implement
        // Example: "racecar" -> true, "hello" -> false
    }

    // 3. Count vowels and consonants
    public static Map<String, Integer> countVowelsConsonants(String input) {
        // TODO: Implement
        // Return: {"vowels": 3, "consonants": 5}
    }

    // 4. Remove duplicates from string (keep first occurrence)
    public static String removeDuplicates(String input) {
        // TODO: Implement
        // Example: "programming" -> "progamin"
    }

    // 5. Find first non-repeated character
    public static Character firstNonRepeated(String input) {
        // TODO: Implement
        // Example: "swiss" -> 'w', "aabb" -> null
    }

    // Test
    public static void main(String[] args) {
        System.out.println(reverse("Hello"));  // olleH
        System.out.println(isPalindrome("racecar"));  // true
        System.out.println(firstNonRepeated("swiss"));  // w
    }
}
```

---

### 1.2 Array Operations

**Đề bài:** Implement các thuật toán trên array

```java
public class ArrayAlgorithms {

    // 1. Find maximum and minimum in array
    public static Map<String, Integer> findMinMax(int[] arr) {
        // TODO: Implement
    }

    // 2. Find second largest element
    public static Integer findSecondLargest(int[] arr) {
        // TODO: Implement
        // Example: [1, 5, 3, 9, 2] -> 5
    }

    // 3. Rotate array by k positions
    public static void rotate(int[] arr, int k) {
        // TODO: Implement
        // Example: [1,2,3,4,5], k=2 -> [4,5,1,2,3]
    }

    // 4. Remove duplicates from sorted array
    public static int removeDuplicates(int[] arr) {
        // TODO: Implement
        // Return new length, modify array in-place
    }

    // 5. Two Sum - Find two numbers that add up to target
    public static int[] twoSum(int[] arr, int target) {
        // TODO: Implement
        // Return indices of two numbers
        // Example: [2,7,11,15], target=9 -> [0,1]
    }

    // 6. Merge two sorted arrays
    public static int[] mergeSortedArrays(int[] arr1, int[] arr2) {
        // TODO: Implement
    }

    // Test
    public static void main(String[] args) {
        int[] nums = {1, 5, 3, 9, 2};
        System.out.println(findSecondLargest(nums));  // 5

        int[] sorted1 = {1, 3, 5};
        int[] sorted2 = {2, 4, 6};
        System.out.println(Arrays.toString(mergeSortedArrays(sorted1, sorted2)));
    }
}
```

---

## 📝 BÀI TẬP 2: OOP DESIGN (3-4 giờ)

### 2.1 Library Management System

**Đề bài:** Design một hệ thống quản lý thư viện sử dụng OOP principles

```java
// Requirements:
// 1. Books have: title, author, ISBN, publicationYear, isAvailable
// 2. Members can borrow up to 3 books
// 3. Track borrowing history
// 4. Calculate late fees ($1 per day)

// TODO: Design classes with proper encapsulation, inheritance, polymorphism

// Starter code:
abstract class LibraryItem {
    private String title;
    private String id;
    private boolean isAvailable;

    // TODO: Add constructor, getters, abstract methods
    public abstract double calculateLateFee(int daysLate);
}

class Book extends LibraryItem {
    private String author;
    private String isbn;
    private int publicationYear;

    // TODO: Implement
}

class Member {
    private String memberId;
    private String name;
    private List<Book> borrowedBooks;
    private List<BorrowRecord> borrowingHistory;

    // TODO: Implement borrow, return methods
}

class BorrowRecord {
    private Book book;
    private Member member;
    private LocalDate borrowDate;
    private LocalDate dueDate;
    private LocalDate returnDate;

    // TODO: Implement
}

class Library {
    private List<Book> catalog;
    private List<Member> members;

    // TODO: Implement search, borrow, return methods
}
```

**Test cases:**
```java
public class LibraryTest {
    public static void main(String[] args) {
        Library library = new Library();

        // Add books
        library.addBook(new Book("Java Core", "Author1", "ISBN1", 2023));
        library.addBook(new Book("Spring Boot", "Author2", "ISBN2", 2022));

        // Register member
        Member member = new Member("M001", "John Doe");
        library.registerMember(member);

        // Borrow books
        member.borrowBook(library.searchByTitle("Java Core"));

        // Return book late
        member.returnBook("ISBN1", LocalDate.now().minusDays(5));
        // Should calculate late fee
    }
}
```

---

### 2.2 Payment System Design

**Đề bài:** Design payment system với interfaces và enums

```java
// Payment methods: CreditCard, DebitCard, PayPal, Crypto
// Each has different processing fee and validation

enum PaymentMethod {
    CREDIT_CARD(0.029),    // 2.9% fee
    DEBIT_CARD(0.015),     // 1.5% fee
    PAYPAL(0.035),         // 3.5% fee
    BITCOIN(0.01);         // 1% fee

    private final double feePercentage;

    PaymentMethod(double fee) {
        this.feePercentage = fee;
    }

    public double calculateFee(double amount) {
        return amount * feePercentage;
    }
}

interface PaymentProcessor {
    boolean authenticate();
    boolean processPayment(double amount);
    void refund(String transactionId);
}

// TODO: Implement concrete classes
class CreditCardProcessor implements PaymentProcessor {
    // TODO: Implement
}

class PayPalProcessor implements PaymentProcessor {
    // TODO: Implement
}

// Usage
public class PaymentService {
    public void checkout(PaymentProcessor processor, double amount) {
        if (processor.authenticate()) {
            processor.processPayment(amount);
        }
    }
}
```

---

## 📝 BÀI TẬP 3: COLLECTIONS (4-5 giờ)

### 3.1 Custom Data Structures

**Đề bài 1:** Implement ArrayList từ scratch

```java
public class MyArrayList<T> implements List<T> {
    private Object[] elements;
    private int size;
    private static final int DEFAULT_CAPACITY = 10;

    public MyArrayList() {
        elements = new Object[DEFAULT_CAPACITY];
    }

    public MyArrayList(int capacity) {
        elements = new Object[capacity];
    }

    @Override
    public boolean add(T element) {
        // TODO: Implement
        // - Check capacity, resize if needed
        // - Add element at end
        // - Increment size
    }

    @Override
    public void add(int index, T element) {
        // TODO: Implement
        // - Check bounds
        // - Shift elements right
        // - Insert at index
    }

    @Override
    @SuppressWarnings("unchecked")
    public T get(int index) {
        // TODO: Implement
        // - Check bounds
        // - Return element at index
        return (T) elements[index];
    }

    @Override
    public T remove(int index) {
        // TODO: Implement
        // - Check bounds
        // - Save element to return
        // - Shift elements left
        // - Decrement size
    }

    @Override
    public int size() {
        return size;
    }

    // TODO: Implement other methods: set, indexOf, contains, etc.

    private void ensureCapacity() {
        // TODO: Implement resize (double capacity)
    }
}
```

**Đề bài 2:** Implement Stack và Queue

```java
// Stack (LIFO)
public class MyStack<T> {
    private Node<T> top;
    private int size;

    public void push(T value) {
        // TODO: Implement
    }

    public T pop() {
        // TODO: Implement
    }

    public T peek() {
        // TODO: Implement
    }

    public boolean isEmpty() {
        // TODO: Implement
    }

    public int size() {
        return size;
    }

    private static class Node<T> {
        T value;
        Node<T> next;

        Node(T value) {
            this.value = value;
        }
    }
}

// Queue (FIFO)
public class MyQueue<T> {
    private Node<T> front;
    private Node<T> rear;
    private int size;

    public void enqueue(T value) {
        // TODO: Implement
    }

    public T dequeue() {
        // TODO: Implement
    }

    public T peek() {
        // TODO: Implement
    }

    public boolean isEmpty() {
        // TODO: Implement
    }

    public int size() {
        return size;
    }
}
```

---

### 3.2 Collections Practice Problems

```java
public class CollectionsProblems {

    // 1. Group words by their first letter
    public static Map<Character, List<String>> groupByFirstLetter(List<String> words) {
        // TODO: Implement using HashMap
        // Example: ["apple", "banana", "apricot"] -> {a=[apple, apricot], b=[banana]}
    }

    // 2. Find most frequent element
    public static <T> T findMostFrequent(List<T> list) {
        // TODO: Implement using HashMap
        // Example: [1, 2, 2, 3, 2, 4] -> 2
    }

    // 3. Remove duplicates from LinkedList
    public static <T> void removeDuplicates(LinkedList<T> list) {
        // TODO: Implement using HashSet
    }

    // 4. Implement LRU Cache
    public class LRUCache<K, V> {
        private final int capacity;
        private final Map<K, V> map;
        private final LinkedList<K> order;

        public LRUCache(int capacity) {
            this.capacity = capacity;
            this.map = new HashMap<>();
            this.order = new LinkedList<>();
        }

        public void put(K key, V value) {
            // TODO: Implement
            // - If exists, update and move to front
            // - If new and full, remove least recently used
            // - Add to front
        }

        public V get(K key) {
            // TODO: Implement
            // - Return value and move to front
            // - Or return null if not exists
        }
    }

    // 5. Merge K sorted lists
    public static List<Integer> mergeKSortedLists(List<List<Integer>> lists) {
        // TODO: Implement using PriorityQueue
    }

    // Test
    public static void main(String[] args) {
        List<String> words = Arrays.asList("apple", "banana", "apricot", "blueberry");
        System.out.println(groupByFirstLetter(words));

        LRUCache<String, Integer> cache = new LRUCache<>(2);
        cache.put("a", 1);
        cache.put("b", 2);
        cache.get("a");  // Access "a"
        cache.put("c", 3);  // Should evict "b"
    }
}
```

---

## 📝 BÀI TẬP 4: STREAM API & LAMBDA (3-4 giờ)

### 4.1 Stream Exercises

```java
public class StreamExercises {

    // Given list of employees
    List<Employee> employees = Arrays.asList(
        new Employee("John", 30, "IT", 50000),
        new Employee("Jane", 25, "HR", 45000),
        new Employee("Bob", 35, "IT", 60000),
        new Employee("Alice", 28, "Finance", 55000),
        new Employee("Charlie", 32, "IT", 52000)
    );

    // 1. Find all IT employees with salary > 50000
    public List<Employee> findHighPaidITEmployees() {
        return employees.stream()
            // TODO: Complete
            .collect(Collectors.toList());
    }

    // 2. Calculate average salary by department
    public Map<String, Double> getAverageSalaryByDept() {
        return employees.stream()
            // TODO: Complete
    }

    // 3. Find employee with highest salary
    public Optional<Employee> findHighestPaid() {
        return employees.stream()
            // TODO: Complete
    }

    // 4. Get total salary budget per department
    public Map<String, Double> getTotalSalaryByDept() {
        return employees.stream()
            // TODO: Complete
    }

    // 5. Group employees by age range (20s, 30s, 40s, etc.)
    public Map<String, List<Employee>> groupByAgeRange() {
        return employees.stream()
            // TODO: Complete
    }

    // 6. Find sum of all salaries
    public double getTotalSalaryBudget() {
        return employees.stream()
            // TODO: Complete
    }

    // 7. Check if all employees have salary > 30000
    public boolean allWellPaid() {
        return employees.stream()
            // TODO: Complete
    }

    // 8. Get comma-separated list of employee names
    public String getAllNames() {
        return employees.stream()
            // TODO: Complete
    }

    // 9. Find 2 highest paid employees
    public List<Employee> getTop2Earners() {
        return employees.stream()
            // TODO: Complete
    }

    // 10. Partition employees into high/low salary (threshold: 55000)
    public Map<Boolean, List<Employee>> partitionBySalary() {
        return employees.stream()
            // TODO: Complete
    }

    class Employee {
        String name;
        int age;
        String department;
        double salary;

        // Constructor, getters
    }
}
```

---

### 4.2 Functional Interfaces Practice

```java
public class FunctionalInterfaceExercises {

    // 1. Create Predicate that checks if string is palindrome
    public Predicate<String> isPalindrome() {
        // TODO: Implement
    }

    // 2. Create Function that converts List<String> to Map<String, Integer> (word -> length)
    public Function<List<String>, Map<String, Integer>> wordLengthMapper() {
        // TODO: Implement
    }

    // 3. Create Consumer that prints each element with index
    public <T> Consumer<List<T>> indexedPrinter() {
        // TODO: Implement
    }

    // 4. Create Supplier that generates unique IDs
    public Supplier<String> uniqueIdGenerator() {
        // TODO: Implement
    }

    // 5. Compose functions: add 1, then multiply by 2, then square
    public Function<Integer, Integer> composedFunction() {
        Function<Integer, Integer> addOne = x -> x + 1;
        Function<Integer, Integer> multiplyByTwo = x -> x * 2;
        Function<Integer, Integer> square = x -> x * x;

        // TODO: Compose them
    }
}
```

---

## 📝 BÀI TẬP 5: EXCEPTION HANDLING (2 giờ)

### 5.1 Exception Handling Practice

```java
public class ExceptionHandlingExercises {

    // 1. Implement division with proper exception handling
    public static double safeDivide(double a, double b) {
        // TODO: Handle division by zero
    }

    // 2. Implement file reader with try-with-resources
    public static String readFile(String path) {
        // TODO: Use try-with-resources
        // Handle: FileNotFoundException, IOException
    }

    // 3. Create custom exception hierarchy
    /*
     * Create:
     * - BankingException (base)
     * - InsufficientFundsException
     * - InvalidAccountException
     * - TransactionFailedException
     */

    // 4. Implement ATM with exception handling
    public class ATM {
        private double balance;

        public void withdraw(double amount) {
            // TODO: Throw appropriate exceptions for:
            // - Invalid amount (negative)
            // - Insufficient funds
            // - Daily limit exceeded
        }

        public void deposit(double amount) {
            // TODO: Validate amount
        }

        public void transfer(ATM target, double amount) {
            // TODO: Handle transfer with proper exception handling
        }
    }

    // 5. Multi-catch practice
    public void processInput(String input) {
        // TODO: Parse input as integer
        // Handle: NumberFormatException, NullPointerException
        // Use multi-catch where appropriate
    }
}
```

---

## 📝 BÀI TẬP 6: MULTITHREADING (5-6 giờ)

### 6.1 Thread Basics

```java
public class ThreadExercises {

    // 1. Create thread by extending Thread class
    class MyThread extends Thread {
        @Override
        public void run() {
            // TODO: Print numbers 1-10 with thread name
        }
    }

    // 2. Create thread by implementing Runnable
    class MyRunnable implements Runnable {
        @Override
        public void run() {
            // TODO: Print numbers 1-10 with thread name
        }
    }

    // 3. Create thread with lambda
    public void createLambdaThread() {
        // TODO: Create and start thread using lambda
    }

    // 4. Thread join example
    public void demonstrateJoin() throws InterruptedException {
        Thread t = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println(i);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        t.start();
        // TODO: Wait for thread to complete using join()
    }

    // 5. Thread daemon example
    public void demonstrateDaemon() {
        Thread daemon = new Thread(() -> {
            while (true) {
                System.out.println("Daemon running...");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        // TODO: Set as daemon and start
    }
}
```

---

### 6.2 Synchronization Exercises

```java
public class SynchronizationExercises {

    // 1. Thread-safe counter with synchronized
    class SynchronizedCounter {
        private int count = 0;

        public synchronized void increment() {
            // TODO: Implement
        }

        public synchronized int getCount() {
            // TODO: Implement
        }
    }

    // 2. Thread-safe counter with ReentrantLock
    class LockCounter {
        private int count = 0;
        private final ReentrantLock lock = new ReentrantLock();

        public void increment() {
            // TODO: Implement with lock.lock()/unlock()
        }

        public int getCount() {
            // TODO: Implement
        }
    }

    // 3. Thread-safe counter with AtomicInteger
    class AtomicCounter {
        private AtomicInteger count = new AtomicInteger(0);

        public void increment() {
            // TODO: Implement using AtomicInteger
        }

        public int getCount() {
            // TODO: Implement
        }
    }

    // 4. Performance comparison
    public void comparePerformance() throws InterruptedException {
        int numThreads = 10;
        int incrementsPerThread = 10000;

        // TODO: Test all 3 implementations
        // Measure time taken for each
        // Verify final count equals numThreads * incrementsPerThread
    }

    // 5. Producer-Consumer with wait/notify
    class BoundedBuffer {
        private final int[] buffer = new int[10];
        private int count = 0;
        private int in = 0;
        private int out = 0;

        public synchronized void put(int item) throws InterruptedException {
            // TODO: Wait while buffer is full
            // Add item, notify consumers
        }

        public synchronized int take() throws InterruptedException {
            // TODO: Wait while buffer is empty
            // Remove item, notify producers
        }
    }
}
```

---

### 6.3 ExecutorService Exercises

```java
public class ExecutorServiceExercises {

    // 1. Create fixed thread pool and submit tasks
    public void fixedThreadPool() {
        ExecutorService executor = Executors.newFixedThreadPool(5);

        // TODO: Submit 10 tasks, each prints thread name
        // Shutdown executor properly
    }

    // 2. Submit Callable and get result
    public void callableExample() throws Exception {
        ExecutorService executor = Executors.newSingleThreadExecutor();

        Callable<String> task = () -> {
            Thread.sleep(1000);
            return "Hello from Callable!";
        };

        // TODO: Submit and get result using Future
    }

    // 3. Invoke all tasks and wait for completion
    public void invokeAllExample() throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(3);

        List<Callable<Integer>> tasks = Arrays.asList(
            () -> { Thread.sleep(1000); return 1; },
            () -> { Thread.sleep(2000); return 2; },
            () -> { Thread.sleep(3000); return 3; }
        );

        // TODO: Use invokeAll and process results
    }

    // 4. Find first completed task
    public void invokeAnyExample() throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(3);

        List<Callable<String>> tasks = Arrays.asList(
            () -> { Thread.sleep(3000); return "Slow"; },
            () -> { Thread.sleep(1000); return "Fast"; },
            () -> { Thread.sleep(2000); return "Medium"; }
        );

        // TODO: Use invokeAny to get fastest result
    }

    // 5. Scheduled executor
    public void scheduledExecutor() {
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);

        // TODO: Schedule task to run every 2 seconds, 5 times
        // Shutdown after completion
    }
}
```

---

### 6.4 CompletableFuture Exercises

```java
public class CompletableFutureExercises {

    // 1. Simple async operation
    public CompletableFuture<String> fetchData() {
        return CompletableFuture.supplyAsync(() -> {
            // Simulate API call
            try { Thread.sleep(1000); } catch (InterruptedException e) {}
            return "Data";
        });
    }

    // 2. Transform result
    public CompletableFuture<String> processData() {
        return fetchData()
            // TODO: Transform "Data" to "Processed: Data"
    }

    // 3. Handle exception
    public CompletableFuture<String> fetchDataWithFallback() {
        return CompletableFuture.supplyAsync(() -> {
            throw new RuntimeException("API Error");
        })
        // TODO: Return "Default data" on error
        ;
    }

    // 4. Combine two futures
    public CompletableFuture<String> combineFutures() {
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

        // TODO: Combine to get "Hello World"
    }

    // 5. Execute multiple futures and wait for all
    public CompletableFuture<Void> fetchMultiple() {
        CompletableFuture<String> f1 = fetchData();
        CompletableFuture<String> f2 = fetchData();
        CompletableFuture<String> f3 = fetchData();

        // TODO: Wait for all to complete
    }

    // 6. Real-world scenario: Order processing
    public CompletableFuture<OrderResult> processOrder(String orderId) {
        // TODO: Implement async order processing:
        // 1. Fetch order details (async)
        // 2. Check inventory (async, parallel)
        // 3. Process payment (after 1 & 2 complete)
        // 4. Send confirmation email (async)
        // 5. Handle errors at each step
    }
}
```

---

## 📝 BÀI TẬP 7: FILE I/O & NIO (2-3 giờ)

### 7.1 File Operations

```java
public class FileIOExercises {

    // 1. Read file content
    public static String readFile(String path) throws IOException {
        // TODO: Use Files.readString()
    }

    // 2. Write file content
    public static void writeFile(String path, String content) throws IOException {
        // TODO: Use Files.writeString()
    }

    // 3. Read file line by line
    public static List<String> readLines(String path) throws IOException {
        // TODO: Use Files.readAllLines()
    }

    // 4. Copy file
    public static void copyFile(String source, String dest) throws IOException {
        // TODO: Use Files.copy()
    }

    // 5. Walk directory tree
    public static List<Path> findAllFiles(Path startDir, String extension) throws IOException {
        // TODO: Use Files.walk() and filter by extension
    }

    // 6. Read file using Stream API
    public static Stream<String> streamLines(String path) throws IOException {
        // TODO: Use Files.lines()
    }

    // 7. Write with BufferedWriter
    public static void writeLargeFile(String path, List<String> lines) throws IOException {
        // TODO: Use try-with-resources with BufferedWriter
    }
}
```

---

## 📝 BÀI TẬP 8: DATE & TIME (2 giờ)

### 8.1 Java 8 Date/Time API

```java
public class DateTimeExercises {

    // 1. Get current date, time, and datetime
    public static void getCurrentDateTime() {
        // TODO: Use LocalDate, LocalTime, LocalDateTime
    }

    // 2. Create specific date
    public static LocalDate createSpecificDate() {
        // TODO: Create date for January 15, 2024
    }

    // 3. Parse date from string
    public static LocalDate parseDate(String dateString) {
        // TODO: Parse "2024-01-15" format
    }

    // 4. Format date to string
    public static String formatDate(LocalDate date) {
        // TODO: Format to "dd/MM/yyyy"
    }

    // 5. Calculate age from birthdate
    public static int calculateAge(LocalDate birthDate) {
        // TODO: Use Period.between()
    }

    // 6. Add/subtract time
    public static LocalDate addDays(LocalDate date, int days) {
        // TODO: Use plusDays/minusDays
    }

    // 7. Find days between two dates
    public static long daysBetween(LocalDate d1, LocalDate d2) {
        // TODO: Use ChronoUnit.DAYS.between()
    }

    // 8. Check if date is before/after another
    public static boolean isBefore(LocalDate d1, LocalDate d2) {
        // TODO: Use isBefore()
    }

    // 9. Get first/last day of month
    public static LocalDate getFirstDayOfMonth(LocalDate date) {
        // TODO: Use TemporalAdjusters
    }

    // 10. Work with timezones
    public static ZonedDateTime convertTimezone(LocalDateTime dt, ZoneId targetZone) {
        // TODO: Convert to target timezone
    }
}
```

---

## 📝 BÀI TẬP 9: CAPSTONE PROJECT (8-10 giờ)

### 9.1 Employee Management System

**Đề bài:** Build a complete employee management system combining all concepts

```java
// Requirements:
// 1. Employee class with proper encapsulation
// 2. Department enum with budget info
// 3. Custom exceptions for business rules
// 4. Thread-safe employee repository
// 5. Stream-based reporting
// 6. File-based persistence
// 7. Async operations for reports

// TODO: Implement the following:

enum Department {
    IT(100000),
    HR(50000),
    FINANCE(75000),
    MARKETING(60000);

    private final double budget;
    // Constructor, getter
}

class Employee {
    private String id;
    private String name;
    private Department department;
    private double salary;
    private LocalDate hireDate;

    // TODO: Constructor, getters, setters, toString, equals, hashCode
}

class EmployeeRepository {
    // TODO: Thread-safe repository using ConcurrentHashMap
    // Methods: add, remove, findById, findAll
}

class EmployeeService {
    private EmployeeRepository repository;

    // TODO: Implement business logic:
    // - hireEmployee (validate department budget)
    // - terminateEmployee
    // - giveRaise (with validation)
    // - transferDepartment

    // TODO: Implement reporting using Stream API:
    // - getAverageSalaryByDepartment
    // - getEmployeesHiredInYear
    // - getTotalBudgetUsage
}

class ReportService {
    private EmployeeService employeeService;

    // TODO: Generate async reports:
    // - generateAnnualReport (returns CompletableFuture)
    // - exportToCSV (writes to file)
    // - sendReportByEmail (simulated)
}

// Main application
public class EmployeeManagementSystem {
    public static void main(String[] args) {
        // TODO: Create demo with:
        // 1. Initialize repository with sample data
        // 2. Perform CRUD operations
        // 3. Generate reports
        // 4. Handle exceptions properly
        // 5. Use async operations for reports
    }
}
```

---

## ✅ CHECKLIST HOÀN THÀNH

Sau khi hoàn thành Phase 0, bạn sẽ:

- [ ] Thành thạo Java syntax và OOP
- [ ] Hiểu sâu Collections Framework
- [ ] Sử dụng thành thạo Stream API & Lambda
- [ ] Xử lý exception đúng cách
- [ ] Implement được multithreading cơ bản
- [ ] Làm việc với File I/O và NIO.2
- [ ] Sử dụng Java 8+ Date/Time API
- [ ] Build được application hoàn chỉnh

---

## 📤 CÁCH SUBMIT

1. Push code lên GitHub repository
2. Tạo file `PHASE0_SOLUTIONS.md` với:
   - Link đến GitHub
   - Giải pháp cho mỗi bài tập
   - Những gì học được
   - Khó khăn gặp phải

3. Submit qua PR hoặc share link trong team chat

---

## 🎯 ĐÁNH GIÁ

| Tiêu chí | Điểm tối đa |
|----------|-------------|
| Correctness (code chạy đúng) | 40% |
| Code quality (clean code) | 20% |
| Exception handling | 15% |
| Thread safety | 15% |
| Documentation (comments) | 10% |

---

## 🔜 SAU KHI HOÀN THÀNH

Sau Phase 0, bạn sẽ sẵn sàng cho:
- **Phase 1:** Spring Boot Core
- **Phase 2:** Database & JPA
- **Phase 3:** Microservices Patterns

Good luck! 🚀
