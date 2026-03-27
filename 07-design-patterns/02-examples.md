# Design Patterns - Examples trong Spring Framework

> **Mục tiêu:** Hiểu cách Spring Framework áp dụng design patterns

---

## 📚 BÀI 1: CREATIONAL PATTERNS TRONG SPRING

### 1.1 Singleton Pattern trong Spring

**Spring Bean Scope:**
```java
@Component
@Scope("singleton")  // Default scope
public class UserService {
    private final UserRepository repository;

    @Autowired
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}

// Spring đảm bảo chỉ có 1 instance trong ApplicationContext
@Service
public class OrderService {
    @Autowired
    private UserService userService;  // Same instance everywhere
}
```

**Configuration Class:**
```java
@Configuration
public class AppConfig {

    @Bean  // Singleton by default
    public DataSource dataSource() {
        return new HikariDataSource();
    }

    @Bean
    public EntityManagerFactory entityManagerFactory() {
        // Same instance throughout the application
        return new LocalContainerEntityManagerFactoryBean();
    }
}
```

**Khi nào dùng Prototype scope:**
```java
@Component
@Scope("prototype")  // New instance each time
public class ShoppingCart {
    private final List<Item> items = new ArrayList<>();

    public void addItem(Item item) {
        items.add(item);
    }
}

@Service
public class CheckoutService {
    @Autowired
    private ApplicationContext context;

    public void checkout(User user) {
        // Get new cart instance for each user
        ShoppingCart cart = context.getBean(ShoppingCart.class);
        // Process checkout...
    }
}
```

---

### 1.2 Builder Pattern trong Spring

**RestTemplate.Builder:**
```java
RestTemplate restTemplate = RestTemplate.builder()
    .requestFactory(new HttpComponentsClientHttpRequestFactory())
    .errorHandler(new CustomErrorHandler())
    .messageConverters(customConverters())
    .build();
```

**WebClient.Builder (Spring WebFlux):**
```java
@Configuration
public class WebClientConfig {

    @Bean
    public WebClient webClient(WebClient.Builder builder) {
        return builder
            .baseUrl("https://api.example.com")
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .filter(logRequest())
            .filter(logResponse())
            .build();
    }

    private ExchangeFilterFunction logRequest() {
        return ExchangeFilterFunction.ofRequestProcessor(clientRequest -> {
            log.info("Request: {} {}", clientRequest.method(), clientRequest.url());
            return Mono.just(clientRequest);
        });
    }
}
```

**UriComponentsBuilder:**
```java
URI uri = UriComponentsBuilder.fromHttpUrl("https://api.example.com/users")
    .queryParam("page", 0)
    .queryParam("size", 10)
    .queryParam("sort", "name,asc")
    .build()
    .toUri();

User[] users = restTemplate.getForObject(uri, User[].class);
```

**Spring Boot Application Builder:**
```java
new SpringApplicationBuilder(MyApplication.class)
    .bannerMode(Banner.Mode.OFF)
    .profiles("dev")
    .properties("server.port:8081")
    .run(args);
```

---

### 1.3 Factory Method Pattern trong Spring

**FactoryBean Interface:**
```java
// Custom factory for complex bean creation
public class DatabaseConnectionFactory implements FactoryBean<DataSource> {

    private String driverClassName;
    private String url;
    private String username;
    private String password;

    @Override
    public DataSource getObject() throws Exception {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        dataSource.setDriverClassName(driverClassName);
        dataSource.setUrl(url);
        dataSource.setUsername(username);
        dataSource.setPassword(password);
        return dataSource;
    }

    @Override
    public Class<?> getObjectType() {
        return DataSource.class;
    }

    @Override
    public boolean isSingleton() {
        return true;
    }
}

// Usage in configuration
@Configuration
public class DatabaseConfig {

    @Bean
    public DatabaseConnectionFactory connectionFactory() {
        DatabaseConnectionFactory factory = new DatabaseConnectionFactory();
        factory.setDriverClassName("com.mysql.cj.jdbc.Driver");
        factory.setUrl("jdbc:mysql://localhost:3306/mydb");
        factory.setUsername("root");
        factory.setPassword("secret");
        return factory;
    }

    @Bean
    public DataSource dataSource(DatabaseConnectionFactory factory) throws Exception {
        return factory.getObject();
    }
}
```

