# Database - Examples & Code Samples

---

## PHẦN 1: SQL EXAMPLES

### 1.1 E-commerce Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories with hierarchy
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INTEGER REFERENCES categories(id),
    slug VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    stock_quantity INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Items
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL
);

-- Reviews
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES carts(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_reviews_product ON reviews(product_id);
```

---

### 1.2 Common SQL Queries

#### Get products with category info

```sql
SELECT
    p.id,
    p.name,
    p.price,
    c.name AS category_name,
    c.slug AS category_slug
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.status = 'active'
ORDER BY p.created_at DESC
LIMIT 20;
```

#### Get order details with items

```sql
SELECT
    o.id AS order_id,
    o.status,
    o.total_amount,
    o.created_at,
    u.full_name AS customer_name,
    u.email,
    oi.quantity,
    oi.unit_price,
    oi.subtotal,
    pr.name AS product_name
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products pr ON oi.product_id = pr.id
WHERE o.id = 1;
```

#### Get product with average rating

```sql
SELECT
    p.*,
    c.name AS category_name,
    COALESCE(AVG(r.rating), 0) AS avg_rating,
    COUNT(r.id) AS review_count
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN reviews r ON r.product_id = p.id
WHERE p.id = 1
GROUP BY p.id, c.id;
```

#### Get user's order history with totals

```sql
SELECT
    o.id,
    o.status,
    o.total_amount,
    o.created_at,
    COUNT(oi.id) AS item_count
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.id
WHERE o.user_id = 1
GROUP BY o.id, o.status, o.total_amount, o.created_at
ORDER BY o.created_at DESC;
```

#### Get category hierarchy (recursive CTE)

```sql
WITH RECURSIVE category_tree AS (
    -- Base case: top-level categories
    SELECT id, name, parent_id, 0 AS level
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive case: child categories
    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree
ORDER BY level, name;
```

#### Get top-selling products

```sql
SELECT
    p.id,
    p.name,
    p.price,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.subtotal) AS total_revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.id
JOIN orders o ON o.id = oi.order_id
WHERE o.status != 'cancelled'
GROUP BY p.id, p.name, p.price
ORDER BY total_sold DESC
LIMIT 10;
```

#### Monthly sales report

```sql
SELECT
    DATE_TRUNC('month', o.created_at) AS month,
    COUNT(DISTINCT o.id) AS order_count,
    COUNT(DISTINCT o.user_id) AS customer_count,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value
FROM orders o
WHERE o.status != 'cancelled'
GROUP BY DATE_TRUNC('month', o.created_at)
ORDER BY month DESC;
```

#### Get products by price range with window function

```sql
SELECT
    id,
    name,
    price,
    NTILE(4) OVER (ORDER BY price) AS price_quartile,
    PERCENT_RANK() OVER (ORDER BY price) AS price_percentile
FROM products
WHERE status = 'active';
```

#### Running total of daily sales

```sql
SELECT
    DATE_TRUNC('day', created_at) AS sale_date,
    COUNT(*) AS order_count,
    SUM(total_amount) AS daily_revenue,
    SUM(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('day', created_at)) AS running_total
FROM orders
WHERE status != 'cancelled'
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY sale_date;
```

---

### 1.3 Query Optimization Examples

#### Before (N+1 problem)

```sql
-- Query 1: Get all users
SELECT * FROM users;

-- Then for each user, query their orders:
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
SELECT * FROM orders WHERE user_id = 3;
-- ... (100 queries for 100 users)
```

#### After (JOIN FETCH)

```sql
SELECT
    u.id AS user_id,
    u.email,
    u.full_name,
    o.id AS order_id,
    o.status,
    o.total_amount
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active';
```

#### Using Indexes Effectively

```sql
-- Create composite index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Query uses index efficiently
SELECT * FROM orders
WHERE user_id = 1 AND status = 'completed';

-- Query also uses index (leftmost prefix)
SELECT * FROM orders
WHERE user_id = 1;

-- Query does NOT use index (skipped first column)
SELECT * FROM orders
WHERE status = 'completed';
```

---

## PHẦN 2: MONGODB EXAMPLES

### 2.1 Document Schemas

#### User Collection

```javascript
{
    _id: ObjectId("507f1f77bcf86cd799439011"),
    email: "john@example.com",
    passwordHash: "$2b$10$...",
    fullName: "John Doe",
    phone: "+1234567890",
    status: "active",  // active, inactive, banned
    roles: ["user", "admin"],
    profile: {
        avatar: "https://...",
        bio: "Software developer",
        location: {
            city: "New York",
            country: "USA",
            coordinates: [-74.0060, 40.7128]
        }
    },
    settings: {
        notifications: true,
        theme: "dark",
        language: "en"
    },
    createdAt: ISODate("2024-01-15T10:30:00Z"),
    updatedAt: ISODate("2024-01-15T10:30:00Z")
}
```

#### Product Collection (with embedded reviews)

```javascript
{
    _id: ObjectId("507f1f77bcf86cd799439012"),
    name: "iPhone 15 Pro",
    description: "Latest Apple flagship...",
    price: NumberDecimal("999.00"),
    category: "electronics",
    subcategory: "smartphones",
    tags: ["apple", "smartphone", "5g"],
    stock: 100,
    status: "active",
    images: [
        "https://.../image1.jpg",
        "https://.../image2.jpg"
    ],
    specifications: {
        display: "6.1 inch OLED",
        processor: "A17 Pro",
        ram: "8GB",
        storage: "256GB"
    },
    reviews: [
        {
            userId: ObjectId("507f1f77bcf86cd799439011"),
            userName: "John Doe",
            rating: 5,
            comment: "Excellent phone!",
            createdAt: ISODate("2024-01-20T10:30:00Z")
        }
    ],
    reviewStats: {
        averageRating: 4.5,
        totalReviews: 150,
        ratingDistribution: { 5: 100, 4: 30, 3: 15, 2: 3, 1: 2 }
    },
    createdAt: ISODate("2024-01-15T10:30:00Z"),
    updatedAt: ISODate("2024-01-20T10:30:00Z")
}
```

#### Order Collection (with embedded items)

```javascript
{
    _id: ObjectId("507f1f77bcf86cd799439013"),
    userId: ObjectId("507f1f77bcf86cd799439011"),
    status: "completed",  // pending, processing, completed, cancelled
    items: [
        {
            productId: ObjectId("507f1f77bcf86cd799439012"),
            name: "iPhone 15 Pro",
            quantity: 1,
            unitPrice: NumberDecimal("999.00"),
            subtotal: NumberDecimal("999.00")
        }
    ],
    pricing: {
        subtotal: NumberDecimal("999.00"),
        discount: NumberDecimal("0.00"),
        shipping: NumberDecimal("10.00"),
        tax: NumberDecimal("89.91"),
        total: NumberDecimal("1098.91")
    },
    shippingAddress: {
        fullName: "John Doe",
        street: "123 Main St",
        city: "New York",
        state: "NY",
        zipCode: "10001",
        country: "USA",
        phone: "+1234567890"
    },
    payment: {
        method: "credit_card",
        status: "paid",
        transactionId: "txn_123456"
    },
    timeline: [
        { status: "pending", timestamp: ISODate("2024-01-20T10:30:00Z") },
        { status: "processing", timestamp: ISODate("2024-01-20T11:00:00Z") },
        { status: "shipped", timestamp: ISODate("2024-01-20T15:00:00Z") },
        { status: "completed", timestamp: ISODate("2024-01-22T10:00:00Z") }
    ],
    createdAt: ISODate("2024-01-20T10:30:00Z"),
    updatedAt: ISODate("2024-01-22T10:00:00Z")
}
```

---

### 2.2 CRUD Operations

#### Insert Operations

```javascript
// Insert single document
db.users.insertOne({
    email: "john@example.com",
    fullName: "John Doe",
    status: "active",
    createdAt: new Date()
});

// Insert multiple documents
db.products.insertMany([
    {
        name: "iPhone 15 Pro",
        price: NumberDecimal("999.00"),
        category: "electronics",
        stock: 100,
        createdAt: new Date()
    },
    {
        name: "Samsung Galaxy S24",
        price: NumberDecimal("899.00"),
        category: "electronics",
        stock: 150,
        createdAt: new Date()
    }
]);

// Insert with generated fields
db.orders.insertOne({
    userId: ObjectId("507f1f77bcf86cd799439011"),
    status: "pending",
    items: [],
    pricing: { subtotal: 0, discount: 0, shipping: 0, tax: 0, total: 0 },
    createdAt: new Date(),
    updatedAt: new Date()
});
```

#### Query Operations

```javascript
// Basic find
db.users.find({ status: "active" });

// Find with projection
db.users.find(
    { status: "active" },
    { email: 1, fullName: 1, _id: 0 }
);

// Find with nested field
db.users.find({ "profile.location.city": "New York" });

// Find with array contains
db.users.find({ roles: "admin" });

// Find with comparison operators
db.products.find({ price: { $gte: 500, $lte: 1000 } });

// Find with logical operators
db.products.find({
    $or: [
        { stock: { $lt: 10 } },
        { status: "discontinued" }
    ]
});

// Find with array operators
db.products.find({ tags: { $all: ["apple", "5g"] } });

// Find with regex
db.users.find({ email: { $regex: /@gmail\.com$/ } });

// Find with element operator
db.users.find({ phone: { $exists: true } });

// Find sorted and paginated
db.products.find({ status: "active" })
    .sort({ price: -1 })
    .skip(0)
    .limit(20);
```

#### Update Operations

```javascript
// Update single field
db.users.updateOne(
    { email: "john@example.com" },
    { $set: { status: "inactive" } }
);

// Update multiple fields
db.users.updateOne(
    { email: "john@example.com" },
    {
        $set: {
            fullName: "John Smith",
            phone: "+1987654321"
        },
        $currentDate: { updatedAt: true }
    }
);

// Increment numeric field
db.products.updateOne(
    { _id: ObjectId("507f1f77bcf86cd799439012") },
    { $inc: { stock: -1 } }  // Decrease stock by 1
);

// Push to array
db.users.updateOne(
    { _id: ObjectId("507f1f77bcf86cd799439011") },
    { $push: { roles: "premium" } }
);

// Add to set (no duplicates)
db.users.updateOne(
    { _id: ObjectId("507f1f77bcf86cd799439011") },
    { $addToSet: { roles: "vip" } }
);

// Pull from array
db.users.updateOne(
    { _id: ObjectId("507f1f77bcf86cd799439011") },
    { $pull: { roles: "premium" } }
);

// Update nested field
db.users.updateOne(
    { _id: ObjectId("507f1f77bcf86cd799439011") },
    { $set: { "profile.bio": "Senior Developer" } }
);

// Update array element
db.products.updateOne(
    { "reviews.userId": ObjectId("507f1f77bcf86cd799439011") },
    { $set: { "reviews.$.comment": "Updated review" } }
);

// Upsert (update or insert)
db.users.updateOne(
    { email: "newuser@example.com" },
    {
        $set: { status: "active" },
        $setOnInsert: { createdAt: new Date() }
    },
    { upsert: true }
);

// Update many
db.products.updateMany(
    { category: "electronics" },
    { $set: { status: "active" } }
);
```

#### Delete Operations

```javascript
// Delete one
db.users.deleteOne({ email: "john@example.com" });

// Delete many
db.products.deleteMany({ status: "discontinued" });

// Soft delete (recommended)
db.users.updateOne(
    { _id: ObjectId("507f1f77bcf86cd799439011") },
    {
        $set: {
            status: "deleted",
            deletedAt: new Date()
        }
    }
);
```

---

### 2.3 Aggregation Pipeline Examples

#### Get product sales summary

```javascript
db.orders.aggregate([
    // Match completed orders
    { $match: { status: "completed" } },

    // Unwind items array
    { $unwind: "$items" },

    // Group by product
    {
        $group: {
            _id: "$items.productId",
            productName: { $first: "$items.name" },
            totalQuantity: { $sum: "$items.quantity" },
            totalRevenue: { $sum: "$items.subtotal" },
            orderCount: { $sum: 1 }
        }
    },

    // Sort by revenue
    { $sort: { totalRevenue: -1 } },

    // Limit to top 10
    { $limit: 10 }
]);
```

#### Get user order statistics

```javascript
db.orders.aggregate([
    { $match: { status: "completed" } },

    {
        $group: {
            _id: "$userId",
            totalOrders: { $sum: 1 },
            totalSpent: { $sum: "$pricing.total" },
            avgOrderValue: { $avg: "$pricing.total" },
            lastOrderDate: { $max: "$createdAt" }
        }
    },

    {
        $lookup: {
            from: "users",
            localField: "_id",
            foreignField: "_id",
            as: "user"
        }
    },

    { $unwind: "$user" },

    {
        $project: {
            _id: 0,
            userId: "$_id",
            email: "$user.email",
            fullName: "$user.fullName",
            totalOrders: 1,
            totalSpent: { $round: ["$totalSpent", 2] },
            avgOrderValue: { $round: ["$avgOrderValue", 2] },
            lastOrderDate: 1
        }
    },

    { $sort: { totalSpent: -1 } }
]);
```

#### Monthly revenue report

```javascript
db.orders.aggregate([
    { $match: { status: { $ne: "cancelled" } } },

    {
        $group: {
            _id: {
                year: { $year: "$createdAt" },
                month: { $month: "$createdAt" }
            },
            orderCount: { $sum: 1 },
            totalRevenue: { $sum: "$pricing.total" },
            customerCount: { $addToSet: "$userId" }
        }
    },

    {
        $project: {
            _id: 0,
            year: "$_id.year",
            month: "$_id.month",
            orderCount: 1,
            totalRevenue: { $round: ["$totalRevenue", 2] },
            uniqueCustomers: { $size: "$customerCount" }
        }
    },

    { $sort: { year: -1, month: -1 } }
]);
```

#### Product with review analytics

```javascript
db.products.aggregate([
    { $match: { status: "active" } },

    { $unwind: { path: "$reviews", preserveNullAndEmptyArrays: true } },

    {
        $group: {
            _id: "$_id",
            name: { $first: "$name" },
            price: { $first: "$price" },
            avgRating: { $avg: "$reviews.rating" },
            reviewCount: { $sum: { $cond: [{ $ne: ["$reviews", null] }, 1, 0] } },
            ratingDistribution: {
                $push: "$reviews.rating"
            }
        }
    },

    {
        $project: {
            name: 1,
            price: 1,
            avgRating: { $round: [{ $coalesce: ["$avgRating", 0] }, 2] },
            reviewCount: 1,
            ratingDistribution: {
                $cond: [
                    { $gt: ["$reviewCount", 0] },
                    {
                        "5": { $size: { $filter: { input: "$ratingDistribution", cond: { $eq: ["$$this", 5] } } } },
                        "4": { $size: { $filter: { input: "$ratingDistribution", cond: { $eq: ["$$this", 4] } } } },
                        "3": { $size: { $filter: { input: "$ratingDistribution", cond: { $eq: ["$$this", 3] } } } },
                        "2": { $size: { $filter: { input: "$ratingDistribution", cond: { $eq: ["$$this", 2] } } } },
                        "1": { $size: { $filter: { input: "$ratingDistribution", cond: { $eq: ["$$this", 1] } } } }
                    },
                    { "5": 0, "4": 0, "3": 0, "2": 0, "1": 0 }
                ]
            }
        }
    }
]);
```

#### Customer segmentation (RFM Analysis)

```javascript
const referenceDate = new Date();

db.orders.aggregate([
    { $match: { status: "completed" } },

    {
        $group: {
            _id: "$userId",
            totalOrders: { $sum: 1 },
            totalSpent: { $sum: "$pricing.total" },
            lastOrderDate: { $max: "$createdAt" },
            firstOrderDate: { $min: "$createdAt" }
        }
    },

    {
        $project: {
            _id: 0,
            userId: "$_id",
            totalOrders: 1,
            totalSpent: 1,
            recency: {
                $dateDiff: {
                    start: "$lastOrderDate",
                    end: referenceDate,
                    unit: "day"
                }
            },
            frequency: "$totalOrders",
            monetary: "$totalSpent",
            customerSince: "$firstOrderDate"
        }
    },

    {
        $addFields: {
            segment: {
                $switch: {
                    branches: [
                        {
                            case: {
                                $and: [
                                    { $lte: ["$recency", 30] },
                                    { $gte: ["$frequency", 5] },
                                    { $gte: ["$monetary", 500] }
                                ]
                            },
                            then: "VIP"
                        },
                        {
                            case: { $lte: ["$recency", 60] },
                            then: "Active"
                        },
                        {
                            case: { $lte: ["$recency", 180] },
                            then: "At Risk"
                        },
                        {
                            case: { $gt: ["$recency", 180] },
                            then: "Churned"
                        }
                    ],
                    default: "New"
                }
            }
        }
    }
]);
```

---

### 2.4 Index Examples

```javascript
// Create indexes
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ status: 1, createdAt: -1 });
db.users.createIndex({ "profile.location.city": 1 });
db.users.createIndex({ roles: 1 });

