# Phase 0: Java Core Mastery - Lý Thuyết

> **Thời gian:** 4-6 tuần
> **Mục tiêu:** Nắm vững toàn bộ Java Core theo roadmap.sh/java
> **Quan trọng:** Đây là nền tảng cho Senior Java Developer!

---

## 📚 PHẦN 1: JAVA BASICS - CƠ BẢN

### 1.1 Basic Syntax & Variables

```java
// Variable declaration
int age = 25;
final double PI = 3.14159;  // Constant
String name = "John";

// Type inference (Java 10+)
var list = new ArrayList<String>();  // Infer from right side
```

**Variable Scopes:**
- **Local variables:** Trong method/block
- **Instance variables:** Của object
- **Static/Class variables:** Của class (shared)

---

### 1.2 Data Types

**Primitive Types (8 loại):**

| Type | Size | Default | Range |
|------|------|---------|-------|
| byte | 1 byte | 0 | -128 to 127 |
| short | 2 bytes | 0 | -32,768 to 32,767 |
| int | 4 bytes | 0 | -2³¹ to 2³¹-1 |
| long | 8 bytes | 0L | -2⁶³ to 2⁶³-1 |
| float | 4 bytes | 0.0f | ~6-7 decimal digits |
| double | 8 bytes | 0.0d | ~15 decimal digits |
| char | 2 bytes | '\u0000' | Unicode characters |
| boolean | 1 bit | false | true/false |

**Reference Types:**
- String, Arrays, Classes, Interfaces, Enums

---

### 1.3 Type Casting

```java
// Implicit (Widening) - Automatic
int myInt = 9;
double myDouble = myInt;  // 9.0

// Explicit (Narrowing) - Manual
double myDouble = 9.99;
int myInt = (int) myDouble;  // 9 (loses decimal)

// String parsing
String str = "123";
int num = Integer.parseInt(str);
double d = Double.parseDouble(str);
```

---

### 1.4 Strings and Methods

```java
// String creation
String s1 = "Hello";  // String literal (String Pool)
String s2 = new String("Hello");  // Heap object

// Important methods
s1.length();
s1.charAt(0);
s1.substring(1, 4);
s1.toUpperCase();
s1.toLowerCase();
s1.trim();
s1.replace("l", "L");
s1.split(",");
s1.contains("ell");
s1.startsWith("He");
s1.endsWith("lo");

// String concatenation
String result = "Hello" + " " + "World";  // Uses StringBuilder internally

// String comparison
"abc".equals("abc");      // true (content)
"abc" == "abc";           // true (reference - String Pool)
"abc".compareTo("abd");   // negative (lexicographical)
```

**String Pool:**
```
String s1 = "Java";   // Created in String Pool
String s2 = "Java";   // Reuses s1 from Pool
String s3 = new String("Java");  // New object in Heap

s1 == s2   // true (same reference)
s1 == s3   // false (different references)
s1.equals(s3)  // true (same content)
```

---

### 1.5 Conditionals

```java
// if-else
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {
    grade = "B";
} else {
    grade = "C";
}

// switch (traditional)
switch (day) {
    case MONDAY:
        System.out.println("Monday");
        break;
    case TUESDAY:
        System.out.println("Tuesday");
        break;
    default:
        System.out.println("Other day");
}

// switch expression (Java 14+)
String result = switch (day) {
    case MONDAY, TUESDAY -> "Weekday";
    case SATURDAY, SUNDAY -> "Weekend";
    default -> "Unknown";
};
```

---

### 1.6 Arrays

```java
// Declaration
int[] numbers;
String[] names;

// Initialization
int[] numbers = {1, 2, 3, 4, 5};
int[] numbers = new int[5];  // All zeros
String[] names = new String[3];  // All null

// Multidimensional
int[][] matrix = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Common operations
Arrays.sort(numbers);
Arrays.binarySearch(numbers, 3);
Arrays.fill(numbers, 0);
int length = numbers.length;  // Property, not method!
```

---

### 1.7 Loops

```java
// for loop
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// enhanced for loop (for-each)
for (String name : names) {
    System.out.println(name);
}

// while loop
int i = 0;
while (i < 10) {
    System.out.println(i);
    i++;
}

// do-while loop
do {
    System.out.println(i);
    i++;
} while (i < 10);

// break and continue
for (int i = 0; i < 10; i++) {
    if (i == 5) break;      // Exit loop
    if (i % 2 == 0) continue;  // Skip to next iteration
    System.out.println(i);
}
```

---

### 1.8 Math Operations