**BeanFactory PostProcessor:**
```java
@Component
public class CustomPropertyConfigurer implements BeanFactoryPostProcessor {

    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) {
        // Modify bean definitions before instantiation
        BeanDefinition def = beanFactory.getBeanDefinition("userService");
        // Customize...
    }
}
```

---

### 1.4 Abstract Factory Pattern trong Spring

**Multiple Database Abstract Factory:**
```java
// Abstract Factory
public interface DatabaseFactory {
    Connection createConnection();
    Statement createStatement();
    ResultSet executeQuery(String sql);
}

// MySQL Factory
public class MySqlFactory implements DatabaseFactory {
    @Override
    public Connection createConnection() {
        // MySQL-specific connection
    }

    @Override
    public Statement createStatement() {
        // MySQL-specific statement
    }

    @Override
    public ResultSet executeQuery(String sql) {
        // MySQL-specific query execution
    }
}

// PostgreSQL Factory
public class PostgresFactory implements DatabaseFactory {
    @Override
    public Connection createConnection() {
        // PostgreSQL-specific connection
    }

    @Override
    public Statement createStatement() {
        // PostgreSQL-specific statement
    }

    @Override
    public ResultSet executeQuery(String sql) {
        // PostgreSQL-specific query execution
    }
}

// Factory Provider
@Component
public class DatabaseFactoryProvider {

    private final DatabaseFactory factory;

    public DatabaseFactoryProvider(@Value("${database.type}") String dbType) {
        if ("mysql".equals(dbType)) {
            this.factory = new MySqlFactory();
        } else if ("postgres".equals(dbType)) {
            this.factory = new PostgresFactory();
        } else {
            throw new IllegalArgumentException("Unsupported database: " + dbType);
        }
    }

    public DatabaseFactory getFactory() {
        return factory;
    }
}
```

---

## 📚 BÀI 2: STRUCTURAL PATTERNS TRONG SPRING

### 2.1 Adapter Pattern trong Spring

**Spring MVC HandlerAdapter:**
```java
// HandlerAdapter is an Adapter pattern
public interface HandlerAdapter {
    boolean supports(Object handler);
    ModelAndView handle(HttpServletRequest request,
                       HttpServletResponse response,
                       Object handler,
                       ModelMap model) throws Exception;
}

// Adapts Controller to Spring MVC
public class SimpleControllerHandlerAdapter implements HandlerAdapter {

    @Override
    public boolean supports(Object handler) {
        return handler instanceof Controller;
    }

    @Override
    public ModelAndView handle(HttpServletRequest request,
                              HttpServletResponse response,
                              Object handler,
                              ModelMap model) throws Exception {
        Controller controller = (Controller) handler;
        return controller.handleRequest(request, response);
    }
}

// Your Controller (legacy interface)
public class MyController implements Controller {
    @Override
    public ModelAndView handleRequest(HttpServletRequest request,
                                     HttpServletResponse response) {
        // Legacy controller logic
        ModelAndView mav = new ModelAndView();
        mav.addObject("message", "Hello");
        mav.setViewName("hello");
        return mav;
    }
}
```

**Spring Web Adapter (REST):**
```java
// Adapts third-party API to your service
@RestController
@RequestMapping("/api/weather")
public class WeatherAdapterController {

    private final ThirdPartyWeatherApi thirdPartyApi;

    public WeatherAdapterController(ThirdPartyWeatherApi api) {
        this.thirdPartyApi = api;
    }

    @GetMapping("/{city}")
    public WeatherResponse getWeather(@PathVariable String city) {
        // Adapt third-party response to your domain model
        ThirdPartyWeatherData data = thirdPartyApi.fetchWeather(city);

        WeatherResponse response = new WeatherResponse();
        response.setCity(city);
        response.setTemperature(data.getTempCelsius());
        response.setHumidity(data.getHumidityPercent());
        response.setCondition(convertCondition(data.getConditionCode()));

        return response;
    }

    private String convertCondition(int code) {
        // Map third-party codes to your conditions
        return switch (code) {
            case 1 -> "Sunny";
            case 2 -> "Cloudy";
            case 3 -> "Rainy";
            default -> "Unknown";
        };
    }
}
```

