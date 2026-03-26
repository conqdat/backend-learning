# Phase 2: Database & Hibernate - Bài Tập Thực Hành

> **Thời gian:** 6-8 giờ
> **Đầu ra:** Code submit lên GitHub + Report kết quả

---

## 📝 BÀI TẬP 1: THIẾT KẾ DATABASE SCHEMA (1 giờ)

### Đề bài

Thiết kế database schema cho **E-commerce Platform** với các entities sau:

**Yêu cầu:**
1. User (khách hàng)
2. Product (sản phẩm)
3. Category (danh mục - có hierarchy: Electronics → Phones → iPhone)
4. Order (đơn hàng)
5. OrderItem (chi tiết đơn hàng)
6. Review (đánh giá sản phẩm)
7. Cart (giỏ hàng)

**Rules:**
- 1 User có nhiều Orders
- 1 Order có nhiều OrderItems
- 1 Product thuộc 1 Category
- 1 Category có thể có nhiều cha/con (hierarchy)
- 1 User viết nhiều Reviews
- 1 Product có nhiều Reviews
- Cart và CartItem cho giỏ hàng

### Cách submit

```java
// User.java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String fullName;

    private String email;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Order> orders = new ArrayList<>();

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Review> reviews = new ArrayList<>();

    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private Cart cart;

    // Helper methods
    public void addOrder(Order order) {
        orders.add(order);
        order.setUser(this);
    }

    // Getters, Setters, Constructors
}

// Tiếp tục cho các entities khác...
```

---

## 📝 BÀI TẬP 2: FIX N+1 PROBLEM (2 giờ)

### Đề bài

Cho project với các entities:

```java
@Entity
public class Department {
    @Id
    @GeneratedValue
    private Long id;
    private String name;

    @OneToMany(mappedBy = "department", fetch = FetchType.LAZY)
    private List<Employee> employees;
}

@Entity
public class Employee {
    @Id
    @GeneratedValue
    private Long id;
    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;

    @OneToMany(mappedBy = "employee", fetch = FetchType.LAZY)
    private List<Project> projects;
}

@Entity
public class Project {
    @Id
    @GeneratedValue
    private Long id;
    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "employee_id")
    private Employee employee;
}
```

**Yêu cầu:**

1. Viết API trả về danh sách Departments với số lượng employees
2. Viết API trả về danh sách Employees với tên department
3. Viết API trả về danh sách Projects với tên employee và department

**Bước 1:** Implement version gây N+1 (để thấy vấn đề)

**Bước 2:** Fix bằng JOIN FETCH

**Bước 3:** Fix bằng @BatchSize

**Bước 4:** So sánh số lượng queries

### Cách submit

```markdown
## Kết quả bài tập N+1

### API 1: Departments với employee count

#### Version N+1 (chưa fix):
```java
@GetMapping("/departments")
public List<DepartmentDTO> getDepartments() {
    List<Department> depts = departmentRepository.findAll();
    return depts.stream().map(d -> {
        DepartmentDTO dto = new DepartmentDTO();
        dto.setName(d.getName());
        dto.setEmployeeCount(d.getEmployees().size());  // N+1!
        return dto;
    }).collect(Collectors.toList());
}
```

**SQL queries:** 1 + N (với N = số departments)

#### Version fix với JOIN FETCH:
```java
@Query("SELECT DISTINCT d FROM Department d JOIN FETCH d.employees")
List<Department> findAllWithEmployees();
```

**SQL queries:** 2 (1 query chính + 1 query cho collection)

### API 2: Employees với department name

...

### So sánh performance:

| API | Trước (queries) | Sau (queries) | Improvement |
|-----|----------------|---------------|-------------|
| /departments | 11 | 2 | 81% |
| /employees | 21 | 2 | 90% |
| /projects | 31 | 3 | 90% |
```

---

## 📝 BÀI TẬP 3: IMPLEMENT DTO PATTERN (2 giờ)

### Đề bài

Implement DTO projection cho các API sau:

**Scenario:** Blog platform với User, Post, Comment

```java
// Yêu cầu 1: List posts với author info
GET /api/posts

Response:
[
  {
    "id": 1,
    "title": "Hello World",
    "authorName": "John Doe",
    "commentCount": 5,
    "createdAt": "2024-01-15T10:30:00"
  }
]

// Yêu cầu 2: Post detail với comments
GET /api/posts/1

Response:
{
  "id": 1,
  "title": "Hello World",
  "content": "...",
  "author": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "comments": [
    {
      "id": 1,
      "content": "Great post!",
      "authorName": "Jane",
      "createdAt": "2024-01-15T11:00:00"
    }
  ]
}
```

### Cách submit

