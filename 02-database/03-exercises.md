# Database - Bài Tập Thực Hành

> **Thời gian:** 8-10 giờ
> **Đầu ra:** Code submit lên GitHub + Report kết quả

---

## PHẦN 1: SQL EXERCISES

### Bài 1: Thiết kế Database Schema (1.5 giờ)

#### Đề bài

Thiết kế database schema cho **Blog Platform** với các yêu cầu sau:

**Entities:**
1. **Users** - bloggers và readers
2. **Posts** - blog posts
3. **Categories** - có hierarchy (Technology → Programming → Java)
4. **Tags** - tags cho posts (many-to-many)
5. **Comments** - comments cho posts (có thể reply comments khác)
6. **Reactions** - like, love, haha, etc. cho posts và comments

**Requirements:**
- 1 User có thể viết nhiều Posts
- 1 Post thuộc 1 Category
- 1 Post có nhiều Tags, 1 Tag áp dụng cho nhiều Posts (many-to-many)
- 1 Post có nhiều Comments
- Comments có thể reply nhau (self-referencing)
- 1 User có thể reaction nhiều Posts và Comments
- Lưu trữ version history của posts (audit trail)

**Submit:**
```sql
-- users.sql
CREATE TABLE users (
    -- Your schema here
);

-- categories.sql (với hierarchy)
CREATE TABLE categories (
    -- Your schema here với parent_id reference
);

-- posts.sql
CREATE TABLE posts (
    -- Your schema here
);

-- tags.sql
CREATE TABLE tags (
    -- Your schema here
);

-- post_tags.sql (junction table)
CREATE TABLE post_tags (
    -- Your schema here
);

-- comments.sql (với self-reference)
CREATE TABLE comments (
    -- Your schema here với parent_id reference
);

-- reactions.sql
CREATE TABLE reactions (
    -- Your schema here
);

-- post_versions.sql (audit trail)
CREATE TABLE post_versions (
    -- Your schema here
);

-- Indexes
-- Create appropriate indexes for performance
```

---

### Bài 2: Viết Queries cho Blog Platform (2 giờ)

#### Đề bài

Viết các queries sau cho schema ở Bài 1:

**Yêu cầu:**

1. **Lấy top 10 posts mới nhất với author info và category**
   ```sql
   -- Expected columns: post_id, title, excerpt, author_name, category_name, published_at, reaction_count
   ```

2. **Lấy danh sách posts của một category với pagination**
   ```sql
   -- Input: category_id, page, page_size
   -- Expected: posts với author, reaction count, comment count
   ```

3. **Lấy comment tree cho một post (recursive CTE)**
   ```sql
   -- Input: post_id
   -- Expected: comment_id, content, author_name, parent_id, level (depth)
   ```

4. **Lập báo cáo monthly stats**
   ```sql
   -- Expected: month, new_users, new_posts, new_comments, total_reactions
   -- Last 12 months
   ```

5. **Tìm users có engagement cao nhất (window functions)**
   ```sql
   -- Expected: user_id, name, post_count, total_reactions_received, rank
   -- Rank by total_reactions_received
   ```

6. **Lấy posts có average rating cao nhất trong mỗi category**
   ```sql
   -- Expected: category_name, post_id, title, avg_rating
   -- One post per category
   ```

7. **Tìm similar posts dựa trên shared tags**
   ```sql
   -- Input: post_id
   -- Expected: similar posts với shared_tag_count
   ```

8. **User activity heatmap data**
   ```sql
   -- Expected: day_of_week (0-6), hour (0-23), activity_count
   -- Cho last 30 days
   ```

**Submit:**
```sql
-- solutions.sql
-- Bài 1: Top 10 posts
SELECT ...

-- Bài 2: Posts by category
SELECT ...

-- Bài 3: Comment tree
WITH RECURSIVE comment_tree AS (
    -- Base case
    ...
    UNION ALL
    -- Recursive case
    ...
)
SELECT ...

-- Bài 4: Monthly stats
SELECT ...

-- Bài 5: User engagement rank
SELECT ...

-- Bài 6: Best posts per category
SELECT ...

-- Bài 7: Similar posts
SELECT ...

-- Bài 8: Activity heatmap
SELECT ...
```