---

### 2.2 Decorator Pattern trong Spring

**Spring AOP as Decorator:**
```java
// Custom annotation for caching
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface CacheResult {
    String cacheName();
    String key();
}

// Aspect as Decorator
@Aspect
@Component
public class CacheAspect {

    private final CacheManager cacheManager;

    public CacheAspect(CacheManager cacheManager) {
        this.cacheManager = cacheManager;
    }

    @Around("@annotation(cacheResult)")
    public Object cache(ProceedingJoinPoint pjp, CacheResult cacheResult) throws Throwable {
        String cacheName = cacheResult.cacheName();
        String key = generateKey(pjp, cacheResult.key());

        Cache cache = cacheManager.getCache(cacheName);
        if (cache != null) {
            Object cached = cache.get(key, Object.class);
            if (cached != null) {
                return cached;  // Return cached value
            }
        }

        Object result = pjp.proceed();  // Call actual method

        if (cache != null && result != null) {
            cache.put(key, result);  // Cache result
        }

        return result;
    }

    private String generateKey(ProceedingJoinPoint pjp, String keyTemplate) {
        // Generate cache key from method parameters
        return pjp.getSignature().toShortString() + Arrays.hashCode(pjp.getArgs());
    }
}

// Usage
@Service
public class ProductService {

    @CacheResult(cacheName = "products", key = "#id")
    public Product findById(Long id) {
        // Expensive database query
        return productRepository.findById(id).orElse(null);
    }
}
```

**HttpHeaders Decorator:**
```java
// Custom HttpHeaders decorator
public class CustomHttpHeaders extends HttpHeaders {

    private final HttpHeaders delegate;

    public CustomHttpHeaders(HttpHeaders delegate) {
        this.delegate = delegate;
    }

    @Override
    public void setContentType(MediaType mediaType) {
        // Add custom logic before setting content type
        log.info("Setting content type: {}", mediaType);
        super.setContentType(mediaType);
    }

    @Override
    public void add(String headerName, String headerValue) {
        // Validate headers before adding
        if (isValidHeader(headerName, headerValue)) {
            super.add(headerName, headerValue);
        }
    }

    private boolean isValidHeader(String name, String value) {
        // Security validation
        return !name.contains("\n") && !value.contains("\n");
    }
}
```

---

### 2.3 Facade Pattern trong Spring

**Spring Facade for Microservices:**
```java
@RestController
@RequestMapping("/api/orders")
public class OrderFacadeController {

    private final OrderService orderService;
    private final InventoryService inventoryService;
    private final PaymentService paymentService;
    private final NotificationService notificationService;

    public OrderFacadeController(OrderService orderService,
                                 InventoryService inventoryService,
                                 PaymentService paymentService,
                                 NotificationService notificationService) {
        this.orderService = orderService;
        this.inventoryService = inventoryService;
        this.paymentService = paymentService;
        this.notificationService = notificationService;
    }

    @PostMapping
    public ResponseEntity<OrderResponse> placeOrder(@RequestBody OrderRequest request) {
        // Simplified interface for complex operation
        try {
            // 1. Validate order
            orderService.validate(request);

            // 2. Check and reserve inventory
            inventoryService.checkStock(request.getItems());
            inventoryService.reserve(request.getItems());

            // 3. Process payment
            PaymentResult payment = paymentService.charge(request.getUserId(), request.getTotal());

            // 4. Create order
            Order order = orderService.create(request, payment.getTransactionId());

            // 5. Send confirmation
            notificationService.sendOrderConfirmation(order);

            return ResponseEntity.ok(OrderResponse.from(order));

        } catch (Exception e) {
            // Compensating transactions
            inventoryService.release(request.getItems());
            throw e;
        }
    }
}
```