db.products.createIndex({ category: 1, status: 1 });
db.products.createIndex({ price: 1 });
db.products.createIndex({ tags: 1 });
db.products.createIndex({ name: "text", description: "text" });

db.orders.createIndex({ userId: 1, createdAt: -1 });
db.orders.createIndex({ status: 1 });
db.orders.createIndex({ createdAt: -1 });

// Text search
db.products.createIndex({ name: "text", description: "text" });

// Search products
db.products.find({
    $text: { $search: "iphone case" }
});

// Text search with score
db.products.find(
    { $text: { $search: "iphone" } },
    { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } });

// Geospatial index
db.places.createIndex({ location: "2dsphere" });

// Find nearby places
db.places.find({
    location: {
        $near: {
            $geometry: {
                type: "Point",
                coordinates: [-74.0060, 40.7128]
            },
            $maxDistance: 5000  // 5km
        }
    }
});

// TTL index for sessions
db.sessions.createIndex(
    { expiresAt: 1 },
    { expireAfterSeconds: 0 }
);
```

---

## PHẦN 3: SPRING DATA INTEGRATION

### 3.1 Spring Data JPA Repository

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(name = "full_name", nullable = false)
    private String fullName;

    private String status = "active";

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Order> orders = new ArrayList<>();

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    // Constructors, getters, setters
}

@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    private String status;

    @Column(name = "total_amount")
    private BigDecimal totalAmount;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    // Constructors, getters, setters
}

public interface UserRepository extends JpaRepository<User, Long> {

    // Derived query methods
    Optional<User> findByEmail(String email);
    List<User> findByStatus(String status);
    List<User> findByStatusAndCreatedAtAfter(String status, LocalDateTime date);

    // With pagination
    Page<User> findByStatus(String status, Pageable pageable);

    // With sorting
    List<User> findByStatusOrderByCreatedAtDesc(String status);

    // Custom query
    @Query("SELECT u FROM User u JOIN FETCH u.orders WHERE u.id = :id")
    Optional<User> findByIdWithOrders(@Param("id") Long id);

    // Native query
    @Query(value = "SELECT * FROM users WHERE email LIKE %:domain", nativeQuery = true)
    List<User> findByEmailDomain(@Param("domain") String domain);

    // Update query
    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.status = :status WHERE u.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") String status);

    // Delete query
    @Modifying
    @Transactional
    @Query("DELETE FROM User u WHERE u.status = :status")
    int deleteByStatus(@Param("status") String status);
}

public interface OrderRepository extends JpaRepository<Order, Long> {

    List<Order> findByUserId(Long userId);

    List<Order> findByStatus(String status);

    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
    Optional<Order> findByIdWithItems(@Param("id") Long id);

    // Aggregation query
    @Query("SELECT SUM(o.totalAmount) FROM Order o WHERE o.user.id = :userId")
    BigDecimal getTotalSpentByUser(@Param("userId") Long userId);

    // Monthly revenue
    @Query("""
        SELECT FUNCTION('DATE_TRUNC', 'month', o.createdAt) as month,
               SUM(o.totalAmount) as total
        FROM Order o
        WHERE o.status != 'cancelled'
        GROUP BY FUNCTION('DATE_TRUNC', 'month', o.createdAt)
        ORDER BY month DESC
        """)
    List<Object[]> getMonthlyRevenue();
}
```

