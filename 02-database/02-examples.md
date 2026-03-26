# Phase 2: Database & Hibernate - Ví Dụ Thực Tế

---

## 📁 BÀI 1: ENTITY LIFECYCLE DEMO

### Ví dụ 1.1: Demo 4 trạng thái của Entity

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private String email;

    @Version  // Optimistic locking
    private Integer version;

    // Constructors, Getters, Setters
}
```

```java
@Service
@Transactional
public class UserLifecycleDemo {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EntityManager entityManager;

    public void demonstrateLifecycle() {
        System.out.println("=== ENTITY LIFECYCLE DEMO ===\n");

        // 1. NEW (TRANSIENT) STATE
        System.out.println("1. NEW STATE");
        User newUser = new User();
        newUser.setName("John Doe");
        newUser.setEmail("john@example.com");
        // newUser chưa được persist, ở trạng thái NEW
        System.out.println("   - Created new User: " + newUser.getName());
        System.out.println("   - ID: " + newUser.getId());  // null
        System.out.println("   - State: NEW/TRANSIENT\n");

        // 2. MANAGED STATE
        System.out.println("2. MANAGED STATE");
        userRepository.save(newUser);
        // newUser bây giờ được EntityManager quản lý
        System.out.println("   - After save(): ID = " + newUser.getId());
        System.out.println("   - State: MANAGED\n");

        // 3. AUTO-DIRTY CHECKING
        System.out.println("3. AUTO-DIRTY CHECKING");
        newUser.setName("Jane Doe");
        // Không cần gọi update()!
        System.out.println("   - Changed name to: " + newUser.getName());
        System.out.println("   - No update() call needed!\n");

        // 4. DETACHED STATE
        System.out.println("4. DETACHED STATE");
        // Transaction kết thúc ở cuối method
        // newUser trở thành DETACHED
        System.out.println("   - After transaction ends: State = DETACHED\n");

        // 5. MERGE DETACHED ENTITY
        System.out.println("5. MERGE STATE");
        User detachedUser = userRepository.findById(newUser.getId()).get();
        entityManager.detach(detachedUser);
        System.out.println("   - After detach(): State = DETACHED");

        detachedUser.setName("Bob Smith");

        User mergedUser = entityManager.merge(detachedUser);
        System.out.println("   - After merge(): State = MANAGED");
        System.out.println("   - Updated name: " + mergedUser.getName());
    }

    public void demonstrateRemove() {
        // 6. REMOVED STATE
        User user = userRepository.findById(1L).get();
        System.out.println("Before remove: State = MANAGED");

        userRepository.delete(user);
        System.out.println("After delete(): State = REMOVED");
        // user vẫn có thể access nhưng không thể persist lại
    }
}
```

---

## 📁 BÀI 2: RELATIONSHIPS - BEST PRACTICES

### Ví dụ 2.1: @OneToMany / @ManyToOne đúng cách

**Sai lầm phổ biến:**
```java
// ❌ SAI: Không có helper methods, orphanRemoval = false
@Entity
public class User {
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<Post> posts;
}

// Khi muốn xóa post:
user.getPosts().remove(post);
// ❌ Post vẫn tồn tại trong DB! orphanRemoval = false
```

**Đúng:**
```java
// ✅ ĐÚNG
@Entity
public class User {
    @OneToMany(
        mappedBy = "user",
        cascade = CascadeType.ALL,
        orphanRemoval = true
    )
    private List<Post> posts = new ArrayList<>();

    // Helper methods - QUAN TRỌNG!
    public void addPost(Post post) {
        posts.add(post);
        post.setUser(this);
    }

    public void removePost(Post post) {
        posts.remove(post);
        post.setUser(null);
        // orphanRemoval = true sẽ tự DELETE post khỏi DB
    }
}

@Entity
public class Post {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
}
```

**Sử dụng:**
```java
@Service
public class PostService {

    @Autowired
    private UserRepository userRepository;

