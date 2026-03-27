# Phase 1: Spring Boot Core Mastery - Bài Tập Thực Hành

> **Thời gian:** 1-2 tuần
> **Đầu ra:** Code submit lên GitHub hoặc gửi cho mentor review

---

## 📝 BÀI TẬP 1: PHÂN TÍCH SPRING BOOT STARTERS (30 phút)

### Đề bài

1. Tạo project Spring Boot mới từ [start.spring.io](https://start.spring.io) với:
   - Spring Web
   - Spring Data JPA
   - PostgreSQL Driver
   - Spring Boot Actuator
   - Lombok

2. Chạy lệnh xem dependency tree:
   ```bash
   mvn dependency:tree > deps.txt
   ```

3. Trả lời câu hỏi:

   **a)** `spring-boot-starter-web` kéo theo những dependencies gì?
   ```
   - Embedded server: ? (Tomcat/Jetty/Undertow)
   - JSON library: ? (Jackson version)
   - Spring MVC version: ?
   - Validation library: ?
   ```

   **b)** `spring-boot-starter-data-jpa` kéo theo những gì?
   ```
   - ORM framework: ? (Hibernate version)
   - Connection pool: ? (HikariCP)
   - Spring Data JPA version: ?
   ```

   **c)** Có bao nhiêu total dependencies trong project?

### Cách submit

```markdown
## Kết quả phân tích dependencies

### a) spring-boot-starter-web dependencies
- Embedded server: Tomcat 10.1.16
- JSON library: Jackson 2.15.3
- Spring MVC: Spring Web 6.1.1
- Validation: hibernate-validator 8.0.1

### b) spring-boot-starter-data-jpa dependencies
- ORM: Hibernate 6.3.1.Final
- Connection pool: HikariCP 5.0.1
- Spring Data JPA: 3.2.0

### c) Total dependencies
- Total: 85 dependencies

### Bài học rút ra
- Starters giúp giảm đáng kể việc quản lý dependencies
- Spring Boot parent POM quản lý version tự động
```

---

## 📝 BÀI TẬP 2: TÌM HIỂU AUTO-CONFIGURATION (1 giờ)

### Đề bài

1. Tạo project Spring Boot mới với `spring-boot-starter-web`

2. Thêm vào `application.yml`:
   ```yaml
   debug: true
   logging:
     level:
       org.springframework.boot.autoconfigure: DEBUG
   ```

3. Chạy application và tìm log `CONDITIONS EVALUATION REPORT`

4. Chọn 5 auto-configuration classes và phân tích:

   | Class | Matched? | Reason |
   |-------|----------|--------|
   | `WebMvcAutoConfiguration` | ✅ Yes | Web application detected |
   | `HttpEncodingAutoConfiguration` | ✅ Yes | CharacterEncodingFilter class found |
   | `RedisAutoConfiguration` | ❌ No | RedisTemplate class not found |
   | `SecurityAutoConfiguration` | ❌ No | spring-security not in classpath |
   | `...` | ... | ... |

5. Thử disable `WebMvcAutoConfiguration` và xem điều gì xảy ra

### Cách submit

```markdown
## Kết quả debug auto-configuration

### 5 auto-configuration classes phân tích

#### 1. WebMvcAutoConfiguration
- Status: ✅ Positive (matched)
- Reason: Web application detected, DispatcherServlet found
- Conditions:
  - OnClassCondition: matched (DispatcherServlet)
  - OnWebApplicationCondition: matched (servlet web app)

#### 2. HttpEncodingAutoConfiguration
- Status: ✅ Positive
- Reason: CharacterEncodingFilter class found
- ...

#### 3. RedisAutoConfiguration
- Status: ❌ Negative
- Reason: RedisTemplate class not in classpath
- ...

### Thử disable WebMvcAutoConfiguration

Code:
@SpringBootApplication(exclude = {WebMvcAutoConfiguration.class})

Kết quả:
- Application vẫn chạy nhưng không có MVC endpoints
- Whitelabel error page hiển thị
- Bài học: Auto-configuration rất quan trọng!
```

---

## 📝 BÀI TẬP 3: TẠO CUSTOM STARTER - GREETING SERVICE (3-4 giờ)

### Đề bài

Tạo custom starter `greeting-starter` với các yêu cầu:

