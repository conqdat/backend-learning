# Phase 07: Testing - Lý Thuyết

> **Thời gian:** 2 tuần
> **Mục tiêu:** Master testing strategies cho production-ready code

---

## 📚 BÀI 1: TESTING PYRAMID

### 1.1 Testing Pyramid

```
                    ┌─────────────┐
                   /│             │\
                  / │   E2E (10%)  │\
                 /  │             │  \
                /─────────────────\
               /│                 │\
              / │ Integration (20%) │\
             /  │                 │  \
            /───────────────────────\
           /│                       │\
          / │    Unit (70%)         │ \
         /  │                       │  \
        /─────────────────────────────\
```

**Unit Tests (70%):**
- Test individual classes/methods
- Fast execution (< 10ms per test)
- No external dependencies (mock everything)
- Example: Test Service layer với mocked Repository

**Integration Tests (20%):**
- Test interaction between components
- Medium speed (< 1s per test)
- Real database, real external services
- Example: Test Repository với test database

**E2E Tests (10%):**
- Test complete user flows
- Slow execution (seconds per test)
- Full system, production-like environment
- Example: Test API endpoint từ đầu đến cuối

---

### 1.2 Test Categories trong Spring Boot

```java
// 1. Unit Test (không cần Spring context)
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository repository;

    @InjectMocks
    private UserService service;

    @Test
    void shouldReturnUser() {
        // Arrange
        User mockUser = new User("John");
        when(repository.findById(1L)).thenReturn(Optional.of(mockUser));

        // Act
        User result = service.findById(1L);

        // Assert
        assertEquals("John", result.getName());
    }
}

// 2. Integration Test (với Spring context)
@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.ANY)
class UserRepositoryIntegrationTest {

    @Autowired
    private UserRepository repository;

    @Test
    void shouldSaveAndFindUser() {
        // Arrange
        User user = new User("John", "john@example.com");

        // Act
        User saved = repository.save(user);
        User found = repository.findById(saved.getId()).get();

        // Assert
        assertEquals("John", found.getName());
    }
}

// 3. Slice Test (chỉ load web layer)
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService service;

    @Test
    void shouldReturnUser() throws Exception {
        // Arrange
        when(service.findById(1L)).thenReturn(new UserDTO("John"));

        // Act & Assert
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }
}

// 4. E2E Test (full application)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserE2ETest {

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldCreateAndGetUser() {
        // Arrange
        CreateUserRequest request = new CreateUserRequest("John", "john@example.com");

        // Act
        ResponseEntity<UserDTO> response = restTemplate.postForEntity(
            "http://localhost:" + port + "/api/users",
            request,
            UserDTO.class
        );

        // Assert
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertEquals("John", response.getBody().getName());
    }
}
```

---

## 📚 BÀI 2: JUNIT 5 & MOCKITO

### 2.1 JUnit 5 Annotations

```java
@ExtendWith(MockitoExtension.class)
class JUnit5Tests {

    @BeforeAll
    static void beforeAll() {
        // Chạy 1 lần trước tất cả tests
    }

    @AfterAll
    static void afterAll() {
        // Chạy 1 lần sau tất cả tests
    }

    @BeforeEach
    void beforeEach() {
        // Chạy trước mỗi test method
    }

    @AfterEach
    void afterEach() {
        // Chạy sau mỗi test method
    }

    @Test
    @DisplayName("Should return user when id exists")
    @Disabled("Not implemented yet")
    void testExample() {
        // Test code
    }

    @Test
    @RepeatedTest(5)
    void repeatedTest() {
        // Chạy 5 lần
    }

    @ParameterizedTest
    @ValueSource(ints = {1, 2, 3, 4, 5})
    void parameterizedTest(int value) {
        // Chạy với nhiều giá trị
        assertTrue(value > 0);
    }

    @ParameterizedTest
    @CsvSource({
        "John, 25, true",
        "Jane, 30, false",
        "Bob, 17, false"
    })
    void csvParameterizedTest(String name, int age, boolean isAdult) {
        // Test với nhiều combinations
    }
}
```

