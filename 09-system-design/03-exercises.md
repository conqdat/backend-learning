# Phase 09: System Design - Bài Tập Thực Hành

> **Thời gian:** 3-4 giờ
> **Mục tiêu:** Practice system design interviews và design scalable systems

---

## 📝 BÀI TẬP 1: DESIGN A PASTEBIN (1 giờ)

### Đề bài

Design a service like Pastebin.com where users can paste text and get a shareable URL.

### Requirements

**Functional:**
- User can paste text and get a unique URL
- User can optionally set expiration time
- User can optionally set password
- Others can view paste via URL

**Non-functional:**
- Pastes should be available immediately
- Read-heavy (100:1 read:write ratio)
- Support 1M pastes/day
- Paste size up to 10MB

### Bài tập

**1. Capacity Estimation:**
```
TODO: Calculate:
- QPS for writes
- QPS for reads
- Storage required for 5 years
- Bandwidth requirements
```

**2. API Design:**
```java
// TODO: Design REST API endpoints
POST /api/v1/pastes
GET /api/v1/pastes/{pasteId}
DELETE /api/v1/pastes/{pasteId}
```

**3. Database Schema:**
```sql
-- TODO: Design database tables
-- Consider: Should you use SQL or NoSQL?
```

**4. Algorithm:**
```java
// TODO: How to generate unique paste IDs?
// Options: UUID, Base62 encoding, Hash function
```

**5. Architecture Diagram:**
```
TODO: Draw architecture with:
- Load balancer
- Application servers
- Database
- Cache (if needed)
```

---

## 📝 BÀI TẬP 2: DESIGN A CHAT SYSTEM (1 giờ)

### Đề bài

Design a real-time chat system like WhatsApp/Slack.

### Requirements

**Functional:**
- Users can send/receive messages
- Support 1-on-1 and group chats
- Message history
- Online/offline status
- Read receipts

**Non-functional:**
- Messages should be delivered in < 100ms
- Support 1B users, 100M DAU
- Messages should not be lost
- Scale to 10B messages/day

### Bài tập

**1. Capacity Estimation:**
```
TODO: Calculate:
- Messages per second
- Storage for message history (1 year)
- Bandwidth requirements
- Connection requirements (WebSocket)
```

**2. Protocol Design:**
```
TODO: Choose protocol:
- WebSocket vs HTTP Long Polling vs Server-Sent Events
- Message format (JSON, Protocol Buffers)
```

**3. Data Model:**
```sql
-- TODO: Design schema for:
-- Users, Conversations, Messages, Participants
-- Consider: How to shard? What to cache?
```

**4. Architecture:**
```
TODO: Design architecture addressing:
- How to maintain WebSocket connections?
- How to route messages between users on different servers?
- How to handle reconnection/offline messages?
- Message queue for reliability?
```

**5. Message Flow:**
```
TODO: Draw sequence diagrams for:
- User A sends message to User B
- User B receives message
- User B reads message (read receipt)
```

---

## 📝 BÀI TẬP 3: DESIGN AN E-COMMERCE PLATFORM (1 giờ)

### Đề bài

Design a flash sale system like Shopee Flash Sale or Amazon Lightning Deals.

### Requirements

**Functional:**
- Users can browse products
- Users can add to cart and checkout
- Flash sales at specific times
- Limited quantity per flash sale
- Payment integration

**Non-functional:**
- Handle 10M concurrent users during flash sale
- Prevent overselling
- Low latency for product pages
- 99.99% availability during sales

### Bài tập

**1. Capacity Estimation:**
```
TODO: Calculate:
- Peak QPS during flash sale
- Database writes per second
- Cache requirements
- Bandwidth for product images
```

**2. Key Challenges:**
```
TODO: Design solutions for:
- Overselling prevention (distributed lock?)
- Inventory management
- Queue for checkout during peak
- Bot/Crawler prevention
```

**3. Database Schema:**
```sql
-- TODO: Design schema for:
-- Products, Inventory, Orders, OrderItems, FlashSales
-- Consider: How to handle high write load?
```

**4. Architecture:**
```
TODO: Design architecture with:
- CDN for static content
- Caching strategy (multi-level?)
- Message queue for order processing
- Database replication/sharding
```

**5. Flash Sale Flow:**
```
TODO: Design the checkout flow:
- User clicks "Buy Now" at flash sale time
- How to handle the rush?
- Queue design
- Inventory deduction
- Order creation
```

---

## 📝 BÀI TẬP 4: DESIGN A VIDEO STREAMING SERVICE (1 giờ)