```java
// Math class methods
Math.abs(-5);           // 5
Math.ceil(4.3);         // 5.0
Math.floor(4.7);        // 4.0
Math.round(4.5);        // 5
Math.sqrt(16);          // 4.0
Math.pow(2, 3);         // 8.0
Math.random();          // 0.0 to 1.0
Math.max(5, 10);        // 10
Math.min(5, 10);        // 5

// Random class
Random rand = new Random();
int randomInt = rand.nextInt(100);  // 0-99
double randomDouble = rand.nextDouble();  // 0.0-1.0
boolean randomBool = rand.nextBoolean();
```

---

### 1.9 Lifecycle of a Java Program

```
1. Write (.java file)
2. Compile (javac) → Bytecode (.class file)
3. Load (ClassLoader)
4. Verify (Bytecode Verifier)
5. Execute (JVM - JIT Compiler)
6. Garbage Collection (automatic memory management)
```

**JVM Memory Areas:**
```
┌─────────────────────────────────────┐
│         Heap (Shared)               │
│  - Object instances                 │
│  - Arrays                           │
│  - GC managed                       │
├─────────────────────────────────────┤
│         Stack (Per Thread)          │
│  - Local variables                  │
│  - Method frames                    │
│  - Call stack                       │
├─────────────────────────────────────┤
│         Metaspace                   │
│  - Class metadata                   │
│  - Static variables                 │
└─────────────────────────────────────┘
```

---

## 📚 PHẦN 2: OBJECT ORIENTED PROGRAMMING (OOP)

### 2.1 Classes and Objects

```java
// Class definition
public class Person {
    // Fields (attributes)
    private String name;
    private int age;

    // Constructor
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Methods (behavior)
    public void sayHello() {
        System.out.println("Hello, I'm " + name);
    }

    // Getters/Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}

// Creating objects
Person person = new Person("John", 30);
person.sayHello();
```

---

### 2.2 Access Specifiers

| Modifier | Class | Package | Subclass | World |
|----------|-------|---------|----------|-------|
| public | ✅ | ✅ | ✅ | ✅ |
| protected | ✅ | ✅ | ✅ | ❌ |
| default (no modifier) | ✅ | ✅ | ❌ | ❌ |
| private | ✅ | ❌ | ❌ | ❌ |

```java
public class AccessDemo {
    public int publicVar = 1;      // Accessible everywhere
    protected int protectedVar = 2; // Package + subclasses
    int defaultVar = 3;            // Package only
    private int privateVar = 4;    // Class only
}
```

---

### 2.3 Static Keyword

```java
public class Counter {
    // Static variable (shared across all instances)
    private static int count = 0;

    // Instance variable
    private int value;

    // Static method (can only access static members)
    public static int getCount() {
        return count;
    }

    // Static block (runs once when class loads)
    static {
        System.out.println("Counter class loaded!");
    }

    // Static nested class
    static class Helper {
        void help() { /* can't access instance members */ }
    }
}

// Usage
Counter.getCount();  // No instance needed
Counter.Helper h = new Counter.Helper();
```

---

### 2.4 Nested Classes

```java
public class OuterClass {
    private String outerField = "Outer";

    // Static nested class
    static class StaticNested {
        void display() {
            // Can't access outerField directly
        }
    }

    // Inner class (non-static)
    class InnerClass {
        void display() {
            System.out.println(outerField);  // Can access
        }
    }

    // Local inner class (inside method)
    public void method() {
        class LocalClass {
            void display() {
                System.out.println(outerField);
            }
        }
    }

    // Anonymous inner class
    Runnable r = new Runnable() {
        public void run() {
            System.out.println("Running");
        }
    };
}
```

---

### 2.5 Method Overloading vs Overriding

```java
// Overloading (Compile-time polymorphism)
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public double add(double a, double b) {
        return a + b;
    }

    public int add(int a, int b, int c) {
        return a + b + c;
    }
}

// Overriding (Runtime polymorphism)
class Animal {
    void sound() {
        System.out.println("Some sound");
    }
}

class Dog extends Animal {
    @Override  // Annotation (optional but recommended)
    void sound() {
        System.out.println("Bark");
    }
}
```

**Rules for Overriding:**
- Same method signature
- Same return type (or covariant)
- Cannot reduce visibility
- Cannot throw broader checked exceptions

---

### 2.6 Inheritance

```java
// extends for classes
class Animal {
    void eat() { System.out.println("Eating..."); }
}

class Dog extends Animal {
    void bark() { System.out.println("Barking..."); }
}

// implements for interfaces
interface Swimmable {
    void swim();
}

class Fish implements Swimmable {
    public void swim() { System.out.println("Swimming..."); }
}

// Multiple interfaces
class Amphibian implements Swimmable, Walkable {
    public void swim() { /* ... */ }
    public void walk() { /* ... */ }
}
```

**Important:**
- Java doesn't support multiple inheritance (classes)
- Supports multiple interface implementation
- `super` keyword to call parent methods/constructors

