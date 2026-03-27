# Design Patterns - Theory

> **Thời gian:** 3 tuần
> **Mục tiêu:** Master các design patterns phổ biến trong Java/Spring
>
> **Tham khảo:** [java-design-patterns.com](https://java-design-patterns.com)

---

## 📚 BÀI 0: DESIGN PATTERNS OVERVIEW

### 0.1 What are Design Patterns?

```
Design Pattern = Giải pháp tối ưu cho vấn đề thiết kế code thường gặp

Đặc điểm:
- Không phải code cụ thể, mà là template/ý tưởng
- Có thể áp dụng cho nhiều ngôn ngữ
- Giải quyết vấn đề thiết kế lặp đi lặp lại
- Được kiểm chứng qua thời gian
```

### 0.2 Pattern Categories

```
┌─────────────────────────────────────────────────────────────┐
│              DESIGN PATTERNS CATEGORIES                      │
├─────────────────────────────────────────────────────────────┤
│  CREATIONAL PATTERNS (5 patterns)                            │
│  - Singleton                                                 │
│  - Builder                                                   │
│  - Factory Method                                            │
│  - Abstract Factory                                          │
│  - Prototype                                                 │
│  → Tạo objects một cách linh hoạt                            │
├─────────────────────────────────────────────────────────────┤
│  STRUCTURAL PATTERNS (7 patterns)                            │
│  - Adapter                                                   │
│  - Bridge                                                    │
│  - Composite                                                 │
│  - Decorator                                                 │
│  - Facade                                                    │
│  - Flyweight                                                 │
│  - Proxy                                                     │
│  → Tổ chức classes/objects thành cấu trúc lớn hơn            │
├─────────────────────────────────────────────────────────────┤
│  BEHAVIORAL PATTERNS (9 patterns)                            │
│  - Chain of Responsibility                                   │
│  - Command                                                   │
│  - Interpreter                                               │
│  - Iterator                                                  │
│  - Mediator                                                  │
│  - Memento                                                   │
│  - Observer                                                  │
│  - State                                                     │
│  - Strategy                                                  │
│  - Template Method                                           │
│  - Visitor                                                   │
│  → Communication giữa objects                                │
└─────────────────────────────────────────────────────────────┘
```

### 0.3 SOLID Principles

```
┌─────────────────────────────────────────────────────────────┐
│                    SOLID PRINCIPLES                          │
├─────────────────────────────────────────────────────────────┤
│  S - Single Responsibility Principle                         │
│  - Một class chỉ có một lý do để thay đổi                    │
│  - Một class chỉ làm một việc                                │
├─────────────────────────────────────────────────────────────┤
│  O - Open/Closed Principle                                   │
│  - Open for extension                                        │
│  - Closed for modification                                   │
│  - Thêm tính năng mới bằng cách thêm code, không sửa code cũ │
├─────────────────────────────────────────────────────────────┤
│  L - Liskov Substitution Principle                           │
│  - Subclasses phải thay thế được base class                  │
│  - Không phá vỡ chương trình khi dùng subclass              │
├─────────────────────────────────────────────────────────────┤
│  I - Interface Segregation Principle                         │
│  - Nhiều interface nhỏ tốt hơn 1 interface lớn               │
│  - Không implement methods không dùng đến                    │
├─────────────────────────────────────────────────────────────┤
│  E - Dependency Inversion Principle                          │
│  - Depend vào abstractions, không depend vào concrete        │
│  - High-level modules không depend vào low-level modules     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 1: CREATIONAL PATTERNS

### 1.1 Singleton Pattern

**Mục đích:** Đảm bảo chỉ có 1 instance của class

**Khi nào dùng:**
- ✅ Logger
- ✅ Configuration manager
- ✅ Database connection pool
- ✅ Cache

**Implementation:**

```java
// ❌ NOT thread-safe
public class Singleton {
    private static Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}

// ✅ Thread-safe (Eager initialization)
public class Singleton {
    private static final Singleton INSTANCE = new Singleton();

    private Singleton() {}

    public static Singleton getInstance() {
        return INSTANCE;
    }
}

// ✅ Thread-safe (Double-checked locking)
public class Singleton {
    private static volatile Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}

// ✅ Best: Enum Singleton (effective Java recommendation)
public enum Singleton {
    INSTANCE;

    public void doSomething() {
        // Business logic
    }
}
```

**Spring @Singleton:**
```java
@Component  // hoặc @Service, @Repository
@Scope("singleton")  // Default scope trong Spring
public class UserService {
    // Spring đảm bảo chỉ có 1 instance
}
```

---

### 1.2 Builder Pattern

**Mục đích:** Tạo complex objects step-by-step

**Khi nào dùng:**
- ✅ Object với nhiều optional parameters
- ✅ Object cần validation trước khi tạo
- ✅ Fluent API cho readability

**Implementation:**

```java
// ❌ Anti-pattern: Telescoping constructor
public class User {
    private final String name;
    private final String email;
    private final String phone;
    private final String address;

    public User(String name, String email) {
        this(name, email, null, null);
    }

    public User(String name, String email, String phone, String address) {
        this.name = name;
        this.email = email;
        this.phone = phone;
        this.address = address;
    }
}

// ✅ Builder Pattern
public class User {
    private final String name;
    private final String email;
    private final String phone;
    private final String address;

    private User(Builder builder) {
        this.name = builder.name;
        this.email = builder.email;
        this.phone = builder.phone;
        this.address = builder.address;
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private String name;
        private String email;
        private String phone;
        private String address;

        public Builder name(String name) {
            this.name = name;
            return this;
        }

        public Builder email(String email) {
            this.email = email;
            return this;
        }

        public Builder phone(String phone) {
            this.phone = phone;
            return this;
        }

        public Builder address(String address) {
            this.address = address;
            return this;
        }

        public User build() {
            // Validation
            if (name == null || email == null) {
                throw new IllegalStateException("name and email are required");
            }
            return new User(this);
        }
    }
}

// Usage
User user = User.builder()
    .name("John Doe")
    .email("john@example.com")
    .phone("123456789")
    .build();
```

**Lombok @Builder:**
```java
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class User {
    private String name;
    private String email;
    private String phone;
    private String address;
}

// Usage
User user = User.builder()
    .name("John Doe")
    .email("john@example.com")
    .build();
```

---

### 1.3 Factory Method Pattern

**Mục đích:** Tạo objects mà không specify exact class

**Khi nào dùng:**
- ✅ Không biết trước type của object cần tạo
- ✅ Muốn cung cấp extension points
- ✅ Framework/Library design

**Implementation:**

```java
// Product interface
public interface Payment {
    void pay(BigDecimal amount);
}

// Concrete products
public class CreditCardPayment implements Payment {
    @Override
    public void pay(BigDecimal amount) {
        // Credit card processing
    }
}

public class PayPalPayment implements Payment {
    @Override
    public void pay(BigDecimal amount) {
        // PayPal processing
    }
}

public class CryptoPayment implements Payment {
    @Override
    public void pay(BigDecimal amount) {
        // Crypto processing
    }
}

// Creator với factory method
public abstract class PaymentService {

    // Factory method
    protected abstract Payment createPayment();

    public void processPayment(BigDecimal amount) {
        Payment payment = createPayment();
        payment.pay(amount);
        // Common processing logic
    }
}

// Concrete creators
public class CreditCardPaymentService extends PaymentService {
    @Override
    protected Payment createPayment() {
        return new CreditCardPayment();
    }
}

public class PayPalPaymentService extends PaymentService {
    @Override
    protected Payment createPayment() {
        return new PayPalPayment();
    }
}

// Usage
PaymentService service = new CreditCardPaymentService();
service.processPayment(new BigDecimal("100.00"));
```

**Spring FactoryBean:**
```java
public class DatabaseConnectionFactory implements FactoryBean<Connection> {

    private String url;
    private String username;
    private String password;

    @Override
    public Connection getObject() throws Exception {
        return DriverManager.getConnection(url, username, password);
    }

    @Override
    public Class<?> getObjectType() {
        return Connection.class;
    }
}
```

---

### 1.4 Abstract Factory Pattern

**Mục đích:** Tạo families of related objects

**Khi nào dùng:**
- ✅ Multiple product families
- ✅ Ensure compatibility between products
- ✅ UI frameworks (Windows/Mac/Linux widgets)

**Implementation:**

```java
// Abstract Factory
public interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
    Menu createMenu();
}

