# Phase 1: Spring Boot Core Mastery - Lý Thuyết

> **Thời gian:** 3-4 tuần
> **Mục tiêu:** Nắm vững Spring Boot theo roadmap.sh/java
> **Quan trọng:** Hiểu sâu cơ chế hoạt động, không chỉ biết dùng!

---

## 📚 PHẦN 1: SPRING FUNDAMENTALS

### 1.1 Why Spring?

**Vấn đề trước khi có Spring:**
- Enterprise Java (J2EE) phức tạp, nặng nề
- Phụ thuộc chặt vào application server (WebLogic, WebSphere)
- Khó test, khó maintain
- Cấu hình XML everywhere

**Spring giải quyết:**
- Lightweight container
- POJO-based programming
- Dependency Injection
- Aspect-Oriented Programming
- Consistent abstraction layer

---

### 1.2 Spring Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Spring Framework                          │
├─────────────────────────────────────────────────────────────┤
│  Core Container                                              │
│  ├── Beans (DI, IoC)                                        │
│  ├── Core (SPI utilities)                                   │
│  ├── Context (ApplicationContext)                           │
│  └── SpEL (Expression Language)                             │
├─────────────────────────────────────────────────────────────┤
│  Data Access/Integration                                     │
│  ├── JDBC                                                   │
│  ├── ORM (Hibernate, JPA)                                   │
│  ├── OXM (XML binding)                                      │
│  ├── JMS (Messaging)                                        │
│  └── Transactions                                           │
├─────────────────────────────────────────────────────────────┤
│  Web                                                         │
│  ├── Web (Servlet, WebSocket)                               │
│  ├── Web MVC (REST, views)                                  │
│  └── WebFlux (Reactive)                                     │
├─────────────────────────────────────────────────────────────┤
│  AOP (Aspect-Oriented Programming)                          │
│  ├── Aspects                                                │
│  ├── Instrumentation                                        │
│  └── Messaging                                              │
├─────────────────────────────────────────────────────────────┤
│  Test                                                        │
│  ├── Unit Testing (JUnit integration)                       │
│  └── Integration Testing                                    │
└─────────────────────────────────────────────────────────────┘
```

---

### 1.3 Dependency Injection (DI) & Inversion of Control (IoC)

**Dependency Injection là gì?**

```java
// ❌ WITHOUT DI - Tight coupling
public class UserService {
    private UserRepository repository = new UserRepository();

    public User getUser(Long id) {
        return repository.findById(id);
    }
}

// ✅ WITH DI - Loose coupling
public class UserService {
    private final UserRepository repository;

    // Constructor Injection (recommended)
    public UserService(UserRepository repository) {
        this.repository = repository;
    }

    public User getUser(Long id) {
        return repository.findById(id);
    }
}
```

**Types of DI:**

```java
// 1. Constructor Injection (Best practice)
@Component
public class UserService {
    private final UserRepository repository;

    @Autowired  // Optional if only one constructor (Spring 4.3+)
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}

// 2. Setter Injection
@Component
public class UserService {
    private UserRepository repository;

    @Autowired
    public void setRepository(UserRepository repository) {
        this.repository = repository;
    }
}

// 3. Field Injection (Not recommended - hard to test)
@Component
public class UserService {
    @Autowired
    private UserRepository repository;
}
```

---

### 1.4 Spring Bean Scopes

```java
// 1. Singleton (default) - One instance per Spring context
@Scope("singleton")
@Component
public class SingletonBean {
    // Shared across entire application
}

// 2. Prototype - New instance each time requested
@Scope("prototype")
@Component
public class PrototypeBean {
    // New instance for each injection point
}

// 3. Request - One instance per HTTP request (web apps)
@Scope(value = WebApplicationContext.SCOPE_REQUEST)
@Component
public class RequestBean {
    // Lives for one HTTP request
}

// 4. Session - One instance per HTTP session (web apps)
@Scope(value = WebApplicationContext.SCOPE_SESSION)
@Component
public class SessionBean {
    // Lives for HTTP session lifetime
}

// 5. Application - One instance per ServletContext
@Scope(value = WebApplicationContext.SCOPE_APPLICATION)
@Component
public class ApplicationBean {
    // Lives for ServletContext lifetime
}