---

### 2.7 Abstract Classes

```java
abstract class Shape {
    // Abstract method (no implementation)
    abstract double area();

    // Concrete method
    void display() {
        System.out.println("Displaying shape");
    }

    // Can have constructors
    public Shape() {
        System.out.println("Shape constructor");
    }
}

class Circle extends Shape {
    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    double area() {
        return Math.PI * radius * radius;
    }
}
```

**Abstract Class vs Interface:**

| Feature | Abstract Class | Interface |
|---------|---------------|-----------|
| Methods | Abstract + concrete | All abstract (before Java 8) |
| Variables | Any type | public static final only |
| Constructors | Yes | No |
| Inheritance | Single | Multiple |
| When to use | Related classes | Unrelated classes with common capability |

---

### 2.8 Interfaces

```java
// Basic interface
interface Flyable {
    void fly();  // public abstract by default
}

// Interface with default methods (Java 8+)
interface Vehicle {
    void start();

    default void stop() {
        System.out.println("Stopping...");
    }

    static void honk() {
        System.out.println("Honking!");
    }
}

// Interface with private methods (Java 9+)
interface PaymentProcessor {
    void processPayment(double amount);

    private boolean validateAmount(double amount) {
        return amount > 0;
    }

    private void logTransaction(String message) {
        System.out.println(message);
    }
}

// Marker interface (no methods)
interface Serializable {
    // Just a marker for JVM
}
```

---

### 2.9 Encapsulation

```java
public class BankAccount {
    // Private fields
    private String accountNumber;
    private double balance;

    // Public getters/setters with validation
    public String getAccountNumber() {
        return accountNumber;
    }

    public void setAccountNumber(String accountNumber) {
        if (accountNumber != null && accountNumber.length() == 10) {
            this.accountNumber = accountNumber;
        }
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            return true;
        }
        return false;
    }
}
```

---

### 2.10 Enums

```java
// Basic enum
enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}

// Enum with fields and methods
enum Status {
    PENDING("Pending approval"),
    APPROVED("Approved"),
    REJECTED("Rejected"),
    COMPLETED("Completed");

    private final String description;

    Status(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}

// Usage
Status status = Status.APPROVED;
String desc = status.getDescription();

// Enum in switch
switch (status) {
    case PENDING -> System.out.println("Waiting...");
    case APPROVED -> System.out.println("Good!");
    default -> System.out.println("Other");
}
```

---

### 2.11 Final Keyword

```java
// final variable (constant)
final int MAX_VALUE = 100;
// MAX_VALUE = 101;  // ERROR!

// final method (cannot be overridden)
class Parent {
    public final void display() {
        System.out.println("Cannot override");
    }
}

// final class (cannot be inherited)
final class UtilityClass {
    // Cannot extend this class
}

// final parameter
public void method(final int x) {
    // x = 10;  // ERROR! Cannot modify final parameter
}
```

---

### 2.12 Object Lifecycle

```java
public class LifecycleDemo {
    // Constructor
    public LifecycleDemo() {
        System.out.println("Object created");
    }

    // finalize() - Called before GC (deprecated in Java 9+)
    @Deprecated
    protected void finalize() {
        System.out.println("Object being garbage collected");
    }

    // toString() - String representation
    @Override
    public String toString() {
        return "LifecycleDemo{}";
    }

    // equals() - Content comparison
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        LifecycleDemo that = (LifecycleDemo) o;
        return true;
    }

    // hashCode() - For hash-based collections
    @Override
    public int hashCode() {
        return Objects.hash(/* fields */);
    }
}

// Usage
LifecycleDemo obj = new LifecycleDemo();  // Created
obj = null;  // Eligible for GC
System.gc();  // Suggest GC (not guaranteed)
```

---

### 2.13 Static vs Dynamic Binding

```java
// Static Binding (Compile-time)
class Dog {
    void bark() { System.out.println("Bark"); }
}

Dog myDog = new Dog();
myDog.bark();  // Resolved at compile time

// Dynamic Binding (Runtime)
class Animal {
    void sound() { System.out.println("Animal sound"); }
}

class Cat extends Animal {
    @Override
    void sound() { System.out.println("Meow"); }
}

Animal myPet = new Cat();
myPet.sound();  // "Meow" - Resolved at runtime (polymorphism)
```

---

### 2.14 Method Chaining

```java
public class Builder {
    private String name;
    private int age;

    public Builder setName(String name) {
        this.name = name;
        return this;  // Return current object
    }

    public Builder setAge(int age) {
        this.age = age;
        return this;
    }

    public Builder build() {
        return this;
    }
}

// Usage
Builder builder = new Builder()
    .setName("John")
    .setAge(30)
    .build();
```

---