#### Yêu cầu bắt buộc

1. **Project structure:**
   ```
   greeting-starter/
   ├── pom.xml
   ├── src/main/java/com/example/greeting/
   │   ├── GreetingAutoConfiguration.java
   │   ├── GreetingProperties.java
   │   └── GreetingService.java
   └── src/main/resources/META-INF/spring/
       └── org.springframework.boot.autoconfigure.AutoConfiguration.imports
   ```

2. **GreetingProperties:**
   ```java
   @ConfigurationProperties(prefix = "greeting")
   public class GreetingProperties {
       private boolean enabled = true;
       private String message = "Hello";
       private String suffix = "!";
       // Getters, Setters
   }
   ```

3. **GreetingService:**
   ```java
   public class GreetingService {
       private final GreetingProperties properties;

       public GreetingService(GreetingProperties properties) {
           this.properties = properties;
       }

       public String greet(String name) {
           // Return: "Hello John!" nếu message="Hello", suffix="!"
       }
   }
   ```

4. **GreetingAutoConfiguration:**
   - Chỉ create bean khi `greeting.enabled=true`
   - Bind properties từ `@EnableConfigurationProperties`

5. **Register auto-configuration** trong file `.imports`

#### Yêu cầu nâng cao (bonus)

6. Thêm `GreetingController` tự động expose endpoint `/greet/{name}`

7. Thêm `GreetingHealthIndicator` cho actuator health endpoint

8. Thêm unit test cho `GreetingService`

### Hướng dẫn từng bước

#### Step 1: Tạo project structure

```bash
mkdir greeting-starter
cd greeting-starter

# Tạo cấu trúc thư mục
mkdir -p src/main/java/com/example/greeting
mkdir -p src/main/resources/META-INF/spring
```

#### Step 2: Tạo pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>greeting-starter</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- Spring Boot AutoConfigure -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-autoconfigure</artifactId>
            <version>3.2.0</version>
        </dependency>

        <!-- Configuration Processor (cho autocomplete) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-configuration-processor</artifactId>
            <version>3.2.0</version>
            <optional>true</optional>
        </dependency>

        <!-- Spring Boot Starter Web (provided) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
            <scope>provided</scope>
        </dependency>

        <!-- Test -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <version>3.2.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

#### Step 3: Tạo GreetingProperties.java

```java
package com.example.greeting;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "greeting")
public class GreetingProperties {

    private boolean enabled = true;
    private String message = "Hello";
    private String suffix = "!";

    public boolean isEnabled() { return enabled; }
    public void setEnabled(boolean enabled) { this.enabled = enabled; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public String getSuffix() { return suffix; }
    public void setSuffix(String suffix) { this.suffix = suffix; }
}
```

#### Step 4: Tạo GreetingService.java

```java
package com.example.greeting;

import org.springframework.util.StringUtils;

public class GreetingService {

    private final GreetingProperties properties;

    public GreetingService(GreetingProperties properties) {
        this.properties = properties;
    }

    public String greet(String name) {
        if (!properties.isEnabled()) {
            throw new IllegalStateException("Greeting service is disabled");
        }

        if (!StringUtils.hasText(name)) {
            name = "Guest";
        }

        return String.format("%s %s%s",
            properties.getMessage(),
            name,
            properties.getSuffix());
    }
}
```

#### Step 5: Tạo GreetingAutoConfiguration.java

```java
package com.example.greeting;

import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConditionalOnClass(GreetingService.class)
@EnableConfigurationProperties(GreetingProperties.class)
public class GreetingAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(prefix = "greeting", name = "enabled",
                          havingValue = "true", matchIfMissing = true)
    public GreetingService greetingService(GreetingProperties properties) {
        return new GreetingService(properties);
    }
}
```

#### Step 6: Tạo file register auto-configuration

File: `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`

```
com.example.greeting.GreetingAutoConfiguration
```

#### Step 7: Install vào local Maven repository

```bash
mvn clean install
```

#### Step 8: Tạo project test để sử dụng starter

```bash
mkdir greeting-demo
cd greeting-demo
# Tạo Spring Boot project mới
```

Thêm dependency:
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>greeting-starter</artifactId>
    <version>1.0.0</version>