    @Transactional
    public void addPostToUser(Long userId, Post post) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));

        user.addPost(post);  // Dùng helper method
        // Không cần gọi userRepository.save(user)!
        // Hibernate tự detect changes và persist
    }

    @Transactional
    public void removePost(Post post) {
        User user = post.getUser();
        if (user != null) {
            user.removePost(post);  // orphanRemoval sẽ DELETE
        }
    }
}
```

---

### Ví dụ 2.2: @OneToOne với cascade

```java
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @OneToOne(
        mappedBy = "user",
        cascade = CascadeType.ALL,
        orphanRemoval = true,
        fetch = FetchType.LAZY
    )
    @Cascade(org.hibernate.annotations.CascadeType.ALL)
    private UserProfile profile;

    public void setProfile(UserProfile profile) {
        if (this.profile != null) {
            this.profile.setUser(null);
        }
        this.profile = profile;
        if (profile != null) {
            profile.setUser(this);
        }
    }
}

@Entity
public class UserProfile {
    @Id
    @GeneratedValue
    private Long id;

    private String bio;

    private String avatarUrl;

    @OneToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", unique = true, nullable = false)
    private User user;
}
```

---

### Ví dụ 2.3: @ManyToMany với extra columns

**Vấn đề:** Bảng trung gian cần thêm columns (created_at, created_by)

**Giải pháp:** Tạo entity cho bảng trung gian

```java
// ❌ KHÔNG THỂ thêm columns vào @ManyToMany thuần
@ManyToMany
@JoinTable(
    name = "user_courses",
    // Không thể thêm created_at ở đây!
)
```

**Đúng:**
```java
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<UserCourse> userCourses = new ArrayList<>();

    // Convenience method
    public void enrollInCourse(Course course) {
        UserCourse uc = new UserCourse(this, course);
        userCourses.add(uc);
    }
}

@Entity
public class Course {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @OneToMany(mappedBy = "course", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<UserCourse> userCourses = new ArrayList<>();

    public int getEnrolledCount() {
        return userCourses.size();
    }
}

// Entity trung gian
@Entity
@Table(name = "user_courses")
public class UserCourse {
    @Id
    @GeneratedValue
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "course_id", nullable = false)
    private Course course;

    @Column(name = "enrolled_at")
    private LocalDateTime enrolledAt;

    @Column(name = "completed")
    private boolean completed;

    @Column(name = "completed_at")
    private LocalDateTime completedAt;

    // Constructors
    public UserCourse() {}

    public UserCourse(User user, Course course) {
        this.user = user;
        this.course = course;
        this.enrolledAt = LocalDateTime.now();
        this.completed = false;
    }

    // Getters, Setters
}
```

---

## 📁 BÀI 3: FETCH TYPES - THỰC TẾ

### Ví dụ 3.1: LazyInitializationException và cách fix

**Scenario:** API trả về User với posts

```java
// ❌ SAI: Gặp LazyInitializationException
@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        return user;  // OK
    }

    @GetMapping("/{id}/with-posts")
    public User getUserWithPosts(@PathVariable Long id) {
        User user = userService.findById(id);
        // Access posts outside transaction!
        return user;  // ❌ Khi serialize JSON, getPosts() bị call → Exception!
    }
}

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Transactional(readOnly = true)
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
    }
}
```

**Error:**
```
org.hibernate.LazyInitializationException:
could not initialize proxy - no Session
```

---

**Fix 1: JOIN FETCH trong repository**

```java
public interface UserRepository extends JpaRepository<User, Long> {

    @Query("SELECT DISTINCT u FROM User u JOIN FETCH u.posts WHERE u.id = :id")
    Optional<User> findByIdWithPosts(@Param("id") Long id);

    @Query("SELECT DISTINCT u FROM User u JOIN FETCH u.posts WHERE u.email = :email")
    Optional<User> findByEmailWithPosts(@Param("email") String email);
}

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public User findByIdWithPosts(Long id) {
        return userRepository.findByIdWithPosts(id)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
    }
}
```

---

**Fix 2: @Transactional ở controller layer (không khuyến khích)**

```java
@RestController
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/{id}/with-posts")
    @Transactional(readOnly = true)  // Giữ transaction mở
    public User getUserWithPosts(@PathVariable Long id) {
        User user = userService.findById(id);
        Hibernate.initialize(user.getPosts());  // Force load
        return user;
    }
}
```

---

**Fix 3: DTO projection (BEST PRACTICE)**

```java
// DTO interface
public interface UserWithPostsDTO {
    Long getId();
    String getName();
    String getEmail();
    List<PostDTO> getPosts();

    interface PostDTO {
        Long getId();
        String getTitle();
        String getContent();
        LocalDateTime getCreatedAt();
    }
}

