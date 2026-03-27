# Elasticsearch - Examples với Spring Data Elasticsearch

> **Mục tiêu:** Implement Elasticsearch trong Spring Boot applications

---

## 📚 BÀI 1: SPRING DATA ELASTICSEARCH SETUP

### 1.1 Dependencies

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
</dependency>

<!-- For high-level REST client -->
<dependency>
    <groupId>co.elastic.clients</groupId>
    <artifactId>elasticsearch-java</artifactId>
    <version>8.11.0</version>
</dependency>
```

### 1.2 Configuration

```yaml
# application.yml
spring:
  elasticsearch:
    uris: http://localhost:9200
    username: elastic
    password: changeme
    connection-timeout: 5s
    socket-timeout: 10s
```

```java
@Configuration
public class ElasticsearchConfig {

    @Bean
    public ElasticsearchClient elasticsearchClient(
            RestClientBuilder restClientBuilder) {
        return new ElasticsearchClient(restClientBuilder);
    }

    @Bean
    public RestClientBuilder restClientBuilder(
            @Value("${spring.elasticsearch.uris}") List<String> uris,
            @Value("${spring.elasticsearch.username}") String username,
            @Value("${spring.elasticsearch.password}") String password) {

        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(
            AuthScope.ANY,
            new UsernamePasswordCredentials(username, password)
        );

        return RestClient.builder(
                uris.stream().map(Host::create).toArray(Host[]::new))
            .setHttpClientConfigCallback(httpClientBuilder ->
                httpClientBuilder
                    .setDefaultCredentialsProvider(credentialsProvider)
                    .setSSLContext(SSLContexts.createDefault())
            );
    }
}
```

---

## 📚 BÀI 2: DOCUMENT MAPPING

### 2.1 Entity Class

```java
@Document(indexName = "products")
@Setting(shards = 3, replicas = 2)
public class Product {

    @Id
    private String id;

    @Field(type = FieldType.Text, analyzer = "standard")
    private String name;

    @Field(type = FieldType.Text, analyzer = "standard")
    private String description;

    @Field(type = FieldType.Keyword)
    private String category;

    @Field(type = FieldType.Double)
    private Double price;

    @Field(type = FieldType.Integer)
    private Integer quantity;

    @Field(type = FieldType.Boolean)
    private Boolean inStock;

    @Field(type = FieldType.Date, format = DateFormat.date_time)
    private LocalDateTime createdAt;

    @Field(type = FieldType.Nested)
    private List<Tag> tags;

    @Field(type = FieldType.GeoPoint)
    private GeoPoint location;

    // Constructors, getters, setters
}

@Document
public class Tag {
    @Field(type = FieldType.Keyword)
    private String name;

    @Field(type = FieldType.Double)
    private Double score;

    // Constructors, getters, setters
}
```

### 2.2 Custom Mapping

```java
@Configuration
public class ElasticsearchMappingConfig {

    @Bean
    public IndexManager indexManager(ElasticsearchClient client) {
        return new IndexManager(client);
    }
}

// Create index with custom mapping
public class IndexInitializer implements ApplicationRunner {

    private final ElasticsearchClient client;

    @Override
    public void run(ApplicationArguments args) {
        // Create index with custom settings
        client.indices().create(c -> c
            .index("products")
            .settings(s -> s
                .numberOfShards("3")
                .numberOfReplicas("2")
                .analysis(a -> a
                    .analyzer("product_analyzer", an -> an
                        .custom(b -> b
                            .tokenizer("standard")
                            .filter("lowercase", "stop", "synonym_filter")
                        )
                    )
                )
            )
            .mappings(m -> m
                .properties("name", p -> p
                    .type(FieldType.Text)
                    .analyzer("product_analyzer")
                )
                .properties("category", p -> p
                    .type(FieldType.Keyword)
                )
                .properties("description", p -> p
                    .type(FieldType.Text)
                    .analyzer("product_analyzer")
                )
                .properties("price", p -> p
                    .type(FieldType.Double)
                )
                .properties("location", p -> p
                    .type(FieldType.GeoPoint)
                )
            )
        );
    }
}
```

---

## 📚 BÀI 3: REPOSITORY LAYER

### 3.1 Elasticsearch Repository

```java
@Repository
public interface ProductRepository extends ElasticsearchRepository<Product, String> {

