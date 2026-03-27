# Elasticsearch - Exercises

> **Mục tiêu:** Thực hành Elasticsearch qua các bài tập thực tế

---

## 📚 BÀI 1: SETUP & BASIC OPERATIONS

### Exercise 1.1: Install Elasticsearch với Docker

```bash
# TODO: Tạo docker-compose.yml để chạy Elasticsearch + Kibana
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - es-data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  es-data:
```

**Kiểm tra:**
```bash
docker-compose up -d
curl http://localhost:9200/_cluster/health
```

---

### Exercise 1.2: Index Operations

```json
// TODO: Tạo index với custom settings
PUT /products

// TODO: Thêm mapping cho các fields:
// - name (text với analyzer)
// - description (text)
// - category (keyword)
// - price (double)
// - created_at (date)
// - tags (nested)
// - location (geo_point)

// TODO: Index 10 sản phẩm mẫu
POST /products/_doc/1
{
  "name": "Laptop Pro 15",
  "description": "High-performance laptop for professionals",
  "category": "Electronics",
  "price": 1999.99,
  "created_at": "2024-01-15T10:00:00Z",
  "tags": [
    {"name": "laptop", "score": 1.0},
    {"name": "professional", "score": 0.8}
  ],
  "location": {
    "lat": 40.7128,
    "lon": -74.0060
  }
}

// TODO: Get, update, delete operations
```

---

## 📚 BÀI 2: SEARCH QUERIES

### Exercise 2.1: Basic Queries

```json
// 1. Tìm tất cả products trong category "Electronics"
GET /products/_search
{
  "query": {
    // TODO: Fill in
  }
}

// 2. Tìm products có price trong range 100-500
GET /products/_search
{
  "query": {
    // TODO: Fill in
  }
}

// 3. Tìm products có name chứa "laptop" (full-text search)
GET /products/_search
{
  "query": {
    // TODO: Fill in
  }
}

// 4. Tìm products với multiple criteria:
// - Category: Electronics
// - Price: 500-2000
// - Name contains "pro"
GET /products/_search
{
  "query": {
    // TODO: Fill in
  }
}
```

---

### Exercise 2.2: Advanced Queries

```json
// 1. Bool query với must, should, must_not, filter
// Tìm Electronics products, price < 1000, ưu tiên có tag "sale"
GET /products/_search
{
  "query": {
    "bool": {
      "must": [
        // TODO
      ],
      "should": [
        // TODO
      ],
      "must_not": [
        // TODO
      ],
      "filter": [
        // TODO
      ]
    }
  }
}

// 2. Multi-match query
// Search "wireless keyboard" trong name và description
GET /products/_search
{
  "query": {
    "multi_match": {
      "query": "wireless keyboard",
      "fields": // TODO
    }
  }
}

// 3. Nested query
// Tìm products có tag name là "gaming"
GET /products/_search
{
  "query": {
    "nested": {
      // TODO
    }
  }
}

// 4. Geo query
// Tìm products trong bán kính 10km từ NYC (40.7128, -74.0060)
GET /products/_search
{
  "query": {
    "geo_distance": {
      // TODO
    }
  }
}
```

---

## 📚 BÀI 3: AGGREGATIONS

### Exercise 3.1: Metric Aggregations

```json
// 1. Tính tổng số products
GET /products/_search
{
  "size": 0,
  "aggs": {
    "total_products": {
      // TODO
    }
  }
}

// 2. Tính trung bình giá
GET /products/_search
{
  "size": 0,
  "aggs": {
    "avg_price": {
      // TODO
    }
  }
}

// 3. Thống kê giá (min, max, avg, sum)
GET /products/_search
{
  "size": 0,
  "aggs": {
    "price_stats": {
      // TODO
    }
  }
}
```

---

### Exercise 3.2: Bucket Aggregations

```json
// 1. Group products by category
GET /products/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      // TODO
    }
  }
}

// 2. Group products by price ranges
// - Cheap: 0-100
// - Moderate: 100-500
// - Expensive: 500+
GET /products/_search
{
  "size": 0,
  "aggs": {
    "price_ranges": {
      // TODO
    }
  }
}

// 3. Nested aggregation:
// - Group by category
// - Trong mỗi category: tính avg_price và count
GET /products/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": { "field": "category" },
      "aggs": {
        // TODO
      }
    }
  }
}
```

---

## 📚 BÀI 4: TEXT ANALYSIS

### Exercise 4.1: Custom Analyzer

```json
// TODO: Tạo index với custom analyzer
// - Tokenizer: standard
// - Token filters: lowercase, stop (English), synonym (laptop=>notebook)
PUT /products-custom
{
  "settings": {
    "analysis": {
      // TODO
    }
  },
  "mappings": {
    // TODO
  }
}

// TODO: Test analyzer với Analyze API
POST /products-custom/_analyze
{
  "analyzer": "product_analyzer",
  "text": "The Quick Brown Laptop"
}

// TODO: So sánh kết quả search với và không có analyzer
```

