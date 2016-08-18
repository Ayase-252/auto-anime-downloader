"""
Scraper Management module

This module imports scrapers into program.
"""

import importlib

import configure


def import_scrapers():
    """
    Import scraper designated in INSTALLED_SCRAPERS of configure.py

    return
    List of objects representing scrapers
    """
    scrapers = [importlib.import_module(scraper)
                for scraper in configure.INSTALLED_SCRAPERS]
    return scrapers
