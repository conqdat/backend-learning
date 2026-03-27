# Phase 1: Spring Boot Core Mastery - Ví Dụ Thực Tế

> **Mục tiêu:** Code mẫu thực tế cho từng chủ đề trong roadmap.sh/spring-boot

---

## 📁 PHẦN 1: SPRING CORE EXAMPLES

### 1.1 Dependency Injection Patterns

```java
// ❌ BAD: Field injection (hard to test)
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EmailService emailService;
}

// ✅ GOOD: Constructor injection (immutable, testable)
@Service
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;

    // Spring 4.3+: @Autowired optional if only one constructor
    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
}

// ✅ BEST: With record (Java 16+)
@Service
@RequiredArgsConstructor  // Lombok
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
}
```

---

### 1.2 Bean Scopes in Action

```java
// Singleton - Default scope, shared instance
@Component
public class ShoppingCartService {
    // Same instance for all requests
    // Use for stateless services
}

// Prototype - New instance each time
@Scope("prototype")
@Component
public class ShoppingCartItem {
    private String productId;
    private int quantity;
    // Each injection creates new instance
}

// Request - One instance per HTTP request
@Scope(value = WebApplicationContext.SCOPE_REQUEST)
@Component
public class RequestCounter {
    private int count = 0;

    public void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
    // Same counter throughout one request
}

// Session - One instance per user session
@Scope(value = WebApplicationContext.SCOPE_SESSION)
@Component
public class UserPreferences {
    private String language = "en";
    private String currency = "USD";

    // Getters/setters - persists across requests for same user
}

// Usage in controller
@RestController
public class CartController {

    @Autowired
    private RequestCounter counter;  // Fresh per request

    @Autowired
    private UserPreferences preferences;  // Same for user session

    @GetMapping("/cart")
    public ResponseEntity<Cart> getCart() {
        counter.increment();
        log.info("Request #{} for user with language: {}",
                 counter.getCount(), preferences.getLanguage());
        return ResponseEntity.ok(cartService.getCart());
    }
}
```

---

### 1.3 @Configuration with @Bean

```java
@Configuration
public class AppConfig {

    // Simple bean
    @Bean
    public ModelMapper modelMapper() {
        return new ModelMapper();
    }

    // Bean with dependencies
    @Bean
    public DataSource dataSource(
            @Value("${spring.datasource.url}") String url,
            @Value("${spring.datasource.username}") String username,
            @Value("${spring.datasource.password}") String password) {

        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(url);
        config.setUsername(username);
        config.setPassword(password);
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setConnectionTimeout(30000);

        return new HikariDataSource(config);
    }

    // Bean using another bean
    @Bean
    public JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    // Bean with lifecycle callbacks
    @Bean(initMethod = "initialize", destroyMethod = "cleanup")
    public CacheManager cacheManager() {
        return new CustomCacheManager();
    }

    // Conditional bean
    @Bean
    @ConditionalOnProperty(name = "redis.enabled", havingValue = "true")
    public RedisTemplate<String, Object> redisTemplate() {
        return new RedisTemplate<>();
    }
}
```

---

## 📁 PHẦN 2: SPRING BOOT AUTO-CONFIGURATION

### 2.1 Viewing Auto-Configuration Report

```yaml
# application.yml - Enable debug logging
debug: true
logging:
  level:
    org.springframework.boot.autoconfigure: DEBUG
```

**Sample output from CONDITIONS EVALUATION REPORT:**

```
Positive matches:
-----------------

   DataSourceAutoConfiguration matched:
      - @OnClassCondition found required classes
        'javax.sql.DataSource', 'org.springframework.jdbc.datasource.embedded.EmbeddedDatabaseType'
      - @OnPropertyCondition matched properties 'spring.datasource.url'
      - @OnMissingBeanCondition no beans of type DataSource found

   HibernateJpaAutoConfiguration matched:
      - @OnClassCondition found required class 'org.hibernate.jpa.HibernatePersistenceProvider'

Negative matches:
-----------------

   RedisAutoConfiguration:
      Did not match:
         - @OnClassCondition did not find required class 'org.springframework.data.redis.core.RedisTemplate'

   SecurityAutoConfiguration:
      Did not match:
         - @OnPropertyCondition spring.security.enabled=false
```

---

### 2.2 Overriding Auto-Configuration

```java
// Scenario 1: Custom DataSource with @Primary
@Configuration
public class CustomDataSourceConfig {

    @Bean
    @Primary  // This bean takes precedence
    @ConfigurationProperties("spring.datasource.primary")
    public DataSource primaryDataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:postgresql://localhost:5432/primary_db");
        ds.setMaximumPoolSize(20);
        ds.setIdleTimeout(30000);
        ds.setConnectionTimeout(30000);
        return ds;
    }

    @Bean
    @ConfigurationProperties("spring.datasource.secondary")
    public DataSource secondaryDataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:postgresql://localhost:5432/secondary_db");
        ds.setMaximumPoolSize(10);
        return ds;
    }
}

// Scenario 2: Excluding auto-configuration
@SpringBootApplication(exclude = {
    DataSourceAutoConfiguration.class,
    SecurityAutoConfiguration.class,
    HibernateJpaAutoConfiguration.class
})
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// Or via properties
// application.properties
spring.autoconfigure.exclude=\
  org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration,\
  org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration
```

