# Design Patterns - Exercises

> **Mục tiêu:** Thực hành áp dụng design patterns trong Java/Spring

---

## 📚 BÀI 1: CREATIONAL PATTERNS EXERCISES

### Exercise 1.1: Singleton Pattern - Configuration Manager

**Yêu cầu:** Tạo thread-safe singleton cho application configuration

```java
// TODO: Implement thread-safe singleton
public class AppConfig {
    // Your code here
}

// Test cases to pass:
@Test
void testSingletonInstance() {
    AppConfig instance1 = AppConfig.getInstance();
    AppConfig instance2 = AppConfig.getInstance();
    assertSame(instance1, instance2);
}

@Test
void testThreadSafety() throws InterruptedException {
    // Multiple threads should get same instance
    CountDownLatch latch = new CountDownLatch(100);
    Set<AppConfig> instances = ConcurrentHashMap.newKeySet();

    for (int i = 0; i < 100; i++) {
        new Thread(() -> {
            instances.add(AppConfig.getInstance());
            latch.countDown();
        }).start();
    }

    latch.await();
    assertEquals(1, instances.size());
}
```

---

### Exercise 1.2: Builder Pattern - API Response

**Yêu cầu:** Tạo Builder pattern cho complex API response object

```java
// TODO: Implement Builder pattern
public class ApiResponse<T> {
    // Fields: status, message, data, timestamp, errors (optional), meta (optional)

    // Builder với validation:
    // - status và message bắt buộc
    // - timestamp tự động set
    // - Fluent API
}

// Usage should be:
ApiResponse<User> response = ApiResponse.<User>builder()
    .status(200)
    .message("Success")
    .data(user)
    .meta(Map.of("page", 1, "size", 10))
    .build();
```

---

### Exercise 1.3: Factory Method - Notification System

**Yêu cầu:** Implement factory method cho notification types

```java
// Product interface
public interface Notification {
    void send(String recipient, String message);
}

// TODO: Implement concrete products
// - EmailNotification
// - SmsNotification
// - PushNotification

// Creator
public abstract class NotificationFactory {
    // TODO: Implement factory method
    protected abstract Notification createNotification();

    public void sendNotification(String recipient, String message) {
        Notification notification = createNotification();
        // Common logic: log, validate, etc.
        notification.send(recipient, message);
    }
}

// TODO: Implement concrete factories
// - EmailNotificationFactory
// - SmsNotificationFactory
// - PushNotificationFactory
```

---

### Exercise 1.4: Abstract Factory - Database Connection

**Yêu cầu:** Tạo abstract factory cho multi-database support

```java
// Product families
public interface Connection { void connect(); }
public interface QueryBuilder { String build(); }
public interface TransactionManager { void begin(); void commit(); void rollback(); }

// TODO: Implement abstract factory
public interface DatabaseFactory {
    Connection createConnection();
    QueryBuilder createQueryBuilder();
    TransactionManager createTransactionManager();
}

// TODO: Implement concrete factories
// - MySqlDatabaseFactory
// - PostgresDatabaseFactory
// - MongoDatabaseFactory

// Client code
public class DatabaseService {
    private final DatabaseFactory factory;

    public DatabaseService(DatabaseFactory factory) {
        this.factory = factory;
    }

    public void executeTransaction() {
        Connection conn = factory.createConnection();
        TransactionManager tx = factory.createTransactionManager();
        QueryBuilder qb = factory.createQueryBuilder();

        tx.begin();
        try {
            conn.connect();
            String query = qb.build();
            // Execute query...
            tx.commit();
        } catch (Exception e) {
            tx.rollback();
        }
    }
}
```

---

## 📚 BÀI 2: STRUCTURAL PATTERNS EXERCISES

### Exercise 2.1: Adapter Pattern - Third-party Payment

**Yêu cầu:** Tạo adapter cho third-party payment gateway

```java
// Target interface
public interface PaymentProcessor {
    PaymentResult processPayment(PaymentRequest request);
}

// Adaptee (third-party library - cannot modify)
public class StripeClient {
    public Charge createCharge(double amountInCents, String currency, String source) {
        // Stripe API
        return new Charge();
    }

    public Refund createRefund(String chargeId) {
        // Stripe API
        return new Refund();
    }
}

// TODO: Implement adapter
public class StripeAdapter implements PaymentProcessor {
    private final StripeClient stripeClient;

    // Convert PaymentRequest to Stripe Charge
    // Convert Stripe Charge to PaymentResult
}

// Client code should work with PaymentProcessor interface
public class CheckoutService {
    private final PaymentProcessor paymentProcessor;

    public CheckoutService(PaymentProcessor paymentProcessor) {
        this.paymentProcessor = paymentProcessor;
    }

    public PaymentResult checkout(PaymentRequest request) {
        return paymentProcessor.processPayment(request);
    }
}
```