// Concrete Factory 1: Windows
public class WindowsFactory implements GUIFactory {
    @Override
    public Button createButton() {
        return new WindowsButton();
    }

    @Override
    public Checkbox createCheckbox() {
        return new WindowsCheckbox();
    }

    @Override
    public Menu createMenu() {
        return new WindowsMenu();
    }
}

// Concrete Factory 2: Mac
public class MacFactory implements GUIFactory {
    @Override
    public Button createButton() {
        return new MacButton();
    }

    @Override
    public Checkbox createCheckbox() {
        return new MacCheckbox();
    }

    @Override
    public Menu createMenu() {
        return new MacMenu();
    }
}

// Product families
public interface Button { void render(); }
public interface Checkbox { void toggle(); }
public interface Menu { void display(); }

public class WindowsButton implements Button {
    public void render() { /* Windows style */ }
}

public class MacButton implements Button {
    public void render() { /* Mac style */ }
}

// Client code
public class Application {
    private final GUIFactory factory;

    public Application(GUIFactory factory) {
        this.factory = factory;
    }

    public void render() {
        Button button = factory.createButton();
        Checkbox checkbox = factory.createCheckbox();
        Menu menu = factory.createMenu();

        button.render();
        checkbox.toggle();
        menu.display();
    }
}

// Usage
String os = System.getProperty("os.name").toLowerCase();
GUIFactory factory = os.contains("win")
    ? new WindowsFactory()
    : new MacFactory();

