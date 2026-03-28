# Database Fundamentals - Theory

> **Thời gian:** 3-4 tuần
> **Mục tiêu:** Master cả SQL và NoSQL databases, từ cơ bản đến advanced topics

---

## PHẦN 1: SQL FUNDAMENTALS

### 1.1 Relational Databases & SQL Overview

**What is a Relational Database?**

- Data organized in **tables** (relations) with rows and columns
- Tables can be related through **keys** (primary, foreign)
- Follows **ACID properties** (Atomicity, Consistency, Isolation, Durability)

**SQL vs NoSQL:**

| Aspect | SQL (Relational) | NoSQL |
|--------|-----------------|-------|
| Data Model | Tables with fixed schema | Documents, Key-Value, Graph, Column-family |
| Schema | Pre-defined, rigid | Dynamic, flexible |
| Scaling | Vertical (scale-up) | Horizontal (scale-out) |
| Transactions | ACID compliant | BASE (Basically Available, Soft state, Eventual consistency) |
| Examples | PostgreSQL, MySQL, Oracle | MongoDB, Redis, Cassandra |

**When to use SQL:**
- Complex queries and joins required
- Data integrity is critical (financial systems)
- Well-structured, predictable data
- Vertical scaling is sufficient

**When to use NoSQL:**
- Large volume of unstructured/semi-structured data
- Rapid prototyping, evolving schema
- Horizontal scaling needed
- High write throughput

---

### 1.2 Basic SQL Syntax

#### SQL Keywords Categories

**DDL (Data Definition Language):**
- `CREATE` - Create database objects
- `ALTER` - Modify existing objects
- `DROP` - Delete objects
- `TRUNCATE` - Remove all data from table

**DML (Data Manipulation Language):**
- `SELECT` - Query data
- `INSERT` - Add new rows
- `UPDATE` - Modify existing rows
- `DELETE` - Remove rows

**DCL (Data Control Language):**
- `GRANT` - Give privileges
- `REVOKE` - Remove privileges

**TCL (Transaction Control Language):**
- `COMMIT` - Save changes
- `ROLLBACK` - Undo changes
- `SAVEPOINT` - Set rollback point

---

#### Data Types

**Numeric:**
```sql
INTEGER, INT, BIGINT, SMALLINT     -- Whole numbers
DECIMAL(10,2), NUMERIC(10,2)       -- Exact decimals
FLOAT, REAL, DOUBLE PRECISION      -- Approximate decimals
```

**String:**
```sql
CHAR(n)           -- Fixed length
VARCHAR(n)        -- Variable length
TEXT              -- Large text
```

**Date/Time:**
```sql
DATE              -- YYYY-MM-DD
TIME              -- HH:MM:SS
TIMESTAMP         -- Date + Time
INTERVAL          -- Time span
```

**Boolean:**
```sql
BOOLEAN           -- TRUE, FALSE, NULL
```

---

#### Constraints

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,                    -- Unique + NOT NULL
    email VARCHAR(255) UNIQUE NOT NULL,        -- Must be unique, required
    name VARCHAR(100) NOT NULL,                -- Required
    age INTEGER CHECK (age >= 18),             -- Must satisfy condition
    status VARCHAR(20) DEFAULT 'active',       -- Default value
    created_at TIMESTAMP DEFAULT NOW()         -- Auto timestamp
);
```

**Constraint Types:**
- `PRIMARY KEY` - Uniquely identifies each record
- `FOREIGN KEY` - References another table's primary key
- `UNIQUE` - All values must be different
- `NOT NULL` - Value cannot be null
- `CHECK` - Value must satisfy condition
- `DEFAULT` - Default value if not specified

---

### 1.3 DDL - Data Definition Language

#### CREATE TABLE

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### ALTER TABLE

```sql
-- Add column
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Modify column
ALTER TABLE users ALTER COLUMN name TYPE VARCHAR(150);

-- Drop column
ALTER TABLE users DROP COLUMN phone;

-- Add constraint
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);

-- Rename table
ALTER TABLE users RENAME TO app_users;
```

#### DROP & TRUNCATE

```sql
-- Drop table (structure + data)
DROP TABLE users;

-- Truncate table (keep structure, remove all data)
TRUNCATE TABLE users;

-- Drop with cascade (drop dependent objects too)
DROP TABLE users CASCADE;
```

---

### 1.4 DML - Data Manipulation Language

#### SELECT

```sql
-- Basic select
SELECT id, name, email FROM users;

-- Select all columns
SELECT * FROM users;

-- Select with DISTINCT
SELECT DISTINCT country FROM users;

-- Select with WHERE
SELECT * FROM users WHERE age >= 18 AND status = 'active';

-- Select with ORDER BY
SELECT * FROM users ORDER BY created_at DESC;

-- Select with LIMIT/OFFSET (pagination)
SELECT * FROM users ORDER BY created_at DESC LIMIT 10 OFFSET 20;
```

#### INSERT

```sql
-- Insert single row
INSERT INTO users (name, email, age)
VALUES ('John Doe', 'john@example.com', 25);