---

### 2.3 Creating Custom Starter

**Project structure:**
```
custom-logging-starter/
├── pom.xml
├── src/main/java/com/company/logging/
│   ├── LoggingAutoConfiguration.java
│   ├── LoggingProperties.java
│   ├── JsonLogger.java
│   └── CorrelationIdFilter.java
└── src/main/resources/META-INF/spring/
    └── org.springframework.boot.autoconfigure.AutoConfiguration.imports
```

**pom.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.company</groupId>
    <artifactId>custom-logging-starter</artifactId>
    <version>1.0.0</version>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-autoconfigure</artifactId>
            <version>3.2.0</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-configuration-processor</artifactId>
            <version>3.2.0</version>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.15.3</version>
        </dependency>
    </dependencies>
</project>
```

**LoggingProperties.java:**
```java
package com.company.logging;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "company.logging")
public class LoggingProperties {

    private boolean enabled = true;
    private String format = "JSON";
    private String elkEndpoint = "http://logstash:5000";
    private boolean includeCorrelationId = true;
    private boolean includeTimestamp = true;

    // Getters and Setters
    public boolean isEnabled() { return enabled; }
    public void setEnabled(boolean enabled) { this.enabled = enabled; }

    public String getFormat() { return format; }
    public void setFormat(String format) { this.format = format; }

    public String getElkEndpoint() { return elkEndpoint; }
    public void setElkEndpoint(String elkEndpoint) { this.elkEndpoint = elkEndpoint; }

    public boolean isIncludeCorrelationId() { return includeCorrelationId; }
    public void setIncludeCorrelationId(boolean includeCorrelationId) {
        this.includeCorrelationId = includeCorrelationId;
    }

    public boolean isIncludeTimestamp() { return includeTimestamp; }
    public void setIncludeTimestamp(boolean includeTimestamp) {
        this.includeTimestamp = includeTimestamp;
    }
}
```

**JsonLogger.java:**
```java
package com.company.logging;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

public class JsonLogger {

    private static final Logger log = LoggerFactory.getLogger(JsonLogger.class);
    private final LoggingProperties properties;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public JsonLogger(LoggingProperties properties) {
        this.properties = properties;
    }

    public void info(String event, String message) {
        if (!properties.isEnabled()) return;
        log.info(createJsonLog("INFO", event, message));
    }

    public void error(String event, String message, Throwable throwable) {
        if (!properties.isEnabled()) return;
        log.error(createJsonLog("ERROR", event, message), throwable);
    }

    public void warn(String event, String message) {
        if (!properties.isEnabled()) return;
        log.warn(createJsonLog("WARN", event, message));
    }

    private String createJsonLog(String level, String event, String message) {
        try {
            Map<String, Object> logData = new HashMap<>();
            if (properties.isIncludeTimestamp()) {
                logData.put("timestamp", Instant.now().toString());
            }
            logData.put("level", level);
            logData.put("event", event);
            logData.put("message", message);
            logData.put("service", getServiceName());

            if (properties.isIncludeCorrelationId()) {
                logData.put("correlationId", getCorrelationId());
            }

            return objectMapper.writeValueAsString(logData);
        } catch (Exception e) {
            log.error("Failed to create JSON log", e);
            return message;
        }
    }

    private String getServiceName() {
        return System.getenv().getOrDefault("SERVICE_NAME", "unknown");
    }

    private String getCorrelationId() {
        ServletRequestAttributes attributes =
            (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        if (attributes != null) {
            String correlationId = attributes.getRequest().getHeader("X-Correlation-ID");
            return correlationId != null ? correlationId : "no-correlation-id";
        }
        return "no-correlation-id";
    }
}
```

**LoggingAutoConfiguration.java:**
```java
package com.company.logging;

import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConditionalOnClass(JsonLogger.class)
@EnableConfigurationProperties(LoggingProperties.class)
public class LoggingAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(prefix = "company.logging", name = "enabled",
                          havingValue = "true", matchIfMissing = true)
    public JsonLogger jsonLogger(LoggingProperties properties) {
        return new JsonLogger(properties);
    }

    @Bean
    @ConditionalOnProperty(prefix = "company.logging", name = "include-correlation-id",
                          havingValue = "true", matchIfMissing = true)
    public FilterRegistrationBean<CorrelationIdFilter> correlationIdFilter() {
        FilterRegistrationBean<CorrelationIdFilter> registration =
            new FilterRegistrationBean<>();
        registration.setFilter(new CorrelationIdFilter());
        registration.addUrlPatterns("/*");
        registration.setOrder(1);  // Run early in filter chain
        return registration;
    }
}
```

**CorrelationIdFilter.java:**
```java
package com.company.logging;