Application app = new Application(factory);
app.render();
```

---

### 1.5 Prototype Pattern

**Mục đích:** Tạo objects bằng cách clone existing objects

**Khi nào dùng:**
- ✅ Tạo object tốn kém (expensive initialization)
- ✅ Cần tạo nhiều objects giống nhau
- ✅ Object state cần được preserve

**Implementation:**

```java
// Prototype interface
public interface Prototype<T> {
    T clone();
}

// Concrete Prototype
public class User implements Prototype<User> {
    private String name;
    private String email;
    private List<String> roles;

    public User(String name, String email, List<String> roles) {
        this.name = name;
        this.email = email;
        this.roles = roles;
    }

    @Override
    public User clone() {
        try {
            User cloned = (User) super.clone();
            // Deep copy for mutable fields
            cloned.roles = new ArrayList<>(this.roles);
            return cloned;
        } catch (CloneNotSupportedException e) {
            throw new AssertionError();
        }
    }

    // Getters and setters
}

// Usage
User original = new User("John", "john@example.com", List.of("USER", "ADMIN"));
User clone1 = original.clone();
User clone2 = original.clone();

// Modify clone without affecting original
clone1.setName("Jane");
```

---

## 📚 BÀI 2: STRUCTURAL PATTERNS

### 2.1 Adapter Pattern

**Mục đích:** Convert interface của class này thành interface khác mà client mong đợi

**Khi nào dùng:**
- ✅ Làm việc với legacy code
- ✅ Tích hợp third-party libraries
- ✅ Multiple classes với incompatible interfaces

**Implementation:**

```java
// Target interface
public interface PaymentProcessor {
    void processPayment(BigDecimal amount);
}

// Adaptee (incompatible interface)
public class PayPalGateway {
    public void makePayment(double amountInCents) {
        // PayPal API
    }
}

// Adapter
public class PayPalAdapter implements PaymentProcessor {
    private final PayPalGateway payPalGateway;

    public PayPalAdapter(PayPalGateway payPalGateway) {
        this.payPalGateway = payPalGateway;
    }

    @Override
    public void processPayment(BigDecimal amount) {
        // Convert dollars to cents
        double amountInCents = amount.multiply(new BigDecimal("100")).doubleValue();
        payPalGateway.makePayment(amountInCents);
    }
}

// Client code
public class CheckoutService {
    private final PaymentProcessor paymentProcessor;

    public CheckoutService(PaymentProcessor paymentProcessor) {
        this.paymentProcessor = paymentProcessor;
    }

    public void checkout(BigDecimal amount) {
        paymentProcessor.processPayment(amount);
    }
}

// Usage
PayPalGateway gateway = new PayPalGateway();
PaymentProcessor adapter = new PayPalAdapter(gateway);
CheckoutService checkout = new CheckoutService(adapter);
checkout.checkout(new BigDecimal("99.99"));
```

---

### 2.2 Decorator Pattern

**Mục đích:** Add behavior cho objects dynamically

**Khi nào dùng:**
- ✅ Add responsibilities dynamically
- ✅ Avoid subclass explosion
- ✅ Cross-cutting concerns (logging, caching, validation)

**Implementation:**

```java
// Component interface
public interface DataSource {
    void writeData(String data);
    String readData();
}

// Concrete Component
public class FileDataSource implements DataSource {
    private final String filename;

    public FileDataSource(String filename) {
        this.filename = filename;
    }

    @Override
    public void writeData(String data) {
        // Write to file
    }

    @Override
    public String readData() {
        // Read from file
        return "data";
    }
}

// Abstract Decorator
public abstract class DataSourceDecorator implements DataSource {
    protected final DataSource wrappee;

    public DataSourceDecorator(DataSource wrappee) {
        this.wrappee = wrappee;
    }

    @Override
    public void writeData(String data) {
        wrappee.writeData(data);
    }

    @Override
    public String readData() {
        return wrappee.readData();
    }
}

// Concrete Decorator 1: Compression
public class CompressionDecorator extends DataSourceDecorator {

    public CompressionDecorator(DataSource wrappee) {
        super(wrappee);
    }

    @Override
    public void writeData(String data) {
        super.writeData(compress(data));
    }

    @Override
    public String readData() {
        return decompress(super.readData());
    }

    private String compress(String data) { /* ... */ }
    private String decompress(String data) { /* ... */ }
}

// Concrete Decorator 2: Encryption
public class EncryptionDecorator extends DataSourceDecorator {

    public EncryptionDecorator(DataSource wrappee) {
        super(wrappee);
    }

    @Override
    public void writeData(String data) {
        super.writeData(encrypt(data));
    }

    @Override
    public String readData() {
        return decrypt(super.readData());
    }

    private String encrypt(String data) { /* ... */ }
    private String decrypt(String data) { /* ... */ }
}

// Usage
DataSource fileDataSource = new FileDataSource("data.txt");
DataSource compressed = new CompressionDecorator(fileDataSource);
DataSource encryptedAndCompressed = new EncryptionDecorator(compressed);

encryptedAndCompressed.writeData("secret data");
String data = encryptedAndCompressed.readData();
```

**Spring AOP là một form của Decorator:**
```java
@Service
public class UserService {

