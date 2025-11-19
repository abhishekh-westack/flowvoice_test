# pages/login_page.py
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from config.env import BASE_URL


class LoginPage(BasePage):
    """Page Object for Login Page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}/login"
        
        # Locators
        self._email_field = 'input[name="email"], input[type="email"]'
        self._submit_button = 'button[type="submit"]'
        
        # Error message selectors
        self._error_selectors = [
            'text=/invalid|error|incorrect|failed|not found/i',
            '.text-red-500',           # Tailwind errors
            '.text-destructive',       # ShadCN errors
            '[data-error]',            # Custom errors
            '#email-error',            # Common pattern
        ]
    
    def navigate(self):
        """Navigate to login page"""
        super().navigate(self.url)
        return self
    
    def get_email_field(self):
        """Get email input field locator"""
        return self.page.locator(self._email_field)
    
    def get_submit_button(self):
        """Get submit button locator"""
        return self.page.get_by_role("button")
    
    def fill_email(self, email: str):
        """Fill email field"""
        email_field = self.get_email_field()
        expect(email_field).to_be_visible(timeout=5000)
        email_field.fill(email)
        return self
    
    def click_submit(self):
        """Click submit button"""
        self.get_submit_button().click()
        return self
    
    def check_for_errors(self) -> tuple[bool, str]:
        """
        Check if any error messages are visible on the page
        Returns: (has_error: bool, error_text: str)
        """
        self.wait_for_timeout(1500)  # Wait for error to appear
        
        for selector in self._error_selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                error_text = locator.first.text_content()
                return True, error_text
        
        return False, ""
    
    def submit_email(self, email: str):
        """Complete email submission flow"""
        self.fill_email(email)
        self.click_submit()
        return self
    
    def verify_navigation_to_otp(self, timeout: int = 7000):
        """Verify that page navigated to OTP page"""
        try:
            self.wait_for_url(r".*/login/otp.*", timeout=timeout)
            return True
        except Exception as e:
            return False