</dependency>
```

Cấu hình:
```yaml
greeting:
  enabled: true
  message: "Xin chào"
  suffix: "!"
```

Controller test:
```java
@RestController
@RequestMapping("/api")
public class GreetingController {

    @Autowired
    private GreetingService greetingService;

    @GetMapping("/greet/{name}")
    public String greet(@PathVariable String name) {
        return greetingService.greet(name);
    }
}
```

#### Step 9: Test

```bash
# Run application
mvn spring-boot:run

# Test endpoint
curl http://localhost:8080/api/greet/John
# Expected: "Xin chào John!"

# Test với enabled=false
# Thêm vào application.yml: greeting.enabled: false
# Restart và test lại - phải lỗi IllegalStateException
```

### Cách submit

```markdown
## Kết quả bài tập Greeting Starter

### Link GitHub repository
https://github.com/yourusername/greeting-starter

### Các bước đã làm
1. ✅ Tạo project structure
2. ✅ Implement GreetingProperties
3. ✅ Implement GreetingService
4. ✅ Implement GreetingAutoConfiguration
5. ✅ Register auto-configuration
6. ✅ Test thành công

### Bonus (nếu có)
- ✅ GreetingController với endpoint /greet/{name}
- ✅ GreetingHealthIndicator
- ✅ Unit tests

### Khó khăn gặp phải
- Vấn đề: File .imports không được nhận diện
- Cách giải quyết: Kiểm tra lại path META-INF/spring/

### Bài học rút ra
- Hiểu cách auto-configuration hoạt động
- Biết cách tạo custom starter cho team
```

---

## 📝 BÀI TẬP 4: XÂY DỰNG REST API (4-5 giờ)

### Đề bài

Xây dựng REST API cho **Product Management** với các yêu cầu:

#### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | List products (pagination) |
| GET | `/api/products/{id}` | Get product by ID |
| POST | `/api/products` | Create product |
| PUT | `/api/products/{id}` | Update product |
| DELETE | `/api/products/{id}` | Delete product |
| GET | `/api/products/search` | Search products by name |

#### Entity: Product

```java
@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String sku;

    private String description;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal price;

    @Column(nullable = false)
    private Integer stock = 0;

    @Enumerated(EnumType.STRING)
    private ProductStatus status = ProductStatus.ACTIVE;

    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;
}

enum ProductStatus {
    ACTIVE, INACTIVE, OUT_OF_STOCK
}
```

#### DTOs

```java
// ProductCreateRequest
public record ProductCreateRequest(
    @NotBlank(message = "Name is required")
    String name,

    @NotBlank(message = "SKU is required")
    String sku,

    String description,

    @NotNull(message = "Price is required")
    @Positive(message = "Price must be positive")
    BigDecimal price,

    @NotNull(message = "Stock is required")
    @Min(value = 0, message = "Stock cannot be negative")
    Integer stock
) {}

// ProductUpdateRequest
public record ProductUpdateRequest(
    String name,
    String sku,
    String description,
    @Positive BigDecimal price,
    @Min(0) Integer stock
) {}

// ProductResponse
public record ProductResponse(
    Long id,
    String name,
    String sku,
    String description,
    BigDecimal price,
    Integer stock,
    ProductStatus status,
    LocalDateTime createdAt,
    LocalDateTime updatedAt
) {}
```

#### Yêu cầu bổ sung

1. **Validation:**
   - Name: required, min 2 characters
   - SKU: required, unique
   - Price: required, positive
   - Stock: required, non-negative

2. **Exception Handling:**
   - 404 khi product không tồn tại
   - 400 khi validation fail
   - 409 khi SKU bị trùng
   - 500 khi có lỗi server

3. **Pagination:**
   ```
   GET /api/products?page=0&size=10&sortBy=name&sortDir=asc
   ```

4. **Search:**
   ```
   GET /api/products/search?keyword=laptop
   ```

### Cách submit

```markdown
## Kết quả bài tập Product API

### Link GitHub repository
https://github.com/yourusername/product-api

### API Documentation

#### 1. List Products
```bash
curl http://localhost:8080/api/products?page=0&size=10
```

Response:
```json
{
  "content": [...],
  "page": 0,
  "size": 10,
  "totalElements": 100,
  "totalPages": 10
}
```

#### 2. Create Product
```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","sku":"LAP001","price":999.99,"stock":50}'
```

