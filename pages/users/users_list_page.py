"""
Page object for the users list page (/users)
"""
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class UsersListPage(BasePage):
    """Page Object for Users List Page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Locators
        self._page_title = 'h1:has-text("Users")'
        self._create_new_button = 'button:has-text("Create New")'
        self._user_cards = '.shadow-sm.border.rounded-lg'
        self._empty_state = 'text=/no users/i'
        self._loading_spinner = '.animate-spin'
        self._add_user_modal = '[role="dialog"]'
        self._user_name = '.font-bold.text-sm'
        self._user_email = '.text-\[\#666666\].break-all.text-sm'
        self._role_badge = '.px-2.py-1.rounded-md'
    
    def navigate_to_users(self, base_url: str):
        """Navigate to users page"""
        self.navigate(f"{base_url}/users")
        return self
    
    def is_page_loaded(self) -> bool:
        """Check if users page is loaded"""
        try:
            expect(self.page.locator(self._page_title)).to_be_visible(timeout=5000)
            return True
        except:
            return False
    
    def get_create_new_button(self):
        """Get create new button locator"""
        return self.page.locator(self._create_new_button)
    
    def click_create_new(self):
        """Click create new button"""
        self.get_create_new_button().click()
        return self
    
    def is_add_user_modal_visible(self) -> bool:
        """Check if add user modal is visible"""
        return self.page.locator(self._add_user_modal).is_visible()
    
    def get_user_cards(self):
        """Get all user cards"""
        return self.page.locator(self._user_cards)
    
    def get_user_count(self) -> int:
        """Get number of user cards"""
        self.wait_for_timeout(1000)  # Wait for cards to render
        return self.get_user_cards().count()
    
    def click_user_by_index(self, index: int):
        """Click on a user card by index"""
        self.get_user_cards().nth(index).click()
        return self
    
    def is_empty_state_visible(self) -> bool:
        """Check if empty state message is visible"""
        return self.page.locator(self._empty_state).is_visible()
    
    def is_loading(self) -> bool:
        """Check if loading spinner is visible"""
        return self.page.locator(self._loading_spinner).is_visible()
    
    def wait_for_users_to_load(self, timeout: int = 10000):
        """Wait for users to load (spinner to disappear)"""
        try:
            self.page.wait_for_selector(self._loading_spinner, state='hidden', timeout=timeout)
        except:
            pass  # Spinner might not appear if loading is fast
        return self
    
    def get_user_name_by_index(self, index: int) -> str:
        """Get user name by index"""
        return self.get_user_cards().nth(index).locator(self._user_name).text_content()
    
    def get_user_email_by_index(self, index: int) -> str:
        """Get user email by index"""
        return self.get_user_cards().nth(index).locator(self._user_email).text_content()
    
    def get_user_roles_by_index(self, index: int) -> list:
        """Get user roles by index"""
        role_badges = self.get_user_cards().nth(index).locator(self._role_badge)
        count = role_badges.count()
        return [role_badges.nth(i).text_content() for i in range(count)]