    @Cacheable("users")  // Decorator
    @Transactional       // Decorator
    @LogExecutionTime    // Decorator
    public User findById(Long id) {
        // Business logic
    }
}
```

---

### 2.3 Facade Pattern

**Mục đích:** Provide simplified interface cho complex subsystem

**Khi nào dùng:**
- ✅ Complex system với nhiều dependencies
- ✅ Need simple interface cho common tasks
- ✅ Layered architecture

**Implementation:**

```java
// Complex subsystem
public class OrderProcessor {
    public void validateOrder(Order order) { /* ... */ }
}

public class InventoryService {
    public void checkStock(String productId) { /* ... */ }
    public void reserveStock(String productId, int quantity) { /* ... */ }
}

public class PaymentGateway {
    public void processPayment(BigDecimal amount) { /* ... */ }
}

public class NotificationService {
    public void sendConfirmation(String email) { /* ... */ }
}

// Facade
public class OrderFacade {
    private final OrderProcessor orderProcessor;
    private final InventoryService inventoryService;
    private final PaymentGateway paymentGateway;
    private final NotificationService notificationService;

    public OrderFacade() {
        this.orderProcessor = new OrderProcessor();
        this.inventoryService = new InventoryService();
        this.paymentGateway = new PaymentGateway();
        this.notificationService = new NotificationService();
    }

    public void placeOrder(Order order) {
        // Simplified interface for complex operation
        orderProcessor.validateOrder(order);
        inventoryService.checkStock(order.getProductId());
        inventoryService.reserveStock(order.getProductId(), order.getQuantity());
        paymentGateway.processPayment(order.getTotalAmount());
        notificationService.sendConfirmation(order.getUserEmail());
    }
}

// Usage
OrderFacade orderFacade = new OrderFacade();
orderFacade.placeOrder(order);
// Client doesn't need to know about subsystem complexity
```

---

### 2.4 Proxy Pattern

**Mục đích:** Control access to object

**Khi nào dùng:**
- ✅ Lazy initialization (virtual proxy)
- ✅ Access control (protection proxy)
- ✅ Logging/monitoring (logging proxy)
- ✅ Caching (cache proxy)

**Implementation:**

```java
// Subject interface
public interface Image {
    void display();
}

// Real Subject
public class HighResolutionImage implements Image {
    private final String filename;

    public HighResolutionImage(String filename) {
        this.filename = filename;
        // Expensive operation: load image from disk
        loadImage();
    }

    private void loadImage() {
        System.out.println("Loading " + filename);
        // Simulate slow loading
        try { Thread.sleep(3000); } catch (InterruptedException e) {}
    }

    @Override
    public void display() {
        System.out.println("Displaying " + filename);
    }
}

// Proxy
public class ImageProxy implements Image {
    private final String filename;
    private HighResolutionImage image;  // Lazy initialization

    public ImageProxy(String filename) {
        this.filename = filename;
    }

    @Override
    public void display() {
        if (image == null) {
            image = new HighResolutionImage(filename);  // Load on demand
        }
        image.display();
    }
}

// Usage
Image image = new ImageProxy("photo.jpg");
// Image not loaded yet

image.display();  // Now image is loaded
image.display();  // Use cached image
```

**Spring AOP Proxy:**
```java
@Service
public class UserService {

    @Transactional
    public void updateUser(User user) {
        // Spring tạo proxy để manage transaction
    }
}

// Spring tạo proxy class như sau:
public class UserServiceProxy extends UserService {
    @Override
    public void updateUser(User user) {
        try {
            transactionManager.begin();
            super.updateUser(user);
            transactionManager.commit();
        } catch (Exception e) {
            transactionManager.rollback();
        }
    }
}
```

---

### 2.5 Composite Pattern

**Mục đích:** Compose objects vào tree structures

**Khi nào dùng:**
- ✅ Part-whole hierarchies
- ✅ Tree structures (file systems, organization charts)
- ✅ Uniform treatment of individual and composite objects

**Implementation:**

```java
// Component
public interface FileSystemComponent {
    void showDetails();
    long getSize();
}

// Leaf
public class File implements FileSystemComponent {
    private final String name;
    private final long size;

    public File(String name, long size) {
        this.name = name;
        this.size = size;
    }

    @Override
    public void showDetails() {
        System.out.println("File: " + name + " (" + size + " bytes)");
    }

    @Override
    public long getSize() {
        return size;
    }
}

// Composite
public class Directory implements FileSystemComponent {
    private final String name;
    private final List<FileSystemComponent> children = new ArrayList<>();

    public Directory(String name) {
        this.name = name;
    }

    public void add(FileSystemComponent component) {
        children.add(component);
    }

    public void remove(FileSystemComponent component) {
        children.remove(component);
    }

    @Override
    public void showDetails() {
        System.out.println("Directory: " + name);
        for (FileSystemComponent child : children) {
            child.showDetails();
        }
    }

    @Override
    public long getSize() {
        return children.stream().mapToLong(FileSystemComponent::getSize).sum();
    }
}