---

### Exercise 2.2: Decorator Pattern - Data Stream

**Yêu cầu:** Implement decorators cho data processing pipeline

```java
// Component interface
public interface DataStream {
    byte[] read();
    void write(byte[] data);
}

// Concrete Component
public class FileStream implements DataStream {
    private final String path;

    public FileStream(String path) {
        this.path = path;
    }

    @Override
    public byte[] read() {
        // Read from file
        return new byte[0];
    }

    @Override
    public void write(byte[] data) {
        // Write to file
    }
}

// TODO: Implement decorators
// - CompressionDecorator (compress on write, decompress on read)
// - EncryptionDecorator (encrypt on write, decrypt on read)
// - LoggingDecorator (log all read/write operations)

// Usage:
DataStream stream = new FileStream("data.bin");
DataStream compressed = new CompressionDecorator(stream);
DataStream encrypted = new EncryptionDecorator(compressed);
DataStream logged = new LoggingDecorator(encrypted);

logged.write("secret data".getBytes());
```

---

### Exercise 2.3: Facade Pattern - Video Converter

**Yêu cầu:** Tạo facade cho complex video conversion subsystem

```java
// Complex subsystem
public class VideoCodec {
    public void decode(String filename) { /* ... */ }
    public byte[] encode(byte[] raw) { /* ... */ }
}

public class AudioCodec {
    public void extract(String filename) { /* ... */ }
    public byte[] compress(byte[] audio) { /* ... */ }
}

public class ContainerMuxer {
    public void mux(byte[] video, byte[] audio, String format) { /* ... */ }
}

public class QualityAnalyzer {
    public QualityReport analyze(byte[] video) { /* ... */ }
}

// TODO: Implement facade
public class VideoConverterFacade {
    // Simplified interface for complex conversion
    public byte[] convert(String inputPath, String outputFormat, QualityLevel quality) {
        // Hide complexity from client
    }
}

// Client code - simple usage
public class ConversionService {
    private final VideoConverterFacade converter;

    public void convertVideo(String input, String format) {
        byte[] result = converter.convert(input, format, QualityLevel.HIGH);
        // Save result...
    }
}
```

---

### Exercise 2.4: Proxy Pattern - Image Service

**Yêu cầu:** Implement virtual proxy cho image loading service

```java
// Subject interface
public interface Image {
    void display();
    int getWidth();
    int getHeight();
}

// Real Subject (expensive to load)
public class HighResolutionImage implements Image {
    private final String url;
    private byte[] imageData;  // Loaded on demand

    public HighResolutionImage(String url) {
        this.url = url;
        // Don't load yet - lazy loading
    }

    private void loadImage() {
        // Simulate network delay
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        // Load image data from URL
    }

    @Override
    public void display() {
        if (imageData == null) {
            loadImage();
        }
        // Display image
    }
}

// TODO: Implement proxy
public class ImageProxy implements Image {
    // - Cache loaded images
    // - Show loading indicator
    // - Handle loading errors
    // - Lazy initialization
}
```

---

## 📚 BÀI 3: BEHAVIORAL PATTERNS EXERCISES

### Exercise 3.1: Strategy Pattern - Discount Calculator

**Yêu cầu:** Implement strategies cho discount calculation

```java
// Strategy interface
public interface DiscountStrategy {
    BigDecimal applyDiscount(BigDecimal price, int quantity);
}

// TODO: Implement strategies
// - NoDiscountStrategy (no discount)
// - PercentageDiscountStrategy (e.g., 10% off)
// - FixedAmountDiscountStrategy (e.g., $5 off)
// - BuyOneGetOneStrategy (BOGO)
// - TieredDiscountStrategy (more quantity = more discount)

// Context
public class ShoppingCart {
    private DiscountStrategy discountStrategy;

    public void setDiscountStrategy(DiscountStrategy strategy) {
        this.discountStrategy = strategy;
    }

    public BigDecimal calculateTotal(BigDecimal price, int quantity) {
        return discountStrategy.applyDiscount(price, quantity);
    }
}

// Usage
ShoppingCart cart = new ShoppingCart();
cart.setDiscountStrategy(new PercentageDiscountStrategy(10));
BigDecimal total = cart.calculateTotal(new BigDecimal("100"), 2);
```