---

### Bài 3: Query Optimization (1.5 giờ)

#### Đề bài

Cho database schema và các queries sau đang chạy chậm. Hãy optimize chúng.

**Schema:**
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    category_id INTEGER,
    title VARCHAR(255),
    content TEXT,
    status VARCHAR(20),
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER,
    user_id INTEGER,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(100),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Data volume:
-- posts: 1M rows
-- comments: 10M rows
-- users: 100K rows
```

**Slow Queries:**

```sql
-- Query 1: Get active posts with author (2 seconds)
SELECT p.*, u.name as author_name
FROM posts p
JOIN users u ON p.user_id = u.id
WHERE p.status = 'published'
ORDER BY p.created_at DESC
LIMIT 20 OFFSET 1000;

-- Query 2: Get post with comment count (5 seconds)
SELECT
    p.*,
    COUNT(c.id) as comment_count
FROM posts p
LEFT JOIN comments c ON c.post_id = p.id
WHERE p.category_id = 5
GROUP BY p.id
ORDER BY p.created_at DESC;

-- Query 3: Get user's posts with reactions (3 seconds)
SELECT
    p.id,
    p.title,
    p.content,
    COUNT(DISTINCT r.id) as reaction_count
FROM posts p
LEFT JOIN reactions r ON r.post_id = p.id
WHERE p.user_id = 12345
GROUP BY p.id
ORDER BY p.created_at DESC;

-- Query 4: Search posts by title (10 seconds)
SELECT * FROM posts
WHERE LOWER(title) LIKE '%java tutorial%';

-- Query 5: Get recent activity (8 seconds)
SELECT
    'post' as type,
    p.id,
    p.title,
    p.created_at,
    u.name as author_name
FROM posts p
JOIN users u ON p.user_id = u.id
WHERE p.created_at > NOW() - INTERVAL '7 days'

UNION ALL

SELECT
    'comment' as type,
    c.id,
    c.content,
    c.created_at,
    u.name as author_name
FROM comments c
JOIN users u ON c.user_id = u.id
WHERE c.created_at > NOW() - INTERVAL '7 days'

ORDER BY created_at DESC
LIMIT 50;
```

**Yêu cầu:**

1. Phân tích execution plan (giả sử)
2. Đề xuất indexes
3. Rewrite queries nếu cần
4. Giải thích tại sao optimization giúp query nhanh hơn

**Submit:**
```markdown
# Query Optimization Report

## Query 1: Active posts with author

### Current execution plan (giả sử):
- Seq Scan on posts (cost=0.00..50000.00)
- Hash Join with users (cost=50000.00..60000.00)
- Sort (cost=70000.00)

### Proposed indexes:
```sql
CREATE INDEX idx_posts_status_created ON posts(status, created_at DESC);
CREATE INDEX idx_users_id_name ON users(id, name);
```

### Optimized query:
```sql
-- Same query, but with proper index
```

### Why it's faster:
- Index on (status, created_at) allows index scan instead of seq scan
- Covering index reduces table lookups
- ...
```

---

## PHẦN 2: MONGODB EXERCISES

### Bài 4: MongoDB Schema Design (1.5 giờ)

#### Đề bài

Thiết kế document schemas cho **Food Delivery App** sử dụng MongoDB.

**Requirements:**

1. **Restaurant Collection**
   - Basic info: name, description, cuisine types, rating
   - Location with geospatial data
   - Operating hours
   - Menu với categories và items (embedded)
   - Reviews (embedded với limit)

2. **Order Collection**
   - Customer reference
   - Restaurant reference
   - Order items với customization (embedded)
   - Pricing breakdown
   - Delivery address
   - Status timeline
   - Driver assignment

3. **User Collection**
   - Profile info
   - Saved addresses (array)
   - Favorite restaurants (array)
   - Order history (references)

**Submit:**
```javascript
// restaurants.js
// Schema design với comments giải thích choices
{
    _id: ObjectId,
    name: String,
    description: String,
    cuisineTypes: [String],  // Why embedded?
    rating: {
        average: Number,
        count: Number
    },
    location: {
        type: "Point",
        coordinates: [longitude, latitude]
    },
    address: {
        street: String,
        city: String,
        district: String
    },
    operatingHours: {
        monday: { open: String, close: String },
        // ...
    },
    menu: {
        categories: [
            {
                name: String,
                items: [
                    {
                        name: String,
                        description: String,
                        price: Number,
                        image: String,
                        available: Boolean,
                        customizations: [...]
                    }
                ]
            }
        ]
    },
    reviews: [
        {
            userId: ObjectId,
            userName: String,
            rating: Number,
            comment: String,
            createdAt: Date
        }
    ],
    createdAt: Date,
    updatedAt: Date
}