-- Insert multiple rows
INSERT INTO users (name, email, age)
VALUES
    ('John Doe', 'john@example.com', 25),
    ('Jane Smith', 'jane@example.com', 30),
    ('Bob Wilson', 'bob@example.com', 28);

-- Insert from SELECT
INSERT INTO premium_users (id, name, email)
SELECT id, name, email FROM users WHERE subscription = 'premium';
```

#### UPDATE

```sql
-- Update all rows
UPDATE users SET status = 'inactive';

-- Update with WHERE
UPDATE users
SET status = 'active', last_login = NOW()
WHERE id = 1;

-- Update with CASE
UPDATE users
SET status = CASE
    WHEN last_login < NOW() - INTERVAL '1 year' THEN 'inactive'
    ELSE 'active'
END;
```

#### DELETE

```sql
-- Delete all rows
DELETE FROM users;

-- Delete with WHERE
DELETE FROM users WHERE id = 1;

-- Delete with USING (join)
DELETE FROM orders
USING users
WHERE orders.user_id = users.id AND users.status = 'deleted';
```

---

### 1.5 JOINs

**Sample Tables:**
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    department_id INT
);

CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO users VALUES
    (1, 'Alice', 1),
    (2, 'Bob', 2),
    (3, 'Charlie', NULL),
    (4, 'Diana', 1);

INSERT INTO departments VALUES
    (1, 'Engineering'),
    (2, 'Marketing'),
    (3, 'Sales');
```

#### INNER JOIN

```sql
-- Returns only matching rows from both tables
SELECT u.name, d.name AS department
FROM users u
INNER JOIN departments d ON u.department_id = d.id;

-- Result:
-- Alice | Engineering
-- Bob   | Marketing
-- Diana | Engineering
```

#### LEFT JOIN (LEFT OUTER JOIN)

```sql
-- Returns all rows from left table, matching from right
SELECT u.name, d.name AS department
FROM users u
LEFT JOIN departments d ON u.department_id = d.id;

-- Result:
-- Alice   | Engineering
-- Bob     | Marketing
-- Charlie | NULL      (no department)
-- Diana   | Engineering
```

#### RIGHT JOIN (RIGHT OUTER JOIN)

```sql
-- Returns all rows from right table, matching from left
SELECT u.name, d.name AS department
FROM users u
RIGHT JOIN departments d ON u.department_id = d.id;

-- Result:
-- Alice   | Engineering
-- Bob     | Marketing
-- Diana   | Engineering
-- NULL    | Sales     (no users in Sales)
```

#### FULL OUTER JOIN

```sql
-- Returns all rows from both tables
SELECT u.name, d.name AS department
FROM users u
FULL OUTER JOIN departments d ON u.department_id = d.id;

-- Result:
-- Alice   | Engineering
-- Bob     | Marketing
-- Charlie | NULL
-- Diana   | Engineering
-- NULL    | Sales
```

#### CROSS JOIN

```sql
-- Cartesian product (all combinations)
SELECT u.name, d.name AS department
FROM users u
CROSS JOIN departments d;

-- Result: 4 users × 3 departments = 12 rows
```

#### SELF JOIN

```sql
-- Join table with itself (for hierarchy)
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

---

### 1.6 Aggregate Functions & GROUP BY

```sql
-- Basic aggregates
SELECT
    COUNT(*) AS total_users,
    COUNT(DISTINCT department_id) AS total_departments,
    SUM(salary) AS total_salary,
    AVG(salary) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM employees;
```

#### GROUP BY

```sql
-- Group by single column
SELECT department_id, COUNT(*) AS employee_count
FROM employees
GROUP BY department_id;

-- Group by multiple columns
SELECT department_id, role, COUNT(*) AS count
FROM employees
GROUP BY department_id, role;

-- Group by with aggregates
SELECT
    department_id,
    COUNT(*) AS employee_count,
    AVG(salary) AS avg_salary,
    SUM(salary) AS total_salary
FROM employees
GROUP BY department_id;
```

#### HAVING Clause

```sql
-- Filter groups (WHERE filters rows, HAVING filters groups)
SELECT department_id, COUNT(*) AS employee_count
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 5;

-- Combined with WHERE
SELECT department_id, AVG(salary) AS avg_salary
FROM employees
WHERE hire_date > '2020-01-01'
GROUP BY department_id
HAVING AVG(salary) > 50000
ORDER BY avg_salary DESC;
```

---

### 1.7 Subqueries

#### Scalar Subquery (returns single value)

```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

#### Column Subquery (returns single column)

```sql
SELECT name, department_id
FROM employees
WHERE department_id IN (
    SELECT id FROM departments WHERE location = 'New York'
);
```

#### Row Subquery (returns single row)

```sql
SELECT *
FROM employees
WHERE (department_id, salary) = (
    SELECT department_id, MAX(salary)
    FROM employees
    GROUP BY department_id
);
```

#### Table Subquery (returns table)

```sql
SELECT dept_stats.*
FROM (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
) dept_stats
WHERE dept_stats.avg_salary > 50000;
```