import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.UUID;

public class CorrelationIdFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        // Get or create correlation ID
        String correlationId = httpRequest.getHeader("X-Correlation-ID");
        if (correlationId == null || correlationId.isEmpty()) {
            correlationId = UUID.randomUUID().toString();
        }

        // Add to response headers
        httpResponse.setHeader("X-Correlation-ID", correlationId);
        httpResponse.setHeader("Access-Control-Expose-Headers", "X-Correlation-ID");

        // Continue filter chain
        chain.doFilter(request, response);
    }
}
```

**Register auto-configuration:**

File: `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`

```
com.company.logging.LoggingAutoConfiguration
```

**Usage in microservice:**

```xml
<!-- pom.xml -->
<dependency>
    <groupId>com.company</groupId>
    <artifactId>custom-logging-starter</artifactId>
    <version>1.0.0</version>
</dependency>
```

```yaml
# application.yml
company:
  logging:
    enabled: true
    format: JSON
    elk-endpoint: http://logstash.company.internal:5000
    include-correlation-id: true
    include-timestamp: true
```

```java
// In your service
@RestController
@RequestMapping("/orders")
public class OrderController {

    @Autowired
    private JsonLogger logger;

    @PostMapping
    public Order createOrder(@RequestBody OrderRequest request) {
        logger.info("ORDER_CREATE", "Creating order for user: " + request.getUserId());

        try {
            Order order = orderService.create(request);
            logger.info("ORDER_CREATED", "Order created: " + order.getId());
            return order;
        } catch (Exception e) {
            logger.error("ORDER_CREATE_FAILED", "Failed to create order", e);
            throw e;
        }
    }
}
```

**Sample log output:**
```json
{"timestamp":"2024-01-15T10:30:45.123Z","level":"INFO","event":"ORDER_CREATE","message":"Creating order for user: 123","service":"order-service","correlationId":"abc-123-def"}
{"timestamp":"2024-01-15T10:30:45.456Z","level":"INFO","event":"ORDER_CREATED","message":"Order created: 456","service":"order-service","correlationId":"abc-123-def"}
```

---

## 📁 PHẦN 3: SPRING MVC & REST API EXAMPLES

### 3.1 Complete REST Controller

```java
@RestController
@RequestMapping("/api/v1/users")
@Validated
public class UserController {

    @Autowired
    private UserService userService;

