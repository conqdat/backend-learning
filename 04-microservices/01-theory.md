# Phase 4: Microservices Architecture - Lý Thuyết

> **Thời gian:** 4 tuần
> **Mục tiêu:** Design và implement microservices architecture production-ready

---

## 📚 BÀI 1: MONOLITH VS MICROSERVICES

### 1.1 Monolithic Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MONOLITH APPLICATION                      │
├─────────────────────────────────────────────────────────────┤
│  UI Layer (Controllers)                                      │
│  ├── User Controller                                         │
│  ├── Product Controller                                      │
│  ├── Order Controller                                        │
│  └── Payment Controller                                      │
├─────────────────────────────────────────────────────────────┤
│  Business Logic (Services)                                   │
│  ├── User Service                                            │
│  ├── Product Service                                         │
│  ├── Order Service                                           │
│  └── Payment Service                                         │
├─────────────────────────────────────────────────────────────┤
│  Data Access (Repositories)                                  │
│  ├── User Repository                                         │
│  ├── Product Repository                                      │
│  ├── Order Repository                                        │
│  └── Payment Repository                                      │
├─────────────────────────────────────────────────────────────┤
│                    SINGLE DATABASE                           │
│  ├── users_table                                             │
│  ├── products_table                                          │
│  ├── orders_table                                            │
│  └── payments_table                                          │
└─────────────────────────────────────────────────────────────┘
```

**Ưu điểm:**
- ✅ Đơn giản develop, test, deploy
- ✅ Transaction dễ dàng (ACID)
- ✅ Phù hợp cho startup, team nhỏ
- ✅ Debug dễ dàng

**Nhược điểm:**
- ❌ Khó scale khi lượng traffic tăng
- ❌ Codebase lớn, phức tạp
- ❌ Tất cả services phải cùng release cycle
- ❌ Khó adopt công nghệ mới
- ❌ Single point of failure

---

### 1.2 Microservices Architecture

```
                         ┌──────────────┐
                         │  API Gateway │
                         └──────┬───────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│  User Service │       │ Order Service │       │Product Service│
├───────────────┤       ├───────────────┤       ├───────────────┤
│ User DB       │       │ Order DB      │       │ Product DB    │
│ (PostgreSQL)  │       │ (PostgreSQL)  │       │ (MongoDB)     │
└───────────────┘       └───────────────┘       └───────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                        ┌───────▼───────┐
                        │ Message Broker│
                        │    (Kafka)    │
                        └───────────────┘
```

**Ưu điểm:**
- ✅ Mỗi service độc lập deploy, scale
- ✅ Mỗi service có thể dùng công nghệ khác nhau
- ✅ Fault isolation - 1 service fail không ảnh hưởng toàn system
- ✅ Team nhỏ có thể ownership 1 service
- ✅ Dễ adopt công nghệ mới

**Nhược điểm:**
- ❌ Complex distributed system
- ❌ Data consistency khó (eventual consistency)
- ❌ Network latency
- ❌ Debug khó khăn (distributed tracing cần thiết)
- ❌ Operational overhead cao

---

### 1.3 Khi nào nên dùng Microservices?

**ĐỪNG dùng microservices nếu:**
- ❌ Startup giai đoạn đầu (< 10 developers)
- ❌ Product chưa tìm được product-market fit
- ❌ Team chưa có kinh nghiệm distributed systems
- ❌ Requirements chưa rõ ràng

**NÊN dùng microservices nếu:**
- ✅ Team lớn (> 20 developers)
- ✅ System cần scale độc lập các components
- ✅ Cần different technology stacks
- ✅ Có team DevOps成熟

---

## 📚 BÀI 2: SERVICE DECOMPOSITION PATTERNS

### 2.1 Decompose by Business Capability

**Phổ biến nhất - align với business domains**

```
E-commerce Platform
├── User Service (quản lý users, authentication)
├── Product Service (quản lý products, categories)
├── Order Service (xử lý orders)
├── Payment Service (xử lý payments)
├── Inventory Service (quản lý stock)
├── Shipping Service (vận chuyển)
└── Notification Service (email, SMS, push)
```

---

### 2.2 Decompose by Subdomain (DDD)

**Domain-Driven Design approach**

```
E-commerce Domain
├── Core Domain
│   ├── Catalog Subdomain (Product Service)
│   └── Order Subdomain (Order Service)
├── Supporting Domain
│   ├── Payment Subdomain (Payment Service)
│   └── Inventory Subdomain (Inventory Service)
└── Generic Domain
    ├── Identity Subdomain (User Service)
    └── Notification Subdomain (Notification Service)
