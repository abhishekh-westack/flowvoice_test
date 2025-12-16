"""
Page object for the contacts list page (/contacts)
"""
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class ContactsListPage(BasePage):
    """Page Object for Contacts List Page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Locators
        self._page_title = 'h1:has-text("Contacts")'
        self._add_contact_button = 'button:has-text("Add Contact")'
        self._contacts_table = 'table'
        self._table_rows = 'table tbody tr'
        self._empty_state = 'text=/no contacts found/i'
        self._loading_spinner = '.animate-spin'
        self._first_contact_button = 'button:has-text("Add your first contact")'
    
    def navigate_to_contacts(self, base_url: str):
        """Navigate to contacts page"""
        self.navigate(f"{base_url}/contacts")
        return self
    
    def is_page_loaded(self) -> bool:
        """Check if contacts page is loaded"""
        try:
            expect(self.page.locator(self._page_title)).to_be_visible(timeout=5000)
            return True
        except:
            return False
    
    def get_add_contact_button(self):
        """Get add contact button locator"""
        return self.page.locator(self._add_contact_button)
    
    def click_add_contact(self):
        """Click add contact button"""
        self.get_add_contact_button().click()
        return self
    
    def get_contacts_table(self):
        """Get contacts table locator"""
        return self.page.locator(self._contacts_table)
    
    def get_table_rows(self):
        """Get all table rows"""
        return self.page.locator(self._table_rows)
    
    def get_contact_count(self) -> int:
        """Get number of contacts in the table"""
        self.wait_for_timeout(1000)  # Wait for table to render
        return self.get_table_rows().count()
    
    def click_contact_by_index(self, index: int):
        """Click on a contact row by index to navigate to edit page"""
        self.get_table_rows().nth(index).click()
        return self
    
    def is_empty_state_visible(self) -> bool:
        """Check if empty state message is visible"""
        return self.page.locator(self._empty_state).is_visible()
    
    def is_loading(self) -> bool:
        """Check if loading spinner is visible"""
        return self.page.locator(self._loading_spinner).is_visible()
    
    def wait_for_contacts_to_load(self, timeout: int = 10000):
        """Wait for contacts to load (spinner to disappear)"""
        try:
            self.page.wait_for_selector(self._loading_spinner, state='hidden', timeout=timeout)
        except:
            pass  # Spinner might not appear if loading is fast
        return self
    
    def get_contact_name_by_index(self, index: int) -> str:
        """Get contact name by index"""
        row = self.get_table_rows().nth(index)
        # Name is in the second column (index 1)
        name_cell = row.locator('td').nth(1)
        return name_cell.text_content() or ""
    
    def get_contact_email_by_index(self, index: int) -> str:
        """Get contact email by index"""
        row = self.get_table_rows().nth(index)
        # Email is in the third column (index 2)
        email_cell = row.locator('td').nth(2)
        return email_cell.text_content() or ""
    
    def get_contact_phone_by_index(self, index: int) -> str:
        """Get contact phone by index"""
        row = self.get_table_rows().nth(index)
        # Phone is in the fourth column (index 3)
        phone_cell = row.locator('td').nth(3)
        return phone_cell.text_content() or ""
    
    def click_call_button_by_index(self, index: int):
        """Click the call button for a contact by index"""
        row = self.get_table_rows().nth(index)
        # Call button is in the actions column
        call_button = row.locator('button').first
        call_button.click()
        return self