    // GET /api/v1/users - List all users with pagination
    @GetMapping
    public ResponseEntity<Page<UserResponse>> getUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String sortDir) {

        Pageable pageable = PageRequest.of(page, size,
            sortDir.equalsIgnoreCase("asc") ? Sort.by(sortBy).ascending() : Sort.by(sortBy).descending());

        Page<UserResponse> users = userService.findAll(pageable);
        return ResponseEntity.ok(users);
    }

    // GET /api/v1/users/{id} - Get single user
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // POST /api/v1/users - Create user
    @PostMapping
    public ResponseEntity<UserResponse> createUser(@Valid @RequestBody UserCreateRequest request) {
        UserResponse user = userService.create(request);
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .header(HttpHeaders.LOCATION, "/api/v1/users/" + user.getId())
            .body(user);
    }

    // PUT /api/v1/users/{id} - Full update
    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserUpdateRequest request) {
        return userService.update(id, request)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // PATCH /api/v1/users/{id} - Partial update
    @PatchMapping("/{id}")
    public ResponseEntity<UserResponse> patchUser(
            @PathVariable Long id,
            @RequestBody Map<String, Object> updates) {
        return userService.patch(id, updates)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // DELETE /api/v1/users/{id} - Delete user
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }

    // GET /api/v1/users/search/email?email=test@example.com
    @GetMapping("/search/email")
    public ResponseEntity<UserResponse> getUserByEmail(@RequestParam String email) {
        return userService.findByEmail(email)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}
```

---

### 3.2 DTOs and Validation

```java
// Create Request DTO
public record UserCreateRequest(
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    String email,

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    String name,

    @NotNull(message = "Age is required")
    @Min(value = 18, message = "Must be at least 18 years old")
    @Max(value = 150, message = "Age cannot exceed 150")
    Integer age,

    @Pattern(regexp = "^\\+?[0-9\\s-]{8,15}$", message = "Invalid phone number")
    String phoneNumber
) {}

// Update Request DTO (all fields optional)
public record UserUpdateRequest(
    @Email(message = "Invalid email format")
    String email,

    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    String name,

    @Min(value = 18, message = "Must be at least 18 years old")
    @Max(value = 150, message = "Age cannot exceed 150")
    Integer age
) {}

// Response DTO
public record UserResponse(
    Long id,
    String email,
    String name,
    Integer age,
    String phoneNumber,
    LocalDateTime createdAt,
    LocalDateTime updatedAt
) {}
```

---

### 3.3 Global Exception Handler

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    // Resource not found
    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(ResourceNotFoundException ex) {
        return new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage(),
            LocalDateTime.now()
        );
    }

    // Validation errors
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ValidationErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        List<FieldError> fieldErrors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(error -> new FieldError(
                error.getField(),
                error.getRejectedValue(),
                error.getDefaultMessage()
            ))
            .collect(Collectors.toList());

        return new ValidationErrorResponse(
            HttpStatus.BAD_REQUEST.value(),
            "Validation failed",
            fieldErrors,
            LocalDateTime.now()
        );
    }

    // Constraint violation
    @ExceptionHandler(ConstraintViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ValidationErrorResponse handleConstraintViolation(ConstraintViolationException ex) {
        List<FieldError> fieldErrors = ex.getConstraintViolations()
            .stream()
            .map(violation -> new FieldError(
                violation.getPropertyPath().toString(),
                violation.getInvalidValue(),
                violation.getMessage()
            ))
            .collect(Collectors.toList());

        return new ValidationErrorResponse(
            HttpStatus.BAD_REQUEST.value(),
            "Constraint violation",
            fieldErrors,
            LocalDateTime.now()
        );
    }

    // Duplicate resource
    @ExceptionHandler(DuplicateResourceException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ErrorResponse handleDuplicate(DuplicateResourceException ex) {
        return new ErrorResponse(
            HttpStatus.CONFLICT.value(),
            ex.getMessage(),
            LocalDateTime.now()
        );
    }

    // Generic exception
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleGeneric(Exception ex) {
        // Log the exception
        LoggerFactory.getLogger(GlobalExceptionHandler.class)
            .error("Unhandled exception", ex);

        return new ErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "An unexpected error occurred",
            LocalDateTime.now()
        );
    }
}

// Error response DTOs
public record ErrorResponse(
    int status,
    String message,
    LocalDateTime timestamp
) {}

public record ValidationErrorResponse(
    int status,
    String message,
    List<FieldError> errors,
    LocalDateTime timestamp
) {}

public record FieldError(
    String field,
    Object rejectedValue,
    String message
) {}

// Custom exceptions
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}

public class DuplicateResourceException extends RuntimeException {
    public DuplicateResourceException(String message) {
        super(message);
    }
}
```

---

## 📁 PHẦN 4: SPRING DATA JPA EXAMPLES

### 4.1 Entity with Relationships

```java
@Entity
@Table(name = "orders")
@EntityListeners(AuditingEntityListener.class)  // Auto-manage createdAt/updatedAt
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String orderNumber;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    @JsonBackReference  // Prevent infinite serialization
    private User user;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    @JsonManagedReference
    private List<OrderItem> items = new ArrayList<>();

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private OrderStatus status = OrderStatus.PENDING;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal totalAmount;

    @Column(name = "created_at")
    @CreatedDate
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    @LastModifiedDate
    private LocalDateTime updatedAt;

    // Constructors
    public Order() {}

    // Helper methods for bidirectional relationship
    public void addItem(OrderItem item) {
        items.add(item);
        item.setOrder(this);
    }

    public void removeItem(OrderItem item) {
        items.remove(item);
        item.setOrder(null);
    }

    // Calculate total
    public BigDecimal calculateTotal() {
        return items.stream()
            .map(OrderItem::getSubtotal)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    // Getters, setters, equals, hashCode...
}

// OrderItem entity
@Entity
@Table(name = "order_items")
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    @Column(nullable = false)
    private Integer quantity;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal unitPrice;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal subtotal;

    // Getters, setters...

    @PrePersist
    @PreUpdate
    public void calculateSubtotal() {
        if (quantity != null && unitPrice != null) {
            this.subtotal = unitPrice.multiply(BigDecimal.valueOf(quantity));
        }
    }
}

// Enum for order status
public enum OrderStatus {
    PENDING,
    CONFIRMED,
    PROCESSING,
    SHIPPED,
    DELIVERED,
    CANCELLED
}
```

---

### 4.2 Repository with Custom Queries

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    // Derived query method
    List<Order> findByUserId(Long userId);

    // Derived query with multiple conditions
    List<Order> findByUserIdAndStatus(Long userId, OrderStatus status);

    // Derived query with date range
    List<Order> findByCreatedAtBetween(LocalDateTime start, LocalDateTime end);

    // Derived query with sorting
    List<Order> findByStatusOrderByCreatedAtDesc(OrderStatus status);

    // Custom query with @Query
    @Query("SELECT o FROM Order o JOIN o.user u WHERE u.email = :email")
    List<Order> findByUserEmail(@Param("email") String email);

    // Native query
    @Query(value = """
        SELECT o.* FROM orders o
        WHERE o.total_amount > :minAmount
        AND o.status = :status
        ORDER BY o.created_at DESC
        LIMIT :limit
        """, nativeQuery = true)
    List<Order> findHighValueOrders(
        @Param("minAmount") BigDecimal minAmount,
        @Param("status") OrderStatus status,
        @Param("limit") int limit
    );

    // Aggregation query
    @Query("SELECT o.status, COUNT(o) FROM Order o GROUP BY o.status")
    List<Object[]> countOrdersByStatus();

    // Update query
    @Modifying
    @Transactional
    @Query("UPDATE Order o SET o.status = :status WHERE o.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") OrderStatus status);

    // Delete query
    @Modifying
    @Transactional
    @Query("DELETE FROM Order o WHERE o.status = :status AND o.createdAt < :date")
    int deleteOldOrders(@Param("status") OrderStatus status, @Param("date") LocalDateTime date);

    // Exists query
    boolean existsByOrderNumber(String orderNumber);

    // Count query
    long countByUserId(Long userId);
}
```

---

### 4.3 Transaction Management Example

```java
@Service
@Transactional(readOnly = true)  // Default: read-only transactions
public class OrderService {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private InventoryService inventoryService;