**JdbcTemplate as Facade:**
```java
// JdbcTemplate simplifies JDBC operations
@Service
public class UserRepository {

    private final JdbcTemplate jdbcTemplate;

    public UserRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    // Facade methods hide JDBC complexity
    public User findById(Long id) {
        return jdbcTemplate.queryForObject(
            "SELECT * FROM users WHERE id = ?",
            new Object[]{id},
            this::mapRowToUser
        );
    }

    public List<User> findAll() {
        return jdbcTemplate.query(
            "SELECT * FROM users",
            this::mapRowToUser
        );
    }

    public void save(User user) {
        jdbcTemplate.update(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            user.getName(),
            user.getEmail()
        );
    }

    private User mapRowToUser(ResultSet rs, int rowNum) throws SQLException {
        User user = new User();
        user.setId(rs.getLong("id"));
        user.setName(rs.getString("name"));
        user.setEmail(rs.getString("email"));
        return user;
    }
}
```

---

### 2.4 Proxy Pattern trong Spring

**@Transactional Proxy:**
```java
@Service
public class UserService {

    private final UserRepository repository;

    @Transactional  // Spring creates proxy
    public void updateUser(User user) {
        User existing = repository.findById(user.getId());
        existing.setName(user.getName());
        existing.setEmail(user.getEmail());
        repository.save(existing);
        // If exception thrown, entire method rolls back
    }

    @Transactional(readOnly = true)  // Read-only transaction
    public User getUser(Long id) {
        return repository.findById(id);
    }
}

// Spring creates proxy like:
public class UserServiceProxy extends UserService {
    private final TransactionManager txManager;

    @Override
    public void updateUser(User user) {
        TransactionStatus status = txManager.getTransaction();
        try {
            super.updateUser(user);
            txManager.commit(status);
        } catch (Exception e) {
            txManager.rollback(status);
            throw e;
        }
    }

    @Override
    public User getUser(Long id) {
        // Read-only transaction
        TransactionStatus status = txManager.getTransaction(
            new DefaultTransactionDefinition(TransactionDefinition.PROPAGATION_REQUIRED)
        );
        try {
            User user = super.getUser(id);
            txManager.commit(status);
            return user;
        } catch (Exception e) {
            txManager.rollback(status);
            throw e;
        }
    }
}
```

**@Async Proxy:**
```java
@Service
public class EmailService {

    @Async  // Runs in separate thread
    public void sendEmail(String to, String subject, String body) {
        // Slow email sending operation
        mailClient.send(to, subject, body);
    }

    @Async
    @Retryable(maxAttempts = 3)
    public void sendBulkEmails(List<EmailRequest> requests) {
        for (EmailRequest request : requests) {
            sendEmail(request.getTo(), request.getSubject(), request.getBody());
        }
    }
}

// Proxy executes in async thread pool
```

**@Cacheable Proxy:**
```java
@Service
public class ProductService {

    @Cacheable(value = "products", key = "#id")
    public Product findById(Long id) {
        // Database call - cached after first call
        return productRepository.findById(id).orElse(null);
    }

    @CacheEvict(value = "products", key = "#product.id")
    public void update(Product product) {
        // Evicts cache on update
        productRepository.save(product);
    }
}
```

---

### 2.5 Composite Pattern trong Spring

**CompositeViewResolver:**
```java
// Spring's ViewResolver uses Composite pattern
public class CompositeViewResolver implements ViewResolver {

    private final List<ViewResolver> viewResolvers = new ArrayList<>();

    public void addViewResolver(ViewResolver resolver) {
        viewResolvers.add(resolver);
    }

    @Override
    public View resolveViewName(String viewName, Locale locale) throws Exception {
        for (ViewResolver resolver : viewResolvers) {
            View view = resolver.resolveViewName(viewName, locale);
            if (view != null) {
                return view;
            }
        }
        return null;
    }
}

// Configuration
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void configureViewResolvers(ViewResolverRegistry registry) {
        registry.jsp("/WEB-INF/views/", ".jsp");      // JSP resolver
        registry.thymeleaf();                          // Thymeleaf resolver
        registry.freemarker();                         // FreeMarker resolver
        // Spring composites these resolvers
    }
}
```

---

## 📚 BÀI 3: BEHAVIORAL PATTERNS TRONG SPRING

### 3.1 Strategy Pattern trong Spring