// Usage
File file1 = new File("file1.txt", 100);
File file2 = new File("file2.txt", 200);
Directory dir1 = new Directory("Documents");
dir1.add(file1);
dir1.add(file2);

Directory root = new Directory("root");
root.add(dir1);
root.add(new File("file3.txt", 300));

root.showDetails();
System.out.println("Total size: " + root.getSize() + " bytes");
```

---

## 📚 BÀI 3: BEHAVIORAL PATTERNS

### 3.1 Strategy Pattern

**Mục đích:** Define family of algorithms, encapsulate each one, make them interchangeable

**Khi nào dùng:**
- ✅ Multiple algorithms for same task
- ✅ Runtime algorithm selection
- ✅ Avoid conditional statements

**Implementation:**

```java
// Strategy interface
public interface PaymentStrategy {
    void pay(BigDecimal amount);
}

// Concrete Strategies
public class CreditCardStrategy implements PaymentStrategy {
    private final String cardNumber;
    private final String cvv;

    public CreditCardStrategy(String cardNumber, String cvv) {
        this.cardNumber = cardNumber;
        this.cvv = cvv;
    }

    @Override
    public void pay(BigDecimal amount) {
        System.out.println("Paid " + amount + " using Credit Card");
    }
}

public class PayPalStrategy implements PaymentStrategy {
    private final String email;
    private final String password;

    public PayPalStrategy(String email, String password) {
        this.email = email;
        this.password = password;
    }

    @Override
    public void pay(BigDecimal amount) {
        System.out.println("Paid " + amount + " using PayPal");
    }
}

public class CryptoStrategy implements PaymentStrategy {
    private final String walletAddress;

    public CryptoStrategy(String walletAddress) {
        this.walletAddress = walletAddress;
    }

    @Override
    public void pay(BigDecimal amount) {
        System.out.println("Paid " + amount + " using Crypto");
    }
}

// Context
public class ShoppingCart {
    private PaymentStrategy paymentStrategy;

    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;
    }

    public void checkout(BigDecimal amount) {
        paymentStrategy.pay(amount);
    }
}

// Usage
ShoppingCart cart = new ShoppingCart();

cart.setPaymentStrategy(new CreditCardStrategy("1234-5678", "123"));
cart.checkout(new BigDecimal("100"));

cart.setPaymentStrategy(new PayPalStrategy("user@example.com", "pass"));
cart.checkout(new BigDecimal("200"));
```

**Java 8+ với Lambda:**
```java
@FunctionalInterface
public interface PaymentStrategy {
    void pay(BigDecimal amount);
}

// Usage
ShoppingCart cart = new ShoppingCart();

cart.setPaymentStrategy(amount ->
    System.out.println("Paid " + amount + " using Lambda"));
```

---

### 3.2 Observer Pattern

**Mục đích:** Define one-to-many dependency, notify dependents when state changes

**Khi nào dùng:**
- ✅ Event handling
- ✅ Pub/sub systems
- ✅ Reactive programming

**Implementation:**

```java
// Observer interface
public interface Observer {
    void update(String event);
}

// Subject
public class OrderSubject {
    private final List<Observer> observers = new ArrayList<>();
    private String orderStatus;

    public void attach(Observer observer) {
        observers.add(observer);
    }

    public void detach(Observer observer) {
        observers.remove(observer);
    }

    public void setOrderStatus(String status) {
        this.orderStatus = status;
        notifyObservers();
    }

    private void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(orderStatus);
        }
    }
}

// Concrete Observers
public class EmailNotificationObserver implements Observer {
    @Override
    public void update(String event) {
        System.out.println("Sending email: " + event);
    }
}

public class SmsNotificationObserver implements Observer {
    @Override
    public void update(String event) {
        System.out.println("Sending SMS: " + event);
    }
}

public class InventoryObserver implements Observer {
    @Override
    public void update(String event) {
        if ("CANCELLED".equals(event)) {
            System.out.println("Restocking inventory...");
        }
    }
}

// Usage
OrderSubject order = new OrderSubject();
order.attach(new EmailNotificationObserver());
order.attach(new SmsNotificationObserver());
order.attach(new InventoryObserver());

order.setOrderStatus("PROCESSING");
order.setOrderStatus("SHIPPED");
order.setOrderStatus("DELIVERED");
```

**Java Built-in Observer:**
```java
import java.util.Observable;
import java.util.Observer;

// Or use PropertyChangeSupport for better practice
public class Order {
    private final PropertyChangeSupport support;
    private String status;

    public Order() {
        support = new PropertyChangeSupport(this);
    }

    public void addPropertyChangeListener(PropertyChangeListener listener) {
        support.addPropertyChangeListener(listener);
    }

    public void setStatus(String status) {
        String oldStatus = this.status;
        this.status = status;
        support.firePropertyChange("status", oldStatus, status);
    }
}
```

**Spring Application Events:**
```java
// Event
public class OrderCreatedEvent extends ApplicationEvent {
    private final Order order;

    public OrderCreatedEvent(Object source, Order order) {
        super(source);
        this.order = order;
    }

    public Order getOrder() { return order; }
}