```

---

## 📚 BÀI 3: INTER-SERVICE COMMUNICATION

### 3.1 Synchronous Communication (HTTP/REST)

```
┌─────────────┐      HTTP/REST      ┌─────────────┐
│   Service A │ ───────────────────►│   Service B │
│             │ ◄───────────────────│             │
└─────────────┘     JSON Response   └─────────────┘
```

**Khi nào dùng:**
- ✅ Cần immediate response
- ✅ Simple request-response
- ✅ Real-time validation

**Khi nào KHÔNG dùng:**
- ❌ Long-running operations
- ❌ Chain nhiều services (latency)
- ❌ Need high availability

**Ví dụ:**
```java
// Order Service gọi User Service để validate user
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @Autowired
    private RestTemplate restTemplate;

    @PostMapping
    public Order createOrder(@RequestBody OrderRequest request) {
        // Validate user exists (synchronous call)
        ResponseEntity<User> userResponse = restTemplate.getForEntity(
            "http://user-service/api/users/" + request.getUserId(),
            User.class
        );

        if (userResponse.getStatusCode() != HttpStatus.OK) {
            throw new InvalidUserException("User not found");
        }

        // Create order...
    }
}
```

---

### 3.2 Asynchronous Communication (Message Queue)

```
┌─────────────┐      Publish       ┌──────────────┐      Subscribe     ┌─────────────┐
│   Service A │ ──────────────────►│    Kafka     │───────────────────►│   Service B │
└─────────────┘      Event         └──────────────┘      Consume       └─────────────┘
                                                          │
                                                          ▼
                                                    ┌─────────────┐
                                                    │   Service C │
                                                    └─────────────┘
```

**Khi nào dùng:**
- ✅ Event-driven architecture
- ✅ Need loose coupling
- ✅ Background processing
- ✅ Eventual consistency acceptable

**Ví dụ:**
```java
// Order Service publish event
@Service
public class OrderService {

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Transactional
    public Order createOrder(OrderRequest request) {
        Order order = orderRepository.save(request.toOrder());

        // Publish event asynchronously
        kafkaTemplate.send("order-created", new OrderCreatedEvent(
            order.getId(),
            order.getUserId(),
            order.getTotalAmount(),
            LocalDateTime.now()
        ));

        return order;
    }
}

// Inventory Service consume event
@Component
public class InventoryListener {

    @KafkaListener(topics = "order-created", groupId = "inventory-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Reserve inventory
        inventoryService.reserveItems(event.getOrderId());
    }
}

// Payment Service cũng consume cùng event
@Component
public class PaymentListener {

    @KafkaListener(topics = "order-created", groupId = "payment-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Process payment
        paymentService.processPayment(event.getOrderId(), event.getAmount());
    }
}
```

---

### 3.3 So sánh Sync vs Async

| Aspect | Synchronous | Asynchronous |
|--------|-------------|--------------|
| Coupling | Tight | Loose |
| Response time | Immediate | Delayed |
| Availability | Dependent on callee | Independent |
| Complexity | Simple | Complex |
| Use case | Validation, real-time | Events, background jobs |

---

## 📚 BÀI 4: SAGA PATTERN FOR DISTRIBUTED TRANSACTIONS

### 4.1 Bài toán distributed transaction

**Scenario:** Place order

```
1. Order Service: Create order (PENDING status)
2. Payment Service: Charge credit card
3. Inventory Service: Reserve items
4. Shipping Service: Create shipment

Nếu step 2 fail (payment failed):
→ Step 1 phải rollback (cancel order)
→ Step 3 không cần làm
```

Trong monolith: Dùng `@Transactional` - tự động rollback

Trong microservices: Mỗi service có database riêng → KHÔNG THỂ dùng distributed transaction (2PC quá chậm)

**Giải pháp: SAGA Pattern**

---

### 4.2 Choreography-based Saga

**Mỗi service tự publish events và react**

```
┌─────────────┐    OrderCreated    ┌─────────────┐
│Order Service│───────────────────►│Payment Svc  │
└─────────────┘                    └──────┬──────┘
                                          │
                     PaymentProcessed     ▼
                    ┌─────────────────┌─────────────┐
                    │                 │Inventory Svc│
                    │                 └──────┬──────┘
                    │                        │
                    │      StockReserved     ▼
                    │     ┌─────────────────┌─────────────┐
                    │     │                 │Shipping Svc │
                    │     │                 └──────┬──────┘
                    │     │                        │
                    │     │     ShipmentCreated    │
                    ▼     ▼                        ▼
                ┌────────────────────────────────────────┐
                │          All steps completed           │
                └────────────────────────────────────────┘