**RestTemplate RequestFactory Strategy:**
```java
// Different strategies for HTTP client
@Configuration
public class RestTemplateConfig {

    @Bean
    @Profile("default")
    public RestTemplate defaultRestTemplate() {
        return new RestTemplate();  // Simple strategy
    }

    @Bean
    @Profile("production")
    public RestTemplate productionRestTemplate() {
        // Apache HttpClient strategy for production
        HttpComponentsClientHttpRequestFactory factory =
            new HttpComponentsClientHttpRequestFactory();
        factory.setConnectTimeout(5000);
        factory.setReadTimeout(5000);
        return new RestTemplate(factory);
    }

    @Bean
    @Profile("secure")
    public RestTemplate secureRestTemplate() throws Exception {
        // SSL strategy
        SSLContext sslContext = SSLContextBuilder.create()
            .loadTrustMaterial(trustStore, trustPassword)
            .build();

        SSLConnectionSocketFactory socketFactory =
            new SSLConnectionSocketFactory(sslContext);

        CloseableHttpClient httpClient = HttpClients.custom()
            .setSSLSocketFactory(socketFactory)
            .build();

        HttpComponentsClientHttpRequestFactory factory =
            new HttpComponentsClientHttpRequestFactory(httpClient);

        return new RestTemplate(factory);
    }
}
```

**Authentication Strategy:**
```java
// Strategy interface
public interface AuthenticationStrategy {
    boolean authenticate(AuthenticationRequest request);
}

// OAuth2 Strategy
@Component
public class OAuth2Strategy implements AuthenticationStrategy {
    @Override
    public boolean authenticate(AuthenticationRequest request) {
        // OAuth2 authentication logic
        return true;
    }
}

// JWT Strategy
@Component
public class JwtStrategy implements AuthenticationStrategy {
    @Override
    public boolean authenticate(AuthenticationRequest request) {
        // JWT validation logic
        return true;
    }
}

// LDAP Strategy
@Component
public class LdapStrategy implements AuthenticationStrategy {
    @Override
    public boolean authenticate(AuthenticationRequest request) {
        // LDAP authentication logic
        return true;
    }
}

// Context with strategy selection
@Service
public class AuthenticationService {

    private final Map<String, AuthenticationStrategy> strategies;

    public AuthenticationService(List<AuthenticationStrategy> strategyList) {
        this.strategies = strategyList.stream()
            .collect(Collectors.toMap(
                s -> s.getClass().getSimpleName().replace("Strategy", ""),
                s -> s
            ));
    }

    public boolean authenticate(AuthenticationRequest request) {
        AuthenticationStrategy strategy = strategies.get(request.getType());
        if (strategy == null) {
            throw new IllegalArgumentException("Unknown auth type: " + request.getType());
        }
        return strategy.authenticate(request);
    }
}
```

---

### 3.2 Observer Pattern trong Spring

**Application Events:**
```java
// Event class
public class OrderCreatedEvent extends ApplicationEvent {
    private final Order order;

    public OrderCreatedEvent(Object source, Order order) {
        super(source);
        this.order = order;
    }

    public Order getOrder() {
        return order;
    }
}

// Publisher
@Service
public class OrderService {

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    public Order createOrder(OrderRequest request) {
        Order order = orderRepository.save(request.toOrder());
        eventPublisher.publishEvent(new OrderCreatedEvent(this, order));
        return order;
    }
}

// Listener 1: Send email
@Component
public class OrderEmailListener {

    @Autowired
    private EmailService emailService;

    @EventListener
    @Async
    public void handleOrderCreated(OrderCreatedEvent event) {
        emailService.sendOrderConfirmation(event.getOrder());
    }
}

// Listener 2: Update inventory
@Component
public class InventoryListener {

    @Autowired
    private InventoryService inventoryService;

    @EventListener
    @Transactional
    public void handleOrderCreated(OrderCreatedEvent event) {
        inventoryService.reserveItems(event.getOrder().getItems());
    }
}

// Listener 3: Send analytics
@Component
public class AnalyticsListener {

    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        analytics.track("order_created", Map.of(
            "orderId", event.getOrder().getId(),
            "amount", event.getOrder().getTotal()
        ));
    }
}
```