    @Autowired
    private PaymentService paymentService;

    @Autowired
    private EventPublisher eventPublisher;

    // Full transaction - all or nothing
    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        // 1. Validate user exists
        User user = userRepository.findById(request.getUserId())
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        // 2. Check and reserve inventory
        inventoryService.reserveItems(request.getItems());

        // 3. Process payment
        PaymentResult payment = paymentService.charge(
            user.getPaymentMethod(),
            request.getTotalAmount()
        );

        if (!payment.isSuccess()) {
            throw new PaymentFailedException("Payment declined");
        }

        // 4. Create order
        Order order = new Order();
        order.setOrderNumber(generateOrderNumber());
        order.setUser(user);
        order.setStatus(OrderStatus.CONFIRMED);
        order.setTotalAmount(request.getTotalAmount());

        request.getItems().forEach(item -> {
            OrderItem orderItem = new OrderItem();
            orderItem.setProduct(item.getProduct());
            orderItem.setQuantity(item.getQuantity());
            orderItem.setUnitPrice(item.getProduct().getPrice());
            order.addItem(orderItem);
        });

        Order savedOrder = orderRepository.save(order);

        // 5. Publish event (async, outside main transaction)
        eventPublisher.publishOrderCreated(savedOrder);

        return savedOrder;
    }

    // Read-only transaction (optimization)
    public Order getOrder(Long id) {
        return orderRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Order not found"));
    }

    // REQUIRES_NEW - creates new transaction even if one exists
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void sendOrderConfirmation(Order order) {
        // Email sending logic
        // If this fails, it won't rollback the main order transaction
        emailService.sendConfirmation(order);
    }

    // NESTED - creates savepoint within existing transaction
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void updateInventory(Order order) {
        // Inventory update logic
        // Can be rolled back independently
        inventoryService.deductItems(order.getItems());
    }

    // Timeout - rollback if takes too long
    @Transactional(timeout = 30)  // 30 seconds timeout
    public Order processLargeOrder(CreateOrderRequest request) {
        // Complex processing that should complete within timeout
        return createOrder(request);
    }

    // No transaction - for operations that shouldn't be in transaction
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void generateOrderReport(Order order) {
        // Report generation - can take time, doesn't need transaction
        reportService.generate(order);
    }

    private String generateOrderNumber() {
        return "ORD-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 8);
    }
}
```

---

## 📁 PHẦN 5: SPRING SECURITY EXAMPLES

### 5.1 Basic Security Configuration

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity  // Enable @PreAuthorize, @PostAuthorize
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // Disable CSRF for stateless API
            .csrf(csrf -> csrf.disable())

            // Configure authorization
            .authorizeHttpRequests(auth -> auth
                // Public endpoints
                .requestMatchers(
                    "/api/auth/**",
                    "/api/public/**",
                    "/swagger-ui/**",
                    "/v3/api-docs/**",
                    "/actuator/health"
                ).permitAll()

                // Admin-only endpoints
                .requestMatchers("/api/admin/**").hasRole("ADMIN")

                // User or Admin
                .requestMatchers("/api/users/**").hasAnyRole("USER", "ADMIN")

                // All other endpoints require authentication
                .anyRequest().authenticated()
            )

            // Enable HTTP Basic
            .httpBasic(Customizer.withDefaults())

            // Stateless session (for REST API)
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )

            // Exception handling
            .exceptionHandling(exceptions -> exceptions
                .authenticationEntryPoint(new JwtAuthenticationEntryPoint())
                .accessDeniedHandler(new JwtAccessDeniedHandler())
            );

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration authConfig) throws Exception {
        return authConfig.getAuthenticationManager();
    }
}
```

---

### 5.2 JWT Authentication Implementation