// orders.js
{
    // Your schema here
}

// users.js
{
    // Your schema here
}

// Giải thích tại sao chọn embedded vs referenced cho mỗi field
```

---

### Bài 5: MongoDB CRUD Operations (1 giờ)

#### Đề bài

Viết các MongoDB queries cho Food Delivery schema ở Bài 4.

**Yêu cầu:**

1. **Find restaurants:**
   - Near a location (within 5km)
   - With specific cuisine type
   - Rating >= 4.0
   - Currently open (based on operating hours)
   - Sorted by rating, paginated

2. **Search menu items:**
   - Search by name/description (text search)
   - Filter by price range
   - Filter by available items only
   - From specific restaurants

3. **Create order:**
   - Create new order document
   - Update restaurant's daily order count
   - Update user's order history

4. **Update order status:**
   - Add status to timeline
   - Update current status
   - Notify if status is "delivered"

5. **Add review:**
   - Add review to restaurant's reviews array
   - Update average rating
   - Limit reviews to last 100 (using $slice)

6. **Analytics queries:**
   - Get orders by status for a restaurant today
   - Get top 10 customers by total spending
   - Get popular dishes (most ordered items) this week

**Submit:**
```javascript
// 1. Find nearby restaurants
db.restaurants.find({
    location: {
        $near: {
            $geometry: { type: "Point", coordinates: [106.6296, 10.8231] },
            $maxDistance: 5000
        }
    },
    cuisineTypes: "vietnamese",
    "rating.average": { $gte: 4.0 }
}).sort({ "rating.average": -1 }).limit(10);

// 2. Search menu items
// Your query here

// 3. Create order
// Your query here

// 4. Update order status
// Your query here

// 5. Add review
// Your query here

// 6. Analytics
// Your queries here
```

---

### Bài 6: MongoDB Aggregation Pipeline (2 giờ)

#### Đề bài

Viết aggregation pipelines cho các yêu cầu sau:

**1. Restaurant Dashboard**
```javascript
// Input: restaurantId, dateRange
// Output:
{
    restaurantId: ObjectId,
    period: { start: Date, end: Date },
    metrics: {
        totalOrders: Number,
        completedOrders: Number,
        cancelledOrders: Number,
        totalRevenue: Number,
        averageOrderValue: Number,
        averageRating: Number,
        newReviews: Number
    },
    topDishes: [
        { name: String, orderCount: Number, revenue: Number }
    ],
    ordersByHour: [
        { hour: Number, orderCount: Number }
    ]
}
```

**2. Customer Insights**
```javascript
// Output: Customer segmentation
[
    {
        userId: ObjectId,
        name: String,
        segment: "VIP" | "Regular" | "New" | "Churned",
        metrics: {
            totalOrders: Number,
            totalSpent: Number,
            averageOrderValue: Number,
            favoriteCuisine: String,
            lastOrderDate: Date,
            daysSinceLastOrder: Number
        }
    }
]

// Segmentation rules:
// VIP: totalOrders >= 10 AND totalSpent >= 1000000 AND daysSinceLastOrder <= 7
// Regular: totalOrders >= 3 AND daysSinceLastOrder <= 30
// New: totalOrders === 1
// Churned: daysSinceLastOrder > 30
```

**3. Delivery Performance Analysis**
```javascript
// Output:
[
    {
        date: Date,
        district: String,
        metrics: {
            totalDeliveries: Number,
            onTimeDeliveries: Number,
            lateDeliveries: Number,
            onTimePercentage: Number,
            averageDeliveryTimeMinutes: Number
        }
    }
]

