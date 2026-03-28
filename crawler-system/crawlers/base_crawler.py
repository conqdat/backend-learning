"""
Base Crawler Module
Provides common functionality for all crawlers
"""

import requests
import time
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from markdownify import markdownify
from typing import List, Dict, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class BaseCrawler(ABC):
    """Abstract base class for all crawlers"""

    def __init__(
        self,
        base_url: str,
        target_folder: str,
        rate_limit_ms: int = 1000,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.target_folder = Path(target_folder)
        self.rate_limit_ms = rate_limit_ms
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Cache-Control": "max-age=0",
            }
        )
        self._last_request_time = 0

    def _rate_limit(self):
        """Apply rate limiting between requests"""
        elapsed = (time.time() - self._last_request_time) * 1000
        if elapsed < self.rate_limit_ms:
            sleep_time = (self.rate_limit_ms - elapsed) / 1000
            time.sleep(sleep_time)
        self._last_request_time = time.time()

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch HTML content from URL with retry logic"""
        if not url.startswith("http"):
            url = f"{self.base_url}{url}"

        for attempt in range(self.max_retries):
            try:
                self._rate_limit()
                logger.info(f"Fetching: {url}")
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
        return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, "lxml")

    def html_to_markdown(self, html: str, **kwargs) -> str:
        """Convert HTML to Markdown"""
        return markdownify(html, **kwargs)

    def extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content area from HTML"""
        # Try common main content selectors
        main_selectors = [
            "main",
            "article",
            ".content",
            "#content",
            ".main-content",
            ".article-body",
            "[role='main']",
        ]

        for selector in main_selectors:
            element = soup.select_one(selector)
            if element:
                return str(element)

        # Fallback to body
        body = soup.find("body")
        if body:
            return str(body)

        return str(soup)

    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        # Try h1 first
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        # Fallback to title tag
        title = soup.find("title")
        if title:
            return title.get_text(strip=True)

        return "Untitled"

    def save_content(self, content: str, filename: str):
        """Save content to target folder"""
        self.target_folder.mkdir(parents=True, exist_ok=True)
        filepath = self.target_folder / filename
        filepath.write_text(content, encoding="utf-8")
        logger.info(f"Saved: {filepath}")

    @abstractmethod
    def crawl(self, pages: List[str]) -> Dict[str, str]:
        """
        Crawl multiple pages and return content mapping
        Returns: Dict mapping output filename to content
        """
        pass

    @abstractmethod
    def process_content(self, html: str, url: str) -> Dict[str, str]:
        """
        Process HTML and return content for different files
        Returns: Dict mapping filename to processed content
        """
        pass
