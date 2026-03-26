# Phase 2: Database & Hibernate - Lý Thuyết

> **Thời gian:** 3 tuần
> **Mục tiêu:** Master JPA/Hibernate, query optimization, fix N+1 problems

---

## 📚 BÀI 1: JPA VS HIBERNATE - PHÂN BIỆT VÀ CÁCH HOẠT ĐỘNG

### 1.1 JPA là gì? Hibernate là gì?

**JPA (Jakarta Persistence API):**
- Là **specification** (đặc tả) - giống như interface
- Định nghĩa các annotation: `@Entity`, `@Table`, `@OneToMany`...
- Định nghĩa các interface: `EntityManager`, `EntityTransaction`

**Hibernate:**
- Là **implementation** của JPA - giống như class implement interface
- Cung cấp code thật để chạy
- Có thêm features riêng mà JPA không có

```
┌─────────────────────────────────────────┐
│           YOUR CODE                     │
│   (dùng @Entity, EntityManager...)      │
├─────────────────────────────────────────┤
│           JPA (Specification)           │
│   - Jakarta Persistence API             │
│   - Chỉ là interface/annotation         │
├─────────────────────────────────────────┤
│        HIBERNATE (Implementation)       │
│   - Code thật chạy bên dưới             │
│   - Có thêm @LazyToOne, @BatchSize...   │
├─────────────────────────────────────────┤
│          DATABASE (PostgreSQL)          │
└─────────────────────────────────────────┘
```

**Spring Data JPA:**
- Layer trên cùng, auto-generate repository implementation
- Bạn chỉ cần interface, Spring Data tự implement

```
Your Repository Interface  →  Spring Data JPA  →  Hibernate  →  Database
```

---

### 1.2 EntityManager là gì?

**EntityManager** = "Cửa sổ" để tương tác với database

```java
// Cách dùng EntityManager trực tiếp (không khuyến khích)
@Autowired
private EntityManager em;

public User findById(Long id) {
    return em.find(User.class, id);
}

public void save(User user) {
    em.persist(user);  // INSERT
    em.merge(user);    // UPDATE
    em.remove(user);   // DELETE
}
```

**Spring Data JPA** (nên dùng):
```java
// Chỉ cần interface, Spring tự implement
public interface UserRepository extends JpaRepository<User, Long> {
    // Tự động có: findById, save, findAll, delete...
}
```

---

### 1.3 Vòng đời của Entity (Entity Lifecycle)

```
                    ┌──────────────┐
                    │   NEW/TRANSIENT │
                    │  (chưa attach)  │
                    └───────┬──────┘
                            │ persist()
                            ▼
┌──────────────┐    ┌──────────────┐
│   REMOVED    │◄───│   MANAGED   │
│  (đã delete) │    │ (đang quản lý)│
└──────────────┘    └───────┬──────┘
                            │ detach() / close()
                            ▼
                    ┌──────────────┐
                    │   DETACHED   │
                    │  (không attach)│
                    └──────────────┘
```

**4 trạng thái:**

| State | Mô tả | Ví dụ |
|-------|-------|-------|
| **NEW/TRANSIENT** | Entity mới tạo, chưa gắn với EntityManager | `new User()` |
| **MANAGED** | Entity đang được EntityManager quản lý, changes tự động sync | Sau `persist()` hoặc `find()` |
| **DETACHED** | Entity từng được quản lý, nhưng EntityManager đã đóng | Sau khi transaction kết thúc |
| **REMOVED** | Entity đã được mark để delete | Sau `remove()` |

**Ví dụ thực tế:**

```java
@Transactional
public void demonstrateLifecycle() {
    // 1. NEW state
    User user = new User("John");

    // 2. Chuyển sang MANAGED state
    em.persist(user);  // Hoặc repository.save(user)

    // user vẫn đang MANAGED, thay đổi sẽ tự động sync
    user.setName("Jane");  // Không cần gọi update!

    // 3. Transaction kết thúc → DETACHED state
    // user bây giờ là DETACHED
}
```

---

## 📚 BÀI 2: RELATIONSHIPS TRONG JPA

### 2.1 Các loại relationships

```
@OneToOne          User → Profile (1-1)
@OneToMany         User → Posts (1-n)
@ManyToOne         Post → User (n-1)
@ManyToMany        User ↔ Roles (n-n)
```

---

### 2.2 @OneToMany / @ManyToOne (Phổ biến nhất)

**Ví dụ:** User có nhiều Posts

**Cách 1: One-directional (1 chiều) - KHÔNG NÊN**
```java
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @OneToMany
    @JoinColumn(name = "user_id")  // Foreign key
    private List<Post> posts;
}

@Entity
public class Post {
    @Id
    @GeneratedValue
    private Long id;

    private String title;
    // Không có reference về User
}
```

**Vấn đề:** Từ Post không biết được thuộc User nào

---