### 2.15 Packages

```java
// Package declaration (top of file)
package com.example.myapp;

// Import statements
import java.util.ArrayList;
import java.util.List;
import static java.lang.Math.PI;  // Static import
import static java.lang.System.out;  // Static import

// Common package structure
/*
com.example.myapp/
├── controller/
├── service/
├── repository/
├── model/
├── dto/
├── config/
└── util/
*/
```

---

### 2.16 Initializer Blocks

```java
public class InitializerDemo {
    // Static initializer (runs once when class loads)
    static {
        System.out.println("Static block");
    }

    // Instance initializer (runs before constructor)
    {
        System.out.println("Instance block");
    }

    // Constructor
    public InitializerDemo() {
        System.out.println("Constructor");
    }

    public static void main(String[] args) {
        new InitializerDemo();
        // Output:
        // Static block
        // Instance block
        // Constructor
    }
}
```

---

### 2.17 Pass by Value vs Pass by Reference

```java
// Java is ALWAYS pass-by-value

// Primitive types
void modifyPrimitive(int x) {
    x = 100;  // Only modifies copy
}

int a = 10;
modifyPrimitive(a);
System.out.println(a);  // Still 10!

// Object references
void modifyObject(StringBuilder sb) {
    sb.append(" World");  // Modifies the object
    sb = new StringBuilder("New");  // Only modifies local copy of reference
}

StringBuilder sb = new StringBuilder("Hello");
modifyObject(sb);
System.out.println(sb);  // "Hello World" (object modified)
```

**Key Point:** Java passes the VALUE of the reference, not the reference itself.

---

## 📚 PHẦN 3: COLLECTIONS FRAMEWORK

### 3.1 Collections Hierarchy

```
Iterable
  └── Collection
      ├── List
      │   ├── ArrayList
      │   ├── LinkedList
      │   └── Vector (legacy, use ArrayList)
      ├── Set
      │   ├── HashSet
      │   ├── LinkedHashSet
      │   └── TreeSet
      └── Queue
          ├── PriorityQueue
          └── Deque
              ├── ArrayDeque
              └── LinkedList

Map (separate hierarchy)
├── HashMap
├── LinkedHashMap
├── TreeMap
└── Hashtable (legacy, use ConcurrentHashMap)
```

---

### 3.2 List Implementations

```java
// ArrayList - Fast random access, slow insert/delete in middle
List<String> arrayList = new ArrayList<>();
arrayList.add("A");
arrayList.add(0, "B");  // Shifts elements
arrayList.get(0);       // O(1)
arrayList.remove(0);    // O(n)

// LinkedList - Fast insert/delete, slow random access
List<String> linkedList = new LinkedList<>();
linkedList.add("A");
linkedList.addFirst("B");
linkedList.addLast("C");
linkedList.get(0);      // O(n)
linkedList.removeFirst(); // O(1)

// Vector - Thread-safe (legacy)
List<String> vector = new Vector<>();
```

**When to use:**
- ArrayList: Most common, read-heavy
- LinkedList: Frequent insert/delete at ends

---

### 3.3 Set Implementations

```java
// HashSet - No order, O(1) operations
Set<String> hashSet = new HashSet<>();
hashSet.add("A");
hashSet.add("B");
hashSet.contains("A");  // O(1)

// LinkedHashSet - Insertion order
Set<String> linkedHashSet = new LinkedHashSet<>();
linkedHashSet.add("A");
linkedHashSet.add("B");  // Will iterate A, B

// TreeSet - Sorted order
Set<String> treeSet = new TreeSet<>();
treeSet.add("C");
treeSet.add("A");
treeSet.add("B");  // Will iterate A, B, C
```

---

### 3.4 Map Implementations

```java
// HashMap - No order, O(1) operations
Map<String, Integer> hashMap = new HashMap<>();
hashMap.put("A", 1);
hashMap.get("A");  // O(1)
hashMap.remove("A");

// LinkedHashMap - Insertion order
Map<String, Integer> linkedMap = new LinkedHashMap<>();

// TreeMap - Sorted by keys
Map<String, Integer> treeMap = new TreeMap<>();

// Hashtable - Thread-safe (legacy)
Map<String, Integer> hashtable = new Hashtable<>();

// ConcurrentHashMap - Thread-safe (recommended)
Map<String, Integer> concurrentMap = new ConcurrentHashMap<>();
```

---

### 3.5 Queue and Deque