    // Basic query methods
    List<Product> findByCategory(String category);

    List<Product> findByPriceBetween(Double minPrice, Double maxPrice);

    List<Product> findByInStockTrue();

    // Full-text search
    List<Product> findByNameContaining(String keyword);

    // Combined queries
    List<Product> findByCategoryAndPriceLessThan(String category, Double price);

    // With sorting
    List<Product> findByCategoryOrderByPriceAsc(String category);

    // With Pageable
    Page<Product> findByCategory(String category, Pageable pageable);

    // Highlighting
    @Highlight(fields = {
        @HighlightField(name = "name"),
        @HighlightField(name = "description")
    })
    SearchHits<Product> searchByName(String name, Pageable pageable);
}
```

### 3.2 Custom Query with @Query

```java
@Repository
public interface ProductRepository extends ElasticsearchRepository<Product, String> {

    // Match query
    @Query("{\"match\": {\"name\": \"?0\"}}")
    List<Product> searchByName(String name);

    // Multi-match query
    @Query("{\"multi_match\": {\"query\": \"?0\", \"fields\": [\"name\", \"description\"]}}")
    List<Product> searchFullText(String query);

    // Bool query with filter
    @Query("{\"bool\": {\"must\": [{\"match\": {\"category\": \"?0\"}}], \"filter\": [{\"range\": {\"price\": {\"lte\": \"?1\"}}}]}}")
    List<Product> findByCategoryAndMaxPrice(String category, Double maxPrice);

    // Nested query
    @Query("{\"nested\": {\"path\": \"tags\", \"query\": {\"term\": {\"tags.name\": \"?0\"}}}}")
    List<Product> findByTagName(String tagName);

    // Geo query
    @Query("{\"geo_distance\": {\"distance\": \"?1km\", \"location\": {\"lat\": ?2, \"lon\": ?3}}}")
    List<Product> findNearby(Double lat, Double lon, Double distanceKm);
}
```

---

## 📚 BÀI 4: SERVICE LAYER

### 4.1 Product Service

```java
@Service
public class ProductService {

    private final ProductRepository repository;
    private final ElasticsearchOperations elasticsearchOperations;
    private final ElasticsearchClient client;

    public ProductService(ProductRepository repository,
                         ElasticsearchOperations elasticsearchOperations,
                         ElasticsearchClient client) {
        this.repository = repository;
        this.elasticsearchOperations = elasticsearchOperations;
        this.client = client;
    }

    // CRUD Operations
    public Product save(Product product) {
        return repository.save(product);
    }

    public Product findById(String id) {
        return repository.findById(id).orElse(null);
    }

    public void deleteById(String id) {
        repository.deleteById(id);
    }

    // Full-text search
    public List<Product> search(String query) {
        NativeQuery nativeQuery = NativeQuery.builder()
            .query(q -> q
                .multiMatch(mm -> mm
                    .query(query)
                    .fields("name^3", "description")
                )
            )
            .withPageable(PageRequest.of(0, 10))
            .build();

        SearchHits<Product> hits = elasticsearchOperations.search(nativeQuery, Product.class);
        return hits.getSearchHits().stream()
            .map(SearchHit::content)
            .toList();
    }

    // Aggregation
    public Map<String, Long> getProductsByCategory() {
        NativeQuery nativeQuery = NativeQuery.builder()
            .withQuery(q -> q.matchAll(m -> m))
            .withAggregation("categories", a -> a
                .terms(t -> t
                    .field("category")
                    .size(10)
                )
            )
            .build();

        SearchHits<Product> hits = elasticsearchOperations.search(nativeQuery, Product.class);
        AggregationsContainer aggregations = hits.getAggregations();

        // Process aggregation results
        return extractCategoryCounts(aggregations);
    }