// 6. Websocket - One instance per WebSocket session
@Scope(value = WebApplicationContext.SCOPE_WEBSOCKET)
@Component
public class WebsocketBean {
    // Lives for WebSocket session
}
```

**Scope comparison:**

| Scope | Lifecycle | Use Case |
|-------|-----------|----------|
| singleton | Entire application lifetime | Statelesss services, repositories (default) |
| prototype | Each time requested | Stateful beans, command objects |
| request | HTTP request lifetime | Request-scoped data |
| session | HTTP session lifetime | User session data |
| application | ServletContext lifetime | Application-wide cache |

---

### 1.5 Spring Annotations

**Core Annotations:**

| Annotation | Purpose | Example |
|------------|---------|---------|
| `@Component` | Generic Spring component | `@Component public class Helper {}` |
| `@Service` | Business logic layer | `@Service public class UserService {}` |
| `@Repository` | Data access layer | `@Repository public interface UserRepository {}` |
| `@Controller` | MVC controller | `@Controller public class HomeController {}` |
| `@RestController` | REST controller | `@RestController public class ApiController {}` |
| `@Configuration` | Configuration class | `@Configuration public class AppConfig {}` |
| `@Bean` | Declare bean in configuration | `@Bean public DataSource ds() {}` |
| `@Autowired` | Inject dependency | `@Autowired private Repository repo;` |
| `@Qualifier` | Specify which bean to inject | `@Qualifier("primaryRepo")` |
| `@Primary` | Mark bean as primary candidate | `@Primary @Bean` |
| `@Value` | Inject property value | `@Value("${app.name}")` |
| `@PropertySource` | Load properties file | `@PropertySource("classpath:app.properties")` |

**Component Scan:**

```java
@Configuration
@ComponentScan(basePackages = {"com.example.service", "com.example.repository"})
public class AppConfig {
    // Spring will scan and register @Component, @Service, @Repository, etc.
}
```

---

## 📚 PHẦN 2: SPRING BOOT CORE

### 2.1 What is Spring Boot?

**Spring Boot = Spring + Convention over Configuration**

Spring Boot solves:
- ❌ Too much XML configuration
- ❌ Dependency version management
- ❌ Complex deployment setup
- ❌ Time-consuming project initialization

**Key Features:**
- ✅ Starter dependencies
- ✅ Auto-configuration
- ✅ Embedded servers
- ✅ Production-ready monitoring (Actuator)
- ✅ No XML configuration required

---

### 2.2 Spring Boot Starters

**Starter = Dependency bundle**

```xml
<!-- Instead of adding 15+ dependencies manually -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>
<!-- ... many more -->

<!-- Just add one starter -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

**Common Starters:**

| Starter | Dependencies Included | Use Case |
|---------|----------------------|----------|
| `spring-boot-starter-web` | Spring MVC, Tomcat, Jackson | REST APIs, Web apps |
| `spring-boot-starter-data-jpa` | Hibernate, Spring Data JPA | Database access |
| `spring-boot-starter-data-redis` | Spring Data Redis, Lettuce | Redis caching |
| `spring-boot-starter-security` | Spring Security | Authentication, Authorization |
| `spring-boot-starter-validation` | Hibernate Validator | Input validation |
| `spring-boot-starter-actuator` | Metrics, Health endpoints | Production monitoring |
| `spring-boot-starter-test` | JUnit, Mockito, AssertJ | Testing |
| `spring-boot-starter-webflux` | Spring WebFlux, Reactor | Reactive web apps |
| `spring-boot-starter-aop` | Spring AOP, AspectJ | Aspect-oriented programming |

**View dependency tree:**
```bash
mvn dependency:tree
```

---

### 2.3 Auto-Configuration

**How it works:**

1. Spring Boot scans classpath for `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`
2. Loads auto-configuration classes
3. Each configuration has **conditions** - only activate if conditions are met

**Conditional Annotations:**