#### Correlated Subquery

```sql
-- Subquery references outer query
SELECT e.name, e.salary
FROM employees e
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE department_id = e.department_id
);

-- Using EXISTS
SELECT d.name
FROM departments d
WHERE EXISTS (
    SELECT 1 FROM employees e
    WHERE e.department_id = d.id AND e.salary > 100000
);
```

---

### 1.8 String, Numeric & Conditional Functions

#### String Functions

```sql
SELECT
    CONCAT(first_name, ' ', last_name) AS full_name,
    LENGTH(email) AS email_length,
    UPPER(name) AS upper_name,
    LOWER(email) AS lower_email,
    SUBSTRING(name, 1, 3) AS short_name,
    REPLACE(description, 'old', 'new') AS updated_desc,
    TRIM('  hello  ') AS trimmed,      -- 'hello'
    LTRIM('  hello') AS left_trimmed,  -- 'hello'
    RTRIM('hello  ') AS right_trimmed; -- 'hello'
```

#### Numeric Functions

```sql
SELECT
    ABS(-10) AS absolute,           -- 10
    ROUND(10.567, 2) AS rounded,    -- 10.57
    FLOOR(10.9) AS floored,         -- 10
    CEILING(10.1) AS ceiled,        -- 11
    MOD(10, 3) AS remainder,        -- 1
    POWER(2, 3) AS powered,         -- 8
    SQRT(16) AS squared;            -- 4
```

#### Conditional Functions

```sql
-- CASE expression
SELECT
    name,
    salary,
    CASE
        WHEN salary > 100000 THEN 'High'
        WHEN salary > 50000 THEN 'Medium'
        ELSE 'Low'
    END AS salary_level
FROM employees;

-- COALESCE (returns first non-null)
SELECT
    name,
    COALESCE(phone, mobile, 'No contact') AS contact
FROM users;

-- NULLIF (returns NULL if equal)
SELECT
    name,
    NULLIF(salary, 0) AS safe_salary  -- NULL if salary = 0
FROM employees;
```

---

### 1.9 Date & Time Functions

```sql
-- Current date/time
SELECT
    CURRENT_DATE,      -- 2024-01-15
    CURRENT_TIME,      -- 10:30:00
    CURRENT_TIMESTAMP, -- 2024-01-15 10:30:00.123
    NOW();             -- Same as CURRENT_TIMESTAMP

-- Date parts
SELECT
    DATE_PART('year', hire_date) AS hire_year,
    EXTRACT(MONTH FROM birth_date) AS birth_month,
    DATE_TRUNC('month', created_at) AS month_start;

-- Date arithmetic
SELECT
    hire_date + INTERVAL '1 year' AS one_year_later,
    end_date - start_date AS duration,
    AGE(CURRENT_DATE, birth_date) AS age;

-- Date formatting
SELECT
    TO_CHAR(CURRENT_DATE, 'DD/MM/YYYY') AS formatted_date,  -- 15/01/2024
    TO_DATE('2024-01-15', 'YYYY-MM-DD') AS date_value;
```

---

### 1.10 Views

```sql
-- Create view
CREATE VIEW active_users AS
SELECT id, name, email, department_id
FROM users
WHERE status = 'active';

-- Use view
SELECT * FROM active_users WHERE department_id = 1;

-- Create view with aggregation
CREATE VIEW department_stats AS
SELECT
    d.id,
    d.name,
    COUNT(e.id) AS employee_count,
    AVG(e.salary) AS avg_salary
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.name;

-- Modify view
CREATE OR REPLACE VIEW active_users AS
SELECT id, name, email, department_id, hire_date
FROM users
WHERE status = 'active';

-- Drop view
DROP VIEW active_users;
```

---

### 1.11 Indexes

**What is an Index?**
- Data structure that improves query speed
- Trade-off: faster reads, slower writes (index maintenance)

**Types of Indexes:**

```sql
-- B-Tree Index (default, most common)
CREATE INDEX idx_users_email ON users(email);

-- Composite Index (multiple columns)
CREATE INDEX idx_users_dept_status ON users(department_id, status);

-- Unique Index
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Partial Index (only on subset)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Expression Index
CREATE INDEX idx_lower_email ON users(LOWER(email));

-- Covering Index (INCLUDE - PostgreSQL 11+)
CREATE INDEX idx_users_covering ON users(department_id) INCLUDE (name, email);
```

**When to use indexes:**
- ✅ Columns frequently used in WHERE clauses
- ✅ Columns used in JOIN conditions
- ✅ Columns used in ORDER BY
- ✅ Columns with high cardinality (many unique values)

**When NOT to use indexes:**
- ❌ Small tables (< 1000 rows)
- ❌ Columns frequently updated
- ❌ Columns with low cardinality (e.g., gender, boolean)

---

### 1.12 Transactions & ACID Properties

**ACID Properties:**

| Property | Description |
|----------|-------------|
| **Atomicity** | All operations succeed or all fail |
| **Consistency** | Database remains in valid state |
| **Isolation** | Transactions don't interfere |
| **Durability** | Committed changes persist |