### Đề bài

Design a video streaming platform like YouTube/Netflix.

### Requirements

**Functional:**
- Users can upload videos
- Users can watch videos
- Video recommendations
- Search functionality
- User subscriptions/channels

**Non-functional:**
- Support 1B users
- Video upload: 1M videos/day
- Video streaming: 100M concurrent viewers
- Low buffering, adaptive bitrate

### Bài tập

**1. Capacity Estimation:**
```
TODO: Calculate:
- Storage for videos (assume 10 min avg, 5Mbps)
- Bandwidth for streaming
- CDN requirements
- Transcoding requirements
```

**2. Video Processing Pipeline:**
```
TODO: Design pipeline for:
- Video upload
- Transcoding (multiple resolutions)
- Thumbnail generation
- Content moderation
```

**3. Storage Design:**
```
TODO: Decide:
- Where to store videos? (Object storage)
- Where to store metadata? (Database)
- How to serve videos globally? (CDN)
```

**4. Streaming Architecture:**
```
TODO: Design:
- Video player protocol (HLS, DASH)
- Adaptive bitrate streaming
- CDN integration
- Analytics for watch time
```

**5. Recommendation System:**
```
TODO: High-level design for:
- How to recommend videos?
- Real-time vs batch processing
- Features to consider
```

---

## 📝 BÀI TẬP 5: MOCK INTERVIEW PRACTICE (1 giờ)

### Đề bài

Practice system design interview với timer

### Instructions

**Chọn 1 trong các đề sau:**

1. Design a ride-sharing service (Uber/Grab)
2. Design a food delivery service (GrabFood/Now)
3. Design a hotel booking system (Booking.com)
4. Design a digital wallet (MoMo/PayPal)
5. Design a learning management system (Coursera/Udemy)

**Timer:**

```
┌─────────────────────────────────────────────────────────────┐
│              SYSTEM DESIGN INTERVIEW TIMER                   │
├─────────────────────────────────────────────────────────────┤
│  0-5 min:   Requirements Clarification                      │
│             - Ask questions                                  │
│             - Define scope                                   │
│                                                              │
│  5-10 min:  Back-of-envelope Estimation                     │
│             - QPS, storage, bandwidth                        │
│                                                              │
│  10-20 min: High-level Design                               │
│             - Core components                                │
│             - Data model                                     │
│             - API design                                     │
│                                                              │
│  20-35 min: Deep Dive                                        │
│             - Bottlenecks                                    │
│             - Scaling strategies                             │
│             - Trade-offs                                     │
│                                                              │
│  35-45 min: Summary                                          │
│             - Recap design                                   │
│             - Discuss improvements                           │
└─────────────────────────────────────────────────────────────┘
```

**Self-evaluation Checklist:**

```
Requirements:
[ ] Asked clarifying questions
[ ] Defined functional requirements
[ ] Defined non-functional requirements
[ ] Made reasonable assumptions

Estimation:
[ ] Calculated QPS
[ ] Calculated storage
[ ] Calculated bandwidth
[ ] Used round numbers for simplicity

Design:
[ ] Drew architecture diagram
[ ] Designed database schema
[ ] Designed API endpoints
[ ] Identified key components

Deep Dive:
[ ] Identified bottlenecks
[ ] Proposed scaling solutions
[ ] Discussed trade-offs
[ ] Considered failure scenarios

Communication:
[ ] Explained thinking clearly
[ ] Responded to feedback
[ ] Managed time well
```

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 09

- [ ] Hiểu CAP theorem và consistency models
- [ ] Tính được scale estimation (QPS, storage, bandwidth)
- [ ] Design được URL shortener
- [ ] Design được Rate limiter
- [ ] Design được Twitter/Instagram feed
- [ ] Practice Pastebin design
- [ ] Practice Chat system design
- [ ] Practice E-commerce flash sale design
- [ ] Practice Video streaming design
- [ ] Hoàn thành mock interview practice

---

## 📤 CÁCH SUBMIT

1. Tạo file `SYSTEM_DESIGN_NOTES.md` với:
   - Architecture diagrams cho các bài tập
   - Capacity calculations
   - Trade-off decisions

2. Record mock interview (optional):
   - Record yourself explaining a design
   - Review and identify areas for improvement

3. Gửi cho mentor review:
   - Design decisions
   - Questions you found challenging

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, bạn đã hoàn thành Phase 09!
Chuẩn bị cho Phase 10: Capstone Project!