| Annotation | Condition | Example |
|------------|-----------|---------|
| `@ConditionalOnClass` | Class exists in classpath | `@ConditionalOnClass(RedisTemplate.class)` |
| `@ConditionalOnMissingClass` | Class does NOT exist | `@ConditionalOnMissingClass("com.mysql.Driver")` |
| `@ConditionalOnBean` | Bean exists | `@ConditionalOnBean(DataSource.class)` |
| `@ConditionalOnMissingBean` | Bean does NOT exist | `@ConditionalOnMissingBean(UserService.class)` |
| `@ConditionalOnProperty` | Property is set | `@ConditionalOnProperty(name="cache.enabled")` |
| `@ConditionalOnWebApplication` | Is web application | `@ConditionalOnWebApplication` |
| `@ConditionalOnExpression` | SpEL expression | `@ConditionalOnExpression("${feature.enabled}")` |

**Example: DataSource Auto-Configuration**

```java
@Configuration
@ConditionalOnClass({DataSource.class, JdbcTemplate.class})
@ConditionalOnMissingBean(DataSource.class)
@ConditionalOnProperty(prefix = "spring.datasource", name = "url")
public class DataSourceAutoConfiguration {

    @Bean
    @ConfigurationProperties(prefix = "spring.datasource")
    public DataSource dataSource() {
        return new HikariDataSource();
    }
}
```

---

### 2.4 Embedded Servers

Spring Boot embeds server into JAR:

```bash
java -jar app.jar
```

**Supported Servers:**

| Server | Dependency | Characteristics |
|--------|-----------|-----------------|
| Tomcat | `spring-boot-starter-web` (default) | Most popular, full-featured |
| Jetty | `spring-boot-starter-jetty` | Lightweight, modular |
| Undertow | `spring-boot-starter-undertow` | High performance, non-blocking |

**Change server:**
```xml
<!-- Exclude Tomcat, include Jetty -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>
```

**Configuration:**
```yaml
server:
  port: 8080
  servlet:
    context-path: /api
  compression:
    enabled: true
  tomcat:
    max-threads: 200
    accept-count: 100
```

---

## 📚 PHẦN 3: SPRING MVC & REST API

### 3.1 Spring MVC Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP Request                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              DispatcherServlet (Front Controller)            │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Handler     │ │  View        │ │  Interceptor │
    │  Mapping     │ │  Resolver    │ │              │
    └──────────────┘ └──────────────┘ └──────────────┘
            │
            ▼
    ┌──────────────┐
    │  Controller  │
    │  (@RestController) │
    └──────────────┘
            │
            ▼
    ┌──────────────┐
    │  Service     │
    └──────────────┘
            │
            ▼
    ┌──────────────┐
    │  Repository  │
    └──────────────┘
```

---

### 3.2 REST Controller Annotations

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    // GET /api/users
    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok(userService.findAll());
    }

    // GET /api/users/{id}
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // POST /api/users
    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody UserCreateRequest request) {
        User user = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }

    // PUT /api/users/{id}
    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserUpdateRequest request) {
        return userService.update(id, request)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // PATCH /api/users/{id}
    @PatchMapping("/{id}")
    public ResponseEntity<User> patchUser(
            @PathVariable Long id,
            @RequestBody Map<String, Object> updates) {
        return userService.patch(id, updates)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // DELETE /api/users/{id}
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

---

### 3.3 Request Mapping Variants

```java
@RestController
@RequestMapping("/api")
public class ProductController {

    // PathVariable - Extract from URL path
    @GetMapping("/products/{id}")
    public Product getProduct(@PathVariable Long id) {
        return productService.findById(id);
    }

    // RequestParam - Extract from query string
    @GetMapping("/products")
    public List<Product> searchProducts(
            @RequestParam(required = false) String category,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        return productService.search(category, page, size);
    }

    // RequestBody - Parse JSON to object
    @PostMapping("/products")
    public Product createProduct(@Valid @RequestBody ProductCreateRequest request) {
        return productService.create(request);
    }

    // RequestHeader - Extract from HTTP headers
    @GetMapping("/products/{id}")
    public Product getProductWithHeader(
            @PathVariable Long id,
            @RequestHeader("Authorization") String token) {
        return productService.findById(id);
    }

    // CookieValue - Extract from cookies
    @GetMapping("/profile")
    public User getProfile(@CookieValue(value = "sessionId", required = false) String sessionId) {
        return userService.getBySessionId(sessionId);
    }