**Transaction Control:**

```sql
-- Start transaction
BEGIN;

-- Multiple operations
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Commit (save changes)
COMMIT;

-- Or rollback (undo changes)
ROLLBACK;

-- Savepoint (partial rollback)
BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    SAVEPOINT sp1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
    -- Something went wrong, rollback to savepoint
    ROLLBACK TO sp1;
COMMIT;
```

**Transaction Isolation Levels:**

| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-------|------------|---------------------|--------------|
| READ UNCOMMITTED | Possible | Possible | Possible |
| READ COMMITTED | ❌ | Possible | Possible |
| REPEATABLE READ | ❌ | ❌ | Possible |
| SERIALIZABLE | ❌ | ❌ | ❌ |

```sql
-- Set isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

BEGIN ISOLATION LEVEL SERIALIZABLE;
```

---

### 1.13 Window Functions

**What are Window Functions?**
- Perform calculations across rows related to current row
- Unlike GROUP BY, don't collapse rows

**Syntax:**
```sql
FUNCTION_NAME() OVER (
    PARTITION BY column1, column2
    ORDER BY column3
    ROWS BETWEEN ... AND ...
)
```

**Common Window Functions:**

```sql
-- ROW_NUMBER: Unique sequential number
SELECT
    name,
    department_id,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank
FROM employees;

-- RANK: Rank with gaps for ties
SELECT
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;
-- Ties get same rank, next rank skips (1, 1, 3, 4)

-- DENSE_RANK: Rank without gaps
SELECT
    name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;
-- Ties get same rank, no skip (1, 1, 2, 3)

-- NTILE: Divide into N groups
SELECT
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employees;
```

**LEAD and LAG:**

```sql
-- LAG: Access previous row
SELECT
    date,
    sales,
    LAG(sales, 1) OVER (ORDER BY date) AS prev_day_sales,
    sales - LAG(sales, 1) OVER (ORDER BY date) AS change
FROM daily_sales;

-- LEAD: Access next row
SELECT
    date,
    sales,
    LEAD(sales, 1) OVER (ORDER BY date) AS next_day_sales
FROM daily_sales;
```

**Running Totals:**

```sql
SELECT
    date,
    sales,
    SUM(sales) OVER (ORDER BY date) AS running_total,
    AVG(sales) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM daily_sales;
```

**PARTITION BY:**

```sql
-- Window function per department
SELECT
    name,
    department_id,
    salary,
    AVG(salary) OVER (PARTITION BY department_id) AS dept_avg_salary,
    salary - AVG(salary) OVER (PARTITION BY department_id) AS diff_from_avg
FROM employees;
```

---

### 1.14 Common Table Expressions (CTEs)

**Basic CTE:**

```sql
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE status = 'active'
)
SELECT * FROM active_users
WHERE department_id = 1;
```

**Multiple CTEs:**

```sql
WITH
active_users AS (
    SELECT id, name, department_id
    FROM users
    WHERE status = 'active'
),
dept_counts AS (
    SELECT department_id, COUNT(*) AS user_count
    FROM active_users
    GROUP BY department_id
)
SELECT d.name, dc.user_count
FROM departments d
JOIN dept_counts dc ON d.id = dc.department_id;
```

**Recursive CTE (for hierarchy):**

```sql
-- Find all subordinates of a manager
WITH RECURSIVE subordinates AS (
    -- Base case: direct reports
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id = 1

    UNION ALL

    -- Recursive case: subordinates of subordinates
    SELECT e.id, e.name, e.manager_id, s.level + 1
    FROM employees e
    INNER JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates;
```

---

### 1.15 Query Optimization

**1. Use EXPLAIN to analyze queries:**

```sql
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';

-- Output shows:
-- Scan type (Seq Scan vs Index Scan)
-- Estimated cost
-- Actual time
-- Rows returned
```

**2. Optimization Techniques:**

```sql
-- ❌ SLOW: SELECT *
SELECT * FROM users;

-- ✅ FAST: Select only needed columns
SELECT id, name, email FROM users;

-- ❌ SLOW: Function on indexed column
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- ✅ FAST: Use expression index or store pre-computed
CREATE INDEX idx_lower_email ON users(LOWER(email));

-- ❌ SLOW: LIKE with leading wildcard
SELECT * FROM users WHERE name LIKE '%john%';

-- ✅ FAST: LIKE with trailing wildcard only
SELECT * FROM users WHERE name LIKE 'john%';

-- ❌ SLOW: OR condition
SELECT * FROM users WHERE id = 1 OR email = 'test@example.com';

-- ✅ FAST: UNION ALL
SELECT * FROM users WHERE id = 1
UNION ALL
SELECT * FROM users WHERE email = 'test@example.com';

-- ❌ SLOW: Subquery in WHERE
SELECT * FROM orders
WHERE user_id IN (SELECT id FROM users WHERE status = 'active');

-- ✅ FAST: JOIN
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'active';
```

**3. Index Usage Tips:**