// Repository
public interface UserRepository extends JpaRepository<User, Long> {

    @Query("""
        SELECT u.id as id,
               u.name as name,
               u.email as email,
               p.id as posts.id,
               p.title as posts.title,
               p.content as posts.content,
               p.createdAt as posts.createdAt
        FROM User u
        LEFT JOIN u.posts p
        WHERE u.id = :id
        """)
    Optional<UserWithPostsDTO> findDTOById(@Param("id") Long id);
}

// Service
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public UserWithPostsDTO findDTOById(Long id) {
        return userRepository.findDTOById(id)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
    }
}

// Controller
@RestController
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/{id}")
    public UserWithPostsDTO getUser(@PathVariable Long id) {
        return userService.findDTOById(id);
    }
}
```

**Benefits của DTO:**
- ✅ Chỉ select fields cần thiết
- ✅ Không có lazy loading issues
- ✅ Dễ versioning API
- ✅ Tránh expose entity internals

---

## 📁 BÀI 4: N+1 PROBLEM - DEMO VÀ FIX

### Ví dụ 4.1: Tạo dữ liệu test

```java
@Component
public class DataGenerator implements ApplicationRunner {

    @Autowired
    private UserRepository userRepository;

    @Override
    public void run(ApplicationArguments args) {
        // Tạo 100 users, mỗi user có 5 posts
        for (int i = 1; i <= 100; i++) {
            User user = new User("User " + i, "user" + i + "@example.com");
            userRepository.save(user);

            for (int j = 1; j <= 5; j++) {
                Post post = new Post("Post " + j + " by User " + i, "Content...");
                post.setUser(user);
                user.addPost(post);
            }
        }
    }
}
```

---

### Ví dụ 4.2: Demo N+1 problem

```java
@RestController
@RequestMapping("/api/demo")
public class NPlusOneDemoController {

    @Autowired
    private UserRepository userRepository;

    /**
     * ❌ N+1 PROBLEM: 1 + 100 = 101 queries!
     */
    @GetMapping("/users-naive")
    public List<UserDTO> getAllUsersWithPostCount() {
        List<User> users = userRepository.findAll();

        return users.stream().map(user -> {
            UserDTO dto = new UserDTO();
            dto.setId(user.getId());
            dto.setName(user.getName());
            dto.setPostCount(user.getPosts().size());  // ❌ Trigger N queries!
            return dto;
        }).collect(Collectors.toList());
    }

    /**
     * ✅ FIX 1: JOIN FETCH
     */
    @GetMapping("/users-fetch")
    public List<UserDTO> getAllUsersWithPostCountFixed() {
        List<User> users = userRepository.findAllWithPosts();  // 1 query

        return users.stream().map(user -> {
            UserDTO dto = new UserDTO();
            dto.setId(user.getId());
            dto.setName(user.getName());
            dto.setPostCount(user.getPosts().size());
            return dto;
        }).collect(Collectors.toList());
    }

    /**
     * ✅ FIX 2: COUNT trong query
     */
    @GetMapping("/users-count")
    public List<UserPostCountDTO> getAllUsersWithPostCountOptimized() {
        return userRepository.findAllWithPostCount();
    }
}

// Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // Fix 1: JOIN FETCH
    @Query("SELECT DISTINCT u FROM User u JOIN FETCH u.posts")
    List<User> findAllWithPosts();

    // Fix 2: COUNT aggregate
    @Query("""
        SELECT new com.example.dto.UserPostCountDTO(
            u.id,
            u.name,
            COUNT(p.id)
        )
        FROM User u
        LEFT JOIN u.posts p
        GROUP BY u.id, u.name
        """)
    List<UserPostCountDTO> findAllWithPostCount();
}

// DTO
public class UserPostCountDTO {
    private Long id;
    private String name;
    private Long postCount;

    public UserPostCountDTO(Long id, String name, Long postCount) {
        this.id = id;
        this.name = name;
        this.postCount = postCount;
    }

    // Getters
}
```

---

### Ví dụ 4.3: Enable SQL logging để debug

```yaml
# application.yml
spring:
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        use_sql_comments: true
        generate_statistics: true

logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE  # Show parameters
```

**Output khi chạy N+1:**
```
Hibernate:
    select
        u0_.id as id1_0_,
        u0_.name as name2_0_,
        u0_.email as email3_0_
    from users u0_