```

**Code ví dụ:**

```java
// Order Service
@Service
public class OrderService {

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Transactional
    public Order createOrder(OrderRequest request) {
        Order order = orderRepository.save(request.toOrder());
        order.setStatus("PENDING");

        // Publish event
        kafkaTemplate.send("order-created", new OrderCreatedEvent(
            order.getId(),
            order.getUserId(),
            order.getTotalAmount()
        ));

        return order;
    }

    // Handle completion
    @KafkaListener(topics = "order-completed", groupId = "order-service")
    public void onOrderCompleted(OrderCompletedEvent event) {
        Order order = orderRepository.findById(event.getOrderId()).get();
        order.setStatus("COMPLETED");
        orderRepository.save(order);
    }

    // Handle failure
    @KafkaListener(topics = "payment-failed", groupId = "order-service")
    public void onPaymentFailed(PaymentFailedEvent event) {
        Order order = orderRepository.findById(event.getOrderId()).get();
        order.setStatus("CANCELLED");
        orderRepository.save(order);

        // Publish compensating event
        kafkaTemplate.send("order-cancelled", new OrderCancelledEvent(order.getId()));
    }
}

// Payment Service
@Component
public class PaymentListener {

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @KafkaListener(topics = "order-created", groupId = "payment-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        try {
            // Process payment
            boolean success = paymentGateway.charge(event.getAmount());

            if (success) {
                kafkaTemplate.send("payment-processed",
                    new PaymentProcessedEvent(event.getOrderId()));
            } else {
                kafkaTemplate.send("payment-failed",
                    new PaymentFailedEvent(event.getOrderId(), "Payment declined"));
            }
        } catch (Exception e) {
            kafkaTemplate.send("payment-failed",
                new PaymentFailedEvent(event.getOrderId(), e.getMessage()));
        }
    }
}
```

---

### 4.3 Orchestration-based Saga

**Central coordinator (orchestrator) điều phối các steps**

```
┌──────────────────────────────────────────────────────────┐
│                    Order Orchestrator                     │
├──────────────────────────────────────────────────────────┤
│  1. Call Order Service → Create order                    │
│  2. Call Payment Service → Process payment               │
│  3. Call Inventory Service → Reserve stock               │
│  4. Call Shipping Service → Create shipment              │
│                                                           │
│  Nếu step 2 fail:                                        │
│  → Call Order Service → Cancel order (compensate)        │
└──────────────────────────────────────────────────────────┘
```

**Code ví dụ:**

```java
@Service
public class OrderOrchestrator {

    @Autowired
    private OrderServiceClient orderClient;

    @Autowired
    private PaymentServiceClient paymentClient;

    @Autowired
    private InventoryServiceClient inventoryClient;

    @Autowired
    private ShippingServiceClient shippingClient;

    @Transactional
    public OrderResult placeOrder(OrderRequest request) {
        try {
            // Step 1: Create order
            Order order = orderClient.createOrder(request);

            // Step 2: Process payment
            PaymentResult payment = paymentClient.processPayment(
                new PaymentRequest(order.getId(), request.getAmount())
            );

            if (!payment.isSuccess()) {
                throw new PaymentFailedException("Payment declined");
            }

            // Step 3: Reserve inventory
            inventoryClient.reserveStock(
                new StockRequest(order.getId(), request.getItems())
            );

            // Step 4: Create shipment
            shippingClient.createShipment(
                new ShipmentRequest(order.getId(), request.getAddress())
            );

            // All steps completed
            orderClient.completeOrder(order.getId());
            return OrderResult.success(order.getId());

        } catch (PaymentFailedException e) {
            // Compensating transaction
            orderClient.cancelOrder(request.getOrderId());
            return OrderResult.failure("Payment failed");

        } catch (Exception e) {
            // Compensating transactions
            orderClient.cancelOrder(request.getOrderId());
            return OrderResult.failure("Order failed: " + e.getMessage());
        }
    }
}
```

---

### 4.4 So sánh Choreography vs Orchestration

| Aspect | Choreography | Orchestration |
|--------|-------------|---------------|
| Coupling | Loose | Tight |
| Complexity | Distributed | Centralized |
| Single point of failure | No | Yes (orchestrator) |
| Easy to add new service | Yes | No |
| Visibility | Hard | Easy |
| Best for | Simple workflows | Complex workflows |

---

## 📚 BÀI 5: API GATEWAY PATTERN

### 5.1 API Gateway là gì?

**Single entry point cho tất cả client requests**

```
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                            │
├─────────────────────────────────────────────────────────────┤
│  - Routing                                                  │
│  - Authentication/Authorization                             │
│  - Rate Limiting                                            │
│  - Load Balancing                                           │
│  - Circuit Breaker                                          │
│  - Logging/Metrics                                          │
└─────────────────────────────────────────────────────────────┘
```

---

### 5.2 Spring Cloud Gateway

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
```