    // MatrixVariable - Matrix parameters (less common)
    @GetMapping("/products/{ids}")
    public List<Product> getProducts(@MatrixVariable List<Long> ids) {
        return productService.findAllById(ids);
    }
}
```

---

### 3.4 Exception Handling

```java
// Global Exception Handler
@RestControllerAdvice
public class GlobalExceptionHandler {

    // Handle specific exception
    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(ResourceNotFoundException ex) {
        return new ErrorResponse(HttpStatus.NOT_FOUND.value(), ex.getMessage());
    }

    // Handle validation errors
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ValidationErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        List<FieldError> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(error -> new FieldError(error.getField(), error.getDefaultMessage()))
            .collect(Collectors.toList());
        return new ValidationErrorResponse(HttpStatus.BAD_REQUEST.value(), errors);
    }

    // Handle all other exceptions
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleGeneric(Exception ex) {
        return new ErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR.value(), "An error occurred");
    }
}

// Custom exception
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
```

---

## 📚 PHẦN 4: DATA PERSISTENCE

### 4.1 Spring Data JPA

**Repository Hierarchy:**

```
Repository (marker interface)
    └── CrudRepository
        ├── PagingAndSortingRepository
        │   └── JpaRepository (JPA-specific)
        └── QueryByExampleExecutor
```

**Repository Example:**

```java
// Entity
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String name;

    private LocalDateTime createdAt;

    // Constructors, getters, setters
}

// Repository interface
public interface UserRepository extends JpaRepository<User, Long> {

    // Derived query methods
    Optional<User> findByEmail(String email);
    List<User> findByNameContaining(String namePart);
    List<User> findByCreatedAtAfter(LocalDateTime date);

    // Custom query with @Query
    @Query("SELECT u FROM User u WHERE u.email LIKE %:domain")
    List<User> findByEmailDomain(@Param("domain") String domain);

    // Native query
    @Query(value = "SELECT * FROM users WHERE status = :status", nativeQuery = true)
    List<User> findByStatusNative(@Param("status") String status);

    // Modifying query
    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.name = :name WHERE u.id = :id")
    int updateName(@Param("id") Long id, @Param("name") String name);
}

// Service layer
@Service
@Transactional(readOnly = true)
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public List<User> findAll() {
        return userRepository.findAll();
    }

    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    @Transactional
    public User create(UserCreateRequest request) {
        User user = new User();
        user.setEmail(request.getEmail());
        user.setName(request.getName());
        return userRepository.save(user);
    }

    @Transactional
    public User update(Long id, UserUpdateRequest request) {
        return userRepository.findById(id)
            .map(user -> {
                user.setName(request.getName());
                return userRepository.save(user);
            })
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }

    @Transactional
    public void delete(Long id) {
        userRepository.deleteById(id);
    }
}
```

---

### 4.2 Hibernate Relationships

```java
// One-to-Many / Many-to-One
@Entity
public class Department {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Employee> employees = new ArrayList<>();

    // Add/remove helpers
    public void addEmployee(Employee employee) {
        employees.add(employee);
        employee.setDepartment(this);
    }

    public void removeEmployee(Employee employee) {
        employees.remove(employee);
        employee.setDepartment(null);
    }
}

@Entity
public class Employee {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;
}

// One-to-One
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "profile_id")
    private Profile profile;
}

@Entity
public class Profile {
    @Id
    @GeneratedValue
    private Long id;

    private String bio;

    @OneToOne(mappedBy = "profile")
    private User user;
}

// Many-to-Many
@Entity
public class Student {
    @Id
    @GeneratedValue
    private Long id;

    @ManyToMany
    @JoinTable(
        name = "student_course",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id")
    )
    private List<Course> courses = new ArrayList<>();
}

@Entity
public class Course {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @ManyToMany(mappedBy = "courses")
    private List<Student> students = new ArrayList<>();
}
```

---

### 4.3 Transaction Management

```java
@Service
public class OrderService {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private InventoryService inventoryService;

    @Autowired
    private PaymentService paymentService;

