# pages/otp_page.py
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re


class OTPPage(BasePage):
    """Page Object for OTP Page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Locators
        self._otp_field = 'input[inputmode="numeric"], input[name="pin"], input[data-input-otp="true"]'
        self._submit_button = 'button[type="submit"]'
    
    def get_otp_field(self):
        """Get OTP input field locator"""
        return self.page.locator(self._otp_field)
    
    def get_submit_button(self):
        """Get submit button locator"""
        return self.page.locator(self._submit_button)
    
    def is_on_otp_page(self) -> bool:
        """Check if currently on OTP page"""
        return bool(re.search(r".*/login/otp.*", self.page.url))
    
    def fill_otp(self, otp_code: str):
        """Fill OTP field"""
        otp_field = self.get_otp_field()
        expect(otp_field).to_be_visible(timeout=5000)
        otp_field.fill(otp_code)
        return self
    
    def click_submit(self):
        """Click submit button if visible"""
        submit_btn = self.get_submit_button()
        if submit_btn.is_visible():
            submit_btn.click()
        return self
    
    def submit_otp(self, otp_code: str, auto_submit_wait: int = 1500):
        """
        Complete OTP submission flow
        
        Args:
            otp_code: OTP code to enter
            auto_submit_wait: Wait time for auto-submit (some forms auto-submit)
        """
        self.fill_otp(otp_code)
        
        # Wait for potential auto-submit
        self.wait_for_timeout(auto_submit_wait)
        
        # Submit if button is still visible
        self.click_submit()
        
        return self
    
    def verify_left_otp_page(self) -> bool:
        """Verify that user has left the OTP page (successful login)"""
        try:
            import re
            expect(self.page).not_to_have_url(re.compile(r".*/login/otp.*"))
            return True
        except Exception:
            return False
    
    def wait_for_dashboard(self):
        """Wait for dashboard to load after successful OTP"""
        self.wait_for_load_state("networkidle")
        return self
