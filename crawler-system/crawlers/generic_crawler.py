"""
Generic Crawler
For most educational/tutorial sites with standard structure
"""

import re
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler
import logging

logger = logging.getLogger(__name__)


class GenericCrawler(BaseCrawler):
    """Generic crawler for tutorial sites"""

    def __init__(
        self,
        base_url: str,
        target_folder: str,
        content_selector: Optional[str] = None,
        exclude_selectors: Optional[List[str]] = None,
    ):
        super().__init__(base_url=base_url, target_folder=target_folder)
        self.content_selector = content_selector
        self.exclude_selectors = exclude_selectors or [
            "nav",
            "footer",
            "header",
            ".sidebar",
            ".toc",
            ".table-of-contents",
            ".comments",
            "script",
            "style",
        ]

    def extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content with custom or default selectors"""
        if self.content_selector:
            element = soup.select_one(self.content_selector)
            if element:
                return str(element)

        # Remove unwanted elements
        for selector in self.exclude_selectors:
            for element in soup.select(selector):
                element.decompose()

        return super().extract_main_content(soup)

    def detect_content_type(self, soup: BeautifulSoup, url: str) -> str:
        """Detect if content is theory, exercises, or best practices"""
        text = soup.get_text().lower()

        # Check for exercises
        exercise_patterns = ["exercise", "practice", "problem", "challenge", "quiz", "homework"]
        if any(p in text for p in exercise_patterns):
            return "exercises"

        # Check for best practices
        bp_patterns = ["best practice", "tip", "recommendation", "pitfall", "anti-pattern"]
        if any(p in text for p in bp_patterns):
            return "best_practices"

        return "theory"

    def extract_code_blocks(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all code blocks"""
        code_blocks = []

        # Common code block selectors
        selectors = [
            "pre code",
            "pre",
            "code",
            ".code-block",
            ".highlight",
            "[class*='code']",
        ]

        for selector in selectors:
            for element in soup.select(selector):
                code = element.get_text(strip=True)
                if code and len(code) > 20:  # Filter out tiny snippets
                    # Determine language
                    lang = element.get("class", [""])[0] if element.name == "code" else "unknown"
                    code_blocks.append({"code": code, "language": lang})

        return code_blocks

    def extract_links(self, soup: BeautifulSoup, internal: bool = True) -> List[Dict[str, str]]:
        """Extract links for resources.md"""
        links = []
        base_domain = self.base_url.split("/")[2]

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)

            if not text:
                continue

            if internal:
                # Only internal links
                if href.startswith("/") or base_domain in href:
                    links.append({"text": text, "url": href})
            else:
                # External links
                if not href.startswith("/") and base_domain not in href:
                    links.append({"text": text, "url": href})

        return links

    def process_content(self, html: str, url: str) -> Dict[str, str]:
        """Process generic HTML and categorize content"""
        soup = self.parse_html(html)
        title = self.extract_title(soup)
        content_type = self.detect_content_type(soup, url)

        main_content = self.extract_main_content(soup)
        md_content = self.html_to_markdown(
            main_content,
            heading_style="ATX",
            bullets="-",
        )

        # Build content based on type
        theory = f"# {title}\n\n"
        theory += f"> Source: {url}\n\n"
        theory += md_content

        exercises = f"# Exercises - {title}\n\n"
        exercises += f"> Source: {url}\n\n"

        best_practices = f"# Best Practices - {title}\n\n"
        best_practices += f"> Source: {url}\n\n"

        resources = f"# Resources - {title}\n\n"
        resources += f"> Source: {url}\n\n"

        # Extract and categorize
        code_blocks = self.extract_code_blocks(soup)
        if code_blocks:
            exercises += "## Practice Code Examples\n\n"
            for i, block in enumerate(code_blocks[:10], 1):  # Limit to 10
                lang = block["language"] if block["language"] != "unknown" else ""
                exercises += f"### Example {i}\n\n"
                exercises += f"```{lang}\n{block['code']}\n```\n\n"

        # Extract links for resources
        internal_links = self.extract_links(soup, internal=True)
        if internal_links:
            resources += "## Related Pages\n\n"
            for link in internal_links[:20]:  # Limit
                resources += f"- [{link['text']}]({link['url']})\n"

        return {
            "theory.md": theory,
            "exercises.md": exercises,
            "best-practices.md": best_practices,
            "resources.md": resources,
        }

    def crawl(self, pages: List[str]) -> Dict[str, str]:
        """Crawl multiple pages"""
        all_content = {}

        for page in pages:
            html = self.fetch_page(page)
            if html:
                url = f"{self.base_url}{page}" if not page.startswith("http") else page
                content = self.process_content(html, url)

                for filename, text in content.items():
                    if filename not in all_content:
                        all_content[filename] = ""
                    all_content[filename] += f"\n\n---\n\n{text}"

        return all_content