// Publisher
@Service
public class OrderService {
    @Autowired
    private ApplicationEventPublisher eventPublisher;

    public void createOrder(Order order) {
        // Save order
        eventPublisher.publishEvent(new OrderCreatedEvent(this, order));
    }
}

// Listener
@Component
public class OrderListener {
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Send notification, update inventory, etc.
    }
}
```

---

### 3.3 Command Pattern

**Mục đích:** Encapsulate request as object

**Khi nào dùng:**
- ✅ Undo/redo functionality
- ✅ Command queuing
- ✅ Macro commands
- ✅ Transactional operations

**Implementation:**

```java
// Command interface
public interface Command {
    void execute();
    void undo();
}

// Receiver
public class TextEditor {
    private StringBuilder content = new StringBuilder();

    public void insert(String text) {
        content.append(text);
    }

    public void delete(int start, int end) {
        content.delete(start, end);
    }

    public String getContent() {
        return content.toString();
    }
}

// Concrete Commands
public class InsertCommand implements Command {
    private final TextEditor editor;
    private final String text;

    public InsertCommand(TextEditor editor, String text) {
        this.editor = editor;
        this.text = text;
    }

    @Override
    public void execute() {
        editor.insert(text);
    }

    @Override
    public void undo() {
        // Undo logic (simplified)
        int lastIndex = editor.getContent().lastIndexOf(text);
        if (lastIndex != -1) {
            editor.delete(lastIndex, lastIndex + text.length());
        }
    }
}

// Invoker
public class History {
    private final Stack<Command> commands = new Stack<>();

    public void executeCommand(Command command) {
        command.execute();
        commands.push(command);
    }

    public void undo() {
        if (!commands.isEmpty()) {
            commands.pop().undo();
        }
    }
}

// Usage
TextEditor editor = new TextEditor();
History history = new History();

history.executeCommand(new InsertCommand(editor, "Hello "));
history.executeCommand(new InsertCommand(editor, "World"));

System.out.println(editor.getContent());  // Hello World

history.undo();  // Undo last insert
System.out.println(editor.getContent());  // Hello
```

---

### 3.4 Chain of Responsibility Pattern

**Mục đích:** Pass requests along chain of handlers

**Khi nào dùng:**
- ✅ Multiple handlers for same request
- ✅ Handler order dynamic
- ✅ Logging, validation, processing pipelines

**Implementation:**

```java
// Handler interface
public abstract class SupportHandler {
    protected SupportHandler nextHandler;

    public void setNext(SupportHandler nextHandler) {
        this.nextHandler = nextHandler;
    }

    public abstract void handleRequest(Ticket ticket);
}

// Concrete Handlers
public class Level1SupportHandler extends SupportHandler {
    @Override
    public void handleRequest(Ticket ticket) {
        if (ticket.getSeverity() <= 2) {
            System.out.println("Level 1 support handling ticket: " + ticket.getId());
        } else if (nextHandler != null) {
            nextHandler.handleRequest(ticket);
        }
    }
}

public class Level2SupportHandler extends SupportHandler {
    @Override
    public void handleRequest(Ticket ticket) {
        if (ticket.getSeverity() <= 4) {
            System.out.println("Level 2 support handling ticket: " + ticket.getId());
        } else if (nextHandler != null) {
            nextHandler.handleRequest(ticket);
        }
    }
}

public class Level3SupportHandler extends SupportHandler {
    @Override
    public void handleRequest(Ticket ticket) {
        System.out.println("Level 3 support handling ticket: " + ticket.getId());
    }
}

// Usage
SupportHandler level1 = new Level1SupportHandler();
SupportHandler level2 = new Level2SupportHandler();
SupportHandler level3 = new Level3SupportHandler();

level1.setNext(level2);
level2.setNext(level3);

Ticket ticket1 = new Ticket(1, 1);  // Low severity
Ticket ticket2 = new Ticket(2, 3);  // Medium severity
Ticket ticket3 = new Ticket(3, 5);  // High severity

level1.handleRequest(ticket1);
level1.handleRequest(ticket2);
level1.handleRequest(ticket3);
```

**Spring Security Filter Chain:**
```java
@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(new LoggingFilter(), UsernamePasswordAuthenticationFilter.class)
            .addFilterBefore(new JwtAuthenticationFilter(), LoggingFilter.class);

        return http.build();
    }
}
```

---

### 3.5 Template Method Pattern

**Mục đích:** Define skeleton of algorithm, let subclasses override steps

**Khi nào dùng:**
- ✅ Common algorithm with variant steps
- ✅ Framework design
- ✅ Avoid code duplication

**Implementation:**

```java
// Abstract class với template method
public abstract class DataProcessor {

    // Template method (final để không override)
    public final void process(String filePath) {
        validateFile(filePath);
        Object data = readData(filePath);
        Object transformed = transform(data);
        write(transformed);
        cleanup();
    }

    // Steps với default implementation
    protected void validateFile(String filePath) {
        if (filePath == null || filePath.isEmpty()) {
            throw new IllegalArgumentException("Invalid file path");
        }
    }

