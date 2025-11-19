import pytest
import os
from playwright.sync_api import sync_playwright
from config.env import HEADLESS, SLOW_MO

@pytest.fixture(scope="session")
def browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
    try:
        yield browser
    finally:
        browser.close()
        p.stop()