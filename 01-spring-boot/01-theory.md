# Phase 1: Spring Boot Core - Lý Thuyết

> **Thời gian:** 2 tuần
> **Mục tiêu:** Hiểu sâu cách Spring Boot hoạt động, không chỉ biết dùng

---

## 📚 BÀI 1: SPRING BOOT HOẠT ĐỘNG NHƯ THẾ NÀO?

### 1.1 Vấn đề của Spring "ngày xưa"

Trước Spring Boot (2014 trở về trước), để tạo một Spring MVC app, bạn cần:

```xml
<!-- pom.xml - 20+ dependencies -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-core</artifactId>
    <version>4.0.0.RELEASE</version>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-beans</artifactId>
    <version>4.0.0.RELEASE</version>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>4.0.0.RELEASE</version>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>4.0.0.RELEASE</version>
</dependency>
<!-- Còn spring-security, spring-orm, spring-tx... -->
```

```java
// web.xml - Cấu hình XML
<web-app>
    <servlet>
        <servlet-name>dispatcher</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>/WEB-INF/applicationContext.xml</param-value>
        </init-param>
    </servlet>
    <servlet-mapping>
        <servlet-name>dispatcher</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>

    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>
</web-app>
```

```xml
<!-- applicationContext.xml - Hàng trăm dòng XML -->
<beans>
    <bean id="userService" class="com.example.UserServiceImpl">
        <property name="userRepository" ref="userRepository"/>
    </bean>

    <bean id="userRepository" class="com.example.UserRepository">
        <property name="dataSource" ref="dataSource"/>
    </bean>

    <bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource">
        <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
        <property name="url" value="jdbc:mysql://localhost:3306/mydb"/>
        <property name="username" value="root"/>
        <property name="password" value="password"/>
    </bean>
    <!-- ... thêm 50 beans nữa -->
</beans>
```

**Vấn đề:**
- ❌ Quá nhiều cấu hình thủ công (XML hell)
- ❌ Phải quản lý version của từng dependency
- ❌ Dễ xung đột version
- ❌ Mất 30-60 phút để setup project mới

---

### 1.2 Spring Boot giải quyết như thế nào?

**Spring Boot = Spring + Convention over Configuration**

Với Spring Boot:

```xml
<!-- Chỉ cần 1 dependency -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

```java
// 1 class Java duy nhất
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

```yaml
# application.yml - 5 dòng
server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: secret
```

**Kết quả:**
- ✅ Setup project mới: 2 phút
- ✅ Không cần XML
- ✅ Không cần quản lý version thủ công
- ✅ Chạy ngay với `java -jar`

---

### 1.3 Ba "phép thuật" của Spring Boot

Spring Boot có 3 cơ chế chính:

#### **Phép thuật 1: Starter Dependencies**

Starter = "Dependency bundle" - Một dependency kéo theo nhiều dependency con

```
spring-boot-starter-web
├── spring-web (REST client)
├── spring-webmvc (Spring MVC)
├── jackson-databind (JSON serialization)
├── tomcat-embed-core (Embedded Tomcat)
├── hibernate-validator (Validation)
└── ... (tổng cộng 15+ libraries)
```

**Các starters quan trọng:**

| Starter | Kéo theo | Dùng khi |
|---------|----------|----------|
| `spring-boot-starter-web` | Spring MVC, Tomcat, Jackson | Làm REST API |
| `spring-boot-starter-data-jpa` | Hibernate, Spring Data JPA | Làm việc với database |
| `spring-boot-starter-security` | Spring Security | Authentication, Authorization |
| `spring-boot-starter-data-redis` | Spring Data Redis, Lettuce | Dùng Redis |
| `spring-boot-starter-actuator` | Metrics, Health endpoints | Monitoring |
| `spring-boot-starter-validation` | Hibernate Validator | Validate input |
| `spring-boot-starter-test` | JUnit, Mockito, AssertJ | Testing |

**Xem thực tế:**

Chạy lệnh này để xem dependencies:
```bash
cd your-spring-boot-project
mvn dependency:tree
```

Bạn sẽ thấy output kiểu:
```
[INFO] +- org.springframework.boot:spring-boot-starter-web:jar:3.2.0:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter:jar:3.2.0:compile
[INFO] |  |  +- org.springframework.boot:spring-boot:jar:3.2.0:compile
[INFO] |  |  +- org.springframework.boot:spring-boot-autoconfigure:jar:3.2.0:compile
[INFO] |  |  +- jakarta.annotation:jakarta.annotation-api:jar:2.1.1:compile
[INFO] |  +- org.springframework:spring-web:jar:6.1.1:compile
[INFO] |  +- org.springframework:spring-webmvc:jar:6.1.1:compile
[INFO] |  +- com.fasterxml.jackson.core:jackson-databind:jar:2.15.3:compile
[INFO] |  └── org.apache.tomcat.embed:tomcat-embed-core:jar:10.1.16:compile
```

---

#### **Phép thuật 2: Auto-Configuration**

