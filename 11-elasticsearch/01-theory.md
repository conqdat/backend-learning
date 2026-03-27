# Elasticsearch - Theory

> **Thời gian:** 3 tuần
> **Mục tiêu:** Master Elasticsearch cho search và analytics
>
> **Tham khảo:** [roadmap.sh/elasticsearch](https://roadmap.sh/elasticsearch)

---

## 📚 BÀI 0: ELASTICSEARCH OVERVIEW

### 0.1 What is Elasticsearch?

```
Elasticsearch = Distributed search & analytics engine

Đặc điểm:
- Built on Apache Lucene
- Schema-free (NoSQL document store)
- Distributed by default
- Near real-time search
- RESTful API
```

**Search Engines vs Relational DBs:**

| Aspect | Search Engine | Relational DB |
|--------|--------------|---------------|
| Primary Use | Full-text search | Transactional operations |
| Query Type | Fuzzy, relevance-based | Exact match, joins |
| Scaling | Horizontal (sharding) | Vertical (mostly) |
| Schema | Dynamic/flexible | Rigid schema |
| Performance | Fast search, slower writes | Fast writes, limited search |

---

### 0.2 The ELK Stack

```
┌─────────────────────────────────────────────────────────────┐
│                      ELK STACK                               │
├─────────────────────────────────────────────────────────────┤
│  Elasticsearch  ← Search & Analytics Engine                 │
│  Logstash       ← Data Processing Pipeline                  │
│  Kibana         ← Visualization & Dashboard                  │
│  Beats          ← Lightweight Data Shippers                 │
└─────────────────────────────────────────────────────────────┘
```

**Use Cases:**
- Full-text search (e-commerce, content sites)
- Log analytics (application logs, security logs)
- Metrics monitoring (infrastructure, APM)
- Autocomplete/suggestions
- Geospatial search

---

### 0.3 Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ELASTICSEARCH ARCHITECTURE                │
├─────────────────────────────────────────────────────────────┤
│  Cluster (System)                                           │
│    └── Node 1 (Master-eligible)                             │
│    └── Node 2 (Data Node)                                   │
│        └── Index (Database)                                 │
│            └── Shard 0 (Primary)                            │
│            └── Shard 1 (Replica)                            │
│                └── Document (Row)                           │
│                    └── Field (Column)                       │
└─────────────────────────────────────────────────────────────┘
```

**Node Types:**
- **Master-eligible**: Can be elected as master node
- **Data Nodes**: Store data, handle CRUD operations
- **Coordinating Nodes**: Route requests, handle aggregations

---

### 0.4 Sharding & Scaling

```
┌─────────────────────────────────────────────────────────────┐
│                    SHARDING STRATEGY                         │
├─────────────────────────────────────────────────────────────┤
│  Primary Shards:                                             │
│  - Determined at index creation                              │
│  - Cannot be changed later                                   │
│  - Default: 1 shard per index                                │
├─────────────────────────────────────────────────────────────┤
│  Replica Shards:                                             │
│  - Can be changed dynamically                                │
│  - Provide redundancy & read scaling                         │
│  - Default: 1 replica per primary                            │
├─────────────────────────────────────────────────────────────┤
│  Split Brain Problem:                                        │
│  - Occurs when cluster splits into multiple masters          │
│  - Prevention: minimum_master_nodes = (N/2) + 1             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 BÀI 1: DATA MODELLING

### 1.1 Mappings

**Explicit Mapping (Recommended):**
```json
PUT /products
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "price": { "type": "double" },
      "created_at": { "type": "date" },
      "category": { "type": "keyword" },
      "description": {
        "type": "text",
        "analyzer": "standard"
      }
    }
  }
}
```

**Dynamic Mapping:**
```json
// Elasticsearch auto-detects field types
// ⚠️ Warning: Can lead to "Mapping Explosion"
// Too many unique fields = performance issues
```

---

### 1.2 Data Types

**Core Data Types:**

| Type | Use Case | Example |
|------|----------|---------|
| `text` | Full-text search | Product description |
| `keyword` | Exact match, aggregations | Category, status |
| `numeric` | Numbers | Price, quantity |
| `date` | Dates/times | Created_at |
| `boolean` | True/false | In_stock |
| `geo_point` | Geolocation | Store location |
| `object` | Nested JSON | Metadata |
| `nested` | Array of objects | Tags with scores |
| `flattened` | Unknown structure | Logs |

**Text vs Keyword:**
```
text:
- Analyzed (tokenized)
- Used for full-text search
- "Hello World" → ["hello", "world"]

keyword:
- Not analyzed (stored as-is)
- Used for exact match, sorting, aggregations
- "Hello World" → "Hello World"
```

---

## 📚 BÀI 2: DATA INGESTION

### 2.1 CRUD Operations

```json
// Create Index
PUT /products

// Index Document (with auto ID)
POST /products/_doc
{
  "name": "Laptop",
  "price": 999.99,
  "category": "Electronics"
}

// Index Document (with specific ID)
PUT /products/_doc/1
{
  "name": "Laptop",
  "price": 999.99
}

// Get Document
GET /products/_doc/1

// Update Document
POST /products/_update/1
{
  "doc": {
    "price": 899.99
  }
}

// Delete Document
DELETE /products/_doc/1

// Delete Index
DELETE /products
```

---

### 2.2 Bulk Operations

```json
// Bulk Index (efficient for large datasets)
POST /_bulk
{ "index": { "_index": "products", "_id": "1" } }
{ "name": "Laptop", "price": 999.99 }
{ "index": { "_index": "products", "_id": "2" } }
{ "name": "Mouse", "price": 29.99 }
{ "index": { "_index": "products", "_id": "3" } }
{ "name": "Keyboard", "price": 79.99 }

// Optimizing Bulk Indexing:
// - Batch size: 5-15MB per batch
// - Parallelize from multiple threads
// - Disable refresh interval during bulk load
PUT /products/_settings
{ "index": { "refresh_interval": "-1" } }
```

**Reindex API:**
```json
// Copy data from one index to another
POST /_reindex
{
  "source": { "index": "products-old" },
  "dest": { "index": "products-new" }
}
```

---

## 📚 BÀI 3: SEARCH FUNDAMENTALS

### 3.1 Query Languages

| Language | Use Case |
|----------|----------|
| **EQL** | Event/query sequence search (security) |
| **SQL** | SQL-like queries |
| **ES\|QL** | New query language (Elastic 8.x+) |
| **KQL** | Kibana Query Language (UI) |
| **Lucene** | Low-level query syntax |
| **DSL** | Full Elasticsearch Query DSL |

---

### 3.2 Search Contexts

```
Query Context:
- Calculates relevance score (_score)
- Used for: full-text search, relevance ranking

Filter Context:
- Binary match/no-match (score = 0 or 1)
- Cacheable
- Used for: exact match, ranges, terms
```

---

### 3.3 Leaf Queries

```json
// Match Query (full-text)
GET /products/_search
{
  "query": {
    "match": {
      "description": "wireless keyboard"
    }
  }
}

// Term Query (exact match)
GET /products/_search
{
  "query": {
    "term": {
      "category": "Electronics"
    }
  }
}

// Range Query
GET /products/_search
{
  "query": {
    "range": {
      "price": {
        "gte": 50,
        "lte": 200
      }
    }
  }
}

// Prefix Query
GET /products/_search
{
  "query": {
    "prefix": {
      "name": { "value": "lap" }
    }
  }
}

// Wildcard Query
GET /products/_search
{
  "query": {
    "wildcard": {
      "name": { "value": "*book*" }
    }
  }
}

// Exists Query
GET /products/_search
{
  "query": {
    "exists": {
      "field": "discount"
    }
  }
}

// IDs Query
GET /products/_search
{
  "query": {
    "ids": {
      "values": ["1", "2", "3"]
    }
  }
}
```

---

### 3.4 Bool Queries (Compound)

```json
GET /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "description": "wireless" } }
      ],
      "must_not": [
        { "term": { "category": "Refurbished" } }
      ],
      "should": [
        { "term": { "brand": "Logitech" } },
        { "term": { "brand": "Razer" } }
      ],
      "filter": [
        { "range": { "price": { "lte": 100 } } }
      ]
    }
  }
}
```

**Bool Clauses:**
- `must`: Must match, contributes to score
- `must_not`: Must NOT match
- `should`: Should match (optional), boosts score
- `filter`: Must match, cached, no scoring

---

### 3.5 How Search Works

**The Inverted Index:**
```
Documents:
1: "The quick brown fox"
2: "The quick brown dog"
3: "The lazy dog"

Inverted Index:
Term      → Doc IDs
"the"     → [1, 2, 3]
"quick"   → [1, 2]
"brown"   → [1, 2]
"fox"     → [1]
"dog"     → [2, 3]
"lazy"    → [3]

Search "quick fox" → Docs [1]
```

**Doc Values:**
- Column-oriented storage
- Used for sorting, aggregations, filters
- Stored on disk (unlike inverted index in memory)

---

## 📚 BÀI 4: CONTROLLING SEARCH RESULTS

### 4.1 Pagination

```json
// From/Size (for early pages)
GET /products/_search
{
  "from": 0,
  "size": 10
}

// Search After (for deep pagination)
GET /products/_search
{
  "size": 10,
  "sort": [{ "price": "asc" }],
  "search_after": [999.99, "product-123"]
}
```

---

### 4.2 Source Filtering

```json
GET /products/_search
{
  "_source": ["name", "price"],
  "query": {
    "match_all": {}
  }
}

// Exclude fields
GET /products/_search
{
  "_source": {
    "exclude": ["description", "metadata"]
  }
}
```

---

### 4.3 Sorting

```json
GET /products/_search
{
  "sort": [
    { "price": { "order": "asc" } },
    { "created_at": { "order": "desc" } },
    { "_score": "desc" }
  ]
}
```

---

### 4.4 Highlighting

```json
GET /products/_search
{
  "query": {
    "match": { "description": "wireless" }
  },
  "highlight": {
    "fields": {
      "description": {
        "pre_tags": ["<em>"],
        "post_tags": ["</em>"]
      }
    }
  }
}

// Response includes:
"highlight": {
  "description": ["<em>Wireless</em> mechanical keyboard"]
}
```

---

## 📚 BÀI 5: TEXT ANALYSIS

### 5.1 Analyzers

```
Analyzer = Tokenizer + Token Filters

Standard Analyzer:
Input:  "The Quick Brown Fox"
Output: ["quick", "brown", "fox"]

Steps:
1. Character filters (remove HTML, etc.)
2. Tokenizer (split into tokens)
3. Token filters (lowercase, remove stopwords, stem)
```

---

### 5.2 The Analyze API

```json
// Test how analyzer processes text
POST /_analyze
{
  "analyzer": "standard",
  "text": "The Quick Brown Fox"
}

// Response
{
  "tokens": [
    { "token": "the", "position": 0 },
    { "token": "quick", "position": 1 },
    { "token": "brown", "position": 2 },
    { "token": "fox", "position": 3 }
  ]
}
```

---

### 5.3 Custom Analyzers

```json
PUT /my-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "stop",
            "my_stopwords"
          ]
        }
      },
      "filter": {
        "my_stopwords": {
          "type": "stop",
          "stopwords": ["foo", "bar"]
        }
      }
    }
  }
}
```

---

## 📚 BÀI 6: AGGREGATIONS

### 6.1 Metric Aggregations

```json
GET /products/_search
{
  "size": 0,
  "aggs": {
    "avg_price": { "avg": { "field": "price" } },
    "min_price": { "min": { "field": "price" } },
    "max_price": { "max": { "field": "price" } },
    "total_revenue": { "sum": { "field": "price" } },
    "product_count": { "value_count": { "field": "product_id" } },
    "unique_categories": { "cardinality": { "field": "category" } },
    "price_stats": { "stats": { "field": "price" } },
    "extended_stats": { "extended_stats": { "field": "price" } }
  }
}
```

---

### 6.2 Bucket Aggregations

```json
// Terms Aggregation
GET /products/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": { "field": "category" }
    }
  }
}

// Range Aggregation
GET /products/_search
{
  "size": 0,
  "aggs": {
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          { "to": 50, "key": "cheap" },
          { "from": 50, "to": 200, "key": "moderate" },
          { "from": 200, "key": "expensive" }
        ]
      }
    }
  }
}

// Date Range Aggregation
GET /products/_search
{
  "size": 0,
  "aggs": {
    "products_by_date": {
      "date_range": {
        "field": "created_at",
        "ranges": [
          { "from": "now-1M", "to": "now", "key": "last_month" },
          { "from": "now-1y", "to": "now-1M", "key": "last_year" }
        ]
      }
    }
  }
}
```

---

### 6.3 Nested Aggregations

```json
GET /products/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": { "field": "category" },
      "aggs": {
        "avg_price": { "avg": { "field": "price" } },
        "price_range": {
          "range": {
            "field": "price",
            "ranges": [
              { "to": 50 },
              { "from": 50, "to": 200 },
              { "from": 200 }
            ]
          }
        }
      }
    }
  }
}
```

---

### 6.4 Pipeline Aggregations

```json
GET /sales/_search
{
  "size": 0,
  "aggs": {
    "sales_per_month": {
      "date_histogram": {
        "field": "date",
        "calendar_interval": "month"
      },
      "aggs": {
        "total_sales": { "sum": { "field": "price" } }
      }
    },
    "moving_avg": {
      "moving_fn": {
        "buckets_path": "sales_per_month>total_sales",
        "script": "MovingAverage.agg(values)"
      }
    }
  }
}
```

---

## 📚 BÀI 7: RELEVANCE & TUNING

### 7.1 BM25 Scoring

```
Similarity Score based on:
- Term Frequency (TF): How often term appears in document
- Inverse Document Frequency (IDF): How rare term is across corpus
- Field length normalization: Shorter fields = higher score

BM25 = Modern relevance scoring algorithm
```

---

### 7.2 Boosting Queries

```json
// Field-level boosting
GET /products/_search
{
  "query": {
    "multi_match": {
      "query": "wireless keyboard",
      "fields": [
        "name^3",        // 3x boost
        "description^1",
        "category^0.5"   // 0.5x boost
      ]
    }
  }
}

// Query-level boosting
GET /products/_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "name": "keyboard" } },
        {
          "match": { "description": "keyboard" },
          "boost": 0.5
        }
      ]
    }
  }
}
```

---

### 7.3 Function Score Query

```json
GET /products/_search
{
  "query": {
    "function_score": {
      "query": { "match": { "name": "keyboard" } },
      "functions": [
        {
          "filter": { "range": { "rating": { "gte": 4 } } },
          "weight": 2
        },
        {
          "gauss": {
            "created_at": {
              "origin": "now",
              "scale": "30d",
              "decay": 0.5
            }
          }
        }
      ],
      "score_mode": "sum",
      "boost_mode": "multiply"
    }
  }
}
```

---

### 7.4 Synonyms

```json
PUT /my-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_synonym_filter": {
          "type": "synonym",
          "synonyms": [
            "laptop, notebook, computer",
            "phone, mobile, smartphone",
            "tv, television"
          ]
        }
      },
      "analyzer": {
        "my_synonym_analyzer": {
          "tokenizer": "standard",
          "filter": ["lowercase", "my_synonym_filter"]
        }
      }
    }
  }
}
```

---

## 📚 BÀI 8: PRODUCTION OPERATIONS

### 8.1 CAT APIs

```bash
# Cluster health
GET /_cat/health?v

# Node stats
GET /_cat/nodes?v

# Index stats
GET /_cat/indices?v

# Shard distribution
GET /_cat/shards?v

# Recovery status
GET /_cat/recovery?v

# Thread pool stats
GET /_cat/thread_pool?v
```

---

### 8.2 Cluster Monitoring

```json
// Cluster health
GET /_cluster/health

// Response
{
  "status": "green",  // green/yellow/red
  "number_of_nodes": 5,
  "number_of_data_nodes": 3,
  "active_shards": 100,
  "relocating_shards": 0,
  "unassigned_shards": 0
}

// Node stats
GET /_nodes/stats
```

---

### 8.3 Index Lifecycle Management (ILM)

```json
// ILM Policy
PUT /_ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "50gb",
            "max_age": "7d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}

// Apply to index template
PUT /_index_template/logs-template
{
  "template": {
    "settings": {
      "index.lifecycle.name": "logs-policy"
    }
  }
}
```

---

### 8.4 Snapshots & Restore

```json
// Register snapshot repository
PUT /_snapshot/my-s3-repository
{
  "type": "s3",
  "settings": {
    "bucket": "my-es-backups",
    "region": "us-east-1"
  }
}

// Create snapshot
PUT /_snapshot/my-s3-repository/snapshot-1
{
  "indices": "logs-2024.*",
  "ignore_unavailable": true,
  "include_global_state": false
}

// Restore snapshot
POST /_snapshot/my-s3-repository/snapshot-1/_restore
{
  "indices": "logs-2024.01",
  "include_global_state": false
}
```

---

## 📚 BÀI 9: SECURITY

### 9.1 Authentication

```bash
# Create API Key
POST /_security/api_key
{
  "name": "my-app-key",
  "role_descriptors": {
    "product-reader": {
      "cluster": [],
      "index": [
        {
          "names": ["products-*"],
          "privileges": ["read"]
        }
      ]
    }
  }
}

# Response includes API key to use in Authorization header
```

---

### 9.2 Roles & Users

```json
// Create Role
PUT /_security/role/product_reader
{
  "indices": [
    {
      "names": ["products-*"],
      "privileges": ["read", "search"]
    }
  ]
}

// Create User
PUT /_security/user/analyst
{
  "password": "secure_password",
  "roles": ["product_reader"],
  "full_name": "Data Analyst"
}
```

---

## 📚 BÀI 10: AI-POWERED SEARCH

### 10.1 Vector Search

```json
// Create index with dense_vector field
PUT /products-vectors
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "embedding": {
        "type": "dense_vector",
        "dims": 384
      }
    }
  }
}

// KNN Search
GET /products-vectors/_search
{
  "knn": {
    "field": "embedding",
    "query_vector": [0.1, 0.2, ...],
    "k": 10,
    "num_candidates": 100
  }
}
```

---

### 10.2 Semantic Search

```
Semantic Search = Understanding meaning, not just keywords

Approach:
1. Convert queries/documents to vectors (embeddings)
2. Find similar vectors using cosine similarity
3. Combine with keyword search (hybrid)

Models:
- E5 (Microsoft)
- Sentence Transformers
- OpenAI embeddings
```

---

### 10.3 Hybrid Search

```json
// Combine keyword + vector search
GET /products/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "multi_match": {
            "query": "wireless keyboard",
            "fields": ["name", "description"]
          }
        },
        {
          "knn": {
            "field": "embedding",
            "query_vector": [...],
            "k": 10
          }
        }
      ]
    }
  }
}
```

---

## 📝 TÓM TẮT

| Category | Key Concepts |
|----------|-------------|
| Architecture | Cluster, Node, Index, Shard, Document |
| Data Types | text, keyword, numeric, date, geo_point, nested |
| Search | Query DSL, Bool queries, Filters, Scoring |
| Aggregations | Metrics, Buckets, Nested, Pipeline |
| Text Analysis | Analyzers, Tokenizers, Token Filters |
| Production | ILM, Snapshots, Monitoring, Security |
| Advanced | Vector search, Semantic search, Hybrid |

---

## 🔜 TIẾP THEO

Xem `02-examples.md` để xem Spring Data Elasticsearch examples!