---

### 2.2 Mockito Best Practices

```java
@ExtendWith(MockitoExtension.class)
class MockitoTests {

    @Mock
    private UserRepository repository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private UserService service;

    @Test
    void shouldSaveUserAndSendEmail() {
        // Arrange - Stubbing
        User savedUser = new User(1L, "John", "john@example.com");
        when(repository.save(any(User.class))).thenReturn(savedUser);
        doNothing().when(emailService).sendWelcomeEmail(anyString());

        // Act
        User result = service.register("John", "john@example.com");

        // Assert - Verification
        assertEquals("John", result.getName());
        verify(repository).save(any(User.class));
        verify(emailService).sendWelcomeEmail("john@example.com");
    }

    @Test
    void shouldThrowExceptionWhenUserNotFound() {
        // Arrange
        when(repository.findById(1L)).thenReturn(Optional.empty());

        // Act & Assert
        assertThrows(UserNotFoundException.class, () -> {
            service.findById(1L);
        });
    }

    @Test
    void shouldUseArgumentCaptor() {
        // ArgumentCaptor để verify arguments
        ArgumentCaptor<User> userCaptor = ArgumentCaptor.forClass(User.class);

        service.register("John", "john@example.com");

        verify(repository).save(userCaptor.capture());
        User captured = userCaptor.getValue();
        assertEquals("John", captured.getName());
    }

    @Test
    void shouldUseTimeout() {
        // Timeout cho mock
        when(repository.save(any(User.class)))
            .thenAnswer(invocation -> {
                Thread.sleep(100);
                return invocation.getArgument(0);
            });
    }
}
```

---

## 📚 BÀI 3: TESTCONTAINERS

### 3.1 Testcontainers là gì?

**Vấn đề:** Integration tests cần database thật, nhưng:
- Không thể dùng production DB
- Setup test DB phức tạp
- Data không clean sau mỗi test

**Giải pháp:** Testcontainers = Docker containers cho tests

---

### 3.2 Testcontainers với PostgreSQL

```java
@SpringBootTest
@Testcontainers
class UserRepositoryTest {

    // PostgreSQL container
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
        registry.add("spring.datasource.driver-class-name", postgres::getDriverClassName);
    }

    @Autowired
    private UserRepository repository;

    @Test
    void shouldSaveAndFindUser() {
        // Arrange
        User user = new User("John", "john@example.com");

        // Act
        User saved = repository.save(user);
        User found = repository.findById(saved.getId()).get();

        // Assert
        assertEquals("John", found.getName());
        assertEquals("john@example.com", found.getEmail());
    }

    @Test
    @Transactional
    void shouldDeleteUser() {
        // Arrange
        User user = new User("John", "john@example.com");
        repository.save(user);

        // Act
        repository.delete(user);

        // Assert
        assertThat(repository.findAll()).isEmpty();
    }
}
```

---

### 3.3 Testcontainers với Redis

```java
@SpringBootTest
@Testcontainers
class RedisCacheTest {

    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine")
        .withExposedPorts(6379);

    @DynamicPropertySource
    static void setProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.redis.host", redis::getHost);
        registry.add("spring.data.redis.port", () -> redis.getMappedPort(6379));
    }

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Test
    void shouldCacheAndRetrieve() {
        // Arrange
        String key = "user:1";
        User user = new User("John", "john@example.com");

        // Act
        redisTemplate.opsForValue().set(key, user);
        User cached = (User) redisTemplate.opsForValue().get(key);

        // Assert
        assertEquals("John", cached.getName());
    }
}
```

---

### 3.4 Testcontainers với Kafka