    // @Transactional ensures all operations succeed or all fail
    @Transactional
    public Order placeOrder(OrderRequest request) {
        // 1. Create order
        Order order = new Order();
        order.setItems(request.getItems());
        order.setTotal(request.getTotal());
        order.setStatus("PENDING");
        orderRepository.save(order);

        // 2. Reserve inventory
        inventoryService.reserveItems(request.getItems());

        // 3. Process payment
        PaymentResult payment = paymentService.charge(request.getPaymentMethod(), request.getTotal());

        if (!payment.isSuccess()) {
            throw new PaymentFailedException("Payment failed");
        }

        // 4. Update order status
        order.setStatus("COMPLETED");
        order.setPaymentId(payment.getId());
        return orderRepository.save(order);
    }

    // Read-only transaction (optimization)
    @Transactional(readOnly = true)
    public Order getOrder(Long id) {
        return orderRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Order not found"));
    }

    // Propagation: REQUIRES_NEW creates new transaction
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void sendConfirmationEmail(Order order) {
        // Email sending logic
        // If this fails, it won't rollback the main order transaction
    }

    // Propagation: MANDATORY requires existing transaction
    @Transactional(propagation = Propagation.MANDATORY)
    public void validateOrder(Order order) {
        // Must be called within a transaction
    }
}
```

**Transaction Propagation:**

| Propagation | Behavior |
|-------------|----------|
| REQUIRED (default) | Use existing transaction or create new |
| REQUIRES_NEW | Always create new transaction (suspend existing) |
| SUPPORTS | Use existing if available, otherwise non-transactional |
| NOT_SUPPORTED | Execute non-transactional (suspend existing) |
| MANDATORY | Must have existing transaction, else exception |
| NEVER | Must NOT have transaction, else exception |
| NESTED | Create nested transaction within existing |

---

## 📚 PHẦN 5: SPRING SECURITY

### 5.1 Authentication & Authorization

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers("/api/user/**").hasAnyRole("USER", "ADMIN")
                .anyRequest().authenticated()
            )
            .httpBasic(Customizer.withDefaults())
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            );

        return http.build();
    }

    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails user = User.builder()
            .username("user")
            .password(passwordEncoder().encode("password"))
            .roles("USER")
            .build();

        UserDetails admin = User.builder()
            .username("admin")
            .password(passwordEncoder().encode("admin"))
            .roles("ADMIN")
            .build();

        return new InMemoryUserDetailsManager(user, admin);
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

---

### 5.2 JWT Authentication

```java
// JWT Filter
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
        String token = extractToken(request);

        if (token != null && tokenProvider.validateToken(token)) {
            String username = tokenProvider.getUsername(token);
            UserDetails userDetails = userDetailsService.loadUserByUsername(username);

            UsernamePasswordAuthenticationToken auth =
                new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());

            auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
            SecurityContextHolder.getContext().setAuthentication(auth);
        }

        filterChain.doFilter(request, response);
    }

    private String extractToken(HttpServletRequest request) {
        String bearer = request.getHeader("Authorization");
        if (bearer != null && bearer.startsWith("Bearer ")) {
            return bearer.substring(7);
        }
        return null;
    }
}

// JWT Token Provider
@Component
public class JwtTokenProvider {

    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.expiration}")
    private long expiration;

    public String generateToken(UserDetails userDetails) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + expiration);

        return Jwts.builder()
            .setSubject(userDetails.getUsername())
            .setIssuedAt(now)
            .setExpiration(expiryDate)
            .signWith(SignatureAlgorithm.HS512, secretKey)
            .compact();
    }

    public String getUsername(String token) {
        return Jwts.parser()
            .setSigningKey(secretKey)
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(secretKey).parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
}
```

---

### 5.3 OAuth2 Configuration

```java
@Configuration
@EnableWebSecurity
public class OAuth2SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2Login(oauth2 -> oauth2
                .loginPage("/login")
                .defaultSuccessUrl("/home")
                .failureUrl("/login?error=true")
            )
            .logout(logout -> logout
                .logoutSuccessUrl("/login?logout=true")
            );

        return http.build();
    }
}
```

```yaml
# application.yml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: ${GOOGLE_CLIENT_ID}
            client-secret: ${GOOGLE_CLIENT_SECRET}
            scope: profile, email
          github:
            client-id: ${GITHUB_CLIENT_ID}
            client-secret: ${GITHUB_CLIENT_SECRET}
            scope: read:user
