"""
Flow for users list page actions
"""
from playwright.sync_api import Page
import allure
from pages.users.users_list_page import UsersListPage

class UsersListFlow:
    """High-level flow for users list page"""
    
    def __init__(self, page: Page):
        self.page = page
        self.users_list_page = UsersListPage(page)
    
    @allure.step("Navigate to users page")
    def navigate_to_users(self, base_url: str):
        """Navigate to users page"""
        self.users_list_page.navigate_to_users(base_url)
        self.users_list_page.wait_for_users_to_load()
        return self
    
    @allure.step("Open add user modal")
    def open_add_user_modal(self):
        """Click create new button to open add user modal"""
        self.users_list_page.click_create_new()
        self.page.wait_for_timeout(500)  # Wait for modal animation
        return self
    
    @allure.step("Click user by index: {index}")
    def click_user_by_index(self, index: int):
        """Click on a user card by index to navigate to detail page"""
        self.users_list_page.click_user_by_index(index)
        return self
    
    @allure.step("Verify users are displayed")
    def verify_users_displayed(self) -> bool:
        """Verify that users are displayed on the page"""
        user_count = self.users_list_page.get_user_count()
        return user_count > 0
    
    @allure.step("Verify empty state is shown")
    def verify_empty_state(self) -> bool:
        """Verify that empty state message is shown"""
        return self.users_list_page.is_empty_state_visible()
    
    @allure.step("Wait for page to load")
    def wait_for_page_load(self):
        """Wait for users page to fully load"""
        self.users_list_page.wait_for_users_to_load()
        return self
