# Phase 1: Spring Boot Core - Ví Dụ Thực Tế

> **Note:** Đọc lý thuyết ở `01-theory.md` trước khi vào đây

---

## 📁 BÀI 1: PHÂN TÍCH STARTER DEPENDENCIES

### Ví dụ 1.1: Xem dependency tree

**Project mẫu:** https://start.spring.io/

```xml
<!-- pom.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
    </parent>

    <dependencies>
        <!-- Web starter -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- JPA starter -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- PostgreSQL driver -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Actuator -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
    </dependencies>
</project>
```

**Chạy lệnh để xem tree:**
```bash
mvn dependency:tree
```

**Output thực tế:**
```
[INFO] com.example:demo:jar:0.0.1-SNAPSHOT
[INFO] +- org.springframework.boot:spring-boot-starter-web:jar:3.2.0:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter:jar:3.2.0:compile
[INFO] |  |  +- org.springframework.boot:spring-boot:jar:3.2.0:compile
[INFO] |  |  +- org.springframework.boot:spring-boot-autoconfigure:jar:3.2.0:compile
[INFO] |  |  +- org.springframework.boot:spring-boot-starter-logging:jar:3.2.0:compile
[INFO] |  |  |  +- ch.qos.logback:logback-classic:jar:1.4.14:compile
[INFO] |  |  |  +- org.apache.logging.log4j:log4j-to-slf4j:jar:2.21.1:compile
[INFO] |  |  |  └── org.slf4j:jul-to-slf4j:jar:2.0.9:compile
[INFO] |  |  +- jakarta.annotation:jakarta.annotation-api:jar:2.1.1:compile
[INFO] |  |  └── org.yaml:snakeyaml:jar:2.2:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-json:jar:3.2.0:compile
[INFO] |  |  +- com.fasterxml.jackson.core:jackson-databind:jar:2.15.3:compile
[INFO] |  |  +- com.fasterxml.jackson.datatype:jackson-datatype-jdk8:jar:2.15.3:compile
[INFO] |  |  └── com.fasterxml.jackson.module:jackson-module-parameter-names:jar:2.15.3:compile
[INFO] |  +- org.springframework:spring-web:jar:6.1.1:compile
[INFO] |  |  └── org.springframework:spring-beans:jar:6.1.1:compile
[INFO] |  └── org.springframework:spring-webmvc:jar:6.1.1:compile
[INFO] |     +- org.springframework:spring-context:jar:6.1.1:compile
[INFO] |     └── org.springframework:spring-expression:jar:6.1.1:compile
[INFO] +- org.springframework.boot:spring-boot-starter-data-jpa:jar:3.2.0:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-jdbc:jar:3.2.0:compile
[INFO] |  |  +- com.zaxxer:HikariCP:jar:5.0.1:compile
[INFO] |  |  └── org.springframework:spring-jdbc:jar:6.1.1:compile
[INFO] |  +- org.hibernate.orm:hibernate-core:jar:6.3.1.Final:compile
[INFO] |  |  +- jakarta.persistence:jakarta.persistence-api:jar:3.1.0:compile
[INFO] |  |  └── jakarta.transaction:jakarta.transaction-api:jar:2.0.1:compile
[INFO] |  +- org.springframework.data:spring-data-jpa:jar:3.2.0:compile
[INFO] |  |  +- org.springframework.data:spring-data-commons:jar:3.2.0:compile
[INFO] |  |  └── org.springframework:spring-orm:jar:6.1.1:compile
[INFO] |  └── org.springframework:spring-aspects:jar:6.1.1:compile
[INFO] └── org.postgresql:postgresql:jar:42.6.0:runtime
```

**Bài học rút ra:**
- `spring-boot-starter-web` kéo theo **15+ dependencies**
- `spring-boot-starter-data-jpa` kéo theo **Hibernate, Spring Data JPA, HikariCP**
- Bạn không cần nhớ từng dependency - chỉ cần nhớ starter name

---

## 📁 BÀI 2: AUTO-CONFIGURATION TRONG THỰC TẾ