```

---

## 📚 PHẦN 6: SPRING BOOT ACTUATOR

### 6.1 Actuator Endpoints

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,env,loggers
  endpoint:
    health:
      show-details: always
      probes:
        enabled: true  # Kubernetes probes
  metrics:
    export:
      prometheus:
        enabled: true
```

**Endpoints:**

| Endpoint | URL | Description |
|----------|-----|-------------|
| health | `/actuator/health` | Application health status |
| info | `/actuator/info` | Application info |
| metrics | `/actuator/metrics` | Application metrics |
| prometheus | `/actuator/prometheus` | Prometheus format metrics |
| env | `/actuator/env` | Environment properties |
| loggers | `/actuator/loggers` | View/change log levels |
| httpexchanges | `/actuator/httpexchanges` | Last HTTP exchanges |
| threaddump | `/actuator/threaddump` | Thread dump |
| heapdump | `/actuator/heapdump` | Heap dump |

---

### 6.2 Custom Health Indicator

```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    @Autowired
    private DataSource dataSource;

    @Override
    public Health health() {
        try (Connection conn = dataSource.getConnection()) {
            boolean valid = conn.isValid(1000);
            if (valid) {
                return Health.up()
                    .withDetail("database", "connected")
                    .withDetail("url", conn.getMetaData().getURL())
                    .build();
            }
            return Health.down().withDetail("database", "connection invalid").build();
        } catch (SQLException e) {
            return Health.down(e).build();
        }
    }
}

@Component
public class ExternalApiHealthIndicator implements HealthIndicator {

    @Value("${external.api.url}")
    private String apiUrl;

    @Override
    public Health health() {
        try {
            HttpResponse response = HttpClient.newHttpClient()
                .send(HttpRequest.newBuilder()
                    .uri(URI.create(apiUrl + "/health"))
                    .timeout(Duration.ofSeconds(5))
                    .GET()
                    .build(), HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                return Health.up()
                    .withDetail("external-api", "healthy")
                    .withDetail("response-time", response.headers().map().get("X-Response-Time"))
                    .build();
            }
            return Health.down().withDetail("external-api", "unhealthy status: " + response.statusCode()).build();
        } catch (Exception e) {
            return Health.down(e).build();
        }
    }
}
```

---

## 📚 PHẦN 7: TESTING

### 7.1 Unit Testing with Mockito

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void shouldFindUserById() {
        // Given
        User expectedUser = new User(1L, "john@example.com", "John");
        when(userRepository.findById(1L)).thenReturn(Optional.of(expectedUser));

        // When
        Optional<User> actual = userService.findById(1L);

        // Then
        assertThat(actual).isPresent();
        assertThat(actual.get().getName()).isEqualTo("John");
        verify(userRepository).findById(1L);
    }

    @Test
    void shouldThrowExceptionWhenUserNotFound() {
        // Given
        when(userRepository.findById(1L)).thenReturn(Optional.empty());

        // When/Then
        assertThatThrownBy(() -> userService.findById(1L))
            .isInstanceOf(ResourceNotFoundException.class)
            .hasMessage("User not found");
    }
}
```

---

### 7.2 Integration Testing

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private UserService userService;

    @Test
    void shouldGetAllUsers() throws Exception {
        // Given
        List<User> users = Arrays.asList(
            new User(1L, "john@example.com", "John"),
            new User(2L, "jane@example.com", "Jane")
        );
        when(userService.findAll()).thenReturn(users);

        // When/Then
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$", hasSize(2)))
            .andExpect(jsonPath("$[0].name").value("John"));
    }

    @Test
    void shouldCreateUser() throws Exception {
        // Given
        UserCreateRequest request = new UserCreateRequest("test@example.com", "Test User");
        User createdUser = new User(1L, "test@example.com", "Test User");

        when(userService.create(any())).thenReturn(createdUser);

        // When/Then
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.name").value("Test User"));
    }
}
```

---