**@TransactionalEventListener:**
```java
@Component
public class OrderNotificationListener {

    // Only fires after transaction commits
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    @Async
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Guaranteed to run after DB commit
        notificationService.send(event.getOrder());
    }

    // Fires if transaction rolls back
    @TransactionalEventListener(phase = TransactionPhase.AFTER_ROLLBACK)
    public void handleRollback(OrderCreatedEvent event) {
        log.warn("Order creation rolled back: {}", event.getOrder().getId());
    }
}
```

---

### 3.3 Command Pattern trong Spring

**Spring Batch Job as Command:**
```java
@Configuration
@EnableBatchProcessing
public class BatchConfig {

    @Bean
    public Job importUserJob(JobBuilderFactory jobs, Step step) {
        return jobs.get("importUserJob")
            .start(step)
            .build();
    }

    @Bean
    public Step step(StepBuilderFactory steps,
                    ItemReader<User> reader,
                    ItemProcessor<User, User> processor,
                    ItemWriter<User> writer) {
        return steps.get("step")
            .<User, User>chunk(10)
            .reader(reader)
            .processor(processor)
            .writer(writer)
            .build();
    }
}

// Execute job as command
@Service
public class BatchCommandService {

    @Autowired
    private JobLauncher jobLauncher;

    @Autowired
    private Job importUserJob;

    public void executeImport() {
        JobParameters params = new JobParametersBuilder()
            .addLong("timestamp", System.currentTimeMillis())
            .toJobParameters();

        try {
            jobLauncher.run(importUserJob, params);
        } catch (Exception e) {
            // Handle failure
        }
    }
}
```

**Command Pattern with Undo:**
```java
// Command interface
public interface OrderCommand {
    void execute();
    void undo();
}

// Concrete Commands
public class CreateOrderCommand implements OrderCommand {
    private final OrderService orderService;
    private final OrderRequest request;
    private Order createdOrder;

    public CreateOrderCommand(OrderService orderService, OrderRequest request) {
        this.orderService = orderService;
        this.request = request;
    }

    @Override
    public void execute() {
        createdOrder = orderService.create(request);
    }

    @Override
    public void undo() {
        if (createdOrder != null) {
            orderService.cancel(createdOrder.getId());
        }
    }
}

// Command History
@Component
public class CommandHistory {
    private final Deque<OrderCommand> history = new ArrayDeque<>();

    public void execute(OrderCommand command) {
        command.execute();
        history.push(command);
    }

    public void undo() {
        if (!history.isEmpty()) {
            history.pop().undo();
        }
    }

    public void undoAll() {
        while (!history.isEmpty()) {
            history.pop().undo();
        }
    }
}
```

---

### 3.4 Chain of Responsibility trong Spring

**Spring Security Filter Chain:**
```java
@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // Chain of filters
            .addFilterBefore(new CorsFilter(), ChannelProcessingFilter.class)
            .addFilterBefore(new JwtAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class)
            .addFilterBefore(new LoggingFilter(), JwtAuthenticationFilter.class)
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            );

        return http.build();
    }
}

// Custom filter in chain
@Component
@Order(1)  // First in chain
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                   HttpServletResponse response,
                                   FilterChain filterChain) throws ServletException, IOException {
        String token = extractToken(request);

        if (token != null && JwtUtil.validate(token)) {
            Authentication auth = JwtUtil.getAuthentication(token);
            SecurityContextHolder.getContext().setAuthentication(auth);
        }

        filterChain.doFilter(request, response);  // Pass to next filter
    }
}

@Component
@Order(2)  // Second in chain
public class LoggingFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                   HttpServletResponse response,
                                   FilterChain filterChain) throws ServletException, IOException {
        log.info("Request: {} {}", request.getMethod(), request.getRequestURI());
        filterChain.doFilter(request, response);
    }
}
```