```java
@SpringBootTest
@Testcontainers
class KafkaProducerTest {

    @Container
    static KafkaContainer kafka = new KafkaContainer(
        DockerImageName.parse("confluentinc/cp-kafka:7.4.0")
    );

    @DynamicPropertySource
    static void setProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Test
    void shouldSendMessage() throws Exception {
        // Arrange
        String topic = "test-topic";
        String message = "Hello Kafka";

        // Act
        kafkaTemplate.send(topic, message).get();  // get() để wait completion

        // Assert - Verify message was sent
        // (Cần consumer để verify, hoặc dùng Kafka admin)
    }
}
```

---

## 📚 BÀI 4: CONTRACT TESTING

### 4.1 Consumer-Driven Contracts

**Vấn đề:** Service A gọi Service B, làm sao biết API contract không bị break?

**Giải pháp:** Spring Cloud Contract

```groovy
// Contract definition (Groovy)
Contract.make {
    description("should return user when id exists")

    request {
        method 'GET'
        url '/api/users/1'
    }

    response {
        status 200
        headers {
            contentType 'application/json'
        }
        body("""
        {
            "id": 1,
            "name": "John",
            "email": "john@example.com"
        }
        """)
    }
}
```

```java
// Generated test từ contract
@SpringBootTest
class UserServiceContractTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void shouldReturnUser() throws Exception {
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.name").value("John"))
            .andExpect(jsonPath("$.email").value("john@example.com"));
    }
}
```

---

## 📚 BÀI 5: TEST BEST PRACTICES

### 5.1 AAA Pattern (Arrange-Act-Assert)

```java
// ❌ BAD: Không rõ ràng
@Test
void testUser() {
    User user = new User("John");  // Arrange?
    repository.save(user);          // Act?
    assertEquals("John", user.getName());  // Assert?
}

// ✅ GOOD: Clear AAA pattern
@Test
void shouldSaveUserWithCorrectName() {
    // Arrange
    User user = new User("John", "john@example.com");

    // Act
    User saved = repository.save(user);

    // Assert
    assertEquals("John", saved.getName());
    assertEquals("john@example.com", saved.getEmail());
    assertNotNull(saved.getId());
}
```

---

### 5.2 Test Naming Convention

```java
// ❌ BAD: Không rõ intent
@Test
void test1() {}

@Test
void testUser() {}

// ✅ GOOD: Should + action + expected result
@Test
void shouldReturnUserWhenIdExists() {}

@Test
void shouldThrowExceptionWhenUserNotFound() {}

@Test
void shouldSendEmailAfterUserRegistration() {}

// Alternative: Given-When-Then
@Test
void givenUserExists_whenGetById_thenReturnUser() {}
```

---

### 5.3 Test Data Factory Pattern

```java
// ❌ BAD: Hardcoded test data
@Test
void shouldCreateUser() {
    User user = new User("John", "john@example.com", 30);
    // ...
}

@Test
void shouldUpdateUser() {
    User user = new User("Jane", "jane@example.com", 25);
    // ...
}

// ✅ GOOD: Factory pattern
class UserFactory {
    static User createUser() {
        return new User("John", "john@example.com", 30);
    }

    static User createUser(String name) {
        return new User(name, name.toLowerCase() + "@example.com", 30);
    }

    static User createUser(Long id) {
        User user = createUser();
        ReflectionTestUtils.setField(user, "id", id);
        return user;
    }
}

// Usage
@Test
void shouldCreateUser() {
    User user = UserFactory.createUser();
    // ...
}
```

---

## 📝 TÓM TẮT PHASE 07

1. ✅ Testing Pyramid: Unit (70%), Integration (20%), E2E (10%)
2. ✅ JUnit 5 annotations và assertions
3. ✅ Mockito mocking và verification
4. ✅ Testcontainers cho integration tests
5. ✅ Contract testing với Spring Cloud Contract
6. ✅ Test best practices (AAA, naming, factory)

---

## 🔜 TIẾP THEO

Đọc `02-examples.md` để xem code mẫu thực tế!