### 7.3 Test Slices

```java
// Repository layer test
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TestEntityManager entityManager;

    @Test
    void shouldSaveAndFindUser() {
        User user = new User("test@example.com", "Test");
        userRepository.save(user);

        entityManager.flush();

        Optional<User> found = userRepository.findByEmail("test@example.com");
        assertThat(found).isPresent();
    }
}

// Web layer test
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void shouldReturnUser() throws Exception {
        when(userService.findById(1L)).thenReturn(Optional.of(new User(1L, "test@example.com", "Test")));

        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("Test"));
    }
}

// Service layer test (no Spring)
class UserServiceUnitTest {

    private UserService userService;

    @BeforeEach
    void setUp() {
        userService = new UserService(new InMemoryUserRepository());
    }

    @Test
    void shouldCreateUser() {
        // Pure unit test without Spring
    }
}
```

---

## 📚 PHẦN 8: SPRING CLOUD (MICROSERVICES)

### 8.1 Service Discovery (Eureka)

```java
// Eureka Server
@EnableEurekaServer
@SpringBootApplication
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}
```

```yaml
# Eureka Server application.yml
server:
  port: 8761
eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
```

```java
// Eureka Client
@EnableDiscoveryClient
@SpringBootApplication
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}
```

```yaml
# Client application.yml
eureka:
  client:
    service-url:
      default-zone: http://localhost:8761/eureka
  instance:
    prefer-ip-address: true
```

---

### 8.2 API Gateway (Spring Cloud Gateway)