```sql
-- Leftmost prefix rule for composite indexes
CREATE INDEX idx_name_age ON users(name, age);

-- ✅ Uses index
SELECT * FROM users WHERE name = 'John';
SELECT * FROM users WHERE name = 'John' AND age = 25;

-- ❌ Doesn't use index (skipped first column)
SELECT * FROM users WHERE age = 25;
```

---

## PHẦN 2: MONGODB (NOSQL)

### 2.1 MongoDB Fundamentals

**What is MongoDB?**

- Document-oriented NoSQL database
- Stores data in **BSON** (Binary JSON) format
- Schema-less design
- Horizontal scaling through sharding

**SQL vs MongoDB Terminology:**

| SQL | MongoDB |
|-----|---------|
| Database | Database |
| Table | Collection |
| Row | Document |
| Column | Field |
| Primary Key | _id |
| Foreign Key | Reference (DBRef or manual) |
| JOIN | $lookup |

**When to use MongoDB:**
- ✅ Rapid prototyping, evolving schema
- ✅ Content management, catalogs
- ✅ Real-time analytics
- ✅ IoT applications (high write throughput)
- ✅ Geospatial applications
- ❌ Complex transactions (though MongoDB supports multi-document transactions)
- ❌ Complex joins and aggregations

---

### 2.2 BSON Data Types

**Basic Types:**

```javascript
{
    string: "Hello World",
    integer: 42,
    double: 3.14,
    boolean: true,
    null: null,
    date: new Date(),
    regex: /pattern/i
}
```

**MongoDB-Specific Types:**

```javascript
{
    objectId: ObjectId("507f1f77bcf86cd799439011"),  // 12-byte unique ID
    int32: NumberInt(42),
    int64: NumberLong(42),
    decimal: NumberDecimal("3.14159"),
    array: [1, 2, 3],
    embeddedDoc: { nested: "document" },
    binary: BinData(0, "base64"),
    timestamp: Timestamp(1234567890, 1),
    minKey: MinKey,  // For comparisons
    maxKey: MaxKey
}
```

**BSON vs JSON:**

| Aspect | JSON | BSON |
|--------|------|------|
| Format | Text | Binary |
| Types | Limited | Rich (Date, ObjectId, Binary, etc.) |
| Performance | Slower parsing | Faster, more efficient |
| Size | Compact | Slightly larger (includes length/type info) |

---

### 2.3 Collections & CRUD Operations

**Create Collection:**

```javascript
// Implicit creation (auto-created on first insert)
db.createCollection("users");

// With options
db.createCollection("users", {
    capped: true,
    size: 10485760,  // 10MB
    max: 10000       // Max 10000 documents
});
```

**Insert Operations:**

```javascript
// insertOne
db.users.insertOne({
    name: "John Doe",
    email: "john@example.com",
    age: 25,
    createdAt: new Date()
});

// insertMany
db.users.insertMany([
    { name: "Alice", email: "alice@example.com", age: 30 },
    { name: "Bob", email: "bob@example.com", age: 28 }
]);

// Insert with write concern
db.users.insertOne(
    { name: "Charlie", email: "charlie@example.com" },
    { writeConcern: { w: "majority", wtimeout: 5000 } }
);
```

**Find/Query Operations:**

```javascript
// Find all
db.users.find();

// Find with projection
db.users.find({}, { name: 1, email: 1, _id: 0 });

// Find with filter
db.users.find({ status: "active" });

// Find one
db.users.findOne({ email: "john@example.com" });

// Limit and skip
db.users.find().limit(10).skip(20);

// Sort
db.users.find().sort({ createdAt: -1 });  // -1 = DESC, 1 = ASC

// Count
db.users.countDocuments({ status: "active" });
db.users.estimatedDocumentCount();  // Faster, approximate
```

**Update Operations:**

```javascript
// Update one
db.users.updateOne(
    { email: "john@example.com" },
    { $set: { status: "inactive" } }
);

// Update many
db.users.updateMany(
    { status: "inactive" },
    { $set: { lastUpdated: new Date() } }
);

// Replace document
db.users.replaceOne(
    { email: "john@example.com" },
    { name: "John Smith", email: "john@example.com", age: 26 }
);

// Update with upsert (insert if not exists)
db.users.updateOne(
    { email: "john@example.com" },
    { $set: { name: "John Doe" }, $setOnInsert: { createdAt: new Date() } },
    { upsert: true }
);
```

**Delete Operations:**

```javascript
// Delete one
db.users.deleteOne({ email: "john@example.com" });

// Delete many
db.users.deleteMany({ status: "inactive" });

// Delete all
db.users.deleteMany({});

// Drop collection
db.users.drop();
```

**Bulk Write Operations:**

```javascript
db.users.bulkWrite([
    { insertOne: { document: { name: "Alice", age: 30 } } },
    { updateOne: {
        filter: { name: "Alice" },
        update: { $set: { age: 31 } }
    }},
    { deleteOne: { filter: { name: "Bob" } } },
    { replaceOne: {
        filter: { name: "Charlie" },
        replacement: { name: "Charles", age: 35 }
    }}
]);
```