```java
// Queue - FIFO
Queue<String> queue = new LinkedList<>();
queue.offer("A");  // Add (returns false if fails)
queue.poll();      // Remove and return head (null if empty)
queue.peek();      // View head (null if empty)

// PriorityQueue - Ordered by priority
Queue<Integer> pq = new PriorityQueue<>();
pq.offer(10);
pq.offer(5);
pq.offer(20);
pq.poll();  // Returns 5 (smallest)

// Deque - Double-ended queue
Deque<String> deque = new ArrayDeque<>();
deque.push("A");      // Add to front (stack)
deque.pop();          // Remove from front
deque.offerFirst("B");
deque.offerLast("C");
deque.pollFirst();
deque.pollLast();
```

---

### 3.6 Iterator

```java
List<String> list = new ArrayList<>(Arrays.asList("A", "B", "C"));

// Using Iterator
Iterator<String> iterator = list.iterator();
while (iterator.hasNext()) {
    String item = iterator.next();
    if (item.equals("B")) {
        iterator.remove();  // Safe removal during iteration
    }
}

// Using forEach (Java 8+)
list.forEach(System.out::println);

// ListIterator (for List only)
ListIterator<String> listIterator = list.listIterator();
while (listIterator.hasNext()) {
    String item = listIterator.next();
    listIterator.set(item.toUpperCase());  // Can modify
    listIterator.add("New");  // Can add
}
```

---

### 3.7 Generic Collections

```java
// Before generics (unsafe)
List list = new ArrayList();
list.add("String");
list.add(123);  // Compiles but dangerous!
String s = (String) list.get(0);  // Cast required

// With generics (type-safe)
List<String> list = new ArrayList<>();
list.add("String");
// list.add(123);  // Compile error!
String s = list.get(0);  // No cast needed

// Generic class
class Box<T> {
    private T content;

    public void set(T content) {
        this.content = content;
    }

    public T get() {
        return content;
    }
}

Box<String> stringBox = new Box<>();
stringBox.set("Hello");

// Bounded type parameters
class NumberBox<T extends Number> {
    private T value;
    // T can be Integer, Double, etc.
}
```

---

### 3.8 Array vs ArrayList

| Feature | Array | ArrayList |
|---------|-------|-----------|
| Size | Fixed | Dynamic |
| Type | Primitive + Object | Object only |
| Performance | Faster | Slightly slower |
| Methods | Limited | Rich API |
| Memory | Less | More (overhead) |

```java
// Array
int[] arr = {1, 2, 3};
int first = arr[0];

// ArrayList
List<Integer> list = new ArrayList<>();
list.add(1);
list.add(2);
int first = list.get(0);

// Conversion
int[] array = list.stream().mapToInt(i -> i).toArray();
List<Integer> list = Arrays.stream(array).boxed().collect(Collectors.toList());
```

---

## 📚 PHẦN 4: FUNCTIONAL PROGRAMMING

### 4.1 Lambda Expressions

```java
// Before (Anonymous class)
Runnable r = new Runnable() {
    public void run() {
        System.out.println("Running");
    }
};

// After (Lambda)
Runnable r = () -> System.out.println("Running");

// With parameters
Comparator<String> comp = (s1, s2) -> s1.compareTo(s2);

// With body
Runnable r = () -> {
    System.out.println("Starting");
    // Multiple statements
    System.out.println("Running");
};

// Method reference (shorthand for lambda)
list.forEach(System.out::println);  // Instead of: x -> System.out.println(x)
```

---

### 4.2 Functional Interfaces

```java
// Predefined functional interfaces

// Predicate<T> - Takes T, returns boolean
Predicate<String> isEmpty = s -> s == null || s.isEmpty();
boolean result = isEmpty.test("Hello");

// Function<T, R> - Takes T, returns R
Function<String, Integer> length = String::length;
Integer len = length.apply("Hello");

// Consumer<T> - Takes T, returns void
Consumer<String> printer = System.out::println;
printer.accept("Hello");

// Supplier<T> - Takes nothing, returns T
Supplier<Double> random = Math::random;
Double d = random.get();

// UnaryOperator<T> - Takes T, returns T
UnaryOperator<String> upper = String::toUpperCase;

// BinaryOperator<T> - Takes two T, returns T
BinaryOperator<Integer> sum = (a, b) -> a + b;
```

---

### 4.3 High Order Functions

```java
// Functions that take or return functions

// Function composition
Function<Integer, Integer> addOne = x -> x + 1;
Function<Integer, Integer> multiplyByTwo = x -> x * 2;

// andThen: f then g
Function<Integer, Integer> composed = addOne.andThen(multiplyByTwo);
composed.apply(5);  // (5 + 1) * 2 = 12

// compose: g then f
Function<Integer, Integer> composed2 = addOne.compose(multiplyByTwo);
composed2.apply(5);  // (5 * 2) + 1 = 11

// Chaining predicates
Predicate<String> notEmpty = s -> !s.isEmpty();
Predicate<String> hasLength = s -> s.length() > 3;
Predicate<String> combined = notEmpty.and(hasLength);
```