```java
@EnableZuulProxy  // or use Spring Cloud Gateway
@SpringBootApplication
public class GatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
}
```

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/users/**
      default-filters:
        - AddRequestHeader=X-Request-Source, gateway
```

---

### 8.3 Circuit Breaker (Resilience4j)

```java
@Service
public class OrderService {

    @Autowired
    private UserService userService;

    @CircuitBreaker(name = "userService", fallbackMethod = "getUserFallback")
    public User getUser(Long userId) {
        return userService.findById(userId);
    }

    // Fallback method
    public User getUserFallback(Long userId, Throwable ex) {
        log.error("Circuit breaker triggered for user: {}", userId, ex);
        return new User(userId, "Unknown", "unknown@example.com");
    }
}
```

```yaml
resilience4j:
  circuitbreaker:
    instances:
      userService:
        registerHealthIndicator: true
        slidingWindowSize: 10
        failureRateThreshold: 50
        waitDurationInOpenState: 10000
        permittedNumberOfCallsInHalfOpenState: 3
```

---

## 📝 TÓM TẮT PHASE 1

### Các chủ đề cần nắm vững (theo roadmap.sh/spring-boot):

**1. Spring Fundamentals:**
- ✅ Dependency Injection (DI), Inversion of Control (IoC)
- ✅ Spring IOC Container
- ✅ Spring AOP (Aspect-Oriented Programming)
- ✅ Spring MVC architecture
- ✅ Annotations (@Component, @Service, @Repository, @Controller, etc.)
- ✅ Spring Bean Scopes (singleton, prototype, request, session)
- ✅ Architecture & Terminology
- ✅ "Why use Spring?" - Benefits over plain J2EE

**2. Spring Security:**
- ✅ Authentication (username/password, JWT)
- ✅ Authorization (role-based, permission-based)
- ✅ OAuth2 (authorization flow)
- ✅ JWT Authentication (tokens, validation)

**3. Boot Features:**
- ✅ Spring Boot Starters (web, data-jpa, security, etc.)
- ✅ Auto-configuration (how it works, conditional annotations)
- ✅ Actuators (health, metrics, info endpoints)
- ✅ Embedded Server (Tomcat, Jetty, Undertow)

**4. Data Access:**
- ✅ Hibernate (Transactions, Relationships, Entity Lifecycle)
- ✅ Spring Data JPA (Repository pattern, query methods)
- ✅ Spring Data MongoDB
- ✅ Spring Data JDBC

**5. Microservices (Spring Cloud):**
- ✅ Spring Cloud Gateway
- ✅ Spring Cloud Config (centralized configuration)
- ✅ Spring Cloud Circuit Breaker (Resilience4j)
- ✅ Spring Cloud OpenFeign (declarative REST client)
- ✅ Micrometer (metrics collection)
- ✅ Eureka (service discovery)

**6. Web & Components:**
- ✅ Servlet API
- ✅ JSP Files (legacy, but good to know)
- ✅ Components architecture

**7. Testing:**
- ✅ JPA Test (@DataJpaTest)
- ✅ Mock MVC (web layer testing)
- ✅ @SpringBootTest (integration tests)
- ✅ @MockBean Annotation (mocking beans)

---

Sau phase này, bạn cần nắm được:

1. ✅ Spring Core: DI, IoC, Bean scopes, Annotations
2. ✅ Spring Boot: Starters, Auto-configuration, Embedded servers
3. ✅ Spring MVC: REST controllers, Exception handling, Validation
4. ✅ Spring Data JPA: Repositories, Relationships, Transactions
5. ✅ Spring Security: Authentication, Authorization, JWT, OAuth2
6. ✅ Spring Boot Actuator: Health checks, Metrics, Monitoring
7. ✅ Testing: Unit tests, Integration tests, Test slices
8. ✅ Spring Cloud: Service discovery, Gateway, Circuit breaker

---

## 🔜 TIẾP THEO

Đọc `02-examples.md` để xem code mẫu thực tế và `03-exercises.md` để làm bài tập!

---

## 📚 TÀI LIỆU THAM KHẢO

### Auto-configuration & Starters

| Resource | Link | Nội dung |
|----------|------|----------|
| Spring Boot Auto-configuration | [Spring Docs](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration) | How auto-configuration works, conditional annotations |
| Creating a Custom Starter | [Spring Docs](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration.custom-starter) | Build your own starter |
| Spring Boot Starters | [Baeldung](https://www.baeldung.com/spring-boot-starters) | Complete guide to starters |

### Actuator & Profiles

| Resource | Link | Nội dung |
|----------|------|----------|
| Spring Boot Actuator | [Spring Docs](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html) | Production monitoring, health checks, metrics |
| Custom Health Indicators | [Baeldung](https://www.baeldung.com/spring-boot-health-indicator) | Build custom health indicators |
| Spring Profiles | [Baeldung](https://www.baeldung.com/spring-profiles) | Profile-based configuration |

### Spring MVC & REST

| Resource | Link | Nội dung |
|----------|------|----------|
| Building a RESTful Web Service | [Spring Guide](https://spring.io/guides/gs/rest-service/) | Official REST tutorial |
| Exception Handling in Spring MVC | [Baeldung](https://www.baeldung.com/exception-handling-for-rest-with-spring) | @ControllerAdvice, @ExceptionHandler |
| Request Validation | [Baeldung](https://www.baeldung.com/spring-boot-bean-validation) | Bean validation with @Valid |

### Spring Data JPA & Transactions

| Resource | Link | Nội dung |
|----------|------|----------|
| Spring Data JPA | [Spring Docs](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/) | Repository pattern, query methods |
| @Transactional Explained | [Baeldung](https://www.baeldung.com/spring-transactional-propagation-isolation) | Propagation, isolation levels |
| Hibernate Best Practices | [Vlad Mihalcea](https://vladmihalcea.com/) | JPA/Hibernate performance tips |

### Spring Security

| Resource | Link | Nội dung |
|----------|------|----------|
| Spring Security Reference | [Spring Docs](https://docs.spring.io/spring-security/reference/) | Complete security guide |
| JWT Authentication | [Baeldung](https://www.baeldung.com/security-spring) | Implement JWT auth |
| OAuth2 with Spring | [Baeldung](https://www.baeldung.com/spring-security-oauth) | OAuth2, OIDC configuration |

### Testing

| Resource | Link | Nội dung |
|----------|------|----------|
| Testing Spring Boot | [Spring Docs](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing) | @SpringBootTest, test slices |
| Mocking with Mockito | [Baeldung](https://www.baeldung.com/mockito-mock-annotations) | @Mock, @InjectMocks, @Spy |
| Testcontainers Guide | [Baeldung](https://www.baeldung.com/spring-boot-testcontainers) | Integration tests with Docker |