---

### 2.4 Query Operators

**Comparison Operators:**

```javascript
// $eq (equal)
db.users.find({ age: { $eq: 25 } });  // or just { age: 25 }

// $ne (not equal)
db.users.find({ status: { $ne: "inactive" } });

// $gt, $gte, $lt, $lte
db.users.find({ age: { $gte: 18, $lt: 65 } });

// $in
db.users.find({ status: { $in: ["active", "pending"] } });

// $nin
db.users.find({ status: { $nin: ["deleted", "banned"] } });
```

**Logical Operators:**

```javascript
// $and (implicit for same field)
db.users.find({
    $and: [
        { age: { $gte: 18 } },
        { status: "active" }
    ]
});

// Implicit AND
db.users.find({
    age: { $gte: 18 },
    status: "active"
});

// $or
db.users.find({
    $or: [
        { age: { $gte: 18 } },
        { status: "vip" }
    ]
});

// $not
db.users.find({
    age: { $not: { $lt: 18 } }
});

// $nor (neither/nor)
db.users.find({
    $nor: [
        { status: "deleted" },
        { status: "banned" }
    ]
});
```

**Element Operators:**

```javascript
// $exists
db.users.find({ phone: { $exists: true } });
db.users.find({ phone: { $exists: false } });

// $type
db.users.find({ age: { $type: "int" } });
db.users.find({ value: { $type: ["string", "int", "double"] } });
```

**Array Operators:**

```javascript
// $all (contains all elements)
db.products.find({ tags: { $all: ["electronics", "sale"] } });

// $elemMatch (matches multiple criteria in array)
db.users.find({
    scores: { $elemMatch: { $gte: 80, $lt: 90 } }
});

// $size (array length)
db.users.find({ tags: { $size: 3 } });

// Array index access
db.users.find({ "tags.0": "first" });  // First element is "first"
```

**Projection Operators:**

```javascript
// $slice (limit array elements)
db.posts.find(
    { author: "john" },
    { comments: { $slice: 5 } }  // First 5 comments
);

db.posts.find(
    { author: "john" },
    { comments: { $slice: -5 } }  // Last 5 comments
);

db.posts.find(
    { author: "john" },
    { comments: { $slice: [10, 5] } }  // Skip 10, take 5
);

// $elemMatch (projection)
db.students.find(
    {},
    {
        grades: {
            $elemMatch: { grade: { $gte: 90 } }
        }
    }
);

// $project (aggregation)
db.users.aggregate([
    {
        $project: {
            fullName: { $concat: ["$firstName", " ", "$lastName"] },
            email: 1,
            _id: 0
        }
    }
]);
```

---

### 2.5 Indexes in MongoDB

**Types of Indexes:**

```javascript
// Single field index
db.users.createIndex({ email: 1 });  // 1 = ASC, -1 = DESC

// Compound index
db.users.createIndex({ lastName: 1, firstName: 1 });

// Multikey index (automatically created for arrays)
db.users.createIndex({ tags: 1 });

// Text index
db.posts.createIndex({ title: "text", content: "text" });

// Geospatial index
db.places.createIndex({ location: "2dsphere" });

// Hashed index (for sharding)
db.users.createIndex({ userId: "hashed" });

// Unique index
db.users.createIndex({ email: 1 }, { unique: true });

// Partial index (only on subset)
db.users.createIndex(
    { email: 1 },
    { partialFilterExpression: { status: "active" } }
);

// TTL index (auto-expire documents)
db.logs.createIndex(
    { createdAt: 1 },
    { expireAfterSeconds: 3600 }  // Expire after 1 hour
);
```

**Index Management:**

```javascript
// List indexes
db.users.getIndexes();

// Drop index
db.users.dropIndex("email_1");

// Drop all indexes (except _id)
db.users.dropIndexes();

// Analyze query performance
db.users.find({ email: "test@example.com" }).explain("executionStats");
```

---

### 2.6 Aggregation Pipeline

**Common Stages:**

```javascript
// $match (filter)
db.orders.aggregate([
    { $match: { status: "completed", amount: { $gte: 100 } } }
]);

// $group (aggregate)
db.orders.aggregate([
    {
        $group: {
            _id: "$customerId",
            totalAmount: { $sum: "$amount" },
            avgAmount: { $avg: "$amount" },
            orderCount: { $sum: 1 },
            maxAmount: { $max: "$amount" }
        }
    }
]);

// $sort
db.orders.aggregate([
    { $sort: { createdAt: -1 } }
]);

// $limit, $skip
db.orders.aggregate([
    { $skip: 10 },
    { $limit: 5 }
]);

// $project (transform)
db.users.aggregate([
    {
        $project: {
            fullName: { $concat: ["$firstName", " ", "$lastName"] },
            email: 1,
            isActive: { $eq: ["$status", "active"] }
        }
    }
]);

// $unwind (deconstruct array)
db.posts.aggregate([
    { $unwind: "$tags" }
]);

// $lookup (left outer join)
db.orders.aggregate([
    {
        $lookup: {
            from: "customers",
            localField: "customerId",
            foreignField: "_id",
            as: "customer"
        }
    },
    { $unwind: "$customer" }
]);

// $facet (multiple pipelines)
db.products.aggregate([
    {
        $facet: {
            "byCategory": [
                { $group: { _id: "$category", count: { $sum: 1 } } }
            ],
            "byPriceRange": [
                {
                    $bucket: {
                        groupBy: "$price",
                        boundaries: [0, 50, 100, 200],
                        default: "Other",
                        output: { count: { $sum: 1 } }
                    }
                }
            ]
        }
    }
]);
```

