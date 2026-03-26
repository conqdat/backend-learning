# Phase 8: Capstone Project - E-commerce Platform

> **Thời gian:** 4 tuần
> **Mục tiêu:** Apply TẤT CẢ kiến thức từ Phase 1-7

---

## 📋 PROJECT OVERVIEW

### Build a Complete E-commerce Platform

**Yêu cầu business:**
- Users có thể browse products, add to cart, checkout
- Support multiple payment methods (credit card, PayPal)
- Inventory management
- Order tracking
- Email notifications
- Admin dashboard

**Technical requirements:**
- Microservices architecture (6-8 services)
- API Gateway
- Authentication với JWT
- Caching với Redis
- Async communication với Kafka
- Monitoring với Prometheus/Grafana
- Docker containerization

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                             │
│                    (Spring Cloud Gateway)                    │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  User Service │    │Product Service│    │ Order Service │
│  (PostgreSQL) │    │  (PostgreSQL) │    │  (PostgreSQL) │
│               │    │   + Redis     │    │               │
└───────────────┘    └───────────────┘    └───────┬───────┘
                                                  │
                    ┌─────────────────────────────┼──────────┐
                    │                             │          │
                    ▼                             ▼          ▼
            ┌───────────────┐            ┌───────────────┐
            │Payment Service│            │Inventory Svc  │
            │   (MongoDB)   │            │  (PostgreSQL) │
            └───────────────┘            └───────────────┘
                    │                             │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                          ┌────────────────┐
                          │  Kafka Broker  │
                          └────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌────────────┐ ┌────────────┐ ┌─────────────┐
            │Email Svc   │ │Analytics   │ │Notification │
            │            │ │Service     │ │Service      │
            └────────────┘ └────────────┘ └─────────────┘
```

---

## 📁 SERVICES CHI TIẾT

### 1. User Service

**Responsibilities:**
- User registration, login
- Profile management
- JWT token generation/validation
- Role management (USER, ADMIN)

**APIs:**
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh
GET    /api/users/me
PUT    /api/users/me
GET    /api/users/{id}
```

**Database:**
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

### 2. Product Service

**Responsibilities:**
- Product CRUD
- Category management
- Search products
- Product recommendations

**APIs:**
```
GET    /api/products
GET    /api/products/{id}
GET    /api/products/search?q=iphone
GET    /api/categories
POST   /api/products (ADMIN)
PUT    /api/products/{id} (ADMIN)
DELETE /api/products/{id} (ADMIN)
```

**Database:**
```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id BIGINT REFERENCES categories(id),
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
```

**Caching:**
- Products list: 5 minutes
- Product detail: 30 minutes
- Categories: 1 hour

---

### 3. Order Service

**Responsibilities:**
- Create orders
- Order status tracking
- Order history

**APIs:**
```
POST   /api/orders
GET    /api/orders/my-orders
GET    /api/orders/{id}
GET    /api/admin/orders (ADMIN)
PUT    /api/admin/orders/{id}/status (ADMIN)
```

**Database:**
```sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    total_amount DECIMAL(10,2) NOT NULL,
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id),
    product_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL
);
```

**Saga Pattern:**
```
Order Created → Payment Processing → Inventory Reserved → Shipment Created → Completed
                      ↓                        ↓                    ↓
                Payment Failed          Out of Stock        Shipping Error
                      ↓                        ↓                    ↓
                Order Cancelled ←──── Compensating Transactions ────┘
```

---

### 4. Payment Service

**Responsibilities:**
- Process payments
- Payment method integration (Stripe, PayPal)
- Payment history

**Events:**
```
Consumes: order-created
Produces: payment-processed, payment-failed
```

---

### 5. Inventory Service

**Responsibilities:**
- Stock management
- Reserve stock for orders
- Restock handling

**Events:**
```
Consumes: order-created, order-cancelled
Produces: stock-reserved, stock-insufficient
```

---

### 6. Notification Service

**Responsibilities:**
- Email notifications
- SMS notifications
- Push notifications

**Events:**
```
Consumes: order-created, payment-processed, order-shipped
```

---

## 📝 DELIVERABLES

### Week 1: Foundation
- [ ] Project scaffolding
- [ ] API Gateway setup
- [ ] User Service với JWT auth
- [ ] Docker Compose cho development

### Week 2: Core Services
- [ ] Product Service với Redis caching
- [ ] Order Service
- [ ] Kafka setup cho event-driven communication

### Week 3: Additional Services
- [ ] Payment Service (Stripe integration)
- [ ] Inventory Service
- [ ] Notification Service (email)
- [ ] Saga pattern implementation

### Week 4: Production Ready
- [ ] Prometheus + Grafana setup
- [ ] ELK Stack cho logging
- [ ] Circuit breakers
- [ ] Load testing
- [ ] Documentation

---

## 🎯 EVALUATION CRITERIA

| Criteria | Weight | Description |
|----------|--------|-------------|
| Architecture | 25% | Microservices design, separation of concerns |
| Code Quality | 20% | Clean code, patterns, best practices |
| Caching | 15% | Redis implementation, cache invalidation |
| Resilience | 15% | Circuit breakers, retry, fallbacks |
| Observability | 15% | Metrics, logging, tracing |
| Documentation | 10% | API docs, architecture docs, runbooks |

---

## 📤 SUBMISSION

Submit:
1. GitHub repository với full source code
2. Architecture diagram
3. README với setup instructions
4. Postman collection cho APIs
5. Demo video (optional)

---

## 🔥 BONUS POINTS

- [ ] Kubernetes deployment
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Performance optimization (connection pooling, query optimization)
- [ ] Security hardening (OWASP Top 10)
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] E2E tests

---

**Good luck! 🚀**

Sau khi hoàn thành, bạn sẽ có một portfolio project solid để show trong CV và interview!