    protected void cleanup() {
        // Optional cleanup
    }

    // Abstract steps (subclasses must implement)
    protected abstract Object readData(String filePath);
    protected abstract Object transform(Object data);
    protected abstract void write(Object data);
}

// Concrete implementations
public class CsvDataProcessor extends DataProcessor {
    @Override
    protected Object readData(String filePath) {
        // Read CSV
        return new Object();
    }

    @Override
    protected Object transform(Object data) {
        // Transform CSV data
        return data;
    }

    @Override
    protected void write(Object data) {
        // Write to database
    }
}

public class JsonDataProcessor extends DataProcessor {
    @Override
    protected Object readData(String filePath) {
        // Read JSON
        return new Object();
    }

    @Override
    protected Object transform(Object data) {
        // Transform JSON data
        return data;
    }

    @Override
    protected void write(Object data) {
        // Write to database
    }
}

// Usage
DataProcessor csvProcessor = new CsvDataProcessor();
csvProcessor.process("data.csv");

DataProcessor jsonProcessor = new JsonDataProcessor();
jsonProcessor.process("data.json");
```

---

### 3.6 State Pattern

**Mục đích:** Allow object to change behavior when internal state changes

**Khi nào dùng:**
- ✅ Object behavior depends on state
- ✅ Many conditionals based on state
- ✅ State transitions

**Implementation:**

```java
// State interface
public interface OrderState {
    void processOrder(Order order);
    void cancelOrder(Order order);
}

// Concrete States
public class PendingState implements OrderState {
    @Override
    public void processOrder(Order order) {
        System.out.println("Processing order...");
        order.setState(new ProcessingState());
    }

    @Override
    public void cancelOrder(Order order) {
        System.out.println("Cancelling order...");
        order.setState(new CancelledState());
    }
}

public class ProcessingState implements OrderState {
    @Override
    public void processOrder(Order order) {
        System.out.println("Order already processing");
    }

    @Override
    public void cancelOrder(Order order) {
        System.out.println("Cannot cancel order in processing");
    }
}

public class ShippedState implements OrderState {
    @Override
    public void processOrder(Order order) {
        System.out.println("Order already shipped");
    }

    @Override
    public void cancelOrder(Order order) {
        System.out.println("Cannot cancel shipped order, initiate return instead");
    }
}

public class CancelledState implements OrderState {
    @Override
    public void processOrder(Order order) {
        System.out.println("Cannot process cancelled order");
    }

    @Override
    public void cancelOrder(Order order) {
        System.out.println("Order already cancelled");
    }
}

// Context
public class Order {
    private OrderState state;

    public Order() {
        state = new PendingState();  // Initial state
    }

    public void setState(OrderState state) {
        this.state = state;
    }

    public void processOrder() {
        state.processOrder(this);
    }

    public void cancelOrder() {
        state.cancelOrder(this);
    }
}

// Usage
Order order = new Order();
order.processOrder();  // Pending → Processing
order.cancelOrder();   // Cannot cancel
```

---

### 3.7 Mediator Pattern

**Mục đích:** Reduce coupling between objects by having them communicate through mediator

**Khi nào dùng:**
- ✅ Many-to-many relationships
- ✅ Complex object interactions
- ✅ Chat systems, control towers

**Implementation:**

```java
// Mediator interface
public interface ChatMediator {
    void sendMessage(String message, User user);
    void addUser(User user);
}

// Concrete Mediator
public class ChatRoom implements ChatMediator {
    private final List<User> users = new ArrayList<>();

    @Override
    public void addUser(User user) {
        users.add(user);
    }

    @Override
    public void sendMessage(String message, User sender) {
        for (User user : users) {
            if (user != sender) {
                user.receive(message);
            }
        }
    }
}

// Colleagues
public abstract class User {
    protected final ChatMediator mediator;
    protected final String name;

    public User(ChatMediator mediator, String name) {
        this.mediator = mediator;
        this.name = name;
    }

    public void send(String message) {
        System.out.println(name + " sends: " + message);
        mediator.sendMessage(message, this);
    }

    public abstract void receive(String message);
}

public class ChatUser extends User {
    public ChatUser(ChatMediator mediator, String name) {
        super(mediator, name);
    }

    @Override
    public void receive(String message) {
        System.out.println(name + " received: " + message);
    }
}

// Usage
ChatMediator chatRoom = new ChatRoom();

User user1 = new ChatUser(chatRoom, "Alice");
User user2 = new ChatUser(chatRoom, "Bob");
User user3 = new ChatUser(chatRoom, "Charlie");

chatRoom.addUser(user1);
chatRoom.addUser(user2);
chatRoom.addUser(user3);

user1.send("Hello everyone!");
user2.send("Hi Alice!");
```

---

### 3.8 Memento Pattern

**Mục đích:** Capture and restore object state without exposing internals

**Khi nào dùng:**
- ✅ Undo/redo
- ✅ Savepoints
- ✅ Snapshots

**Implementation:**

```java
// Memento
public class EditorMemento {
    private final String content;
    private final long timestamp;

