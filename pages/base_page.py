# pages/base_page.py
from playwright.sync_api import Page, expect
from pathlib import Path
import allure


class BasePage:
    """Base page class with common methods for all pages"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str, wait_until: str = "networkidle"):
        """Navigate to a URL"""
        self.page.goto(url, wait_until=wait_until)
    
    def wait_for_url(self, pattern: str, timeout: int = 5000):
        """Wait for URL to match a pattern"""
        import re
        expect(self.page).to_have_url(re.compile(pattern), timeout=timeout)
    
    def take_screenshot(self, name: str):
        """Take and attach screenshot to Allure"""
        screenshot_bytes = self.page.screenshot()
        allure.attach(screenshot_bytes, name, allure.attachment_type.PNG)
        return screenshot_bytes
    
    def wait_for_timeout(self, timeout: int):
        """Wait for a specific timeout"""
        self.page.wait_for_timeout(timeout)
    
    def wait_for_load_state(self, state: str = "networkidle"):
        """Wait for page load state"""
        self.page.wait_for_load_state(state)
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