---

### Exercise 3.2: Observer Pattern - Stock Market

**Yêu cầu:** Implement observer pattern cho stock price updates

```java
// Observer interface
public interface Investor {
    void update(String symbol, BigDecimal price);
}

// Subject
public class Stock {
    private final String symbol;
    private BigDecimal price;
    private final List<Investor> investors = new ArrayList<>();

    public Stock(String symbol, BigDecimal initialPrice) {
        this.symbol = symbol;
        this.price = initialPrice;
    }

    // TODO: Implement attach, detach, notify
    public void attach(Investor investor) { /* ... */ }
    public void detach(Investor investor) { /* ... */ }
    private void notifyInvestors() { /* ... */ }

    public void setPrice(BigDecimal newPrice) {
        this.price = newPrice;
        notifyInvestors();
    }
}

// TODO: Implement concrete observers
// - EmailNotificationInvestor (send email on price change)
// - SmsNotificationInvestor (send SMS on price change)
// - LoggingInvestor (log price changes)
// - AutoTradeInvestor (auto-trade when price hits threshold)

// Usage
Stock appleStock = new Stock("AAPL", new BigDecimal("150.00"));
appleStock.attach(new EmailNotificationInvestor("user@example.com"));
appleStock.attach(new AutoTradeInvestor(new BigDecimal("160.00")));

appleStock.setPrice(new BigDecimal("155.00"));  // Notifies all investors
```

---

### Exercise 3.3: Command Pattern - Text Editor

**Yêu cầu:** Implement command pattern với undo/redo

```java
// Command interface
public interface EditorCommand {
    void execute();
    void undo();
}

// Receiver
public class TextDocument {
    private StringBuilder content = new StringBuilder();

    public void insert(int position, String text) { /* ... */ }
    public void delete(int start, int end) { /* ... */ }
    public void replace(int start, int end, String text) { /* ... */ }
    public String getContent() { return content.toString(); }
}

// TODO: Implement commands
// - InsertCommand
// - DeleteCommand
// - ReplaceCommand

// Invoker with history
public class DocumentHistory {
    private final Stack<EditorCommand> undoStack = new Stack<>();
    private final Stack<EditorCommand> redoStack = new Stack<>();

    public void executeCommand(EditorCommand command) {
        command.execute();
        undoStack.push(command);
        redoStack.clear();  // Clear redo on new action
    }

    public void undo() {
        if (!undoStack.isEmpty()) {
            EditorCommand command = undoStack.pop();
            command.undo();
            redoStack.push(command);
        }
    }

    public void redo() {
        if (!redoStack.isEmpty()) {
            EditorCommand command = redoStack.pop();
            command.execute();
            undoStack.push(command);
        }
    }
}
```

---

### Exercise 3.4: Chain of Responsibility - Request Processing

**Yêu cầu:** Implement chain cho HTTP request processing

```java
// Handler interface
public abstract class RequestHandler {
    protected RequestHandler next;

    public RequestHandler setNext(RequestHandler next) {
        this.next = next;
        return next;
    }

    public abstract HttpResponse handle(HttpRequest request);
}

// TODO: Implement handlers
// - AuthenticationHandler (validate JWT token)
// - LoggingHandler (log request details)
// - ValidationHandler (validate request body)
// - RateLimitingHandler (check rate limits)
// - CachingHandler (return cached response if available)

// Build chain
RequestHandler chain = new AuthenticationHandler()
    .setNext(new LoggingHandler())
    .setNext(new ValidationHandler())
    .setNext(new RateLimitingHandler())
    .setNext(new CachingHandler());

// Process request
HttpResponse response = chain.handle(request);
```

---

### Exercise 3.5: State Pattern - Vending Machine

**Yêu cầu:** Implement state pattern cho vending machine

```java
// State interface
public interface VendingMachineState {
    void insertDollar(VendingMachine machine);
    void ejectMoney(VendingMachine machine);
    void dispense(VendingMachine machine);
    void refill(VendingMachine machine);
}

// TODO: Implement states
// - IdleState (waiting for money)
// - HasMoneyState (money inserted, waiting for selection)
// - DispensingState (dispensing product)
// - SoldOutState (no products)

// Context
public class VendingMachine {
    private VendingMachineState state;
    private int itemCount;
    private boolean hasMoney;

    public VendingMachine(int initialCount) {
        this.itemCount = initialCount;
        this.state = itemCount > 0 ? new IdleState() : new SoldOutState();
    }

    public void setState(VendingMachineState state) {
        this.state = state;
    }

    public VendingMachineState getState() {
        return state;
    }

    // Delegate to state
    public void insertDollar() {
        state.insertDollar(this);
    }

    public void ejectMoney() {
        state.ejectMoney(this);
    }

    public void dispense() {
        state.dispense(this);
    }

    public void refill(int count) {
        state.refill(this);
    }
}
```

