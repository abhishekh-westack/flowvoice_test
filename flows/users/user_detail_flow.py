"""
Flow for user detail page actions
"""
from playwright.sync_api import Page
import allure
from pages.users.user_detail_page import UserDetailPage

class UserDetailFlow:
    """High-level flow for user detail page"""
    
    def __init__(self, page: Page):
        self.page = page
        self.user_detail_page = UserDetailPage(page)
    
    @allure.step("Navigate to user detail page: {user_id}")
    def navigate_to_user_detail(self, base_url: str, user_id: str):
        """Navigate to user detail page"""
        self.user_detail_page.navigate_to_user_detail(base_url, user_id)
        self.user_detail_page.wait_for_user_to_load()
        return self
    
    @allure.step("Edit user: {first_name} {last_name}")
    def edit_user(self, first_name: str = None, last_name: str = None, email: str = None):
        """Edit user details and save"""
        if first_name:
            self.user_detail_page.fill_first_name(first_name)
        if last_name:
            self.user_detail_page.fill_last_name(last_name)
        if email:
            self.user_detail_page.fill_email(email)
        
        self.user_detail_page.save()
        self.page.wait_for_timeout(1000)  # Wait for save to complete
        return self
    
    @allure.step("Delete user")
    def delete_user(self):
        """Delete user and confirm"""
        self.user_detail_page.delete()
        self.page.wait_for_timeout(500)  # Wait for alert to appear
        
        if self.user_detail_page.is_delete_alert_visible():
            self.user_detail_page.confirm_delete()
            self.page.wait_for_timeout(1000)  # Wait for deletion to complete
        
        return self
    
    @allure.step("Verify user details loaded")
    def verify_user_details_loaded(self) -> bool:
        """Verify that user details are loaded on the page"""
        return (
            self.user_detail_page.get_first_name_value() != "" and
            self.user_detail_page.get_last_name_value() != "" and
            self.user_detail_page.get_email_value() != ""
        )
    
    @allure.step("Go back to users list")
    def go_back(self):
        """Click back button to return to users list"""
        self.user_detail_page.click_back()
        return self