```java
// Cách 1: Interface-based projection
public interface PostSummary {
    Long getId();
    String getTitle();
    String getAuthorName();
    Long getCommentCount();
    LocalDateTime getCreatedAt();
}

public interface PostDetail {
    Long getId();
    String getTitle();
    String getContent();
    AuthorInfo getAuthor();
    List<CommentInfo> getComments();

    interface AuthorInfo {
        Long getId();
        String getName();
        String getEmail();
    }

    interface CommentInfo {
        Long getId();
        String getContent();
        String getAuthorName();
        LocalDateTime getCreatedAt();
    }
}

// Repository
public interface PostRepository extends JpaRepository<Post, Long> {

    @Query("""
        SELECT p.id as id,
               p.title as title,
               u.name as authorName,
               COUNT(c.id) as commentCount,
               p.createdAt as createdAt
        FROM Post p
        JOIN p.author u
        LEFT JOIN p.comments c
        GROUP BY p.id, p.title, u.name, p.createdAt
        """)
    List<PostSummary> findAllSummaries();

    @Query("""
        SELECT DISTINCT p
        FROM Post p
        JOIN FETCH p.author
        LEFT JOIN FETCH p.comments
        WHERE p.id = :id
        """)
    Optional<Post> findDetailById(@Param("id") Long id);
}
```

---

## 📝 BÀI TẬP 4: CACHING STRATEGY (1 giờ)

### Đề bài

Implement caching strategy cho ứng dụng:

**Yêu cầu:**
1. Enable L2 cache với Ehcache
2. Cache entities: Category, Product
3. Cache query: tìm products theo category
4. Config TTL khác nhau cho mỗi entity type

### Cách submit

```yaml
# application.yml
spring:
  jpa:
    properties:
      hibernate:
        cache:
          use_second_level_cache: true
          use_query_cache: true
          region:
            factory_class: org.hibernate.cache.jcache.JCacheRegionFactory
  cache:
    jcache:
      config: classpath:ehcache.xml
```

```xml
<!-- ehcache.xml -->
<config xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
        xmlns='http://www.ehcache.org/v3'>

    <!-- Categories: ít thay đổi, cache lâu -->
    <cache alias="com.example.Category">
        <heap unit="entries">100</heap>
        <expiry>
            <ttl unit="hours">24</ttl>
        </expiry>
    </cache>

    <!-- Products: nhiều hơn, cache ngắn hơn -->
    <cache alias="com.example.Product">
        <heap unit="entries">1000</heap>
        <expiry>
            <ttl unit="minutes">30</ttl>
        </expiry>
    </cache>

    <!-- Query cache -->
    <cache alias="org.hibernate.cache.internal.QueryCache">
        <heap unit="entries">500</heap>
        <expiry>
            <ttl unit="minutes">10</ttl>
        </expiry>
    </cache>
</config>
```

```java
@Entity
@Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class Category {
    // ...
}

@Entity
@Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class Product {
    // ...
}

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {

    @Query("SELECT p FROM Product p WHERE p.category.id = :categoryId")
    @Cacheable
    List<Product> findByCategoryId(@Param("categoryId") Long categoryId);
}
```

---

## 📝 BÀI TẬP 5: TRANSACTION MANAGEMENT (30 phút)

### Đề bài

Implement các scenarios sau với @Transactional:

**Scenario 1:** Transfer money giữa 2 accounts

```java
@Service
public class AccountService {

    @Autowired
    private AccountRepository accountRepository;

    @Transactional
    public void transferMoney(Long fromAccountId, Long toAccountId, BigDecimal amount) {
        Account from = accountRepository.findById(fromAccountId)
            .orElseThrow(() -> new EntityNotFoundException("From account not found"));

        Account to = accountRepository.findById(toAccountId)
            .orElseThrow(() -> new EntityNotFoundException("To account not found"));

        if (from.getBalance().compareTo(amount) < 0) {
            throw new InsufficientFundsException("Insufficient funds");
        }

        from.setBalance(from.getBalance().subtract(amount));
        to.setBalance(to.getBalance().add(amount));

        accountRepository.save(from);
        accountRepository.save(to);
    }
}
```

**Câu hỏi:**
1. Nếu save(to) throw exception, điều gì xảy ra với save(from)?
2. Nếu muốn save(from) commit ngay cả khi save(to) fail, làm thế nào?

### Cách submit

```markdown
## Transaction Management

### Scenario 1: Transfer Money

**Câu 1:** Nếu save(to) throw exception:
- Cả transaction rollback
- save(from) cũng bị rollback
- Đây là default behavior của @Transactional

**Câu 2:** Muốn save(from) commit dù save(to) fail:

Cách 1: Dùng REQUIRES_NEW
```java
@Transactional
public void transferMoney(...) {
    // ...
    accountRepository.save(from);  // Sẽ commit

    try {
        transferWithNewTransaction(to, amount);
    } catch (Exception e) {
        // Handle exception, from đã commit
    }
}

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void transferWithNewTransaction(Account to, BigDecimal amount) {
    accountRepository.save(to);
}
```

### Scenario 2: ...
```

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 2

- [ ] Thiết kế được database schema với đúng relationships
- [ ] Hiểu và áp dụng được cascade, orphanRemoval
- [ ] Fix được N+1 problem với JOIN FETCH
- [ ] Implement DTO pattern cho queries
- [ ] Config được L2 cache với Ehcache
- [ ] Hiểu transaction propagation

---

## 📤 CÁCH SUBMIT

1. Push code lên GitHub
2. Tạo file `PHASE2_REPORT.md` với kết quả
3. Gửi link cho mentor review

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, tôi sẽ review và unlock Phase 3: Caching với Redis!
