# Phase 1: Spring Boot Core - Bài Tập Thực Hành

> **Thời gian:** 4-6 giờ
> **Đầu ra:** Code submit lên GitHub hoặc gửi file cho mentor review

---

## 📝 BÀI TẬP 1: PHÂN TÍCH DEPENDENCIES (30 phút)

### Đề bài

Vào project Spring Boot bạn đang làm việc (hoặc clone project mẫu), thực hiện:

1. Chạy lệnh:
   ```bash
   mvn dependency:tree > deps.txt
   ```

2. Trả lời các câu hỏi:

   **a)** Project có bao nhiêu `spring-boot-starter-*` dependencies?
   ```
   Gợi ý: grep "spring-boot-starter" deps.txt
   ```

   **b)** `spring-boot-starter-web` kéo theo những dependencies gì quan trọng?
   ```
   - Tomcat version: ?
   - Jackson version: ?
   - Spring Web version: ?
   ```

   **c)** Có dependency nào bị conflict version không?
   ```
   Gợi ý: Tìm các dòng có "omitted for conflict with"
   ```

   **d)** Nếu muốn upgrade Jackson lên 2.16.0, làm thế nào?

### Cách submit

```markdown
## Kết quả phân tích dependencies

### a) Số lượng starters
- spring-boot-starter-web
- spring-boot-starter-data-jpa
- ... (liệt kê)

### b) Dependencies quan trọng từ spring-boot-starter-web
- Tomcat: 10.1.16
- Jackson: 2.15.3
- Spring Web: 6.1.1

### c) Version conflicts
- Found conflict: jackson-databind 2.15.3 vs 2.14.0
- Resolution: ...

### d) Upgrade Jackson
Thêm vào pom.xml:
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.16.0</version>
</dependency>
```

---

## 📝 BÀI TẬP 2: DEBUG AUTO-CONFIGURATION (45 phút)

### Đề bài

1. Tạo project mới từ https://start.spring.io với dependencies:
   - Spring Web
   - Spring Data JPA
   - PostgreSQL Driver
   - Spring Boot Actuator

2. Cấu hình để xem auto-configuration report:

   ```yaml
   # application.yml
   debug: true

   management:
     endpoints:
       web:
         exposure:
           include: "*"
   ```

3. Chạy application và tìm log:
   ```
   CONDITIONS EVALUATION REPORT
   ```

4. Chọn 3 auto-configuration classes và phân tích:

   | Class | Positive/Negative | Reason |
   |-------|------------------|--------|
   | `DataSourceAutoConfiguration` | Positive | found required class 'javax.sql.DataSource' |
   | `HibernateJpaAutoConfiguration` | ? | ? |
   | `RedisAutoConfiguration` | ? | ? |

5. Thử disable `SecurityAutoConfiguration` và restart app

### Cách submit

```markdown
## Kết quả debug auto-configuration

### 3 auto-configuration classes phân tích

#### 1. DataSourceAutoConfiguration
- Status: ✅ Positive (matched)
- Reason: found required class 'javax.sql.DataSource'
- Conditions:
  - OnClassCondition: matched
  - OnPropertyCondition: matched (spring.datasource.url exists)

#### 2. HibernateJpaAutoConfiguration
- Status: ...

#### 3. RedisAutoConfiguration
- Status: ...

### Thử disable SecurityAutoConfiguration

Cách làm:
@SpringBootApplication(exclude = {SecurityAutoConfiguration.class})

Hoặc trong application.yml:
spring:
  autoconfigure:
    exclude: org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration

Kết quả: ...
```

---

## 📝 BÀI TẬP 3: TẠO CUSTOM STARTER - GREETING SERVICE (2 giờ)

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

8. Thêm test unit cho `GreetingService`

### Hướng dẫn từng bước

#### Step 1: Tạo project

