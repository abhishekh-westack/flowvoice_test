"""
Page object for the user detail page (/users/[id])
"""
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class UserDetailPage(BasePage):
    """Page Object for User Detail Page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Locators
        self._page_title = 'h1:has-text("User Detail")'
        self._back_button = 'svg.lucide-chevron-left'
        self._first_name_input = 'input[name="first_name"]'
        self._last_name_input = 'input[name="last_name"]'
        self._email_input = 'input[name="email"]'
        self._role_select = 'button:has-text("Select roles")'
        self._save_button = 'button[type="submit"]:has-text("Save")'
        self._delete_button = 'button.bg-destructive:has-text("Delete"), button:has-text("Delete User")'
        self._loading_spinner = '.animate-spin'
        self._user_avatar = r'.bg-\[#E2F3FF\]'
        self._delete_alert = '[role="alertdialog"]'
        self._confirm_delete = 'button:has-text("Continue")'  # The "Continue" button in the confirmation dialog
        self._success_message = 'text=/saved|success/i'
        self._error_message = 'text=/error|failed/i'
    
    def navigate_to_user_detail(self, base_url: str, user_id: str):
        """Navigate to user detail page"""
        self.navigate(f"{base_url}/users/{user_id}")
        return self
    
    def is_page_loaded(self) -> bool:
        """Check if user detail page is loaded"""
        try:
            expect(self.page.locator(self._page_title)).to_be_visible(timeout=5000)
            return True
        except:
            return False
    
    def click_back(self):
        """Click back button"""
        self.page.locator(self._back_button).click()
        return self
    
    def get_first_name_input(self):
        """Get first name input locator"""
        return self.page.locator(self._first_name_input)
    
    def get_last_name_input(self):
        """Get last name input locator"""
        return self.page.locator(self._last_name_input)
    
    def get_email_input(self):
        """Get email input locator"""
        return self.page.locator(self._email_input)
    
    def get_save_button(self):
        """Get save button locator"""
        return self.page.locator(self._save_button)
    
    def get_delete_button(self):
        """Get delete button locator"""
        return self.page.locator(self._delete_button)
    
    def fill_first_name(self, first_name: str):
        """Fill first name field"""
        self.get_first_name_input().fill(first_name)
        return self
    
    def fill_last_name(self, last_name: str):
        """Fill last name field"""
        self.get_last_name_input().fill(last_name)
        return self
    
    def fill_email(self, email: str):
        """Fill email field"""
        self.get_email_input().fill(email)
        return self
    
    def select_role(self, role: str):
        """Select a role from multi-select dropdown"""
        # Click to open dropdown
        self.page.locator(self._role_select).click()
        # Select the role
        self.page.locator(f'text={role}').click()
        # Click outside to close dropdown
        self.page.locator(self._page_title).click()
        return self
    
    def save(self):
        """Click save button"""
        self.get_save_button().click()
        return self
    
    def delete(self):
        """Click delete button"""
        self.get_delete_button().click()
        return self
    
    def confirm_delete(self):
        """Confirm delete in alert dialog"""
        # Use force=True to bypass backdrop overlay
        self.page.locator(self._confirm_delete).click(force=True)
        return self
    
    def is_delete_alert_visible(self) -> bool:
        """Check if delete alert dialog is visible"""
        return self.page.locator(self._delete_alert).is_visible()
    
    def is_loading(self) -> bool:
        """Check if loading spinner is visible"""
        return self.page.locator(self._loading_spinner).is_visible()
    
    def wait_for_user_to_load(self, timeout: int = 10000):
        """Wait for user data to load (spinner to disappear)"""
        try:
            self.page.wait_for_selector(self._loading_spinner, state='hidden', timeout=timeout)
        except:
            pass  # Spinner might not appear if loading is fast
        return self
    
    def get_first_name_value(self) -> str:
        """Get current first name value"""
        return self.get_first_name_input().input_value()
    
    def get_last_name_value(self) -> str:
        """Get current last name value"""
        return self.get_last_name_input().input_value()
    
    def get_email_value(self) -> str:
        """Get current email value"""
        return self.get_email_input().input_value()
    
    def is_save_successful(self) -> bool:
        """Check if save was successful"""
        try:
            # Look for success indicator (green checkmark or success message)
            return self.page.locator('text=/saved|success/i').is_visible(timeout=3000)
        except:
            return False
    
    def is_delete_button_visible(self) -> bool:
        """Check if delete button is visible (not visible for admin users)"""
        try:
            return self.get_delete_button().is_visible(timeout=1000)
        except:
            return False
    
    def get_user_avatar_text(self) -> str:
        """Get user avatar initials"""
        return self.page.locator(self._user_avatar).text_content()