Hibernate:
    select
        p0_.id as id1_1_0_,
        p0_.title as title2_1_0_,
        p0_.content as content3_1_0_,
        p0_.user_id as user_id4_1_0_
    from posts p0_
    where
        p0_.user_id = ?   -- Parameter: 1

Hibernate:
    select
        p0_.id as id1_1_0_,
        p0_.title as title2_1_0_,
        p0_.content as content3_1_0_,
        p0_.user_id as user_id4_1_0_
    from posts p0_
    where
        p0_.user_id = ?   -- Parameter: 2

... (100 times!)
```

---

### Ví dụ 4.4: @BatchSize để fix N+1

```java
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @OneToMany(mappedBy = "user", fetch = FetchType.LAZY)
    @BatchSize(size = 10)  // Load 10 users cùng lúc
    private List<Post> posts;
}
```

**SQL với @BatchSize(10):**
```sql
-- Thay vì 100 queries riêng lẻ
-- Chỉ 10 queries với IN clause
SELECT * FROM posts WHERE user_id IN (1,2,3,4,5,6,7,8,9,10);
SELECT * FROM posts WHERE user_id IN (11,12,13,14,15,16,17,18,19,20);
...
```

---

## 📁 BÀI 5: CACHING DEMO

### Ví dụ 5.1: Level 1 Cache

```java
@Service
@Transactional
public class L1CacheDemo {

    @Autowired
    private EntityManager entityManager;

    public void demonstrateL1Cache() {
        System.out.println("=== L1 CACHE DEMO ===");

        // Query 1: Load từ DB
        User user1 = entityManager.find(User.class, 1L);
        System.out.println("Loaded user1: " + user1.getName());

        // Query 2: Load từ L1 cache
        User user2 = entityManager.find(User.class, 1L);
        System.out.println("Loaded user2: " + user2.getName());

        // user1 == user2 (cùng reference trong persistence context)
        System.out.println("Same reference? " + (user1 == user2));  // true
    }
}
```

**SQL:**
```sql
-- Chỉ 1 query
SELECT * FROM users WHERE id = 1;
```

---

### Ví dụ 5.2: Level 2 Cache với Ehcache

**Step 1: Dependencies**
```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-jcache</artifactId>
</dependency>
<dependency>
    <groupId>org.ehcache</groupId>
    <artifactId>ehcache</artifactId>
</dependency>
```

**Step 2: Configuration**
```yaml
spring:
  jpa:
    properties:
      hibernate:
        cache:
          use_second_level_cache: true
          use_query_cache: true
          region:
            factory_class: org.hibernate.cache.jcache.JCacheRegionFactory
        jakarta:
          cache:
            missing_cache_strategy: create
  cache:
    jcache:
      config: classpath:ehcache.xml
```

**Step 3: ehcache.xml**
```xml
<config xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
        xmlns='http://www.ehcache.org/v3'
        xsi:schemaLocation="http://www.ehcache.org/v3 http://www.ehcache.org/schema/ehcache-core-3.0.xsd">

    <cache alias="com.example.User">
        <heap unit="entries">1000</heap>
        <expiry>
            <ttl unit="minutes">30</ttl>
        </expiry>
    </cache>

    <cache alias="com.example.Post">
        <heap unit="entries">5000</heap>
        <expiry>
            <ttl unit="minutes">10</ttl>
        </expiry>
    </cache>
</config>
```

**Step 4: Enable cache cho entity**
```java
@Entity
@Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class User {
    // ...
}
```

**Step 5: Demo**
```java
@Service
public class L2CacheDemo {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EntityManager entityManager;

    public void demonstrateL2Cache() {
        // Session 1
        System.out.println("=== Session 1 ===");
        User user1 = userRepository.findById(1L).get();
        System.out.println("Loaded: " + user1.getName());

        entityManager.clear();  // Clear L1 cache

        // Session 2 (L1 cache cleared, but L2 still has data)
        System.out.println("=== Session 2 ===");
        User user2 = userRepository.findById(1L).get();
        System.out.println("Loaded: " + user2.getName());
        // L2 cache hit - no SQL query!
    }
}
```

---

## 📝 BÀI TẬP THỰC HÀNH

Xem `03-exercises.md` để làm bài tập Phase 2.

---

## 🔜 TIẾP THEO

Sau khi đọc xong examples, làm bài tập thực hành ở file tiếp theo.
