"""
Main entry point for the crawler system
"""

import argparse
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from crawlers import W3SchoolsCrawler, GenericCrawler
from processors.content_formatter import ContentFormatter
from storage.file_storage import FileStorage
from utils.logger import setup_logging

import logging

logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict:
    """Load configuration from YAML file"""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def crawl_w3schools(pages: List[str], output_folder: str) -> Dict[str, str]:
    """Crawl W3Schools Java tutorials"""
    crawler = W3SchoolsCrawler(target_folder=output_folder)
    return crawler.crawl(pages)


def crawl_generic(
    base_url: str, pages: List[str], output_folder: str, content_selector: str = None
) -> Dict[str, str]:
    """Crawl generic tutorial sites"""
    crawler = GenericCrawler(
        base_url=base_url,
        target_folder=output_folder,
        content_selector=content_selector,
    )
    return crawler.crawl(pages)


def process_and_save(
    content: Dict[str, str],
    folder: str,
    source: str,
    formatter: ContentFormatter,
    storage: FileStorage,
) -> List[str]:
    """Process content and save to files"""
    date = datetime.now().strftime("%Y-%m-%d")

    # Clean and format each file
    formatted = {}
    for filename, raw_content in content.items():
        cleaned = formatter.clean_markdown(raw_content)
        formatted[filename] = cleaned

    # Save files
    saved_files = storage.save_content(formatted, folder)

    return saved_files


def crawl_all_java_core(base_path: str = "..") -> List[str]:
    """Crawl all Java Core sources automatically"""
    config = load_config("config/sources.yaml")
    formatter = ContentFormatter(output_folder=f"{base_path}/backend/01_java-core")
    storage = FileStorage(base_path=base_path)

    all_content = {}
    total_pages = 0

    # Crawl W3Schools
    if "java_core" in config and "w3schools" in config["java_core"]:
        w3schools_config = config["java_core"]["w3schools"]
        pages = w3schools_config.get("pages", [])
        logger.info(f"Crawling W3Schools: {len(pages)} pages")
        total_pages += len(pages)
        crawler = W3SchoolsCrawler(target_folder=f"{base_path}/backend/01_java-core")
        content = crawler.crawl(pages)
        for k, v in content.items():
            all_content[k] = all_content.get(k, "") + "\n\n" + v if k in all_content else v

    # Crawl Programiz
    if "java_core" in config and "programiz" in config["java_core"]:
        programiz_config = config["java_core"]["programiz"]
        pages = programiz_config.get("pages", [])
        logger.info(f"Crawling Programiz: {len(pages)} pages")
        total_pages += len(pages)
        crawler = GenericCrawler(
            base_url=programiz_config["base_url"],
            target_folder=f"{base_path}/backend/01_java-core",
        )
        content = crawler.crawl(pages)
        for k, v in content.items():
            all_content[k] = all_content.get(k, "") + "\n\n" + v if k in all_content else v

    # Crawl Oracle
    if "java_core" in config and "oracle" in config["java_core"]:
        oracle_config = config["java_core"]["oracle"]
        pages = oracle_config.get("pages", [])
        logger.info(f"Crawling Oracle: {len(pages)} pages")
        total_pages += len(pages)
        crawler = GenericCrawler(
            base_url=oracle_config["base_url"],
            target_folder=f"{base_path}/backend/01_java-core",
        )
        content = crawler.crawl(pages)
        for k, v in content.items():
            all_content[k] = all_content.get(k, "") + "\n\n" + v if k in all_content else v

    # Save all content
    saved_files = []
    if all_content:
        date = datetime.now().strftime("%Y-%m-%d")
        for filename, raw_content in all_content.items():
            cleaned = formatter.clean_markdown(raw_content)
            all_content[filename] = cleaned

        saved_files = storage.save_content(all_content, f"{base_path}/backend/01_java-core")
        logger.info(f"Saved {len(saved_files)} files from {total_pages} pages")

    return saved_files


def main():
    parser = argparse.ArgumentParser(description="Fullstack Learning Crawler")
    parser.add_argument(
        "--source",
        choices=["w3schools-java", "programiz-java", "oracle-java", "all", "auto-java-core"],
        default="auto-java-core",
        help="Source to crawl",
    )
    parser.add_argument(
        "--output",
        default="backend/01_java-core",
        help="Output folder",
    )
    parser.add_argument(
        "--config",
        default="config/sources.yaml",
        help="Path to config file",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )
    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Skip git commit",
    )

    args = parser.parse_args()

    # Setup
    setup_logging(level=args.log_level)
    config = load_config(args.config)
    formatter = ContentFormatter(output_folder=args.output)
    storage = FileStorage()

    logger.info(f"Starting crawl: {args.source} → {args.output}")

    # Crawl based on source
    content = {}

    if args.source in ["w3schools-java", "all", "auto-java-core"]:
        w3schools_config = config["java_core"]["w3schools"]
        pages = w3schools_config.get("pages", [])
        logger.info(f"Crawling W3Schools: {len(pages)} pages")
        w3schools_content = crawl_w3schools(pages, args.output)
        content.update(w3schools_content)

    if args.source in ["programiz-java", "all", "auto-java-core"]:
        programiz_config = config["java_core"]["programiz"]
        pages = programiz_config.get("pages", [])
        logger.info(f"Crawling Programiz: {len(pages)} pages")
        programiz_content = crawl_generic(
            base_url=programiz_config["base_url"],
            pages=pages,
            output_folder=args.output,
        )
        content.update(programiz_content)

    if args.source in ["oracle-java", "all", "auto-java-core"]:
        oracle_config = config["java_core"]["oracle"]
        pages = oracle_config.get("pages", [])
        logger.info(f"Crawling Oracle: {len(pages)} pages")
        oracle_content = crawl_generic(
            base_url=oracle_config["base_url"],
            pages=pages,
            output_folder=args.output,
        )
        content.update(oracle_content)

    # Crawl Baeldung if available
    if "java_core" in config and "baeldung" in config["java_core"]:
        baeldung_config = config["java_core"]["baeldung"]
        pages = baeldung_config.get("pages", [])
        if pages:  # Only crawl if pages are configured
            logger.info(f"Crawling Baeldung: {len(pages)} pages")
            baeldung_content = crawl_generic(
                base_url=baeldung_config["base_url"],
                pages=pages,
                output_folder=args.output,
            )
            content.update(baeldung_content)

    # Process and save
    if content:
        saved_files = process_and_save(
            content=content,
            folder=args.output,
            source=args.source,
            formatter=formatter,
            storage=storage,
        )

        logger.info(f"Saved {len(saved_files)} files")

        # Git commit
        if not args.no_commit and saved_files:
            branch_name = f"crawl/{args.source.replace('/', '-')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            storage.create_branch(branch_name)
            storage.commit_changes(f"chore: crawl content from {args.source}", saved_files)
            logger.info(f"Committed to branch: {branch_name}")
    else:
        logger.warning("No content crawled")

    logger.info("Crawl completed")


if __name__ == "__main__":
    main()