---

### 4.4 Stream API

```java
List<String> names = Arrays.asList("John", "Jane", "Bob", "Alice");

// Stream pipeline
List<String> result = names.stream()
    .filter(s -> s.startsWith("J"))      // Intermediate
    .map(String::toUpperCase)            // Intermediate
    .sorted()                            // Intermediate
    .collect(Collectors.toList());       // Terminal

// Stream operations classification
/*
Intermediate (lazy, return Stream):
- filter(), map(), flatMap()
- sorted(), distinct()
- limit(), skip()

Terminal (eager, return value/void):
- collect(), forEach()
- reduce(), count()
- min(), max()
- anyMatch(), allMatch(), noneMatch()
- findFirst(), findAny()
*/

// Parallel stream (for large data)
List<String> parallelResult = names.parallelStream()
    .filter(s -> s.startsWith("J"))
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

---

### 4.5 Stream Collectors

```java
// Basic collectors
List<String> list = stream.collect(Collectors.toList());
Set<String> set = stream.collect(Collectors.toSet());
Map<String, Integer> map = stream.collect(
    Collectors.toMap(String::toLowerCase, String::length)
);

// Joining
String joined = stream.collect(Collectors.joining(", "));
String withPrefix = stream.collect(Collectors.joining(", ", "[", "]"));

// Grouping
Map<String, List<Employee>> byDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDepartment));

// Partitioning
Map<Boolean, List<Employee>> bySalary = employees.stream()
    .collect(Collectors.partitioningBy(e -> e.getSalary() > 50000));

// Aggregation
Double avgSalary = employees.stream()
    .collect(Collectors.averagingDouble(Employee::getSalary));

Integer sumSalary = employees.stream()
    .collect(Collectors.summingInt(Employee::getSalary));

Long count = employees.stream()
    .collect(Collectors.counting());

// Custom collector
Map<String, String> map = employees.stream()
    .collect(Collectors.toMap(
        Employee::getName,
        Employee::getDepartment,
        (v1, v2) -> v1  // Merge function for duplicate keys
    ));
```

---

## 📚 PHẦN 5: EXCEPTION HANDLING

### 5.1 Exception Hierarchy

```
Throwable
├── Error (unchecked, serious problems)
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── ...
└── Exception
    ├── Checked Exception (must handle)
    │   ├── IOException
    │   ├── SQLException
    │   └── ...
    └── RuntimeException (unchecked)
        ├── NullPointerException
        ├── IllegalArgumentException
        ├── IllegalStateException
        └── ...
```

---

### 5.2 Try-Catch-Finally

```java
// Basic try-catch
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Cannot divide by zero");
}

// Multiple catch blocks
try {
    // Some code
} catch (IOException e) {
    log.error("IO error", e);
} catch (SQLException e) {
    log.error("DB error", e);
} finally {
    // Always executes (cleanup)
    closeResources();
}

// Multi-catch (Java 7+)
try {
    // Some code
} catch (IOException | SQLException e) {
    log.error("Error", e);
}

// Try-with-resources (Java 7+)
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"));
     PreparedStatement stmt = conn.prepareStatement(sql)) {
    // Auto-closed at end
    return reader.readLine();
}  // No finally needed!
```

---

### 5.3 Custom Exceptions

```java
// Checked exception
public class InsufficientFundsException extends Exception {
    public InsufficientFundsException() {
        super("Insufficient funds");
    }

    public InsufficientFundsException(double amount) {
        super("Insufficient funds: $" + amount);
    }
}

// Unchecked exception
public class InvalidUserException extends RuntimeException {
    public InvalidUserException(String message) {
        super(message);
    }
}

// Usage
public void withdraw(double amount) throws InsufficientFundsException {
    if (amount > balance) {
        throw new InsufficientFundsException(amount);
    }
    balance -= amount;
}
```

---

## 📚 PHẦN 6: ANNOTATIONS

### 6.1 Built-in Annotations

```java
@Override  // Override verification
@Deprecated  // Mark as deprecated
@SuppressWarnings("unchecked")  // Suppress warnings

// Meta-annotations (for creating annotations)
@Target(ElementType.METHOD)  // Where annotation can be applied
@Retention(RetentionPolicy.RUNTIME)  // When it's available
@Documented  // Include in javadoc
@Inherited  // Inherited by subclasses
```

---

### 6.2 Custom Annotations

```java
// Define annotation
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface LogExecutionTime {
    String value() default "INFO";  // Optional with default
}

// Use annotation
@LogExecutionTime("DEBUG")
public void processOrder(Order order) {
    // Method implementation
}