    // Bulk operations
    public void bulkSave(List<Product> products) {
        List<BulkOperation> bulkOperations = products.stream()
            .map(p -> BulkOperation.of(b -> b
                .index(i -> i
                    .document(p)
                    .index("products")
                    .id(p.getId())
                )
            ))
            .toList();

        client.bulk(b -> b.operations(bulkOperations));
    }
}
```

---

## 📚 BÀI 5: ADVANCED SEARCH

### 5.1 Search with Filters and Facets

```java
@Service
public class ProductSearchService {

    public SearchResponse<Product> searchWithFilters(SearchRequest request) {
        NativeQuery.Builder queryBuilder = NativeQuery.builder()
            .withQuery(q -> q
                .multiMatch(mm -> mm
                    .query(request.getQuery())
                    .fields("name^3", "description", "category")
                )
            );

        // Apply filters
        if (request.getCategory() != null) {
            queryBuilder.withFilter(f -> f
                .term(t -> t
                    .field("category")
                    .value(request.getCategory())
                )
            );
        }

        if (request.getMinPrice() != null || request.getMaxPrice() != null) {
            queryBuilder.withFilter(f -> f
                .range(r -> r
                    .field("price")
                    .gte(request.getMinPrice() != null ? request.getMinPrice() : 0)
                    .lte(request.getMaxPrice() != null ? request.getMaxPrice() : Double.MAX_VALUE)
                )
            );
        }

        // Add aggregations for facets
        queryBuilder
            .withAggregation("categories", a -> a
                .terms(t -> t.field("category").size(20))
            )
            .withAggregation("price_ranges", a -> a
                .range(r -> r
                    .field("price")
                    .ranges(rb -> rb
                        .range(r -> r.key("cheap").to(50.0))
                        .range(r -> r.key("moderate").from(50.0).to(200.0))
                        .range(r -> r.key("expensive").from(200.0))
                    )
                )
            );

        // Pagination and sorting
        if (request.getSortBy() != null) {
            queryBuilder.withSort(Sort.by(
                request.isSortAsc() ? Sort.Direction.ASC : Sort.Direction.DESC,
                request.getSortBy()
            ));
        }

        queryBuilder.withPageable(PageRequest.of(request.getPage(), request.getSize()));

        SearchHits<Product> hits = elasticsearchOperations.search(queryBuilder.build(), Product.class);

        return mapToSearchResponse(hits);
    }
}
```

---

### 5.2 Highlighting

```java
@Service
public class SearchHighlightService {

    public SearchHits<Product> searchWithHighlight(String query) {
        NativeQuery nativeQuery = NativeQuery.builder()
            .query(q -> q
                .multiMatch(mm -> mm
                    .query(query)
                    .fields("name", "description")
                )
            )
            .withHighlight(h -> h
                .fields("name", hf -> hf
                    .preTags("<em>")
                    .postTags("</em>")
                )
                .fields("description", hf -> hf
                    .preTags("<em>")
                    .postTags("</em>")
                    .fragmentSize(150)
                    .numberOfFragments(3)
                )
            )
            .build();

        return elasticsearchOperations.search(nativeQuery, Product.class);
    }

    public ProductWithHighlight toProductWithHighlight(SearchHit<Product> hit) {
        Product product = hit.content();
        Map<String, List<String>> highlights = hit.getHighlightFields();

        return new ProductWithHighlight(product, highlights);
    }
}

@Data
@AllArgsConstructor
public class ProductWithHighlight {
    private Product product;
    private Map<String, List<String>> highlights;
}
```

---

### 5.3 Suggester (Autocomplete)

```java
@Service
public class SuggestionService {