**Cách 2: Bi-directional (2 chiều) - NÊN DÙNG**
```java
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Post> posts = new ArrayList<>();

    // Helper method
    public void addPost(Post post) {
        posts.add(post);
        post.setUser(this);
    }

    public void removePost(Post post) {
        posts.remove(post);
        post.setUser(null);
    }
}

@Entity
public class Post {
    @Id
    @GeneratedValue
    private Long id;

    private String title;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
}
```

**Quan trọng:**
- `mappedBy = "user"` → Nói với JPA rằng field `user` trong Post là owner
- `cascade = CascadeType.ALL` → Khi save User, tự động save Posts
- `orphanRemoval = true` → Khi remove Post khỏi list, tự động DELETE khỏi DB
- `fetch = FetchType.LAZY` → Chỉ load khi cần (sẽ học kỹ ở bài sau)

---

### 2.3 @OneToOne

**Ví dụ:** User có 1 Profile

```java
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private Profile profile;
}

@Entity
public class Profile {
    @Id
    @GeneratedValue
    private Long id;

    private String bio;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", unique = true, nullable = false)
    private User user;
}
```

**Lưu ý:** `unique = true` để đảm bảo 1-1

---

### 2.4 @ManyToMany

**Ví dụ:** User có nhiều Roles, Role có nhiều Users

```java
@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @ManyToMany
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    private List<Role> roles = new ArrayList<>();
}

@Entity
public class Role {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @ManyToMany(mappedBy = "roles")
    private List<User> users = new ArrayList<>();
}
```

**Bảng trung gian:**
```
user_roles
┌───────────┬──────────┐
│ user_id   │ role_id  │
├───────────┼──────────┤
│ 1         │ 1        │
│ 1         │ 2        │
│ 2         │ 1        │
└───────────┴──────────┘
```

---

## 📚 BÀI 3: FETCH TYPES - LAZY VS EAGER

### 3.1 Sự khác biệt

**EAGER:** Load ngay lập tức khi load entity cha

```java
@Entity
public class User {
    @OneToMany(fetch = FetchType.EAGER)  // Load posts NGAY
    private List<Post> posts;
}

// Khi gọi:
User user = userRepository.findById(1L);
// Posts đã được load sẵn (có thể không cần)
```

**LAZY:** Chỉ load khi access field

```java
@Entity
public class User {
    @OneToMany(fetch = FetchType.LAZY)  // Chỉ load khi cần
    private List<Post> posts;
}

// Khi gọi:
User user = userRepository.findById(1L);
// Posts CHƯA được load

// Chỉ load khi:
user.getPosts().size();  // Lúc này mới query DB
```

---

### 3.2 Default fetch types

| Relationship | Default |
|-------------|---------|
| `@OneToOne` | EAGER |
| `@OneToMany` | LAZY |
| `@ManyToOne` | EAGER |
| `@ManyToMany` | LAZY |

**Khuyến cáo:**
- ✅ Luôn dùng `LAZY` cho collections (`@OneToMany`, `@ManyToMany`)
- ✅ Dùng `LAZY` cho `@ManyToOne` và `@OneToOne` trừ khi chắc chắn cần
- ❌ EAGER là nguyên nhân chính gây performance issues

---

### 3.3 LazyInitializationException

**Vấn đề:** Access lazy field khi EntityManager đã đóng

```java
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public User getUserWithPosts(Long id) {
        User user = userRepository.findById(id).get();
        return user;  // Transaction kết thúc ở đây
    }
}

// Ở Controller:
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    User user = userService.getUserWithPosts(id);
    return user;  // OK
}

// Nhưng nếu access posts:
@GetMapping("/users/{id}/posts")
public List<Post> getUserPosts(@PathVariable Long id) {
    User user = userService.getUserWithPosts(id);
    return user.getPosts();  // ❌ LazyInitializationException!
}
```

**Giải pháp:**

**Cách 1: JOIN FETCH trong query**
```java
public interface UserRepository extends JpaRepository<User, Long> {

    @Query("SELECT u FROM User u JOIN FETCH u.posts WHERE u.id = :id")
    Optional<User> findByIdWithPosts(@Param("id") Long id);
}
```

**Cách 2: @Transactional ở service layer**
```java
@Transactional(readOnly = true)
@GetMapping("/users/{id}/posts")
public List<Post> getUserPosts(@PathVariable Long id) {
    User user = userRepository.findById(id).get();
    return user.getPosts();  // OK vì transaction còn mở
}
```

**Cách 3: Open Session In View (KHÔNG NÊN)**
```yaml
spring:
  jpa:
    open-in-view: true  # Mặc định là true, nhưng không nên dùng
```

---

## 📚 BÀI 4: N+1 QUERY PROBLEM

### 4.1 N+1 là gì?

**N+1 Query:** 1 query để load cha + N queries để load các con

**Ví dụ:**

```java
// Lấy danh sách users và hiển thị số posts của mỗi user
List<User> users = userRepository.findAll();

for (User user : users) {
    System.out.println(user.getName() + " has " + user.getPosts().size() + " posts");
}
```

