"""
W3Schools Crawler
Specialized crawler for w3schools.com Java tutorials
"""

import re
from typing import Dict, List
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler
import logging

logger = logging.getLogger(__name__)


class W3SchoolsCrawler(BaseCrawler):
    """Crawler optimized for W3Schools structure"""

    def __init__(self, target_folder: str = "backend/01_java-core"):
        super().__init__(
            base_url="https://www.w3schools.com",
            target_folder=target_folder,
            rate_limit_ms=2000,  # W3Schools has stricter rate limiting
        )

    def extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from W3Schools pages"""
        # W3Schools uses specific structure
        main = soup.find("div", class_="w3-col l10 m12")
        if main:
            return str(main)

        # Fallback to generic extraction
        return super().extract_main_content(soup)

    def extract_code_examples(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract code examples from W3Schools"""
        examples = []

        # W3Schools code blocks
        code_blocks = soup.find_all("div", class_="w3-code notranslate")
        for block in code_blocks:
            code = block.get_text(strip=True)
            if code:
                examples.append({"type": "code", "content": code})

        # "Try it Yourself" examples
        try_buttons = soup.find_all("a", class_="w3-btn", string=re.compile(r"Try it|Example"))
        for btn in try_buttons:
            href = btn.get("href", "")
            if href:
                examples.append({"type": "try_it", "url": href})

        return examples

    def extract_quiz(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract quiz questions if present"""
        quizzes = []
        quiz_divs = soup.find_all("div", class_="w3-panel w3-leftbar")
        for div in quiz_divs:
            if "quiz" in div.get_text().lower() or "test" in div.get_text().lower():
                quizzes.append({"type": "quiz", "content": str(div)})
        return quizzes

    def process_content(self, html: str, url: str) -> Dict[str, str]:
        """Process W3Schools HTML and categorize content"""
        soup = self.parse_html(html)
        title = self.extract_title(soup)
        main_content = self.extract_main_content(soup)

        # Convert to markdown
        md_content = self.html_to_markdown(
            main_content,
            heading_style="ATX",
            bullets="-",
            newline_style="BACKSLASH",
        )

        # Build theory content
        theory = f"# {title}\n\n"
        theory += f"> Source: {url}\n\n"
        theory += md_content

        # Extract code examples
        code_examples = self.extract_code_examples(soup)
        exercises = f"# Exercises - {title}\n\n"
        exercises += f"> Source: {url}\n\n"

        if code_examples:
            exercises += "## Code Examples\n\n"
            for i, ex in enumerate(code_examples, 1):
                if ex["type"] == "code":
                    exercises += f"### Example {i}\n\n"
                    exercises += "```java\n"
                    exercises += ex["content"]
                    exercises += "\n```\n\n"
                elif ex["type"] == "try_it":
                    exercises += f"### Interactive Example {i}\n\n"
                    exercises += f"[Try it yourself]({ex['url']})\n\n"

        # Extract best practices (W3Schools has "Tips and Notes")
        tips = soup.find_all("div", class_="w3-panel w3-yellow")
        best_practices = f"# Best Practices - {title}\n\n"
        best_practices += f"> Source: {url}\n\n"

        if tips:
            best_practices += "## Tips & Notes\n\n"
            for tip in tips:
                best_practices += f"- {tip.get_text(strip=True)}\n"

        return {
            "theory.md": theory,
            "exercises.md": exercises,
            "best-practices.md": best_practices,
        }

    def crawl(self, pages: List[str]) -> Dict[str, str]:
        """Crawl multiple W3Schools pages"""
        all_content = {}

        for page in pages:
            html = self.fetch_page(page)
            if html:
                url = f"{self.base_url}{page}"
                content = self.process_content(html, url)

                # Merge content
                for filename, text in content.items():
                    if filename not in all_content:
                        all_content[filename] = ""
                    all_content[filename] += f"\n\n---\n\n{text}"

        return all_content