---

## 📚 BÀI 4: SPRING INTEGRATION EXERCISES

### Exercise 4.1: Apply Patterns to Existing Code

**Yêu cầu:** Refactor code để áp dụng design patterns

```java
// ❌ BAD: Tight coupling, no patterns
@Service
public class OrderService {

    public void processOrder(Order order) {
        // Direct dependency
        MySqlDatabase db = new MySqlDatabase();
        db.connect();

        // Complex logic
        if (order.getPaymentType().equals("CREDIT_CARD")) {
            // Credit card logic
        } else if (order.getPaymentType().equals("PAYPAL")) {
            // PayPal logic
        } else if (order.getPaymentType().equals("CRYPTO")) {
            // Crypto logic
        }

        // Direct notification
        EmailSender email = new EmailSender();
        email.send(order.getEmail(), "Order confirmed");

        db.disconnect();
    }
}

// TODO: Refactor using:
// 1. Factory Method for payment processing
// 2. Observer pattern for notifications
// 3. Facade pattern for database operations
// 4. Strategy pattern for payment types
```

---

### Exercise 4.2: Spring AOP with Decorator

**Yêu cầu:** Implement custom AOP decorators

```java
// TODO: Create custom annotations
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Retry {
    int maxAttempts() default 3;
    long delay() default 1000;
}

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface CircuitBreaker {
    String name();
    int failureThreshold() default 5;
}

// TODO: Implement aspects
@Aspect
@Component
public class RetryAspect {
    @Around("@annotation(retry)")
    public Object retry(ProceedingJoinPoint pjp, Retry retry) throws Throwable {
        // Implement retry logic
    }
}

@Aspect
@Component
public class CircuitBreakerAspect {
    // Implement circuit breaker pattern
}

// Usage
@Service
public class ExternalApiService {

    @Retry(maxAttempts = 5, delay = 2000)
    @CircuitBreaker(name = "externalApi", failureThreshold = 3)
    public String callExternalApi() {
        // Unreliable external call
    }
}
```

---

### Exercise 4.3: Event-Driven Architecture

**Yêu cầu:** Implement event-driven order processing

```java
// TODO: Create events
public class OrderCreatedEvent extends ApplicationEvent { /* ... */ }
public class OrderPaidEvent extends ApplicationEvent { /* ... */ }
public class OrderShippedEvent extends ApplicationEvent { /* ... */ }
public class OrderCancelledEvent extends ApplicationEvent { /* ... */ }

// TODO: Create listeners
@Component
public class InventoryListener {
    @EventListener
    public void onOrderCreated(OrderCreatedEvent event) {
        // Reserve inventory
    }

    @EventListener
    public void onOrderCancelled(OrderCancelledEvent event) {
        // Release inventory
    }
}

@Component
public class PaymentListener {
    @EventListener
    public void onOrderCreated(OrderCreatedEvent event) {
        // Process payment
    }
}

// TODO: Create publisher
@Service
public class OrderService {

    @Autowired
    private ApplicationEventPublisher publisher;

    public Order createOrder(OrderRequest request) {
        Order order = repository.save(request.toOrder());
        publisher.publishEvent(new OrderCreatedEvent(this, order));
        return order;
    }
}
```

---

## 📝 CHECKLIST

Sau khi hoàn thành exercises, bạn sẽ hiểu:

- [ ] Cách implement 5 creational patterns
- [ ] Cách implement 5 structural patterns
- [ ] Cách implement 9 behavioral patterns
- [ ] Cách áp dụng patterns trong Spring Framework
- [ ] Cách refactor code để sử dụng patterns
- [ ] Cách kết hợp multiple patterns trong cùng một system

---

## 🔗 TÀI LIỆU THAM KHẢO

- [java-design-patterns.com](https://java-design-patterns.com)
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
- [Spring Framework Documentation](https://spring.io/projects/spring-framework)
- [Head First Design Patterns (Book)](https://www.oreilly.com/library/view/head-first-design/9781492078005/)
