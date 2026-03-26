# Phase 07: Testing - Ví Dụ Thực Tế

---

## 📁 BÀI 1: UNIT TEST VỚI MOCKITO

### Ví dụ 1.1: Service Layer Test

```java
// Service class
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository repository;
    private final EmailService emailService;
    private final PasswordEncoder passwordEncoder;

    public User register(String email, String password, String name) {
        // Validate email not exists
        if (repository.existsByEmail(email)) {
            throw new EmailAlreadyExistsException(email);
        }

        // Create user
        User user = new User();
        user.setEmail(email);
        user.setName(name);
        user.setPasswordHash(passwordEncoder.encode(password));
        user.setRole(Role.USER);

        User saved = repository.save(user);

        // Send welcome email
        emailService.sendWelcomeEmail(user.getEmail());

        return saved;
    }

    public User findById(Long id) {
        return repository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }

    public List<User> findAll() {
        return repository.findAll();
    }
}

// Unit Test
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository repository;

    @Mock
    private EmailService emailService;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService service;

    @Test
    void shouldRegisterUserSuccessfully() {
        // Arrange
        String email = "john@example.com";
        String password = "secret123";
        String name = "John Doe";

        User savedUser = new User(1L, email, name, Role.USER);

        when(repository.existsByEmail(email)).thenReturn(false);
        when(passwordEncoder.encode(password)).thenReturn("encoded_hash");
        when(repository.save(any(User.class))).thenReturn(savedUser);
        doNothing().when(emailService).sendWelcomeEmail(email);

        // Act
        User result = service.register(email, password, name);

        // Assert
        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals(email, result.getEmail());
        assertEquals(name, result.getName());

        // Verify interactions
        verify(repository).existsByEmail(email);
        verify(passwordEncoder).encode(password);
        verify(repository).save(any(User.class));
        verify(emailService).sendWelcomeEmail(email);
    }

    @Test
    void shouldThrowExceptionWhenEmailExists() {
        // Arrange
        String email = "existing@example.com";

        when(repository.existsByEmail(email)).thenReturn(true);

        // Act & Assert
        assertThrows(EmailAlreadyExistsException.class, () -> {
            service.register(email, "password", "Name");
        });

        // Verify save was NOT called
        verify(repository, never()).save(any(User.class));
        verify(emailService, never()).sendWelcomeEmail(anyString());
    }

    @Test
    void shouldReturnUserWhenFound() {
        // Arrange
        Long userId = 1L;
        User user = new User(userId, "John", "john@example.com", Role.USER);

        when(repository.findById(userId)).thenReturn(Optional.of(user));

        // Act
        User result = service.findById(userId);

        // Assert
        assertEquals(userId, result.getId());
        assertEquals("John", result.getName());

        verify(repository).findById(userId);
    }

    @Test
    void shouldThrowExceptionWhenUserNotFound() {
        // Arrange
        Long userId = 999L;
        when(repository.findById(userId)).thenReturn(Optional.empty());

        // Act & Assert
        assertThrows(UserNotFoundException.class, () -> {
            service.findById(userId);
        });
    }

    @Test
    void shouldReturnAllUsers() {
        // Arrange
        List<User> users = Arrays.asList(
            new User(1L, "John", "john@example.com", Role.USER),
            new User(2L, "Jane", "jane@example.com", Role.USER)
        );

        when(repository.findAll()).thenReturn(users);

        // Act
        List<User> result = service.findAll();

        // Assert
        assertEquals(2, result.size());
        verify(repository).findAll();
    }
}
```

---

### Ví dụ 1.2: ArgumentCaptor & InOrder

```java
@ExtendWith(MockitoExtension.class)
class AdvancedMockitoTest {

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderService orderService;

    @Test
    void shouldCaptureAndVerifyOrderDetails() {
        // Arrange
        ArgumentCaptor<Order> orderCaptor = ArgumentCaptor.forClass(Order.class);

        // Act
        orderService.createOrder(1L, Arrays.asList("item1", "item2"));

        // Assert
        verify(orderRepository).save(orderCaptor.capture());

        Order captured = orderCaptor.getValue();
        assertEquals(2, captured.getItems().size());
        assertEquals("item1", captured.getItems().get(0));
    }

    @Test
    void shouldVerifyCallOrder() {
        // Arrange
        InOrder inOrder = Mockito.inOrder(orderRepository);

        // Act
        orderService.processOrder(1L);

        // Assert - Verify call sequence
        inOrder.verify(orderRepository).findById(1L);
        inOrder.verify(orderRepository).save(any(Order.class));
        inOrder.verify(orderRepository).updateStatus(anyLong(), anyString());
    }

    @Test
    void shouldVerifyNeverInteractions() {
        // Act
        orderService.cancelOrder(1L);

        // Assert
        verify(orderRepository, never()).save(any(Order.class));
        verify(orderRepository).updateStatus(1L, "CANCELLED");
    }

    @Test
    void shouldVerifyAtLeastOnce() {
        // Act
        orderService.bulkUpdate(Arrays.asList(1L, 2L, 3L));

        // Assert
        verify(orderRepository, atLeastOnce()).findById(anyLong());
        verify(orderRepository, times(3)).save(any(Order.class));
    }
}
```