```bash
mkdir greeting-starter
cd greeting-starter
mvn archetype:generate -DgroupId=com.example -DartifactId=greeting-starter -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

#### Step 2: Sửa pom.xml

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

        <!-- Spring Boot Configuration Processor (cho autocomplete) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-configuration-processor</artifactId>
            <version>3.2.0</version>
            <optional>true</optional>
        </dependency>

        <!-- Spring Boot Starter Web (provided - user sẽ add) -->
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

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

#### Step 3: Tạo GreetingProperties.java

```java
package com.example.greeting;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "greeting")
public class GreetingProperties {

    /**
     * Enable/disable greeting service
     */
    private boolean enabled = true;

    /**
     * Greeting message template
     */
    private String message = "Hello";

    /**
     * Suffix to append after name
     */
    private String suffix = "!";

    // Getters and Setters
    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getSuffix() {
        return suffix;
    }

    public void setSuffix(String suffix) {
        this.suffix = suffix;
    }
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

    /**
     * Create greeting message for given name
     *
     * @param name person name
     * @return greeting message like "Hello John!"
     * @throws IllegalStateException if service is disabled
     */
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
    @ConditionalOnProperty(prefix = "greeting", name = "enabled", havingValue = "true", matchIfMissing = true)
    public GreetingService greetingService(GreetingProperties properties) {
        return new GreetingService(properties);
    }
}
```

#### Step 6: Tạo file register auto-configuration

Tạo file: `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`

Nội dung:
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
# Tạo project Spring Boot mới từ start.spring.io
```

Thêm dependency vào pom.xml:
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>greeting-starter</artifactId>
    <version>1.0.0</version>
</dependency>
```

Cấu hình trong application.yml:
```yaml
greeting:
  enabled: true
  message: "Xin chào"
  suffix: "!"
```

Tạo controller test:
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
- [ ] GreetingController với endpoint /greet/{name}
- [ ] GreetingHealthIndicator
- [ ] Unit tests

### Khó khăn gặp phải
- Vấn đề 1: ...
- Cách giải quyết: ...

### Bài học rút ra
- ...
```

---

## 📝 BÀI TẬP 4: ACTUATOR HEALTH CUSTOM (1 giờ)

### Đề bài

1. Thêm Actuator vào project hiện tại:
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-actuator</artifactId>
   </dependency>
   ```

2. Cấu hình expose endpoints:
   ```yaml
   management:
     endpoints:
       web:
         exposure:
           include: health,info,metrics
     endpoint:
       health:
         show-details: always
   ```

3. Tạo custom Health Indicator cho service bạn đang dùng (Database, Redis, hoặc External API):

   ```java
   @Component
   public class CustomHealthIndicator implements HealthIndicator {
       @Override
       public Health health() {
           // Implement health check logic
       }
   }
   ```

4. Test endpoint `/actuator/health`

### Cách submit

```markdown
## Kết quả bài tập Actuator

### Custom Health Indicator

Tôi tạo health check cho: [Redis/Database/External API]

Code:
```java
@Component
public class MyServiceHealthIndicator implements HealthIndicator {
    // Code của bạn
}
```

### Test result

```bash
curl http://localhost:8080/actuator/health
```

Output:
```json
{
    "status": "UP",
    "components": {
        "myService": {
            "status": "UP",
            "details": {
                // Chi tiết
            }
        }
    }
}
```

### Bài học rút ra
- ...
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
- [ ] Biết cấu hình và sử dụng Actuator endpoints

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

   Những gì đã làm:
   - Exercise 1: ✅
   - Exercise 2: ✅
   - Exercise 3: ✅
   - Exercise 4: ✅

   Khó khăn gặp phải: ...
   ```

3. **Hoặc gửi file trực tiếp** nếu không muốn public code

---

## 🔜 SAU KHI HOÀN THÀNH

Khi submit xong, tôi sẽ:
1. Review code chi tiết
2. Góp ý về coding style, best practices
3. Giải đáp các câu hỏi
4. Unlock Phase 2: Database & Hibernate

**Good luck! 🚀**
