# 🕷️ Fullstack Learning Crawler

Hệ thống crawl tự động nội dung học liệu từ các nguồn miễn phí để xây dựng [fullstack-learning](../) repository.

## 📁 Cấu trúc

```
crawler-system/
├── crawlers/           # Crawler implementations
│   ├── base_crawler.py
│   ├── w3schools_crawler.py
│   └── generic_crawler.py
├── processors/         # Content processing
│   └── content_formatter.py
├── storage/           # File & git operations
│   └── file_storage.py
├── config/            # Configuration files
│   ├── sources.yaml
│   └── mappings.yaml
├── utils/             # Utilities
│   └── logger.py
├── main.py            # Entry point
└── requirements.txt   # Dependencies
```

## 🚀 Cài đặt

```bash
# Install dependencies
pip install -r requirements.txt

# Install playwright browsers (optional, for JS-rendered sites)
playwright install
```

## 📖 Sử dụng

### Crawl một nguồn

```bash
# Crawl W3Schools Java tutorials
python main.py --source w3schools-java --output backend/01_java-core

# Crawl Programiz Java
python main.py --source programiz-java --output backend/01_java-core

# Crawl Oracle Java docs
python main.py --source oracle-java --output backend/01_java-core
```

### Crawl tất cả nguồn

```bash
# Crawl all Java Core sources
python main.py --source all --output backend/01_java-core
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--source` | Source to crawl | `w3schools-java` |
| `--output` | Output folder | `backend/01_java-core` |
| `--config` | Config file path | `config/sources.yaml` |
| `--log-level` | Logging level | `INFO` |
| `--no-commit` | Skip git commit | `False` |

## ⚙️ Cấu hình

### Thêm nguồn mới (config/sources.yaml)

```yaml
new_source:
  provider_name:
    base_url: "https://example.com"
    target_folder: "backend/xx_topic"
    content_type: "theory"
    pages:
      - "/page1"
      - "/page2"
```

### Tạo custom crawler

```python
from crawlers.base_crawler import BaseCrawler

class MyCustomCrawler(BaseCrawler):
    def crawl(self, pages):
        # Implement crawling logic
        pass

    def process_content(self, html, url):
        # Implement content processing
        pass
```

## 📝 Output

Mỗi folder sẽ có các file:

- `theory.md` — Lý thuyết, concepts
- `exercises.md` — Bài tập thực hành
- `best-practices.md` — Kinh nghiệm, tips
- `resources.md` — Links, tài liệu tham khảo

## ⚠️ Lưu ý

1. **Rate limiting**: Mặc định 1000ms giữa các request
2. **Git branches**: Mỗi crawl session tạo branch mới
3. **Review**: Luôn review nội dung trước khi merge vào main

## 🔧 Troubleshooting

### Bị block bởi website
- Tăng `rate_limit_ms` trong crawler
- Thêm delay thủ công
- Sử dụng proxy nếu cần

### Nội dung không đúng format
- Kiểm tra `content_selector` trong config
- Override `extract_main_content()` trong crawler

## 📄 License

MIT — Tool này phục vụ mục đích học tập.