### Ví dụ 2.1: Xem auto-configuration report

Khi muốn biết Spring Boot đã auto-configure những gì:

**Cách 1: Enable debug logging**

```yaml
# application.yml
debug: true
```

**Cách 2: Dùng endpoint**

```yaml
management:
  endpoints:
    web:
      exposure:
        include: conditions
```

Truy cập: `http://localhost:8080/actuator/conditions`

**Output mẫu (rút gọn):**
```json
{
  "contexts": {
    "application": {
      "positiveMatches": {
        "DataSourceAutoConfiguration": {
          "condition": "OnClassCondition",
          "matched": true,
          "reason": "found required class 'javax.sql.DataSource'"
        },
        "HibernateJpaAutoConfiguration": {
          "condition": "OnClassCondition",
          "matched": true,
          "reason": "found required class 'org.hibernate.jpa.HibernatePersistenceProvider'"
        }
      },
      "negativeMatches": {
        "RedisAutoConfiguration": {
          "condition": "OnClassCondition",
          "matched": false,
          "reason": "did not find required class 'org.springframework.data.redis.core.RedisTemplate'"
        },
        "SecurityAutoConfiguration": {
          "condition": "OnPropertyCondition",
          "matched": false,
          "reason": "@ConditionalOnProperty (spring.security.enabled) did not find property 'spring.security.enabled'"
        }
      }
    }
  }
}
```

**Đọc report này để:**
- ✅ Biết bean nào được tạo, tại sao
- ✅ Biết bean nào KHÔNG được tạo, tại sao
- ✅ Debug khi auto-configuration không hoạt động

---

### Ví dụ 2.2: Override DataSource auto-configuration

**Scenario:** Bạn muốn dùng 2 DataSources (primary cho users, secondary cho reports)

```java
@Configuration
public class DataSourceConfig {

    // Primary DataSource - cho users
    @Bean
    @Primary
    @ConfigurationProperties("spring.datasource.primary")
    public DataSource primaryDataSource() {
        return DataSourceBuilder.create().build();
    }

    // Secondary DataSource - cho reports
    @Bean
    @ConfigurationProperties("spring.datasource.secondary")
    public DataSource secondaryDataSource() {
        return DataSourceBuilder.create().build();
    }

    // Primary EntityManagerFactory
    @Bean
    @Primary
    public LocalContainerEntityManagerFactoryBean primaryEntityManagerFactory(
            EntityManagerFactoryBuilder builder,
            @Qualifier("primaryDataSource") DataSource dataSource) {

        return builder
            .dataSource(dataSource)
            .packages("com.example.user")  // Scan user entities
            .persistenceUnit("primary")
            .build();
    }

    // Secondary EntityManagerFactory
    @Bean
    public LocalContainerEntityManagerFactoryBean secondaryEntityManagerFactory(
            EntityManagerFactoryBuilder builder,
            @Qualifier("secondaryDataSource") DataSource dataSource) {

        return builder
            .dataSource(dataSource)
            .packages("com.example.report")  // Scan report entities
            .persistenceUnit("secondary")
            .build();
    }
}
```

```yaml
# application.yml
spring:
  datasource:
    primary:
      url: jdbc:postgresql://localhost:5432/users_db
      username: postgres
      password: secret1
      driver-class-name: org.postgresql.Driver
    secondary:
      url: jdbc:postgresql://localhost:5432/reports_db
      username: postgres
      password: secret2
      driver-class-name: org.postgresql.Driver
```

```java
// User Repository - dùng primary
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
}

// Report Repository - dùng secondary
@Repository
public interface ReportRepository extends JpaRepository<Report, Long> {
}
```

---

## 📁 BÀI 3: TẠO CUSTOM STARTER - CASE STUDY THỰC TẾ

### Ví dụ 3.1: Logging Starter cho công ty

**Yêu cầu:** Công ty có 10 microservices, cần:
- Centralized logging format (JSON)
- Tự động thêm correlation ID
- Gửi logs về ELK stack
- Dễ dàng enable/disable per service

