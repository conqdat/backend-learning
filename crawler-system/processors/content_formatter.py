"""
Content Formatter Module
Processes crawled content and formats into final markdown files
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ContentFormatter:
    """Format and merge crawled content into final files"""

    def __init__(self, output_folder: str):
        self.output_folder = Path(output_folder)
        self.frontmatter_templates = {
            "theory.md": """---
title: {title}
type: theory
source: {source}
last_updated: {date}
---

""",
            "exercises.md": """---
title: {title}
type: exercises
source: {source}
last_updated: {date}
---

""",
            "best-practices.md": """---
title: {title}
type: best_practices
source: {source}
last_updated: {date}
---

""",
            "resources.md": """---
title: {title}
type: resources
source: {source}
last_updated: {date}
---

""",
        }

    def clean_markdown(self, content: str) -> str:
        """Clean and normalize markdown content"""
        # Remove multiple blank lines
        content = re.sub(r"\n{3,}", "\n\n", content)

        # Remove trailing whitespace
        content = "\n".join(line.rstrip() for line in content.split("\n"))

        # Fix heading spacing
        content = re.sub(r"\n*(#+[^\n]+)\n*", r"\n\1\n\n", content)

        # Normalize code block language tags
        content = re.sub(r"```(\w+)", r"```\1", content)

        return content.strip()

    def add_frontmatter(self, content: str, filename: str, title: str, source: str, date: str) -> str:
        """Add YAML frontmatter to content"""
        template = self.frontmatter_templates.get(filename, self.frontmatter_templates["theory.md"])
        frontmatter = template.format(
            title=title,
            source=source,
            date=date,
        )
        return frontmatter + content

    def merge_content(self, content_list: List[Dict[str, str]], filename: str) -> str:
        """Merge multiple content dicts into single file content"""
        merged = []
        seen_urls = set()

        for content_dict in content_list:
            if filename not in content_dict:
                continue

            content = content_dict[filename]

            # Extract source URL from content
            url_match = re.search(r"> Source: (.+)", content)
            if url_match:
                url = url_match.group(1)
                if url in seen_urls:
                    continue  # Skip duplicates
                seen_urls.add(url)

            merged.append(content)

        if not merged:
            return ""

        # Add table of contents if multiple sources
        if len(merged) > 1:
            toc = "# Table of Contents\n\n"
            for i, content in enumerate(merged, 1):
                title_match = re.search(r"^# (.+)", content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
                    toc += f"{i}. {title}\n"
            toc += "\n---\n\n"
            merged.insert(0, toc)

        return "\n\n---\n\n".join(merged)

    def format_for_topic(self, content: Dict[str, str], topic_name: str) -> Dict[str, str]:
        """Format content for a specific topic/chapter"""
        formatted = {}

        for filename, raw_content in content.items():
            # Add topic header
            header = f"# {topic_name}\n\n"

            # Clean and format
            cleaned = self.clean_markdown(raw_content)
            formatted[filename] = header + cleaned

        return formatted

    def save_files(self, content: Dict[str, str], folder: Optional[str] = None):
        """Save content to files"""
        target = Path(folder) if folder else self.output_folder
        target.mkdir(parents=True, exist_ok=True)

        saved_files = []
        for filename, text in content.items():
            if not text.strip():
                logger.warning(f"Skipping empty file: {filename}")
                continue

            filepath = target / filename
            filepath.write_text(text, encoding="utf-8")
            saved_files.append(str(filepath))
            logger.info(f"Saved: {filepath}")

        return saved_files

    def create_index(self, topics: List[str], folder: Optional[str] = None) -> str:
        """Create index.md for a folder"""
        target = Path(folder) if folder else self.output_folder

        index = "# Index\n\n"
        index += "## Contents\n\n"

        for topic in topics:
            index += f"- [ ] {topic}\n"

        index += "\n## Progress\n\n"
        index += "- Theory: [ ]\n"
        index += "- Exercises: [ ]\n"
        index += "- Best Practices: [ ]\n"

        filepath = target / "INDEX.md"
        filepath.write_text(index, encoding="utf-8")
        logger.info(f"Created index: {filepath}")

        return str(filepath)