    public EditorMemento(String content) {
        this.content = content;
        this.timestamp = System.currentTimeMillis();
    }

    public String getContent() {
        return content;
    }

    public long getTimestamp() {
        return timestamp;
    }
}

// Originator
public class TextEditor {
    private String content = "";

    public void type(String text) {
        content += text;
    }

    public String getContent() {
        return content;
    }

    public EditorMemento save() {
        return new EditorMemento(content);
    }

    public void restore(EditorMemento memento) {
        this.content = memento.getContent();
    }
}

// Caretaker
public class History {
    private final Stack<EditorMemento> states = new Stack<>();

    public void saveState(TextEditor editor) {
        states.push(editor.save());
    }

    public void undo(TextEditor editor) {
        if (!states.isEmpty()) {
            states.pop();  // Remove current state
            if (!states.isEmpty()) {
                editor.restore(states.peek());
            }
        }
    }
}

// Usage
TextEditor editor = new TextEditor();
History history = new History();

editor.type("Hello ");
history.saveState(editor);

editor.type("World");
history.saveState(editor);

editor.type("!");

System.out.println(editor.getContent());  // Hello World!

history.undo(editor);
System.out.println(editor.getContent());  // Hello World
```

---

### 3.9 Visitor Pattern

**Mục đích:** Separate algorithm from object structure

**Khi nào dùng:**
- ✅ Operations on heterogeneous collections
- ✅ Need to add operations without modifying classes
- ✅ Accumulating state while traversing

**Implementation:**

```java
// Element interface
public interface Shape {
    void accept(Visitor visitor);
}

// Concrete Elements
public class Circle implements Shape {
    private final double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    public double getRadius() {
        return radius;
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}

public class Rectangle implements Shape {
    private final double width;
    private final double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    public double getWidth() { return width; }
    public double getHeight() { return height; }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}

// Visitor interface
public interface Visitor {
    void visit(Circle circle);
    void visit(Rectangle rectangle);
}

// Concrete Visitors
public class AreaCalculator implements Visitor {
    private double totalArea = 0;

    @Override
    public void visit(Circle circle) {
        totalArea += Math.PI * circle.getRadius() * circle.getRadius();
    }

    @Override
    public void visit(Rectangle rectangle) {
        totalArea += rectangle.getWidth() * rectangle.getHeight();
    }

    public double getTotalArea() {
        return totalArea;
    }
}

public class PerimeterCalculator implements Visitor {
    private double totalPerimeter = 0;

    @Override
    public void visit(Circle circle) {
        totalPerimeter += 2 * Math.PI * circle.getRadius();
    }

    @Override
    public void visit(Rectangle rectangle) {
        totalPerimeter += 2 * (rectangle.getWidth() + rectangle.getHeight());
    }

    public double getTotalPerimeter() {
        return totalPerimeter;
    }
}

// Usage
List<Shape> shapes = List.of(
    new Circle(5),
    new Rectangle(10, 20),
    new Circle(3)
);

AreaCalculator areaCalc = new AreaCalculator();
for (Shape shape : shapes) {
    shape.accept(areaCalc);
}
System.out.println("Total area: " + areaCalc.getTotalArea());

PerimeterCalculator perimeterCalc = new PerimeterCalculator();
for (Shape shape : shapes) {
    shape.accept(perimeterCalc);
}
System.out.println("Total perimeter: " + perimeterCalc.getTotalPerimeter());
```

---

## 📝 TÓM TẮT

### Creational Patterns (5)
| Pattern | Purpose | Example |
|---------|---------|---------|
| Singleton | One instance | Logger, Config |
| Builder | Step-by-step construction | Complex objects |
| Factory Method | Subclasses decide instantiation | Frameworks |
| Abstract Factory | Family of related objects | UI toolkits |
| Prototype | Clone existing objects | Expensive objects |

### Structural Patterns (7)
| Pattern | Purpose | Example |
|---------|---------|---------|
| Adapter | Incompatible interfaces | Legacy integration |
| Decorator | Add behavior dynamically | Java I/O, Spring AOP |
| Facade | Simplified interface | Complex subsystems |
| Proxy | Control access | Lazy loading, security |
| Composite | Tree structures | File systems |
| Bridge | Separate abstraction from implementation | Cross-platform |
| Flyweight | Share fine-grained objects | Text editors |

### Behavioral Patterns (11)
| Pattern | Purpose | Example |
|---------|---------|---------|
| Strategy | Interchangeable algorithms | Payment methods |
| Observer | One-to-many notifications | Event handling |
| Command | Encapsulate requests | Undo/redo |
| Chain of Responsibility | Pass along chain | Middleware, filters |
| Template Method | Algorithm skeleton | Frameworks |
| State | Behavior based on state | Order processing |
| Mediator | Centralized communication | Chat rooms |
| Memento | Save/restore state | Undo functionality |
| Visitor | Operations on structures | AST processing |
| Iterator | Sequential access | Collections |
| Interpreter | Language grammar | SQL parsers |

---

## 🔜 TIẾP THEO

Xem `02-examples.md` để xem Spring Framework áp dụng design patterns!