```java
// JWT Authentication Filter
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    @Autowired
    private JwtTokenProvider tokenProvider;

    @Autowired
    private UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        try {
            String token = extractToken(request);

            if (token != null && tokenProvider.validateToken(token)) {
                String username = tokenProvider.getUsername(token);
                UserDetails userDetails = userDetailsService.loadUserByUsername(username);

                UsernamePasswordAuthenticationToken authentication =
                    new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,
                        userDetails.getAuthorities()
                    );

                authentication.setDetails(
                    new WebAuthenticationDetailsSource().buildDetails(request)
                );

                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        } catch (Exception ex) {
            logger.error("Could not set user authentication", ex);
            SecurityContextHolder.clearContext();
        }

        filterChain.doFilter(request, response);
    }

    private String extractToken(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
}

// JWT Token Provider
@Component
public class JwtTokenProvider {

    @Value("${jwt.secret}")
    private String jwtSecret;

    @Value("${jwt.expiration-ms}")
    private long jwtExpirationMs;

    public String generateToken(UserDetails userDetails) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + jwtExpirationMs);

        return Jwts.builder()
            .setSubject(userDetails.getUsername())
            .setIssuedAt(now)
            .setExpiration(expiryDate)
            .signWith(SignatureAlgorithm.HS512, jwtSecret)
            .compact();
    }

    public String getUsername(String token) {
        Claims claims = Jwts.parser()
            .setSigningKey(jwtSecret)
            .parseClaimsJws(token)
            .getBody();

        return claims.getSubject();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(jwtSecret).parseClaimsJws(token);
            return true;
        } catch (SignatureException ex) {
            logger.error("Invalid JWT signature");
        } catch (MalformedJwtException ex) {
            logger.error("Invalid JWT token");
        } catch (ExpiredJwtException ex) {
            logger.error("Expired JWT token");
        } catch (UnsupportedJwtException ex) {
            logger.error("Unsupported JWT token");
        } catch (IllegalArgumentException ex) {
            logger.error("JWT claims string is empty");
        }
        return false;
    }

    public long getExpirationMs() {
        return jwtExpirationMs;
    }
}

// Custom UserDetailsService
@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        User user = userRepository.findByEmail(email)
            .orElseThrow(() -> new UsernameNotFoundException("User not found with email: " + email));

        List<GrantedAuthority> authorities = user.getRoles().stream()
            .map(role -> new SimpleGrantedAuthority("ROLE_" + role.getName()))
            .collect(Collectors.toList());

        return new org.springframework.security.core.userdetails.User(
            user.getEmail(),
            user.getPassword(),
            authorities
        );
    }
}

// Auth Controller
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtTokenProvider tokenProvider;

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody LoginRequest request) {
        Authentication authentication = authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(
                request.getEmail(),
                request.getPassword()
            )
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);

        String token = tokenProvider.generateToken(
            (UserDetails) authentication.getPrincipal()
        );

        return ResponseEntity.ok(new AuthResponse(token));
    }
}

// Request/Response DTOs
public record LoginRequest(
    @Email String email,
    String password
) {}

public record AuthResponse(
    String token
) {}
```

---

### 5.3 Method-Level Security

```java
@Service
public class UserService {

    // Only users with ADMIN role can call this
    @PreAuthorize("hasRole('ADMIN')")
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    // Users can only access their own data
    @PreAuthorize("#email == authentication.principal.username")
    public User getUserByEmail(String email) {
        return userRepository.findByEmail(email)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }

    // Check ownership before deleting
    @PreAuthorize("@userService.isOwner(#userId, authentication.principal.username)")
    public void deleteUser(Long userId) {
        userRepository.deleteById(userId);
    }

    // Check if user owns the resource
    @PostAuthorize("returnObject.email == authentication.principal.username")
    public User getUser(Long userId) {
        return userRepository.findById(userId)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }

    // Custom expression using @userService
    public boolean isOwner(Long userId, String email) {
        return userRepository.findById(userId)
            .map(user -> user.getEmail().equals(email))
            .orElse(false);
    }
}
```

---

## 📁 PHẦN 6: ACTUATOR EXAMPLES

### 6.1 Production Configuration

```yaml
# application.yml
management:
  # Separate port for management endpoints (security best practice)
  server:
    port: 9090

  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,env,loggers,threaddump
      base-path: /actuator

  endpoint:
    health:
      show-details: always
      probes:
        enabled: true  # Kubernetes liveness/readiness probes

  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:development}
```

---

### 6.2 Custom Health Indicators