**Giải pháp:** Tạo custom logging starter

**Project structure:**
```
company-logging-starter/
├── pom.xml
├── src/main/java/com/company/logging/
│   ├── LoggingAutoConfiguration.java
│   ├── LoggingProperties.java
│   ├── JsonLoggingService.java
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
    <artifactId>company-logging-starter</artifactId>
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
    </dependencies>
</project>
```

**LoggingProperties.java:**
```java
package com.company.logging;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "company.logging")
public class LoggingProperties {

    /**
     * Enable/disable logging
     */
    private boolean enabled = true;

    /**
     * Log format: JSON or TEXT
     */
    private String format = "JSON";

    /**
     * ELK stack endpoint
     */
    private String elkEndpoint = "http://logstash:5000";

    /**
     * Include correlation ID in logs
     */
    private boolean includeCorrelationId = true;

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
}
```

**JsonLoggingService.java:**
```java
package com.company.logging;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonLoggingService {

    private static final Logger log = LoggerFactory.getLogger(JsonLoggingService.class);
    private final LoggingProperties properties;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public JsonLoggingService(LoggingProperties properties) {
        this.properties = properties;
    }

    /**
     * Log info message
     */
    public void info(String event, String message) {
        if (!properties.isEnabled()) {
            return;
        }

        try {
            String logEntry = createLogEntry("INFO", event, message);
            System.out.println(logEntry);
        } catch (Exception e) {
            log.error("Failed to create log entry", e);
        }
    }

    /**
     * Log error message
     */
    public void error(String event, String message, Throwable throwable) {
        if (!properties.isEnabled()) {
            return;
        }

        try {
            String logEntry = createLogEntry("ERROR", event, message);
            System.err.println(logEntry);
        } catch (Exception e) {
            log.error("Failed to create log entry", e);
        }
    }

    private String createLogEntry(String level, String event, String message) throws Exception {
        var logData = new java.util.HashMap<String, Object>();
        logData.put("timestamp", java.time.Instant.now().toString());
        logData.put("level", level);
        logData.put("event", event);
        logData.put("message", message);
        logData.put("service", getServiceName());

        if (properties.isIncludeCorrelationId()) {
            logData.put("correlationId", getCorrelationId());
        }

        return objectMapper.writeValueAsString(logData);
    }

    private String getServiceName() {
        return System.getenv().getOrDefault("SERVICE_NAME", "unknown");
    }

    private String getCorrelationId() {
        ServletRequestAttributes attributes =
            (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        if (attributes != null) {
            return attributes.getRequest().getHeader("X-Correlation-ID");
        }
        return "no-correlation-id";
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

        // Add to response
        httpResponse.setHeader("X-Correlation-ID", correlationId);

        // Continue chain
        chain.doFilter(request, response);
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
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConditionalOnClass(JsonLoggingService.class)
@EnableConfigurationProperties(LoggingProperties.class)
public class LoggingAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(prefix = "company.logging", name = "enabled", havingValue = "true", matchIfMissing = true)
    public JsonLoggingService jsonLoggingService(LoggingProperties properties) {
        return new JsonLoggingService(properties);
    }

    @Bean
    @ConditionalOnProperty(prefix = "company.logging", name = "include-correlation-id", havingValue = "true", matchIfMissing = true)
    public CorrelationIdFilter correlationIdFilter() {
        return new CorrelationIdFilter();
    }
}
```

**Register auto-configuration:**

File: `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`

```
com.company.logging.LoggingAutoConfiguration
```

**Sử dụng trong microservice:**

```xml
<!-- pom.xml của microservice -->
<dependency>
    <groupId>com.company</groupId>
    <artifactId>company-logging-starter</artifactId>
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
```

```java
// Trong service class
@RestController
public class OrderService {

    @Autowired
    private JsonLoggingService loggingService;

    @PostMapping("/orders")
    public Order createOrder(@RequestBody OrderRequest request) {
        loggingService.info("ORDER_CREATE", "Creating order for user: " + request.getUserId());

        try {
            Order order = orderRepository.save(request.toOrder());
            loggingService.info("ORDER_CREATED", "Order created: " + order.getId());
            return order;
        } catch (Exception e) {
            loggingService.error("ORDER_CREATE_FAILED", "Failed to create order", e);
            throw e;
        }
    }
}
```