### Exception Handling
- ResourceNotFoundException → 404
- ValidationException → 400
- DuplicateResourceException → 409

### Tests
- Unit tests: 15 tests passed
- Integration tests: 8 tests passed

### Bài học rút ra
- Cách tổ chức layer: Controller → Service → Repository
- Validation với @Valid và Bean Validation
- Global exception handling với @RestControllerAdvice
```

---

## 📝 BÀI TẬP 5: SPRING SECURITY + JWT (4-5 giờ)

### Đề bài

Implement JWT Authentication cho Product API:

#### Yêu cầu

1. **Đăng ký user:**
   ```
   POST /api/auth/register
   Body: {
     "email": "user@example.com",
     "password": "password123",
     "name": "John Doe"
   }
   ```

2. **Đăng nhập:**
   ```
   POST /api/auth/login
   Body: {
     "email": "user@example.com",
     "password": "password123"
   }
   Response: {
     "token": "eyJhbGciOiJIUzI1NiIs...",
     "expiresIn": 86400000
   }
   ```

3. **Bảo vệ endpoints:**
   - `/api/auth/**` → Public
   - `/api/products` (GET) → Public
   - `/api/products` (POST, PUT, DELETE) → Requires authentication
   - `/api/admin/**` → Requires ADMIN role

4. **JWT Token:**
   - Secret key từ environment variable
   - Expiration: 24 hours
   - Include user email in claims

### Hướng dẫn

#### Step 1: Thêm dependencies

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.11.5</version>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.11.5</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.11.5</version>
    <scope>runtime</scope>
</dependency>
```

#### Step 2: Cấu hình security

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/products").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .addFilterBefore(jwtAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

#### Step 3: Implement JWT Filter

```java
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
        // Extract token from Authorization header
        String token = extractToken(request);

        if (token != null && tokenProvider.validateToken(token)) {
            String email = tokenProvider.getEmail(token);
            UserDetails userDetails = userDetailsService.loadUserByUsername(email);

            UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());

            authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
            SecurityContextHolder.getContext().setAuthentication(authentication);
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
```

### Cách submit

```markdown
## Kết quả bài tập Spring Security + JWT

### Link GitHub repository
https://github.com/yourusername/product-api-security

### Test Authentication Flow

#### 1. Register
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'
```

#### 2. Login
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 86400000
}
```

#### 3. Access Protected Endpoint
```bash
curl http://localhost:8080/api/products \
  -H "Authorization: Bearer eyJhbGci..."
```

### Security Features
- Password encoding với BCrypt
- JWT token với 24h expiration
- Role-based authorization
- Stateless session

### Bài học rút ra
- Hiểu Spring Security filter chain
- Cách implement JWT authentication
- Role-based access control
```

---

## 📝 BÀI TẬP 6: ACTUATOR & MONITORING (2 giờ)

### Đề bài

1. Thêm Actuator vào project Product API

2. Cấu hình expose endpoints:
   ```yaml
   management:
     endpoints:
       web:
         exposure:
           include: health,info,metrics,prometheus
     endpoint:
       health:
         show-details: always
   ```

3. Tạo custom Health Indicator cho Database:
   ```java
   @Component
   public class DatabaseHealthIndicator implements HealthIndicator {
       // Implement health check
   }
   ```

4. Test endpoints:
   ```bash
   curl http://localhost:8080/actuator/health
   curl http://localhost:8080/actuator/metrics
   ```

### Cách submit

```markdown
## Kết quả bài tập Actuator

### Custom Health Indicator

Code:
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
                return Health.up().withDetail("database", "connected").build();
            }
            return Health.down().withDetail("database", "connection invalid").build();
        } catch (SQLException e) {
            return Health.down(e).build();
        }
    }
}
```

### Test Results

```bash
curl http://localhost:8080/actuator/health
```

Response:
```json
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP",
      "details": {
        "database": "PostgreSQL",
        "validationQuery": "SELECT 1"
      }
    },
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 500000000000,
        "free": 200000000000,
        "threshold": 10000000000
      }
    },
    "database": {
      "status": "UP",
      "details": {
        "database": "connected"
      }
    }
  }
}
```

### Bài học rút ra
- Actuator cung cấp production-ready monitoring
- Custom health indicators cho external services
- Metrics export cho Prometheus/Grafana
```

---

## 📝 BÀI TẬP 7: UNIT TESTING & INTEGRATION TESTING (3-4 giờ)

### Đề bài

Viết tests cho Product API:

#### Unit Tests (Mockito)

1. Test ProductService.create() với valid data
2. Test ProductService.create() với invalid price (negative)
3. Test ProductService.update() với product không tồn tại
4. Test ProductService.delete() với product không tồn tại

#### Integration Tests

1. Test POST /api/products - Create success
2. Test POST /api/products - Validation fail
3. Test GET /api/products/{id} - Found
4. Test GET /api/products/{id} - Not found
5. Test PUT /api/products/{id} - Update success
6. Test DELETE /api/products/{id} - Delete success

### Cách submit

```markdown
## Kết quả bài tập Testing

### Unit Tests

```java
@ExtendWith(MockitoExtension.class)
class ProductServiceTest {

    @Mock
    private ProductRepository productRepository;

    @InjectMocks
    private ProductService productService;

    @Test
    void shouldCreateProductSuccessfully() {
        // Given
        ProductCreateRequest request = new ProductCreateRequest(
            "Laptop", "LAP001", "Description", new BigDecimal("999.99"), 50
        );
        when(productRepository.save(any())).thenReturn(new Product());

        // When
        Product result = productService.create(request);

        // Then
        assertThat(result).isNotNull();
        verify(productRepository).save(any());
    }

    @Test
    void shouldThrowExceptionWhenPriceNegative() {
        // Given
        ProductCreateRequest request = new ProductCreateRequest(
            "Laptop", "LAP001", "Description", new BigDecimal("-100"), 50
        );

        // When/Then
        assertThrows(ValidationException.class, () ->
            productService.create(request)
        );
    }
}
```

### Integration Tests

```java
@SpringBootTest
@AutoConfigureMockMvc
class ProductControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void shouldCreateProduct() throws Exception {
        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Laptop\",\"sku\":\"LAP001\",\"price\":999.99,\"stock\":50}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.name").value("Laptop"));
    }
}
```

### Test Coverage
- Unit tests: 10 tests, 100% pass
- Integration tests: 6 tests, 100% pass
- Code coverage: 85%

### Bài học rút ra
- Phân biệt unit test vs integration test
- Sử dụng @MockBean trong integration tests
- Test slices: @DataJpaTest, @WebMvcTest
```

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 1

Sau khi làm xong bài tập, check xem bạn đã nắm được chưa:

- [ ] Hiểu spring-boot-starter là gì và tại sao cần
- [ ] Biết cách xem dependency tree
- [ ] Hiểu auto-configuration hoạt động như thế nào
- [ ] Biết cách xem conditions evaluation report
- [ ] Hiểu các @ConditionalOn* annotations
- [ ] Biết cách override auto-configuration
- [ ] Tạo được custom starter đơn giản
- [ ] Xây dựng được REST API với validation
- [ ] Implement được JWT authentication
- [ ] Biết cấu hình và sử dụng Actuator endpoints
- [ ] Viết được unit tests và integration tests

---

## 📤 CÁCH SUBMIT BÀI TẬP

1. **Push code lên GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Phase 1: Complete exercises"
   git remote add origin https://github.com/yourusername/java-senior-learning.git
   git push -u origin main
   ```

2. **Gửi link cho mentor:**
   ```
   Chào mentor, tôi đã hoàn thành Phase 1.

   Link GitHub: https://github.com/...

   Bài tập đã làm:
   - Exercise 1: ✅ Dependencies Analysis
   - Exercise 2: ✅ Auto-Configuration Debug
   - Exercise 3: ✅ Custom Starter
   - Exercise 4: ✅ REST API
   - Exercise 5: ✅ Spring Security + JWT
   - Exercise 6: ✅ Actuator
   - Exercise 7: ✅ Testing

   Khó khăn gặp phải: ...
   ```

---

## 🔜 SAU KHI HOÀN THÀNH

Khi submit xong, mentor sẽ:
1. Review code chi tiết
2. Góp ý về coding style, best practices
3. Giải đáp các câu hỏi
4. Unlock Phase 2: Database & Hibernate

**Good luck! 🚀**