```java
@Component
public class RedisHealthIndicator implements HealthIndicator {

    @Autowired
    private RedisConnectionFactory redisConnectionFactory;

    @Override
    public Health health() {
        try {
            RedisConnection connection = redisConnectionFactory.getConnection();
            String ping = connection.ping();
            connection.close();

            if ("PONG".equals(ping)) {
                return Health.up()
                    .withDetail("redis", "connected")
                    .withDetail("host", "redis:6379")
                    .build();
            }

            return Health.down()
                .withDetail("redis", "unexpected response: " + ping)
                .build();

        } catch (Exception e) {
            return Health.down(e)
                .withDetail("redis", "connection failed")
                .build();
        }
    }
}

@Component
public class ExternalApiHealthIndicator implements HealthIndicator {

    @Value("${external.payment-api.url}")
    private String paymentApiUrl;

    private final HttpClient httpClient = HttpClient.newHttpClient();

    @Override
    public Health health() {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(paymentApiUrl + "/health"))
                .timeout(Duration.ofSeconds(5))
                .GET()
                .build();

            HttpResponse<String> response = httpClient.send(
                request,
                HttpResponse.BodyHandlers.ofString()
            );

            if (response.statusCode() == 200) {
                return Health.up()
                    .withDetail("payment-api", "healthy")
                    .withDetail("response-time-ms", response.headers()
                        .firstValue("X-Response-Time").orElse("unknown"))
                    .build();
            }

            return Health.down()
                .withDetail("payment-api", "unhealthy status: " + response.statusCode())
                .build();

        } catch (Exception e) {
            return Health.down(e)
                .withDetail("payment-api", "connection failed")
                .build();
        }
    }
}

@Component
public class DatabasePoolHealthIndicator implements HealthIndicator {

    @Autowired
    private DataSource dataSource;

    @Override
    public Health health() {
        try {
            HikariDataSource hikariDataSource = dataSource.unwrap(HikariDataSource.class);

            if (hikariDataSource == null) {
                return Health.unknown()
                    .withDetail("pool", "HikariCP not detected")
                    .build();
            }

            int activeConnections = hikariDataSource.getHikariPoolMXBean().getActiveConnections();
            int idleConnections = hikariDataSource.getHikariPoolMXBean().getIdleConnections();
            int maxPoolSize = hikariDataSource.getMaximumPoolSize();

            Map<String, Object> details = new HashMap<>();
            details.put("active-connections", activeConnections);
            details.put("idle-connections", idleConnections);
            details.put("max-pool-size", maxPoolSize);
            details.put("utilization-percent", (activeConnections * 100.0) / maxPoolSize);

            // Warning if pool utilization > 80%
            if (activeConnections > (maxPoolSize * 0.8)) {
                return Health.warning()
                    .withDetails(details)
                    .withDetail("warning", "High pool utilization")
                    .build();
            }

            return Health.up()
                .withDetails(details)
                .build();

        } catch (Exception e) {
            return Health.down(e)
                .withDetail("pool", "failed to get pool stats")
                .build();
        }
    }
}
```

---

### 6.3 Custom Metrics

```java
@Component
public class OrderMetrics {

    private final MeterRegistry meterRegistry;
    private final Counter ordersCreatedCounter;
    private final Counter ordersFailedCounter;
    private final Timer orderProcessingTimer;
    private final DistributionSummary orderValueSummary;

    public OrderMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;

        this.ordersCreatedCounter = Counter.builder("orders.created.total")
            .description("Total number of orders created")
            .tag("application", "order-service")
            .register(meterRegistry);

        this.ordersFailedCounter = Counter.builder("orders.failed.total")
            .description("Total number of failed orders")
            .tag("application", "order-service")
            .register(meterRegistry);

        this.orderProcessingTimer = Timer.builder("orders.processing.time")
            .description("Time taken to process orders")
            .tag("application", "order-service")
            .register(meterRegistry);

        this.orderValueSummary = DistributionSummary.builder("orders.value")
            .description("Order values distribution")
            .tag("application", "order-service")
            .baseUnit("USD")
            .register(meterRegistry);
    }

    public void recordOrderCreated() {
        ordersCreatedCounter.increment();
    }

    public void recordOrderFailed() {
        ordersFailedCounter.increment();
    }

    public <T> T recordProcessingTime(Supplier<T> supplier) {
        return orderProcessingTimer.recordSupplier(supplier);
    }

    public void recordOrderValue(double value) {
        orderValueSummary.record(value);
    }
}

// Usage in service
@Service
public class OrderService {

    @Autowired
    private OrderMetrics metrics;

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        return metrics.recordProcessingTime(() -> {
            try {
                Order order = orderRepository.save(createOrderEntity(request));
                metrics.recordOrderCreated();
                metrics.recordOrderValue(order.getTotalAmount().doubleValue());
                return order;
            } catch (Exception e) {
                metrics.recordOrderFailed();
                throw e;
            }
        });
    }
}
```

---

## 📁 PHẦN 7: TESTING EXAMPLES