**Aggregation Operators:**

```javascript
// Arithmetic
{ $add: ["$price", "$tax"] }
{ $subtract: ["$price", "$discount"] }
{ $multiply: ["$price", 1.1] }
{ $divide: ["$total", "$quantity"] }

// String
{ $concat: ["$firstName", " ", "$lastName"] }
{ $substr: ["$name", 0, 3] }
{ $toUpper: "$name" }
{ $toLower: "$email" }

// Array
{ $size: "$tags" }
{ $slice: ["$items", 5] }
{ $concatArrays: ["$arr1", "$arr2"] }
{ $map: { input: "$items", as: "item", in: "$$item.name" } }

// Conditional
{
    $cond: {
        if: { $gte: ["$amount", 100] },
        then: "high",
        else: "low"
    }
}
{ $switch: {
    branches: [
        { case: { $gte: ["$score", 90] }, then: "A" },
        { case: { $gte: ["$score", 80] }, then: "B" }
    ],
    default: "F"
}}
{ $ifNull: ["$nickname", "$name"] }
```

---

### 2.7 MongoDB Security

**Role-Based Access Control (RBAC):**

```javascript
// Create role
db.createRole({
    role: "readWriteUsers",
    privileges: [
        {
            resource: { db: "mydb", collection: "users" },
            actions: ["find", "insert", "update", "remove"]
        }
    ],
    roles: []
});

// Create user
db.createUser({
    user: "appUser",
    pwd: "securePassword",
    roles: [
        { role: "readWriteUsers", db: "mydb" },
        { role: "read", db: "analytics" }
    ]
});

// Grant role
db.grantRolesToUser("appUser", [{ role: "dbAdmin", db: "mydb" }]);

// Revoke role
db.revokeRolesFromUser("appUser", [{ role: "dbAdmin", db: "mydb" }]);

// Update user
db.updateUser("appUser", { pwd: "newPassword" });

// Drop user
db.dropUser("appUser");
```

**Built-in Roles:**
- `read` - Read-only access
- `readWrite` - Read and write access
- `dbAdmin` - Database administration
- `userAdmin` - User management
- `clusterAdmin` - Cluster management
- `root` - Superuser (all privileges)

---

### 2.8 Replication & High Availability

**Replica Set:**
- Group of mongod processes maintaining same dataset
- 1 Primary (receives writes)
- Multiple Secondaries (replicate from primary)
- Automatic failover

**Replica Set Configuration:**

```javascript
// Initialize replica set
rs.initiate({
    _id: "rs0",
    members: [
        { _id: 0, host: "mongo1:27017" },
        { _id: 1, host: "mongo2:27017" },
        { _id: 2, host: "mongo3:27017" }
    ]
});

// Check status
rs.status();

// Add member
rs.add("mongo4:27017");

// Remove member
rs.remove("mongo4:27017");

// Force reconfiguration
rs.reconfig({...}, {force: true});
```

**Read Preferences:**

```javascript
// Read from primary (default)
db.collection.find().readPref("primary");

// Read from secondary
db.collection.find().readPref("secondary");

// Read from nearest
db.collection.find().readPref("nearest");

// Read from secondary with tags
db.collection.find().readPref(
    "secondary",
    [{ dc: "us-east", rack: "r1" }]
);
```

---

### 2.9 Sharding (Horizontal Scaling)

**Sharding Components:**
- **Shard** - Stores subset of data
- **Mongos** - Query router
- **Config Server** - Stores metadata

**Enable Sharding:**

```javascript
// Connect to mongos
mongos> use admin
mongos> db.enableSharding("mydb");

// Shard collection with shard key
mongos> db.adminCommand({
    shardCollection: "mydb.users",
    key: { userId: "hashed" }
});

// Shard key types:
// - Ranged: { userId: 1 }
// - Hashed: { userId: "hashed" }
// - Compound: { userId: 1, createdAt: -1 }
```

**Shard Key Selection:**
- ✅ High cardinality (many unique values)
- ✅ Evenly distributed writes
- ✅ Supports common query patterns
- ❌ Low cardinality (e.g., status, gender)
- ❌ Monotonically increasing (e.g., createdAt, auto-increment)

---

### 2.10 Backup & Recovery

**mongodump:**

```bash
# Backup entire database
mongodump --db mydb --out /backup/

# Backup specific collection
mongodump --db mydb --collection users --out /backup/

# Backup with authentication
mongodump --db mydb --username admin --password pwd --authenticationDatabase admin

# Compressed backup
mongodump --db mydb --gzip --out /backup/
```