    public List<String> getSuggestions(String prefix) {
        NativeQuery nativeQuery = NativeQuery.builder()
            .suggester(s -> s
                .suggesters("product-suggest", ss -> ss
                    .term(t -> t
                        .field("name")
                        .suggestMode(SuggestMode.Missing)
                    )
                )
            )
            .build();

        SearchHits<Product> hits = elasticsearchOperations.search(nativeQuery, Product.class);

        return extractSuggestions(hits.getSuggest());
    }
}

// Index mapping for autocomplete
@Mapping
public class ProductMapping {
    // Use edge_ngram tokenizer for autocomplete
    // "lap" matches "laptop"
}
```

---

## 📚 BÀI 6: AGGREGATIONS

### 6.1 Product Analytics Service

```java
@Service
public class ProductAnalyticsService {

    public ProductStats getStats() {
        NativeQuery nativeQuery = NativeQuery.builder()
            .withQuery(q -> q.matchAll(m -> m))
            .withAggregation("total_products", a -> a
                .valueCount(vc -> vc.field("id"))
            )
            .withAggregation("avg_price", a -> a
                .avg(avg -> avg.field("price"))
            )
            .withAggregation("min_price", a -> a
                .min(min -> min.field("price"))
            )
            .withAggregation("max_price", a -> a
                .max(max -> max.field("price"))
            )
            .withAggregation("total_value", a -> a
                .sum(s -> s.field("price"))
            )
            .build();

        SearchHits<Product> hits = elasticsearchOperations.search(nativeQuery, Product.class);
        return extractStats(hits.getAggregations());
    }

    public CategoryBreakdown getCategoryBreakdown() {
        NativeQuery nativeQuery = NativeQuery.builder()
            .withQuery(q -> q.matchAll(m -> m))
            .withAggregation("categories", a -> a
                .terms(t -> t
                    .field("category")
                    .size(20)
                    .subAggregations("avg_price", sa -> sa
                        .avg(avg -> avg.field("price"))
                    )
                    .subAggregations("product_count", sa -> sa
                        .valueCount(vc -> vc.field("id"))
                    )
                )
            )
            .build();

        SearchHits<Product> hits = elasticsearchOperations.search(nativeQuery, Product.class);
        return extractCategoryBreakdown(hits.getAggregations());
    }
}
```

---

## 📚 BÀI 7: BULK OPERATIONS

### 7.1 Bulk Indexing Service

```java
@Service
public class BulkIndexingService {

    private final ElasticsearchClient client;
    private static final int BULK_SIZE = 1000;

    public void indexAllProducts(List<Product> products) {
        List<List<Product>> batches = Lists.partition(products, BULK_SIZE);

        for (List<Product> batch : batches) {
            indexBatch(batch);
        }
    }

    private void indexBatch(List<Product> batch) {
        List<BulkOperation> operations = batch.stream()
            .map(product -> BulkOperation.of(b -> b
                .index(i -> i
                    .index("products")
                    .id(product.getId())
                    .document(product)
                )
            ))
            .toList();

        BulkResponse response = client.bulk(b -> b
            .operations(operations)
            .refresh(Refresh.True)
        );

        if (response.errors()) {
            log.error("Bulk indexing had errors");
        }
    }

    // Reindex with transformation
    public void reindexWithTransformation(String sourceIndex, String destIndex) {
        ReindexRequest reindexRequest = ReindexRequest.of(r -> r
            .source(s -> s
                .index(sourceIndex)
            )
            .dest(d -> d
                .index(destIndex)
            )
        );

        ReindexResponse response = client.reindex(reindexRequest);
        log.info("Reindexed {} documents", response.updated());
    }
}
```

---

## 📝 TÓM TẮT

| Feature | Spring Data Implementation |
|---------|---------------------------|
| Repository | `ElasticsearchRepository<T, ID>` |
| Query | `@Query`, `NativeQuery` |
| Aggregation | `.withAggregation()` |
| Highlighting | `@Highlight`, `.withHighlight()` |
| Bulk Ops | `client.bulk()` |
| Reindex | `client.reindex()` |

---

## 🔜 TIẾP THEO

Xem `03-exercises.md` để thực hành Elasticsearch!