// Process annotation (Reflection)
Method[] methods = MyClass.class.getMethods();
for (Method method : methods) {
    if (method.isAnnotationPresent(LogExecutionTime.class)) {
        LogExecutionTime annotation = method.getAnnotation(LogExecutionTime.class);
        String level = annotation.value();
        // Process annotation
    }
}
```

---

## 📚 PHẦN 7: CONCURRENCY

### 7.1 Thread Creation

```java
// Extending Thread class
class MyThread extends Thread {
    public void run() {
        System.out.println("Running in: " + Thread.currentThread().getName());
    }
}
MyThread t1 = new MyThread();
t1.start();

// Implementing Runnable
class MyRunnable implements Runnable {
    public void run() {
        System.out.println("Running");
    }
}
Thread t2 = new Thread(new MyRunnable());
t2.start();

// Lambda (Java 8+)
Thread t3 = new Thread(() -> System.out.println("Running"));
t3.start();

// ExecutorService (Recommended)
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(() -> System.out.println("Running"));
executor.shutdown();
```

---

### 7.2 Thread Lifecycle

```
NEW → RUNNABLE → RUNNING → BLOCKED/WAITING/TIMED_WAITING → TERMINATED

NEW: Thread created, not started
RUNNABLE: Ready to run, waiting for CPU
RUNNING: Executing
BLOCKED: Waiting for monitor lock
WAITING: Waiting for another thread (wait(), join(), park())
TIMED_WAITING: Waiting with timeout (sleep(ms), wait(ms))
TERMINATED: Finished execution
```

---

### 7.3 Synchronization

```java
// synchronized method
public synchronized void increment() {
    count++;
}

// synchronized block
public void increment() {
    synchronized(this) {
        count++;
    }
}

// synchronized static method
public static synchronized void increment() {
    count++;  // Locks on class object
}
```

---

### 7.4 Volatile Keyword

```java
// volatile ensures visibility across threads
private volatile boolean running = true;

public void stop() {
    running = false;  // Visible to all threads immediately
}

public void run() {
    while (running) {
        // do work
    }
}

// volatile does NOT ensure atomicity!
private volatile int count = 0;
public void increment() {
    count++;  // NOT thread-safe! Use AtomicInteger
}
```

---

### 7.5 java.util.concurrent Utilities

```java
// AtomicInteger/AtomicLong/AtomicReference
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet();
count.getAndAdd(5);

// CountDownLatch
CountDownLatch latch = new CountDownLatch(3);
// 3 threads do work, then countDown()
// Main thread waits: latch.await()

// CyclicBarrier (reusable)
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All threads reached barrier");
});

// Semaphore
Semaphore semaphore = new Semaphore(5);  // 5 permits
semaphore.acquire();  // Take permit
// ... do work ...
semaphore.release();  // Return permit

// Exchanger
Exchanger<String> exchanger = new Exchanger<>();
String data = exchanger.exchange(myData);  // Swap with another thread
```

---

### 7.6 ExecutorService & Thread Pools

```java
// Fixed thread pool
ExecutorService fixedPool = Executors.newFixedThreadPool(10);

// Cached thread pool (creates threads as needed)
ExecutorService cachedPool = Executors.newCachedThreadPool();

// Single thread executor
ExecutorService singleThread = Executors.newSingleThreadExecutor();

// Scheduled thread pool
ScheduledExecutorService scheduledPool = Executors.newScheduledThreadPool(5);
scheduledPool.scheduleAtFixedRate(task, 0, 1, TimeUnit.MINUTES);

// Custom thread pool (Recommended for production)
ExecutorService customPool = new ThreadPoolExecutor(
    5,              // corePoolSize
    20,             // maxPoolSize
    60L,            // keepAliveTime
    TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(1000),  // Bounded queue
    new ThreadPoolExecutor.CallerRunsPolicy()  // Rejection policy
);

// Graceful shutdown
executor.shutdown();
if (!executor.awaitTermination(30, TimeUnit.SECONDS)) {
    executor.shutdownNow();
}
```

---

### 7.7 CompletableFuture

```java
// Supply async
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> fetchData());

// Then apply
CompletableFuture<String> result = future
    .thenApply(data -> processData(data));

// Then accept (consume result)
future.thenAccept(System.out::println);

// Then run (no return)
future.thenRun(() -> System.out.println("Done"));

// Exception handling
future.exceptionally(ex -> {
    log.error("Error", ex);
    return "default";
});

// Combine futures
CompletableFuture<String> combined = future1
    .thenCombine(future2, (r1, r2) -> r1 + r2);

// All of
CompletableFuture<Void> allDone = CompletableFuture
    .allOf(future1, future2, future3);

// Any of
CompletableFuture<Object> anyDone = CompletableFuture
    .anyOf(future1, future2, future3);
