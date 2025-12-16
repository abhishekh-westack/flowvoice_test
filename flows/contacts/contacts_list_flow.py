"""
Flow for contacts list page actions
"""
from playwright.sync_api import Page
import allure
from pages.contacts.contacts_list_page import ContactsListPage

class ContactsListFlow:
    """High-level flow for contacts list page"""
    
    def __init__(self, page: Page):
        self.page = page
        self.contacts_list_page = ContactsListPage(page)
    
    @allure.step("Navigate to contacts page")
    def navigate_to_contacts(self, base_url: str):
        """Navigate to contacts page"""
        self.contacts_list_page.navigate_to_contacts(base_url)
        self.contacts_list_page.wait_for_contacts_to_load()
        return self
    
    @allure.step("Click add contact button")
    def click_add_contact(self):
        """Click add contact button to navigate to new contact page"""
        self.contacts_list_page.click_add_contact()
        return self
    
    @allure.step("Click contact by index: {index}")
    def click_contact_by_index(self, index: int):
        """Click on a contact row by index to navigate to edit page"""
        self.contacts_list_page.click_contact_by_index(index)
        return self
    
    @allure.step("Verify contacts are displayed")
    def verify_contacts_displayed(self) -> bool:
        """Verify that contacts are displayed on the page"""
        contact_count = self.contacts_list_page.get_contact_count()
        return contact_count > 0
    
    @allure.step("Verify empty state is shown")
    def verify_empty_state(self) -> bool:
        """Verify that empty state message is shown"""
        return self.contacts_list_page.is_empty_state_visible()
    
    @allure.step("Wait for page to load")
    def wait_for_page_load(self):
        """Wait for contacts page to fully load"""
        self.contacts_list_page.wait_for_contacts_to_load()
        return self