// onTime = delivered within estimated time
// late = delivered after estimated time
```

**4. Popular Dishes Report**
```javascript
// Output: Top 50 dishes this month
[
    {
        dishName: String,
        restaurantId: ObjectId,
        restaurantName: String,
        orderCount: Number,
        revenue: Number,
        averageRating: Number,
        cuisineType: String
    }
]
```

**Submit:**
```javascript
// 1. Restaurant Dashboard
db.orders.aggregate([
    // Your pipeline here
]);

// 2. Customer Insights
db.orders.aggregate([
    // Your pipeline here
]);

// 3. Delivery Performance
db.orders.aggregate([
    // Your pipeline here
]);

// 4. Popular Dishes
db.orders.aggregate([
    // Your pipeline here
]);
```

---

## PHẦN 3: SPRING DATA INTEGRATION

### Bài 7: Spring Data JPA Repository (1.5 giờ)

#### Đề bài

Implement repositories cho Blog Platform (Bài 1).

**Yêu cầu:**

1. **UserRepository:**
   ```java
   - findByEmail(String email)
   - findByStatusOrderByCreatedAtDesc(String status, Pageable pageable)
   - findByIdWithPosts(Long id)  // JOIN FETCH
   - existsByEmail(String email)
   - countByStatus(String status)
   ```

2. **PostRepository:**
   ```java
   - findByStatusAndPublishedAtBefore(String status, LocalDateTime date, Pageable pageable)
   - findByCategoryIdAndStatus(Long categoryId, String status, Pageable pageable)
   - findByAuthorIdWithComments(Long authorId)
   - findTop10ByStatusOrderByViewsDesc(String status)
   - countByCategoryId(Long categoryId)
   - @Query for complex searches
   ```

3. **CommentRepository:**
   ```java
   - findByPostIdOrderByCreatedAtAsc(Long postId)
   - findByParentId(Long parentId)  // For replies
   - countByPostId(Long postId)
   - deleteByPostId(Long postId)
   ```

4. **Custom Queries:**
   ```java
   - Get posts with reaction count (using subquery or DTO)
   - Get comment tree for a post
   - Get monthly stats
   ```

**Submit:**
```java
// UserRepository.java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);

    Page<User> findByStatusOrderByCreatedAtDesc(String status, Pageable pageable);

    @Query("SELECT u FROM User u JOIN FETCH u.posts WHERE u.id = :id")
    Optional<User> findByIdWithPosts(@Param("id") Long id);

    boolean existsByEmail(String email);

    long countByStatus(String status);

    // Add more methods as needed
}

// PostRepository.java
public interface PostRepository extends JpaRepository<Post, Long> {
    // Your methods here

    // Custom query example
    @Query("""
        SELECT new com.example.dto.PostWithStatsDTO(
            p.id, p.title, p.excerpt,
            u.name as authorName,
            c.name as categoryName,
            COUNT(DISTINCT r.id) as reactionCount,
            COUNT(DISTINCT c.id) as commentCount
        )
        FROM Post p
        JOIN p.author u
        JOIN p.category c
        LEFT JOIN p.reactions r
        LEFT JOIN p.comments c
        WHERE p.status = :status
        GROUP BY p.id, p.title, p.excerpt, u.name, c.name
        ORDER BY p.publishedAt DESC
        """)
    Page<PostWithStatsDTO> findPostsWithStats(@Param("status") String status, Pageable pageable);
}

// Service layer example
@Service
public class PostService {
    @Autowired
    private PostRepository postRepository;