**Output logs:**
```json
{"timestamp":"2024-01-15T10:30:45.123Z","level":"INFO","event":"ORDER_CREATE","message":"Creating order for user: 123","service":"order-service","correlationId":"abc-123-def"}
{"timestamp":"2024-01-15T10:30:45.456Z","level":"INFO","event":"ORDER_CREATED","message":"Order created: 456","service":"order-service","correlationId":"abc-123-def"}
```

---

## 📁 BÀI 4: ACTUATOR TRONG PRODUCTION

### Ví dụ 4.1: Cấu hình production-ready

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

```yaml
# application.yml
management:
  server:
    port: 9090  # Separate port cho management endpoints

  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,env,loggers
      base-path: /actuator

  endpoint:
    health:
      show-details: always
      probes:
        enabled: true  # Kubernetes readiness/liveness probes

    metrics:
      access: read_only

  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:dev}
```

### Ví dụ 4.2: Custom Health Indicator cho Redis

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
                    .withDetail("host", getRedisHost())
                    .build();
            } else {
                return Health.down()
                    .withDetail("redis", "unexpected response: " + ping)
                    .build();
            }
        } catch (Exception e) {
            return Health.down(e)
                .withDetail("redis", "connection failed")
                .build();
        }
    }

    private String getRedisHost() {
        // Extract from Redis config
        return "redis:6379";
    }
}
```

### Ví dụ 4.3: Custom Metrics

```java
@Component
public class OrderMetrics {

    private final MeterRegistry meterRegistry;

    public OrderMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;

        // Register counter
        meterRegistry.counter("orders.created.total");
        meterRegistry.counter("orders.failed.total");

        // Register timer
        meterRegistry.timer("orders.processing.time");
    }

    public void recordOrderCreated() {
        meterRegistry.counter("orders.created.total").increment();
    }

    public void recordOrderFailed() {
        meterRegistry.counter("orders.failed.total").increment();
    }

    public <T> T recordProcessingTime(Supplier<T> supplier) {
        return meterRegistry.timer("orders.processing.time").recordSupplier(supplier);
    }
}
```

```java
@RestController
@RequestMapping("/orders")
public class OrderController {

    @Autowired
    private OrderMetrics metrics;

    @PostMapping
    public Order createOrder(@RequestBody OrderRequest request) {
        return metrics.recordProcessingTime(() -> {
            try {
                Order order = orderService.create(request);
                metrics.recordOrderCreated();
                return order;
            } catch (Exception e) {
                metrics.recordOrderFailed();
                throw e;
            }
        });
    }
}
```

**Xem metrics:**
```bash
curl http://localhost:9090/actuator/metrics/orders.created.total
curl http://localhost:9090/actuator/prometheus
```

---

## 📝 BÀI TẬP THỰC HÀNH

### Exercise 1: Phân tích project hiện tại

1. Vào project Spring Boot bạn đang làm
2. Chạy `mvn dependency:tree`
3. Liệt kê xem có bao nhiêu starters
4. Với mỗi starter, kể tên 3 dependencies quan trọng nhất

### Exercise 2: Xem auto-configuration report

1. Thêm `debug: true` vào application.yml
2. Chạy application
3. Tìm logs bắt đầu bằng `CONDITIONS EVALUATION REPORT`
4. Chọn 1 auto-configuration và giải thích tại sao nó được activate

### Exercise 3: Tạo custom starter đơn giản

Tạo starter `greeting-starter` với:
- `GreetingProperties` với prefix `greeting`, có properties `message` và `enabled`
- `GreetingService` trả về greeting message
- `GreetingAutoConfiguration` tạo bean khi enabled

Submit code để tôi review!

---

## 🔜 TIẾP THEO

Sau khi đọc xong, làm bài tập ở `03-exercises.md`