**Câu hỏi lớn:** Tại sao chỉ cần add dependency mà Spring Boot tự động tạo ra beans?

**Trả lời:** Spring Boot scan classpath và tự động cấu hình dựa trên những gì nó tìm thấy.

**Cơ chế hoạt động:**

1. Khi khởi động, Spring Boot scan file:
   ```
   META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
   ```

2. File này chứa danh sách các configuration classes:
   ```
   org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration
   org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration
   org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration
   org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration
   ```

3. Mỗi configuration class có **conditions** - chỉ activate nếu thỏa điều kiện:

```java
@Configuration
@ConditionalOnClass({DataSource.class, JdbcTemplate.class})  // Nếu có class này trong classpath
@ConditionalOnMissingBean(DataSource.class)                   // Và chưa có DataSource bean
@ConditionalOnProperty(prefix = "spring.datasource", name = "url")  // Và có config url
public class DataSourceAutoConfiguration {

    @Bean
    @ConfigurationProperties(prefix = "spring.datasource")
    public DataSource dataSource() {
        // Tự động tạo DataSource từ properties
        return new HikariDataSource();
    }
}
```

**Các conditional annotations quan trọng:**

| Annotation | Ý nghĩa | Ví dụ |
|-----------|--------|-------|
| `@ConditionalOnClass` | Chỉ load nếu class tồn tại trong classpath | `@ConditionalOnClass(RedisTemplate.class)` |
| `@ConditionalOnMissingBean` | Chỉ tạo bean nếu chưa có bean cùng type | `@ConditionalOnMissingBean(UserService.class)` |
| `@ConditionalOnProperty` | Chỉ load nếu property được set | `@ConditionalOnProperty(name="cache.enabled")` |
| `@ConditionalOnWebApplication` | Chỉ load nếu là web app | `@ConditionalOnWebApplication` |
| `@ConditionalOnMissingClass` | Chỉ load nếu class KHÔNG tồn tại | `@ConditionalOnMissingClass("com.mysql.Driver")` |

---

#### **Phép thuật 3: Embedded Server**

Spring Boot embed server vào trong JAR, nên bạn có thể chạy:
```bash
java -jar app.jar
```

**Không cần:**
- ❌ Cài đặt Tomcat riêng
- ❌ Deploy WAR file
- ❌ Cấu hình server XML

**Supported embedded servers:**

| Server | Dependency | Default port |
|--------|-----------|--------------|
| Tomcat | `spring-boot-starter-web` (default) | 8080 |
| Jetty | `spring-boot-starter-jetty` | 8080 |
| Undertow | `spring-boot-starter-undertow` | 8080 |

**Đổi port trong application.yml:**
```yaml
server:
  port: 9000  # Đổi từ 8080 sang 9000
```

---

## 📚 BÀI 2: SPRING BOOT AUTO-CONFIGURATION CHI TIẾT

### 2.1 Ví dụ thực tế: JPA Auto-Configuration

Khi bạn add:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
</dependency>
```

Và config:
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: postgres
    password: secret
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
```

**Spring Boot tự động tạo các beans:**

```
1. DataSource (HikariCP)
2. EntityManagerFactory
3. TransactionManager
4. JpaRepositories
5. Entity Manager
```

**Code thật của Spring Boot:**

File: `HibernateJpaAutoConfiguration.java` (rút gọn)

```java
@Configuration
@ConditionalOnClass({ LocalContainerEntityManagerFactoryBean.class, EntityManager.class })
@ConditionalOnBean(DataSource.class)
@AutoConfigureAfter({ DataSourceAutoConfiguration.class })
public class HibernateJpaAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public LocalContainerEntityManagerFactoryBean entityManagerFactory(
            DataSource dataSource,
            JpaProperties jpaProperties) {

        LocalContainerEntityManagerFactoryBean emf = new LocalContainerEntityManagerFactoryBean();
        emf.setDataSource(dataSource);
        emf.setPackagesToScan(jpaProperties.getPackageToScan());
        emf.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
        emf.setJpaPropertyMap(jpaProperties.getProperties());

        return emf;
    }

    @Bean
    @ConditionalOnMissingBean
    public PlatformTransactionManager transactionManager(
            EntityManagerFactory emf) {

        JpaTransactionManager tm = new JpaTransactionManager();
        tm.setEntityManagerFactory(emf);
        return tm;
    }
}
```

---

### 2.2 Cách override auto-configuration

**Scenario 1: Bạn muốn dùng DataSource custom**

```java
@Configuration
public class CustomDataSourceConfig {

    @Bean
    @Primary  // Quan trọng: đánh dấu bean ưu tiên
    public DataSource customDataSource() {
        // Tạo DataSource theo cách riêng của bạn
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:postgresql://localhost:5432/customdb");
        ds.setMaximumPoolSize(20);
        ds.setIdleTimeout(30000);
        return ds;
    }
}
```

Vì có `@ConditionalOnMissingBean(DataSource.class)`, Spring Boot sẽ KHÔNG tạo DataSource mặc định nữa.

