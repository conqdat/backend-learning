# Phase 7: Production Ready - Lý Thuyết

> **Thời gian:** 3 tuần
> **Mục tiêu:** Monitoring, logging, debugging production issues

---

## 📚 BÀI 1: OBSERVABILITY PILLARS

### 3 Pillars of Observability

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                             │
├─────────────────────────────────────────────────────────────┤
│  1. Metrics (Numbers over time)                             │
│     - CPU usage, memory, request count, error rate          │
│     - Tools: Prometheus, Grafana, Datadog                   │
├─────────────────────────────────────────────────────────────┤
│  2. Logs (Records of events)                                │
│     - Application logs, access logs, error logs             │
│     - Tools: ELK Stack, Splunk, Loki                        │
├─────────────────────────────────────────────────────────────┤
│  3. Traces (Request flow across services)                   │
│     - Distributed tracing                                   │
│     - Tools: Jaeger, Zipkin, Tempo                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 2: METRICS & ALERTING

### 2.1 Four Golden Signals

```
1. Latency: Time to process request
   - Target: p99 < 200ms

2. Traffic: Demand on your system
   - QPS, requests/sec

3. Errors: Rate of failed requests
   - Target: < 0.1%

4. Saturation: How full your service is
   - CPU, memory, disk usage
   - Target: < 70%
```

### 2.2 Prometheus Metrics

```java
@Configuration
public class MetricsConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> metricsCommonTags() {
        return registry -> registry.config()
            .commonTags("application", "ecommerce",
                       "environment", "production");
    }
}

@Service
public class OrderService {

    private final MeterRegistry meterRegistry;
    private final Timer orderProcessingTimer;
    private final Counter ordersCreatedCounter;
    private final Counter ordersFailedCounter;

    public OrderService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;

        this.orderProcessingTimer = meterRegistry.timer("orders.processing.time");
        this.ordersCreatedCounter = meterRegistry.counter("orders.created.total");
        this.ordersFailedCounter = meterRegistry.counter("orders.failed.total");
    }

    public Order createOrder(OrderRequest request) {
        return orderProcessingTimer.record(() -> {
            try {
                Order order = orderRepository.save(request.toOrder());
                ordersCreatedCounter.increment();
                return order;
            } catch (Exception e) {
                ordersFailedCounter.increment();
                throw e;
            }
        });
    }
}
```

---

## 📚 BÀI 3: LOGGING BEST PRACTICES

### 3.1 Structured Logging

```java
// ❌ Bad: Unstructured log
log.info("Order " + orderId + " created for user " + userId);

// ✅ Good: Structured log (JSON)
log.info("Order created",
    kv("orderId", orderId),
    kv("userId", userId),
    kv("amount", amount),
    kv("timestamp", Instant.now())
);
```

### 3.2 Log Levels

```
ERROR: Something broke, needs immediate attention
WARN:  Something might be wrong, check it out
INFO:  Normal business events (order created, user logged in)
DEBUG: Detailed technical information for debugging
TRACE: Very detailed, usually disabled in production
```

### 3.3 Correlation IDs

```java
@Component
public class LoggingFilter implements Filter {

    private static final String CORRELATION_ID_HEADER = "X-Correlation-ID";

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        String correlationId = httpRequest.getHeader(CORRELATION_ID_HEADER);
        if (correlationId == null || correlationId.isEmpty()) {
            correlationId = UUID.randomUUID().toString();
        }

        MDC.put("correlationId", correlationId);
        httpResponse.setHeader(CORRELATION_ID_HEADER, correlationId);

        try {
            chain.doFilter(request, response);
        } finally {
            MDC.clear();
        }
    }
}
```

---

## 📚 BÀI 4: CIRCUIT BREAKER PATTERN

### 4.1 Circuit Breaker States

```
┌─────────────────────────────────────────────────────────────┐
│               CIRCUIT BREAKER STATES                         │
├─────────────────────────────────────────────────────────────┤
│  CLOSED (Normal)                                            │
│  - Requests flow through normally                           │
│  - Track failures                                           │
│  - If failures > threshold → OPEN                           │
├─────────────────────────────────────────────────────────────┤
│  OPEN (Tripped)                                             │
│  - All requests fail immediately                            │
│  - No calls to downstream service                           │
│  - After timeout → HALF_OPEN                                │
├─────────────────────────────────────────────────────────────┤
│  HALF_OPEN (Testing)                                        │
│  - Allow limited requests through                           │
│  - If success → CLOSED                                      │
│  - If failure → OPEN                                        │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Resilience4j Implementation

```java
@Service
public class OrderService {

    @Autowired
    private PaymentServiceClient paymentClient;

    @CircuitBreaker(name = "paymentService", fallbackMethod = "createOrderFallback")
    @Retry(name = "paymentService", maxAttempts = 3)
    @Bulkhead(name = "paymentService", maxConcurrentCalls = 10)
    public Order createOrder(OrderRequest request) {
        // Call payment service
        PaymentResult payment = paymentClient.processPayment(request);

        if (!payment.isSuccess()) {
            throw new PaymentFailedException("Payment failed");
        }

        return orderRepository.save(request.toOrder());
    }

    // Fallback method
    public Order createOrderFallback(OrderRequest request, Throwable t) {
        log.warn("Payment service unavailable, queuing order for later processing", t);
        // Queue order for async processing
        return orderRepository.save(request.toOrder());
    }
}
```

---

## 📚 BÀI 5: INCIDENT RESPONSE

### 5.1 Runbook Template

```
# Incident: High Error Rate

## Symptoms
- Error rate > 5% for order service
- Customers reporting checkout failures

## Diagnosis Steps
1. Check Grafana dashboard: [link]
2. Check recent deployments: [link]
3. Check error logs: [query]
4. Check downstream dependencies status

## Resolution Steps
1. If recent deployment: Consider rollback
2. If database issue: Check connections, queries
3. If external service: Enable circuit breaker
4. Notify stakeholders

## Prevention
- Add alert for error rate > 1%
- Add automated rollback
```

---

## 📝 TÓM TẮT PHASE 7

1. ✅ 3 pillars of observability
2. ✅ Four golden signals
3. ✅ Structured logging với correlation IDs
4. ✅ Circuit breaker pattern
5. ✅ Incident response runbooks

---

## 🔜 TIẾP THEO

Phase 8: Capstone Project - Apply tất cả kiến thức!
