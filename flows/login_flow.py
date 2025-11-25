# flows/login_flow.py
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
import allure
import time

class LoginFlow:
    """High-level flow for login process"""
    
    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.otp_page = OTPPage(page)
    
    @allure.step("Complete login flow with email and OTP")
    def complete_login(self, email: str, otp_code: str = "1111") -> bool:
        """
        Complete the full login flow
        
        Args:
            email: User email
            otp_code: OTP code (default: "1111")
        
        Returns:
            bool: True if login successful, False otherwise
        
        Raises:
            AssertionError: If login fails at any step
        """
        # Step 1: Navigate to login page
        with allure.step("Navigate to login page"):
            self.login_page.navigate()
        
        # Step 2: Submit email
        with allure.step(f"Submit email: {email}"):
            self.login_page.submit_email(email)
        
        # Step 3: Check for errors
        with allure.step("Check for email errors"):
            has_error, error_text = self.login_page.check_for_errors()
            if has_error:
                raise AssertionError(f"❌ Login failed: {error_text}")
        
        # Step 4: Verify navigation to OTP page
        with allure.step("Verify navigation to OTP page"):
            time.sleep(0.5)  # Small delay to ensure URL is updated
            if not self.login_page.verify_navigation_to_otp():
                raise AssertionError("❌ Failed to navigate to OTP page")
        
        # Step 5: Submit OTP
        with allure.step(f"Submit OTP: {otp_code}"):
            self.otp_page.submit_otp(otp_code)
        
        # Step 6: Verify successful login
        with allure.step("Wait for dashboard"):
            self.otp_page.wait_for_dashboard()
        
        # Step 7: Verify left OTP page
        with allure.step("Verify successful login"):
            if not self.otp_page.verify_left_otp_page():
                raise AssertionError("❌ Still on OTP page after submission")
        
        return True
    
    @allure.step("Login with email only (stop at OTP page)")
    def login_email_only(self, email: str) -> bool:
        """
        Login with email and stop at OTP page (useful for testing email validation)
        
        Args:
            email: User email
        
        Returns:
            bool: True if reached OTP page, False otherwise
        """
        self.login_page.navigate()
        self.login_page.submit_email(email)
        
        # Check for errors
        has_error, error_text = self.login_page.check_for_errors()
        # If rate limit error, skip raising and return False
        if has_error:
            if error_text and "Please wait 3 minutes before requesting a new code" in error_text:
                print("INFO: OTP rate limit detected, returning False from login_email_only.")
                return False
            raise AssertionError(f"❌ Email validation failed: {error_text}")
        
        # Verify OTP page
        if self.login_page.verify_navigation_to_otp():
            return True
        
        return False
    
    @allure.step("Submit OTP on already loaded OTP page")
    def submit_otp_only(self, otp_code: str = "1111") -> bool:
        """
        Submit OTP when already on OTP page (useful for testing OTP validation)
        
        Args:
            otp_code: OTP code
        
        Returns:
            bool: True if login successful
        """
        if not self.otp_page.is_on_otp_page():
            raise AssertionError("❌ Not on OTP page")
        
        self.otp_page.submit_otp(otp_code)
        self.otp_page.wait_for_dashboard()
        
        return self.otp_page.verify_left_otp_page()