**mongorestore:**

```bash
# Restore entire database
mongorestore /backup/mydb

# Restore specific collection
mongorestore --db mydb --collection users /backup/mydb/users.bson

# Drop existing before restore
mongorestore --drop /backup/mydb
```

---

## PHẦN 3: JPA/HIBERNATE INTEGRATION

### 3.1 When to use SQL vs MongoDB vs JPA

| Use Case | Recommended Approach |
|----------|---------------------|
| Complex transactions | SQL + JPA |
| Reporting/Analytics | SQL (direct queries) |
| Rapid prototyping | MongoDB |
| Content/Catalog management | MongoDB |
| High write throughput | MongoDB |
| Complex relationships | SQL + JPA |
| Event logging | MongoDB |
| Real-time data | MongoDB |

### 3.2 Spring Data JPA vs Spring Data MongoDB

**Spring Data JPA:**
```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByStatus(String status);
    List<User> findByAgeGreaterThan(int age);
    @Query("SELECT u FROM User u WHERE u.email = :email")
    Optional<User> findByEmail(@Param("email") String email);
}
```

**Spring Data MongoDB:**
```java
public interface UserRepository extends MongoRepository<User, String> {
    List<User> findByStatus(String status);
    List<User> findByAgeGreaterThan(int age);
    @Query("{ 'email': ?0 }")
    Optional<User> findByEmail(String email);
}
```

---

## TÓM TẮT

Sau khi học xong phần này, bạn cần nắm được:

### SQL
1. ✅ DDL, DML, DCL, TCL commands
2. ✅ JOINs (INNER, LEFT, RIGHT, FULL, CROSS, SELF)
3. ✅ Aggregate functions & GROUP BY
4. ✅ Subqueries (scalar, column, row, table, correlated)
5. ✅ Window functions (ROW_NUMBER, RANK, LEAD, LAG)
6. ✅ CTEs (including recursive)
7. ✅ Indexes & query optimization
8. ✅ Transactions & ACID properties

### MongoDB
1. ✅ BSON data types
2. ✅ CRUD operations
3. ✅ Query operators
4. ✅ Indexes (single, compound, text, geospatial, TTL)
5. ✅ Aggregation pipeline
6. ✅ Replication & sharding
7. ✅ Security & RBAC

### Next Steps
- Đọc `02-examples.md` để xem code mẫu
- Làm bài tập ở `03-exercises.md`

---

## 📚 TÀI LIỆU THAM KHẢO

### SQL Fundamentals & Query Optimization

| Resource | Link | Nội dung |
|----------|------|----------|
| Use The Index, Luke | [usetheindexluke.com](https://use-the-index-luke.com/) | SQL performance, indexing, query optimization |
| SQL Tutorial | [SQLZoo](https://sqlzoo.net/) | Interactive SQL exercises |
| PostgreSQL Tutorial | [postgresqltutorial.com](https://www.postgresqltutorial.com/) | Comprehensive PostgreSQL guide |

### Advanced SQL & Performance

| Resource | Link | Nội dung |
|----------|------|----------|
| Explain Analyze | [explain.depesz.com](https://explain.depesz.com/) | Visualize EXPLAIN output |
| SQL Performance Tuning | [Brent Ozar](https://www.brentozar.com/) | SQL Server performance tips |
| 10 Tips for Optimal PostgreSQL Indexes | [cybertec-postgresql.com](https://www.cybertec-postgresql.com/en/10-tips-for-optimal-postgresql-indexes/) | Index best practices |

### MongoDB

| Resource | Link | Nội dung |
|----------|------|----------|
| MongoDB University | [university.mongodb.com](https://university.mongodb.com/) | Free MongoDB courses |
| MongoDB Manual | [mongodb.com/docs](https://www.mongodb.com/docs/manual/) | Official documentation |
| MongoDB Schema Design | [mongodb.com/docs](https://www.mongodb.com/docs/manual/data-modeling/) | Embedded vs referenced data |

### JPA/Hibernate

| Resource | Link | Nội dung |
|----------|------|----------|
| Vlad Mihalcea Blog | [vladmihalcea.com](https://vladmihalcea.com/) | Hibernate performance, best practices |
| Hypersistence Utils | [vladmihalcea.com/hypersistence-utils](https://vladmihalcea.com/hypersistence-utils/) | Additional Hibernate utilities |
| JPA Buddy | [jpa-buddy.com](https://jpa-buddy.com/) | JPA tools and tutorials |
| Hibernate User Guide | [hibernate.org](https://hibernate.org/orm/documentation/) | Official Hibernate docs |

### Database Design

| Resource | Link | Nội dung |
|----------|------|----------|
| Database Design Best Practices | [Microsoft](https://learn.microsoft.com/en-us/sql/relational-databases/database-design/database-design-best-practices) | Relational design patterns |
| Normalization | [wikipedia.org](https://en.wikipedia.org/wiki/Database_normalization) | 1NF, 2NF, 3NF, BCNF explained |