    @Transactional(readOnly = true)
    public Page<PostWithStatsDTO> getPublishedPosts(Pageable pageable) {
        return postRepository.findPostsWithStats("published", pageable);
    }
}
```

---

### Bài 8: Spring Data MongoDB Repository (1.5 giờ)

#### Đề bài

Implement repositories cho Food Delivery App (Bài 4).

**Yêu cầu:**

1. **RestaurantRepository:**
   ```java
   - findByNameContaining(String name)
   - findByCuisineTypesContaining(String cuisine)
   - findByRatingAverageGreaterThanEqual(Double rating)
   - findByLocationNear(Point location, Distance distance)
   - @TextSearch for menu items
   - @Aggregation for restaurant stats
   ```

2. **OrderRepository:**
   ```java
   - findByUserId(String userId)
   - findByRestaurantIdAndStatus(String restaurantId, String status)
   - findByCreatedAtBetween(LocalDateTime start, LocalDateTime end)
   - @Aggregation for analytics
   ```

3. **Custom Aggregations:**
   ```java
   - Get top restaurants by orders this month
   - Get customer lifetime value
   - Get daily revenue report
   ```

**Submit:**
```java
// RestaurantRepository.java
public interface RestaurantRepository extends MongoRepository<Restaurant, String> {

    List<Restaurant> findByCuisineTypesContaining(String cuisine);

    List<Restaurant> findByRatingAverageGreaterThanEqual(Double rating);

    List<Restaurant> findByLocationNear(Point location, Distance distance);

    @Query("{ 'menu.categories.items.name': { $regex: ?0, $options: 'i' } }")
    List<Restaurant> searchByMenuItem(String itemName);

    @Aggregation(pipeline = {
        "{ $match: { location: { $near: { $geometry: { type: 'Point', coordinates: ?0 }, $maxDistance: ?1 } } } }",
        "{ $match: { 'rating.average': { $gte: ?2 } } }",
        "{ $sort: { 'rating.average': -1 } }",
        "{ $limit: ?3 }"
    })
    List<Restaurant> findTopNearby(Point coordinates, int maxDistance, Double minRating, int limit);

    @Aggregation(pipeline = {
        "{ $lookup: { from: 'orders', localField: '_id', foreignField: 'restaurantId', as: 'orders' } }",
        "{ $match: { 'orders.status': 'completed', 'orders.createdAt': { $gte: ?0, $lte: ?1 } } }",
        "{ $project: { _id: 1, name: 1, totalOrders: { $size: '$orders' }, totalRevenue: { $sum: '$orders.pricing.total' } } }",
        "{ $sort: { totalOrders: -1 } }"
    })
    List<RestaurantStats> getTopRestaurantsByOrders(LocalDateTime start, LocalDateTime end);
}

// OrderRepository.java
public interface OrderRepository extends MongoRepository<Order, String> {

    List<Order> findByUserId(String userId);

    List<Order> findByRestaurantIdAndStatus(String restaurantId, String status);

    List<Order> findByCreatedAtBetween(LocalDateTime start, LocalDateTime end);

    @Aggregation(pipeline = {
        "{ $match: { userId: ?0 } }",
        "{ $group: { _id: null, totalSpent: { $sum: '$pricing.total' }, orderCount: { $sum: 1 } } }"
    })
    Optional<CustomerStats> getCustomerStats(String userId);

    interface CustomerStats {
        Long getTotalSpent();
        Integer getOrderCount();
    }
}
```

---

## ✅ CHECKLIST HOÀN THÀNH

- [ ] Bài 1: SQL Schema Design
- [ ] Bài 2: SQL Queries
- [ ] Bài 3: Query Optimization
- [ ] Bài 4: MongoDB Schema Design
- [ ] Bài 5: MongoDB CRUD
- [ ] Bài 6: MongoDB Aggregation
- [ ] Bài 7: Spring Data JPA Repository
- [ ] Bài 8: Spring Data MongoDB Repository

---

## 📤 CÁCH SUBMIT

1. Tạo folder `database-exercises` trong project
2. Tạo các file:
   - `01-schema.sql`
   - `02-queries.sql`
   - `03-optimization.md`
   - `04-mongodb-schema.js`
   - `05-mongodb-crud.js`
   - `06-mongodb-aggregation.js`
   - Java repositories trong package appropriate
3. Tạo `README.md` với hướng dẫn chạy code
4. Push lên GitHub và gửi link

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, bạn đã hoàn thành Database Fundamentals phase!
Tiếp theo sẽ là Phase 3: Caching với Redis.