---

## 📁 BÀI 2: INTEGRATION TEST VỚI TESTCONTAINERS

### Ví dụ 2.1: Full Stack Integration Test

```java
@SpringBootTest
@Testcontainers
@AutoConfigureMockMvc
class UserIntegrationTest {

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
    private UserRepository repository;

    @BeforeEach
    void setUp() {
        repository.deleteAll();
    }

    @Test
    void shouldCreateUserViaApi() throws Exception {
        // Arrange
        String requestJson = """
            {
                "email": "john@example.com",
                "password": "secret123",
                "name": "John Doe"
            }
            """;

        // Act & Assert
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(requestJson))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").exists())
            .andExpect(jsonPath("$.email").value("john@example.com"))
            .andExpect(jsonPath("$.name").value("John Doe"));

        // Verify database
        List<User> users = repository.findAll();
        assertEquals(1, users.size());
        assertEquals("john@example.com", users.get(0).getEmail());
    }

    @Test
    void shouldGetUserById() throws Exception {
        // Arrange
        User user = new User("John", "john@example.com", "secret");
        repository.save(user);

        // Act & Assert
        mockMvc.perform(get("/api/users/" + user.getId()))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }

    @Test
    void shouldReturn404WhenUserNotFound() throws Exception {
        // Act & Assert
        mockMvc.perform(get("/api/users/999"))
            .andExpect(status().isNotFound());
    }
}
```

---

### Ví dụ 2.2: Repository Layer Test

```java
@DataJpaTest
@Testcontainers
class UserRepositoryTest {

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
    private UserRepository repository;

    @Autowired
    private TestEntityManager entityManager;

    @Test
    void shouldSaveAndFindUser() {
        // Arrange
        User user = new User("John", "john@example.com", "secret");

        // Act
        User saved = repository.save(user);
        entityManager.flush();
        entityManager.clear();

        Optional<User> found = repository.findById(saved.getId());

        // Assert
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("John");
        assertThat(found.get().getEmail()).isEqualTo("john@example.com");
    }

    @Test
    void shouldFindUserByEmail() {
        // Arrange
        User user = new User("John", "john@example.com", "secret");
        repository.save(user);

        // Act
        Optional<User> found = repository.findByEmail("john@example.com");

        // Assert
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("John");
    }

    @Test
    void shouldReturnEmptyWhenEmailNotFound() {
        // Act
        Optional<User> found = repository.findByEmail("notfound@example.com");

        // Assert
        assertThat(found).isEmpty();
    }

    @Test
    void shouldCheckEmailExists() {
        // Arrange
        User user = new User("John", "john@example.com", "secret");
        repository.save(user);

        // Act & Assert
        assertThat(repository.existsByEmail("john@example.com")).isTrue();
        assertThat(repository.existsByEmail("other@example.com")).isFalse();
    }
}
```

---

## 📁 BÀI 3: PARAMETERIZED TESTS

### Ví dụ 3.1: Multiple Test Cases

```java
@ExtendWith(MockitoExtension.class)
class ParameterizedTestExample {

    @Mock
    private UserRepository repository;

    @InjectMocks
    private UserService service;

    // Test với nhiều giá trị
    @ParameterizedTest
    @ValueSource(strings = {"john@example.com", "jane@example.com", "bob@example.com"})
    void shouldCreateUserWithValidEmail(String email) {
        // Arrange
        when(repository.existsByEmail(email)).thenReturn(false);
        when(repository.save(any(User.class))).thenReturn(new User(1L, email, "Name", Role.USER));

        // Act
        User result = service.register(email, "password", "Name");

        // Assert
        assertNotNull(result);
        assertEquals(email, result.getEmail());
    }

    // Test với nhiều combinations
    @ParameterizedTest
    @CsvSource({
        "john@example.com, John, true",
        "jane@example.com, Jane, true",
        "invalid-email, Bob, false",
        ", Alice, false"
    })
    void shouldValidateUserInput(String email, String name, boolean isValid) {
        // Arrange
        if (isValid) {
            when(repository.existsByEmail(email)).thenReturn(false);
            when(repository.save(any(User.class))).thenReturn(new User(1L, email, name, Role.USER));
        }

        // Act & Assert
        if (isValid) {
            User result = service.register(email, "password", name);
            assertNotNull(result);
        } else {
            assertThrows(InvalidUserException.class, () -> {
                service.register(email, "password", name);
            });
        }
    }

    // Test với arguments từ method
    @ParameterizedTest
    @MethodSource("provideUsers")
    void shouldProcessMultipleUsers(String email, String name, int expectedId) {
        // Arrange
        when(repository.save(any(User.class))).thenReturn(new User((long) expectedId, email, name, Role.USER));

        // Act
        User result = service.register(email, "password", name);

        // Assert
        assertEquals(expectedId, result.getId());
    }

    private static Stream<Arguments> provideUsers() {
        return Stream.of(
            Arguments.of("john@example.com", "John", 1),
            Arguments.of("jane@example.com", "Jane", 2),
            Arguments.of("bob@example.com", "Bob", 3)
        );
    }
}
```

---

## 📝 BÀI TẬP THỰC HÀNH

Xem `03-exercises.md` để làm bài tập!