### 7.1 Unit Test with Mockito

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private InventoryService inventoryService;

    @Mock
    private PaymentService paymentService;

    @InjectMocks
    private OrderService orderService;

    @Test
    void shouldCreateOrderSuccessfully() {
        // Given
        Long userId = 1L;
        CreateOrderRequest request = new CreateOrderRequest(userId, List.of());

        User user = new User(userId, "test@example.com", "Test User");
        when(userRepository.findById(userId)).thenReturn(Optional.of(user));
        when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArguments()[0]);

        // When
        Order result = orderService.createOrder(request);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getUser()).isEqualTo(user);
        verify(inventoryService).reserveItems(request.getItems());
        verify(paymentService).charge(any(), any());
        verify(orderRepository).save(any(Order.class));
    }

    @Test
    void shouldThrowExceptionWhenUserNotFound() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest(999L, List.of());
        when(userRepository.findById(999L)).thenReturn(Optional.empty());

        // When/Then
        assertThrows(ResourceNotFoundException.class, () ->
            orderService.createOrder(request)
        );
    }

    @Test
    void shouldThrowExceptionWhenPaymentFails() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest(1L, List.of());
        User user = new User(1L, "test@example.com", "Test User");

        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(paymentService.charge(any(), any()))
            .thenThrow(new PaymentFailedException("Payment declined"));

        // When/Then
        assertThrows(PaymentFailedException.class, () ->
            orderService.createOrder(request)
        );
        verify(orderRepository, never()).save(any());
    }
}
```

---

### 7.2 Integration Test

```java
@SpringBootTest
@AutoConfigureMockMvc
@Transactional  // Rollback after each test
class OrderControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        // Create test user
        User user = new User();
        user.setEmail("test@example.com");
        user.setName("Test User");
        userRepository.save(user);
    }

    @Test
    void shouldCreateOrder() throws Exception {
        // Given
        CreateOrderRequest request = new CreateOrderRequest(1L, List.of(
            new OrderItemRequest(1L, 2, new BigDecimal("10.00"))
        ));

        // When/Then
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.status").value("CONFIRMED"))
            .andExpect(jsonPath("$.totalAmount").value(20.00));
    }

    @Test
    void shouldGetOrderById() throws Exception {
        // Given
        Order order = createTestOrder();

        // When/Then
        mockMvc.perform(get("/api/orders/{id}", order.getId()))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.orderNumber").value(order.getOrderNumber()));
    }

    @Test
    void shouldReturnNotFoundForNonExistentOrder() throws Exception {
        // When/Then
        mockMvc.perform(get("/api/orders/{id}", 999L))
            .andExpect(status().isNotFound());
    }

    @Test
    void shouldDeleteOrder() throws Exception {
        // Given
        Order order = createTestOrder();

        // When/Then
        mockMvc.perform(delete("/api/orders/{id}", order.getId()))
            .andExpect(status().isNoContent());

        // Verify deletion
        assertThat(orderRepository.findById(order.getId())).isEmpty();
    }

    private Order createTestOrder() {
        User user = userRepository.findAll().get(0);
        Order order = new Order();
        order.setOrderNumber("TEST-001");
        order.setUser(user);
        order.setStatus(OrderStatus.PENDING);
        order.setTotalAmount(new BigDecimal("100.00"));
        return orderRepository.save(order);
    }
}
```

---

### 7.3 Test Slices

```java
// Repository layer test
@DataJpaTest
class OrderRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private OrderRepository orderRepository;

    @Test
    void shouldSaveAndFindOrder() {
        // Given
        Order order = new Order();
        order.setOrderNumber("TEST-001");
        order.setStatus(OrderStatus.PENDING);
        order.setTotalAmount(new BigDecimal("100.00"));

        // When
        Order saved = orderRepository.save(order);
        entityManager.flush();

        // Then
        assertThat(saved.getId()).isNotNull();
        assertThat(orderRepository.findByOrderNumber("TEST-001")).isPresent();
    }

    @Test
    void shouldFindOrdersByStatus() {
        // Given
        Order order1 = createOrder(OrderStatus.PENDING);
        Order order2 = createOrder(OrderStatus.COMPLETED);

        entityManager.flush();

        // When
        List<Order> pendingOrders = orderRepository.findByStatusOrderByCreatedAtDesc(OrderStatus.PENDING);

        // Then
        assertThat(pendingOrders).hasSize(1);
        assertThat(pendingOrders.get(0).getOrderNumber()).isEqualTo("TEST-001");
    }

    private Order createOrder(OrderStatus status) {
        Order order = new Order();
        order.setOrderNumber("TEST-" + UUID.randomUUID());
        order.setStatus(status);
        order.setTotalAmount(new BigDecimal("100.00"));
        return entityManager.persist(order);
    }
}

// Web layer test
@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private OrderService orderService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldReturnOrder() throws Exception {
        // Given
        Order order = new Order();
        order.setId(1L);
        order.setOrderNumber("TEST-001");

        when(orderService.getOrder(1L)).thenReturn(order);

        // When/Then
        mockMvc.perform(get("/api/orders/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.orderNumber").value("TEST-001"));
    }

    @Test
    void shouldReturnNotFound() throws Exception {
        // Given
        when(orderService.getOrder(999L))
            .thenThrow(new ResourceNotFoundException("Order not found"));

        // When/Then
        mockMvc.perform(get("/api/orders/999"))
            .andExpect(status().isNotFound());
    }
}
```

---

## 🔗 TÀI LIỆU THAM KHẢO

- [Spring Boot Official Docs](https://spring.io/projects/spring-boot)
- [Spring Framework Docs](https://spring.io/projects/spring-framework)
- [Spring Security Reference](https://docs.spring.io/spring-security/reference/)
- [Spring Data JPA Docs](https://docs.spring.io/spring-data/jpa/reference/)
- [Roadmap.sh Spring Boot](https://roadmap.sh/spring-boot)

---

Đọc `03-exercises.md` để làm bài tập thực hành!