**Scenario 2: Disable auto-configuration**

```java
@SpringBootApplication(exclude = {
    DataSourceAutoConfiguration.class,
    SecurityAutoConfiguration.class
})
public class Application {
    // ...
}
```

Hoặc trong `application.yml`:
```yaml
spring:
  autoconfigure:
    exclude:
      - org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration
```

---

## 📚 BÀI 3: CUSTOM AUTO-CONFIGURATION (TẠO STARTER RIÊNG)

### 3.1 Khi nào cần tạo custom starter?

- Bạn có library dùng chung trong nhiều project
- Bạn muốn đóng gói auto-configuration cho team
- Bạn build product/seller cho người khác dùng

### 3.2 Structure của custom starter

```
my-custom-starter/
├── src/main/java/
│   └── com/example/
│       ├── MyServiceAutoConfiguration.java
│       ├── MyService.java
│       └── MyServiceProperties.java
├── src/main/resources/
│   └── META-INF/spring/
│       └── org.springframework.boot.autoconfigure.AutoConfiguration.imports
└── pom.xml
```

### 3.3 Các bước implement

**Step 1: Properties class** - Để bind từ application.yml

```java
@ConfigurationProperties(prefix = "my.service")
public class MyServiceProperties {

    private boolean enabled = true;
    private String apiUrl = "https://api.example.com";
    private int timeout = 5000;
    private String apiKey;

    // Getters and Setters
}
```

**Step 2: Service class** - Business logic

```java
public class MyService {

    private final MyServiceProperties properties;

    public MyService(MyServiceProperties properties) {
        this.properties = properties;
    }

    public String callApi(String endpoint) {
        if (!properties.isEnabled()) {
            throw new IllegalStateException("Service is disabled");
        }

        // Call API với properties
        String url = properties.getApiUrl() + endpoint;
        // ... HTTP call logic
        return result;
    }
}
```

**Step 3: Auto-Configuration class**

```java
@Configuration
@ConditionalOnClass(MyService.class)
@EnableConfigurationProperties(MyServiceProperties.class)
public class MyServiceAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(prefix = "my.service", name = "enabled", havingValue = "true", matchIfMissing = true)
    public MyService myService(MyServiceProperties properties) {
        return new MyService(properties);
    }
}
```

**Step 4: Register auto-configuration**

File: `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`

```
com.example.MyServiceAutoConfiguration
```

**Step 5: Sử dụng trong project khác**

```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>my-custom-starter</artifactId>
    <version>1.0.0</version>
</dependency>
```

```yaml
# application.yml
my:
  service:
    enabled: true
    api-url: https://api.mycompany.com
    timeout: 10000
    api-key: ${MY_API_KEY}
```

```java
@RestController
public class MyController {

    @Autowired
    private MyService myService;  // Tự động được inject!

    @GetMapping("/data")
    public String getData() {
        return myService.callApi("/endpoint");
    }
}
```

---

## 📚 BÀI 4: SPRING BOOT ACTUATOR

### 4.1 Actuator là gì?

Actuator cung cấp **production-ready endpoints** để monitor application:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### 4.2 Các endpoints quan trọng

| Endpoint | URL | Mô tả |
|----------|-----|-------|
| health | `/actuator/health` | App health status |
| info | `/actuator/info` | App information |
| metrics | `/actuator/metrics` | Metrics (CPU, memory, HTTP requests) |
| env | `/actuator/env` | Environment properties |
| loggers | `/actuator/loggers` | View/change log levels |
| httpexchanges | `/actuator/httpexchanges` | Last HTTP requests |

### 4.3 Cấu hình

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,env,loggers
  endpoint:
    health:
      show-details: always
  metrics:
    export:
      prometheus:
        enabled: true
```

### 4.4 Custom Health Indicator

```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    @Autowired
    private DataSource dataSource;

    @Override
    public Health health() {
        try {
            Connection conn = dataSource.getConnection();
            boolean valid = conn.isValid(1000);
            conn.close();

            if (valid) {
                return Health.up().withDetail("database", "connected").build();
            } else {
                return Health.down().withDetail("database", "connection invalid").build();
            }
        } catch (Exception e) {
            return Health.down(e).build();
        }
    }
}
```

---

## 📝 TÓM TẮT PHASE 1

Sau phase này, bạn cần nắm được:

1. ✅ Spring Boot giảm cấu hình nhờ **Convention over Configuration**
2. ✅ **Starter dependencies** bundle nhiều libraries vào 1
3. ✅ **Auto-configuration** scan classpath và tạo beans tự động
4. ✅ **Conditional annotations** quyết định khi nào bean được tạo
5. ✅ Có thể **override** auto-configuration bằng `@Primary` hoặc `exclude`
6. ✅ Có thể **tạo custom starter** cho team/product
7. ✅ **Actuator** cung cấp endpoints để monitor production

---

## 🔜 TIẾP THEO

Đọc file `02-examples.md` để xem code mẫu thực tế cho từng concept.