**HandlerInterceptor Chain:**
```java
@Component
public class RequestLoggingInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request,
                            HttpServletResponse response,
                            Object handler) {
        log.info("Before handler: {}", request.getRequestURI());
        request.setAttribute("startTime", System.currentTimeMillis());
        return true;  // Continue chain
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                               HttpServletResponse response,
                               Object handler,
                               Exception ex) {
        long startTime = (Long) request.getAttribute("startTime");
        log.info("Completed in {} ms: {}", System.currentTimeMillis() - startTime, request.getRequestURI());
    }
}

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Autowired
    private RequestLoggingInterceptor loggingInterceptor;

    @Autowired
    private AuthInterceptor authInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(authInterceptor)
            .addPathPatterns("/api/**");

        registry.addInterceptor(loggingInterceptor)
            .addPathPatterns("/**");
    }
}
```

---

### 3.5 Template Method Pattern trong Spring

**JdbcTemplate Template Method:**
```java
// JdbcTemplate defines template for JDBC operations
@Service
public class UserRepository {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    // Template method handles:
    // 1. Get connection
    // 2. Create statement
    // 3. Execute query
    // 4. Process ResultSet
    // 5. Handle exceptions
    // 6. Close resources

    public User findById(Long id) {
        return jdbcTemplate.queryForObject(
            "SELECT * FROM users WHERE id = ?",
            new Object[]{id},
            (rs, rowNum) -> mapRow(rs)  // You provide row mapping
        );
    }

    public List<User> findAll() {
        return jdbcTemplate.query(
            "SELECT * FROM users",
            (rs, rowNum) -> mapRow(rs)  // You provide row mapping
        );
    }

    private User mapRow(ResultSet rs) throws SQLException {
        User user = new User();
        user.setId(rs.getLong("id"));
        user.setName(rs.getString("name"));
        return user;
    }
}
```

**RestTemplate Template Method:**
```java
// RestTemplate defines template for HTTP requests
@Service
public class UserService {

    @Autowired
    private RestTemplate restTemplate;

    // Template handles:
    // 1. Create request
    // 2. Execute HTTP call
    // 3. Handle errors
    // 4. Convert response
    // 5. Handle exceptions

    public User getUser(Long id) {
        return restTemplate.getForObject(
            "https://api.example.com/users/{id}",
            User.class,
            id
        );
    }

    public User createUser(User user) {
        return restTemplate.postForObject(
            "https://api.example.com/users",
            user,
            User.class
        );
    }
}
```

**Abstract Controller:**
```java
// Base controller with template method
public abstract class BaseController<T, ID> {

    protected abstract Service<T, ID> getService();

    @GetMapping("/{id}")
    public ResponseEntity<T> getById(@PathVariable ID id) {
        return getService().findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping
    public ResponseEntity<List<T>> getAll() {
        return ResponseEntity.ok(getService().findAll());
    }

    @PostMapping
    public ResponseEntity<T> create(@RequestBody T entity) {
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(getService().save(entity));
    }

    @PutMapping("/{id}")
    public ResponseEntity<T> update(@PathVariable ID id, @RequestBody T entity) {
        return ResponseEntity.ok(getService().update(id, entity));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable ID id) {
        getService().delete(id);
        return ResponseEntity.noContent().build();
    }
}

// Concrete controller
@RestController
@RequestMapping("/api/users")
public class UserController extends BaseController<User, Long> {

    @Autowired
    private UserService userService;

    @Override
    protected Service<User, Long> getService() {
        return userService;
    }
}
```

---

## 📝 TÓM TẮT

| Pattern | Spring Implementation | Example |
|---------|----------------------|---------|
| Singleton | @Scope("singleton") | All Spring Beans |
| Builder | RestTemplate.builder() | WebClient, UriComponentsBuilder |
| Factory | FactoryBean | DatabaseConnectionFactory |
| Adapter | HandlerAdapter | MVC Controllers |
| Decorator | AOP, @Cacheable | Transaction, Logging |
| Facade | JdbcTemplate | Simplified JDBC |
| Proxy | @Transactional, @Async | Transaction management |
| Composite | ViewResolver | Multiple view technologies |
| Strategy | RequestFactory | HTTP client strategies |
| Observer | ApplicationEvent | Event-driven architecture |
| Command | Spring Batch | Job execution |
| Chain of Responsibility | Filter Chain | Security filters |
| Template Method | JdbcTemplate, RestTemplate | Database, HTTP operations |

---

## 🔜 TIẾP THEO

Xem `03-exercises.md` để thực hành áp dụng design patterns!