```yaml
# application.yml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/users/**
          filters:
            - AuthenticationFilter
            - RateLimiterFilter=100

        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
          filters:
            - AuthenticationFilter
            - CircuitBreakerFilter

        - id: product-service
          uri: lb://product-service
          predicates:
            - Path=/api/products/**
```

**Custom Filter:**

```java
@Component
public class AuthenticationFilter implements GlobalFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();

        // Check if path requires authentication
        if (isPublicPath(request.getPath().value())) {
            return chain.filter(exchange);
        }

        // Validate JWT token
        String authHeader = request.getHeaders().getFirst("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }

        String token = authHeader.substring(7);
        try {
            Claims claims = JwtUtil.parseToken(token);
            // Add user info to headers for downstream services
            ServerHttpRequest modifiedRequest = request.mutate()
                .header("X-User-Id", claims.getSubject())
                .header("X-User-Role", claims.get("role", String.class))
                .build();

            return chain.filter(exchange.mutate().request(modifiedRequest).build());

        } catch (JwtException e) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }
    }

    private boolean isPublicPath(String path) {
        return path.startsWith("/api/auth/") ||
               path.startsWith("/api/products/") ||
               path.startsWith("/api/public/");
    }
}
```

---

## 📝 TÓM TẮT PHASE 4

Sau phase này, bạn cần nắm được:

1. ✅ Monolith vs Microservices - khi nào dùng gì
2. ✅ Service decomposition patterns
3. ✅ Sync (REST) vs Async (Kafka) communication
4. ✅ Saga pattern cho distributed transactions
5. ✅ API Gateway pattern với Spring Cloud Gateway

---

## 🔜 TIẾP THEO

Đọc `02-examples.md` để xem code mẫu thực tế!

---

## 📚 TÀI LIỆU THAM KHẢO

### Microservices Fundamentals

| Resource | Link | Nội dung |
|----------|------|----------|
| Microservices.io | [microservices.io](https://microservices.io/) | Patterns for microservices architecture |
| Martin Fowler - Microservices | [martinfowler.com/microservices](https://martinfowler.com/articles/microservices.html) | Original microservices article |
| Building Microservices (Book) | [O'Reilly](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/) | Comprehensive guide by Sam Newman |

### Service Communication

| Resource | Link | Nội dung |
|----------|------|----------|
| Sync vs Async Communication | [microservices.io](https://microservices.io/patterns/communication-style.html) | When to use each approach |
| Kafka Documentation | [kafka.apache.org](https://kafka.apache.org/documentation/) | Official Kafka docs |
| Spring for Apache Kafka | [Spring Docs](https://docs.spring.io/spring-kafka/reference/html/) | Kafka integration with Spring |

### Saga Pattern

| Resource | Link | Nội dung |
|----------|------|----------|
| Saga Pattern | [microservices.io](https://microservices.io/patterns/data/saga.html) | Choreography vs Orchestration |
| Implementing Sagas | [microservices.io](https://microservices.io/patterns/data/saga-implementation.html) | Code examples |
| Saga Best Practices | [camunda.com](https://camunda.com/learn/microservices/saga-pattern/) | Process orchestration guide |

### API Gateway

| Resource | Link | Nội dung |
|----------|------|----------|
| Spring Cloud Gateway | [Spring Docs](https://docs.spring.io/spring-cloud-gateway/reference/html/) | Official documentation |
| API Gateway Patterns | [microservices.io](https://microservices.io/patterns/apigateway.html) | When and how to use |
| Kong API Gateway | [konghq.com](https://konghq.com/) | Alternative API gateway |

### Service Discovery & Configuration

| Resource | Link | Nội dung |
|----------|------|----------|
| Service Discovery | [microservices.io](https://microservices.io/patterns/service-registry.html) | Service registry pattern |
| Spring Cloud Netflix | [Spring Docs](https://spring.io/projects/spring-cloud-netflix) | Eureka, Hystrix, Zuul |
| Config Server | [Spring Docs](https://spring.io/projects/spring-cloud-config) | Centralized configuration |

### Resilience Patterns

| Resource | Link | Nội dung |
|----------|------|----------|
| Circuit Breaker Pattern | [microservices.io](https://microservices.io/patterns/reliability/circuit-breaker.html) | Handle failures gracefully |
| Resilience4j | [resilience4j.readme.io](https://resilience4j.readme.io/) | Circuit breaker library |
| Bulkhead Pattern | [microservices.io](https://microservices.io/patterns/reliability/bulkhead.html) | Isolate resources |
