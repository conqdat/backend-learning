"""Crawlers package"""
from .base_crawler import BaseCrawler
from .w3schools_crawler import W3SchoolsCrawler
from .generic_crawler import GenericCrawler

__all__ = ["BaseCrawler", "W3SchoolsCrawler", "GenericCrawler"]