---

### 3.2 Spring Data MongoDB Repository

```java
@Document(collection = "users")
public class User {
    @Id
    private String id;

    @Indexed(unique = true)
    private String email;

    private String fullName;

    private String status;

    private List<String> roles;

    @Embedded
    private Profile profile;

    @Field("created_at")
    private LocalDateTime createdAt;

    // Constructors, getters, setters

    @Embeddable
    public static class Profile {
        private String avatar;
        private String bio;

        @Embedded
        private Location location;

        // Getters, setters
    }

    @Embeddable
    public static class Location {
        private String city;
        private String country;
        // Getters, setters
    }
}

@Document(collection = "products")
public class Product {
    @Id
    private String id;

    private String name;

    private String description;

    private BigDecimal price;

    private String category;

    private List<String> tags;

    private Integer stock;

    private String status;

    private List<Review> reviews;

    @Field("created_at")
    private LocalDateTime createdAt;

    // Constructors, getters, setters

    @Embeddable
    public static class Review {
        private String userId;
        private String userName;
        private Integer rating;
        private String comment;
        private LocalDateTime createdAt;
        // Getters, setters
    }
}

public interface UserRepository extends MongoRepository<User, String> {

    // Derived query methods
    Optional<User> findByEmail(String email);
    List<User> findByStatus(String status);
    List<User> findByStatusAndCreatedAtAfter(String status, LocalDateTime date);

    // With sorting
    List<User> findByStatusOrderByCreatedAtDesc(String status);

    // Array contains
    List<User> findByRolesContaining(String role);

    // Nested field
    List<User> findByProfileLocationCity(String city);

    // Custom query with @Query
    @Query("{ 'status': ?0, 'profile.location.city': ?1 }")
    List<User> findByStatusAndCity(String status, String city);

    // Aggregation
    @Aggregation(pipeline = {
        "{ $match: { status: ?0 } }",
        "{ $group: { _id: '$profile.location.city', count: { $sum: 1 } } }"
    })
    List<CityUserCount> getUserCountByCity(String status);

    interface CityUserCount {
        String getCity();
        Long getCount();
    }
}

public interface ProductRepository extends MongoRepository<Product, String> {

    List<Product> findByCategory(String category);

    List<Product> findByStatus(String status);

    List<Product> findByTagsContaining(String tag);

    List<Product> findByPriceBetween(BigDecimal min, BigDecimal max);

    @Query("{ 'price': { $gte: ?0, $lte: ?1 }, 'status': 'active' }")
    List<Product> findByPriceRange(BigDecimal min, BigDecimal max);

    // Text search
    @TextSearch
    List<Product> findByNameOrDescription(String search);

    // Geo query
    List<Product> findByLocationNear(Point location, Distance distance);
}
```

---

## TÓM TẮT

Các ví dụ trong file này bao phủ:

### SQL
- ✅ Schema design cho e-commerce
- ✅ Các queries phổ biến (JOINs, aggregations, window functions)
- ✅ Query optimization techniques
- ✅ Recursive CTEs cho hierarchy

### MongoDB
- ✅ Document schemas (embedded vs referenced)
- ✅ CRUD operations với các operators
- ✅ Aggregation pipeline examples
- ✅ Index types và usage

### Spring Data Integration
- ✅ Repository interfaces cho JPA và MongoDB
- ✅ Custom queries với @Query và @Aggregation
- ✅ Entity/Document mapping
