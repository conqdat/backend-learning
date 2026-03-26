# Phase 07: Testing - Bài Tập Thực Hành

> **Thời gian:** 2-3 giờ
> **Mục tiêu:** Viết tests cho production code

---

## 📝 BÀI TẬP 1: UNIT TESTS CHO SERVICE (1 giờ)

### Đề bài

Cho Service class sau:

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository repository;
    private final PaymentService paymentService;
    private final InventoryService inventoryService;

    public Order createOrder(Long userId, List<Long> productIds) {
        // Validate products in stock
        for (Long productId : productIds) {
            if (!inventoryService.isInStock(productId)) {
                throw new OutOfStockException(productId);
            }
        }

        // Process payment
        BigDecimal total = calculateTotal(productIds);
        PaymentResult payment = paymentService.charge(userId, total);

        if (!payment.isSuccess()) {
            throw new PaymentFailedException(payment.getError());
        }

        // Create order
        Order order = new Order();
        order.setUserId(userId);
        order.setProductIds(productIds);
        order.setTotalAmount(total);
        order.setStatus("CONFIRMED");

        return repository.save(order);
    }

    private BigDecimal calculateTotal(List<Long> productIds) {
        // Simplified calculation
        return productIds.stream()
            .map(id -> new BigDecimal("100.00"))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    public Order getOrderStatus(Long orderId) {
        return repository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));
    }

    public void cancelOrder(Long orderId) {
        Order order = getOrderStatus(orderId);

        if (order.getStatus().equals("SHIPPED")) {
            throw new CannotCancelShippedOrderException(orderId);
        }

        order.setStatus("CANCELLED");
        repository.save(order);

        // Refund payment
        paymentService.refund(order.getUserId(), order.getTotalAmount());
    }
}
```

**Yêu cầu:**

Viết unit tests cho các scenarios:

1. ✅ shouldCreateOrderSuccessfully
2. ✅ shouldThrowExceptionWhenProductOutOfStock
3. ✅ shouldThrowExceptionWhenPaymentFails
4. ✅ shouldGetOrderStatus
5. ✅ shouldThrowExceptionWhenOrderNotFound
6. ✅ shouldCancelOrderSuccessfully
7. ✅ shouldThrowExceptionWhenCancellingShippedOrder

### Template

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository repository;

    @Mock
    private PaymentService paymentService;

    @Mock
    private InventoryService inventoryService;

    @InjectMocks
    private OrderService service;

    // TODO: Implement tests here
}
```

---

## 📝 BÀI TẬP 2: INTEGRATION TEST VỚI TESTCONTAINERS (1 giờ)

### Đề bài

Viết integration test cho REST API:

```java
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService service;

    @PostMapping
    public ResponseEntity<OrderDTO> createOrder(@RequestBody CreateOrderRequest request) {
        Order order = service.createOrder(request.getUserId(), request.getProductIds());
        return ResponseEntity.status(HttpStatus.CREATED).body(toDTO(order));
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderDTO> getOrder(@PathVariable Long id) {
        Order order = service.getOrderStatus(id);
        return ResponseEntity.ok(toDTO(order));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> cancelOrder(@PathVariable Long id) {
        service.cancelOrder(id);
        return ResponseEntity.noContent().build();
    }

    private OrderDTO toDTO(Order order) {
        // Conversion logic
    }
}
```

**Yêu cầu:**

Viết integration tests với Testcontainers (PostgreSQL):

1. ✅ shouldCreateOrderViaApi
2. ✅ shouldGetOrderById
3. ✅ shouldReturn404WhenOrderNotFound
4. ✅ shouldCancelOrderViaApi

### Template

```java
@SpringBootTest
@Testcontainers
@AutoConfigureMockMvc
class OrderControllerIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void setProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    // TODO: Implement tests here
}
```

---

## 📝 BÀI TẬP 3: PARAMETERIZED TESTS (30 phút)

### Đề bài

Viết parameterized tests cho validation logic:

```java
@Service
public class ValidationService {

    public boolean isValidEmail(String email) {
        if (email == null || email.isBlank()) {
            return false;
        }
        return email.matches("^[A-Za-z0-9+_.-]+@(.+)$");
    }

    public boolean isValidPassword(String password) {
        if (password == null || password.length() < 8) {
            return false;
        }
        // Must contain at least one uppercase, one lowercase, one digit
        return password.matches(".*[A-Z].*") &&
               password.matches(".*[a-z].*") &&
               password.matches(".*\\d.*");
    }

    public boolean isValidPhone(String phone) {
        if (phone == null) {
            return false;
        }
        return phone.matches("^\\+?[0-9]{10,15}$");
    }
}
```

**Yêu cầu:**

```java
@ExtendWith(MockitoExtension.class)
class ValidationServiceTest {

    @InjectMocks
    private ValidationService service;

    // Test valid emails
    @ParameterizedTest
    @ValueSource(strings = {
        "john@example.com",
        "jane.doe@company.co.uk",
        "user+tag@gmail.com"
    })
    void shouldReturnTrueForValidEmail(String email) {
        // TODO
    }

    // Test invalid emails
    @ParameterizedTest
    @ValueSource(strings = {
        "",
        " ",
        "invalid",
        "@example.com",
        "user@"
    })
    void shouldReturnFalseForInvalidEmail(String email) {
        // TODO
    }

    // Test valid passwords
    @ParameterizedTest
    @CsvSource({
        "Password1",
        "Secure123",
        "MyP@ssw0rd"
    })
    void shouldReturnTrueForValidPassword(String password) {
        // TODO
    }

    // Test invalid passwords
    @ParameterizedTest
    @CsvSource({
        "short",
        "nouppercase1",
        "NOLOWERCASE1",
        "NoDigitsHere",
        "12345678"
    })
    void shouldReturnFalseForInvalidPassword(String password) {
        // TODO
    }
}
```

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 07

- [ ] Viết được unit tests với Mockito
- [ ] Sử dụng được @Mock, @InjectMocks
- [ ] Verify được method calls
- [ ] Viết được integration tests với Testcontainers
- [ ] Sử dụng được @Testcontainers, @Container
- [ ] Viết được parameterized tests
- [ ] Áp dụng được AAA pattern
- [ ] Đặt tên test methods đúng convention

---

## 📤 CÁCH SUBMIT

1. Push code lên GitHub
2. Tạo file `TESTS_REPORT.md` với:
   - Link GitHub
   - Số lượng tests viết
   - Code coverage (nếu có)
   - Khó khăn gặp phải

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, unlock Phase 08: Network & OS!