**SQL generated:**
```sql
-- Query 1: Load tất cả users
SELECT * FROM users;

-- Query 2: Load posts của user 1
SELECT * FROM posts WHERE user_id = 1;

-- Query 3: Load posts của user 2
SELECT * FROM posts WHERE user_id = 2;

-- Query 4: Load posts của user 3
SELECT * FROM posts WHERE user_id = 3;

... (100 users = 100 queries)

-- TỔNG CỘNG: 1 + 100 = 101 queries! 😱
```

---

### 4.2 Cách phát hiện N+1

**Cách 1: Enable SQL logging**
```yaml
spring:
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        use_sql_comments: true
```

**Cách 2: Dùng datasource-proxy (cho production)**
```xml
<dependency>
    <groupId>com.github.gavlyukovskiy</groupId>
    <artifactId>datasource-proxy-spring-boot-starter</artifactId>
</dependency>
```

```yaml
decorator:
  datasource:
    p6spy:
      enable-logging: true
```

---

### 4.3 Cách fix N+1

**Solution 1: JOIN FETCH (cho 1 collection)**

```java
@Query("SELECT DISTINCT u FROM User u JOIN FETCH u.posts")
List<User> findAllWithPosts();
```

**SQL:**
```sql
SELECT u.*, p.*
FROM users u
LEFT JOIN posts p ON u.id = p.user_id;
-- Chỉ 1 query!
```

**Solution 2: Entity Graph (linh hoạt hơn)**

```java
@Entity
@NamedEntityGraph(
    name = "User.withPosts",
    attributeNodes = @NamedAttributeNode("posts")
)
public class User {
    // ...
}

// Repository:
@EntityGraph(value = "User.withPosts", type = EntityGraph.EntityGraphType.LOAD)
List<User> findAll();
```

**Solution 3: Batch Size (cho nhiều collections)**

```java
@Entity
public class User {
    @OneToMany(fetch = FetchType.LAZY)
    @BatchSize(size = 10)  // Load 10 users cùng lúc
    private List<Post> posts;
}
```

**SQL:**
```sql
-- Thay vì 100 queries riêng lẻ
-- Sẽ có 10 queries với IN clause
SELECT * FROM posts WHERE user_id IN (1,2,3,4,5,6,7,8,9,10);
SELECT * FROM posts WHERE user_id IN (11,12,13,14,15,16,17,18,19,20);
...
```

**Solution 4: Subquery (cho aggregate)**

```java
// Thay vì load posts rồi đếm
@Query("SELECT u, COUNT(p) FROM User u LEFT JOIN u.posts p GROUP BY u.id")
List<Object[]> findAllWithPostCount();
```

---

## 📚 BÀI 5: CACHING TRONG HIBERNATE

### 5.1 3 levels of caching

```
┌─────────────────────────────────────────────────────────┐
│                   L1 CACHE (Persistence Context)        │
│   - Tự động, per EntityManager/Session                  │
│   - Scope: Transaction                                  │
│   - Không cần config                                    │
├─────────────────────────────────────────────────────────┤
│                   L2 CACHE (SessionFactory)             │
│   - Cần config (Ehcache, Hazelcast, Redis)              │
│   - Scope: Application                                  │
│   - Cache entities, collections                         │
├─────────────────────────────────────────────────────────┤
│                   QUERY CACHE                           │
│   - Cache kết quả query                                 │
│   - Phải enable riêng                                   │
└─────────────────────────────────────────────────────────┘
```

---

### 5.2 Level 1 Cache (Tự động)

```java
@Transactional
public void demonstrateL1Cache() {
    // Query 1: Load từ DB
    User user1 = em.find(User.class, 1L);

    // Query 2: Load từ L1 cache (không query DB!)
    User user2 = em.find(User.class, 1L);

    // user1 == user2 (cùng reference)
}
```

**SQL:**
```sql
-- Chỉ 1 query
SELECT * FROM users WHERE id = 1;
```

---

### 5.3 Level 2 Cache (Cần config)

**Step 1: Add dependency**
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

**Step 2: Cấu hình**
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
```

**Step 3: Enable cache cho entity**
```java
@Entity
@Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class User {
    // ...
}
```

---

### 5.4 Khi nào dùng cache?

| Scenario | Nên cache? | Level |
|----------|-----------|-------|
| Reference data (countries, roles) | ✅ | L2 |
| Frequently read, rarely updated | ✅ | L2 |
| User session data | ✅ | L2 (Redis) |
| Real-time data | ❌ | - |
| Frequently updated data | ❌ | - |

---

## 📝 TÓM TẮT PHASE 2

Sau phase này, bạn cần nắm được:

1. ✅ Phân biệt JPA vs Hibernate vs Spring Data JPA
2. ✅ Entity lifecycle (NEW, MANAGED, DETACHED, REMOVED)
3. ✅ Relationships: @OneToMany, @ManyToOne, @OneToOne, @ManyToMany
4. ✅ Fetch types: LAZY vs EAGER và khi nào dùng
5. ✅ N+1 problem: phát hiện và fix
6. ✅ Hibernate caching: L1, L2, Query cache

---

## 🔜 TIẾP THEO

Đọc file `02-examples.md` để xem code mẫu thực tế.