---

### Exercise 4.2: Highlighting

```json
// TODO: Search với highlighting
// - Search "wireless" trong name và description
// - Highlight với <em> tags
// - Fragment size: 100 characters
// - Number of fragments: 3
GET /products/_search
{
  "query": {
    // TODO
  },
  "highlight": {
    // TODO
  }
}
```

---

## 📚 BÀI 5: BULK OPERATIONS & REINDEX

### Exercise 5.1: Bulk Indexing

```json
// TODO: Bulk index 100 products
// Sử dụng _bulk API với format:
// { "index": { "_index": "products", "_id": "1" } }
// { "name": "...", "price": ... }
// ...

// TODO: Optimize bulk indexing:
// - Disable refresh interval
// - Use appropriate batch size (5-15MB)
// - Enable refresh sau khi hoàn thành
```

---

### Exercise 5.2: Reindex

```json
// TODO: Tạo index mới với mapping cải thiện
PUT /products-v2
{
  "mappings": {
    // Improved mapping
  }
}

// TODO: Reindex từ products sang products-v2
POST /_reindex
{
  "source": {
    "index": "products"
  },
  "dest": {
    "index": "products-v2"
  }
}

// TODO: Verify reindex thành công
GET /products-v2/_count
GET /products/_count
```

---

## 📚 BÀI 6: SPRING DATA ELASTICSEARCH

### Exercise 6.1: Entity & Repository

```java
// TODO: Tạo Product entity với annotations
@Document(indexName = "products")
@Setting(shards = 3, replicas = 2)
public class Product {
    // TODO: Add fields with proper @Field annotations
}

// TODO: Tạo ProductRepository
@Repository
public interface ProductRepository extends ElasticsearchRepository<Product, String> {
    // TODO: Add query methods
    // - findByCategory
    // - findByPriceBetween
    // - searchByName
}
```

---

### Exercise 6.2: Service Layer

```java
@Service
public class ProductService {

    @Autowired
    private ProductRepository repository;

    // TODO: Implement search với pagination
    public Page<Product> search(String query, Pageable pageable) {
        // TODO
    }

    // TODO: Implement aggregation service
    public Map<String, Long> getProductsByCategory() {
        // TODO
    }

    // TODO: Implement bulk save
    public void bulkSave(List<Product> products) {
        // TODO
    }
}
```

---

## 📚 BÀI 7: PRODUCTION SCENARIOS

### Exercise 7.1: E-commerce Search

```
Scenario: Xây dựng search cho e-commerce site

Requirements:
1. Full-text search cho product name, description
2. Filter by category, price range, brand
3. Sort by relevance, price, rating
4. Autocomplete/suggestions
5. Faceted search (show counts for each filter)
6. Highlighting cho search terms

TODO:
- Design index mapping
- Implement search queries
- Implement aggregations for facets
- Implement suggestions
```

---

### Exercise 7.2: Log Analytics

```
Scenario: Phân tích logs với Elasticsearch

Data structure:
- timestamp
- level (INFO, WARN, ERROR)
- service
- message
- correlation_id
- metadata (nested)

Requirements:
1. Search logs by time range
2. Filter by log level, service
3. Count errors by service
4. Trace requests by correlation_id
5. Alert on error rate > threshold

TODO:
- Design log index mapping
- Implement search queries
- Implement aggregations
- Setup ILM policy
```

---

### Exercise 7.3: ILM Policy

```json
// TODO: Tạo ILM policy cho logs
// - Hot phase: 7 days, rollover at 50GB or 1 day
// - Warm phase: 7-30 days, shrink to 1 shard
// - Cold phase: 30-90 days, freeze
// - Delete phase: > 90 days

PUT /_ilm/policy/logs-policy
{
  "policy": {
    // TODO
  }
}

// TODO: Apply policy vào index template
PUT /_index_template/logs-template
{
  "indexPatterns": ["logs-*"],
  "template": {
    "settings": {
      // TODO
    }
  }
}
```

---

## 📝 CHECKLIST

Sau khi hoàn thành exercises:

- [ ] Cài đặt Elasticsearch thành công
- [ ] Tạo index với custom mapping
- [ ] Thực hiện CRUD operations
- [ ] Viết được các query: match, term, range, bool
- [ ] Sử dụng aggregations (metrics, buckets)
- [ ] Tạo custom analyzer
- [ ] Implement highlighting
- [ ] Bulk operations và reindex
- [ ] Spring Data Elasticsearch integration
- [ ] Setup ILM policy

---

## 🔗 TÀI LIỆU THAM KHẢO

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Spring Data Elasticsearch](https://spring.io/projects/spring-data-elasticsearch)
- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
- [roadmap.sh/elasticsearch](https://roadmap.sh/elasticsearch)