```

---

## 📚 PHẦN 8: I/O AND NIO

### 8.1 File Operations (Java NIO.2)

```java
Path path = Paths.get("file.txt");

// Read
String content = Files.readString(path);
List<String> lines = Files.readAllLines(path);
byte[] bytes = Files.readAllBytes(path);

// Write
Files.writeString(path, "Hello");
Files.write(path, lines);

// File operations
Files.copy(source, target);
Files.move(source, target);
Files.delete(path);
boolean exists = Files.exists(path);
boolean isDir = Files.isDirectory(path);

// Walk directory
Files.walk(Paths.get("/home"))
    .filter(Files::isRegularFile)
    .forEach(System.out::println);
```

---

### 8.2 Networking

```java
// HTTP Client (Java 11+)
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .GET()
    .build();

HttpResponse<String> response = client.send(
    request,
    HttpResponse.BodyHandlers.ofString()
);

// Async
client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(System.out::println);
```

---

### 8.3 Regular Expressions

```java
// Pattern and Matcher
Pattern pattern = Pattern.compile("\\d{3}-\\d{4}");
Matcher matcher = pattern.matcher("123-4567");
boolean matches = matcher.matches();

// Common patterns
String emailRegex = "^[A-Za-z0-9+_.-]+@(.+)$";
String phoneRegex = "\\d{3}-\\d{3}-\\d{4}";
String urlRegex = "https?://[^\s]+";

// String methods
"Hello123".matches("\\w+");  // true
"123".replaceAll("\\d", "X");  // "XXX"
"abc123def".split("\\d");  // ["abc", "def"]
```

---

### 8.4 Date and Time (Java 8+)

```java
// LocalDate (date only)
LocalDate today = LocalDate.now();
LocalDate specific = LocalDate.of(2024, 1, 15);
LocalDate parsed = LocalDate.parse("2024-01-15");

// LocalTime (time only)
LocalTime now = LocalTime.now();

// LocalDateTime (date and time)
LocalDateTime dt = LocalDateTime.now();
LocalDateTime dt = LocalDateTime.of(2024, 1, 15, 10, 30);

// ZonedDateTime (with timezone)
ZonedDateTime zoned = ZonedDateTime.now(ZoneId.of("America/New_York"));

// Duration and Period
Duration duration = Duration.between(time1, time2);
Period period = Period.between(date1, date2);

// Formatting
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
String formatted = LocalDate.now().format(formatter);
LocalDate parsed = LocalDate.parse("15/01/2024", formatter);
```

---

## 📚 PHẦN 9: RECORDS (JAVA 14+)

```java
// Traditional class
public class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    @Override
    public boolean equals(Object o) { /* ... */ }

    @Override
    public int hashCode() { /* ... */ }

    @Override
    public String toString() { /* ... */ }
}

// Record (Java 14+)
public record Point(int x, int y) {
    // Compact constructor
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Coordinates must be positive");
        }
    }
}

// Usage
Point p = new Point(10, 20);
int x = p.x();  // Auto-generated accessor
```

---

## 📚 PHẦN 10: OPTIONAL

```java
// Creating Optional
Optional<String> empty = Optional.empty();
Optional<String> of = Optional.of("value");  // Null not allowed
Optional<String> ofNullable = Optional.ofNullable(maybeNull);

// Getting value
String value = optional.orElse("default");
String value = optional.orElseGet(() -> generateDefault());
String value = optional.orElseThrow(() -> new IllegalStateException());
String value = optional.get();  // Throws if empty!

// Transforming
Optional<Integer> length = optional.map(String::length);
Optional<Integer> length = optional.flatMap(s -> Optional.of(s.length()));

// Filtering
Optional<String> filtered = optional.filter(s -> s.length() > 3);

// Checking
boolean present = optional.isPresent();
boolean empty = optional.isEmpty();

// Consuming
optional.ifPresent(System.out::println);
optional.ifPresentOrElse(
    System.out::println,
    () -> System.out.println("Empty")
);
```

---

## 📝 TÓM TẮT

### Các chủ đề cần nắm vững:

1. **Basics:** Syntax, Data Types, Strings, Arrays, Loops
2. **OOP:** Classes, Inheritance, Polymorphism, Encapsulation, Abstraction
3. **Collections:** List, Set, Map, Queue, Iterator, Generics
4. **Functional Programming:** Lambda, Stream API, Functional Interfaces
5. **Exception Handling:** Try-catch, Custom exceptions
6. **Concurrency:** Threads, Synchronization, ExecutorService, CompletableFuture
7. **I/O:** File operations, Networking, Regex, Date/Time
8. **Modern Java:** Records, Optional, Modules, Annotations

---

## 🔜 TIẾP THEO

Đọc `02-examples.md` để xem code mẫu thực tế và `03-exercises.md` để làm bài tập!
