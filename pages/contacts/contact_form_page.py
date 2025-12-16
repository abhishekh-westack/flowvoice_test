"""
Page object for the contact form page (/contacts/new and /contacts/edit)
"""
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class ContactFormPage(BasePage):
    """Page Object for Contact Form Page (both new and edit)"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Locators
        self._page_title_new = 'h1:has-text("New Contact")'
        self._page_title_edit = 'h1:has-text("Edit Contact")'
        self._back_button = 'svg.lucide-chevron-left'
        self._first_name_input = 'input[name="FirstName"]'
        self._last_name_input = 'input[name="LastName"]'
        self._email_input = 'input[name="Email"]'
        self._phone_input = 'input[name="PhoneNumber"]'
        self._save_button = 'button[type="submit"]:has-text("Save")'
        self._cancel_button = 'button:has-text("Cancel")'
        self._delete_button = 'button:has-text("Delete")'
        self._loading_spinner = '.animate-spin'
        self._delete_alert = '[role="alertdialog"]'
        self._confirm_delete = 'button:has-text("Continue")'
        self._success_message = 'text=/success/i'
    
    def navigate_to_new_contact(self, base_url: str):
        """Navigate to new contact page"""
        self.navigate(f"{base_url}/contacts/new")
        return self
    
    def navigate_to_edit_contact(self, base_url: str, contact_id: str):
        """Navigate to edit contact page"""
        self.navigate(f"{base_url}/contacts/edit?id={contact_id}")
        return self
    
    def is_new_page_loaded(self) -> bool:
        """Check if new contact page is loaded"""
        try:
            expect(self.page.locator(self._page_title_new)).to_be_visible(timeout=5000)
            return True
        except:
            return False
    
    def is_edit_page_loaded(self) -> bool:
        """Check if edit contact page is loaded"""
        try:
            expect(self.page.locator(self._page_title_edit)).to_be_visible(timeout=5000)
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
    
    def get_phone_input(self):
        """Get phone input locator"""
        return self.page.locator(self._phone_input)
    
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
    
    def fill_phone(self, phone: str):
        """Fill phone field"""
        self.get_phone_input().fill(phone)
        return self
    
    def save(self):
        """Click save button"""
        self.get_save_button().click()
        return self
    
    def cancel(self):
        """Click cancel button"""
        self.page.locator(self._cancel_button).click()
        return self
    
    def delete(self):
        """Click delete button"""
        self.get_delete_button().click()
        return self
    
    def confirm_delete(self):
        """Confirm delete in alert dialog"""
        self.page.locator(self._confirm_delete).click(force=True)
        return self
    
    def is_delete_alert_visible(self) -> bool:
        """Check if delete alert dialog is visible"""
        return self.page.locator(self._delete_alert).is_visible()
    
    def is_loading(self) -> bool:
        """Check if loading spinner is visible"""
        return self.page.locator(self._loading_spinner).is_visible()
    
    def wait_for_contact_to_load(self, timeout: int = 10000):
        """Wait for contact data to load (spinner to disappear)"""
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
    
    def get_phone_value(self) -> str:
        """Get current phone value"""
        return self.get_phone_input().input_value()
    
    def is_delete_button_visible(self) -> bool:
        """Check if delete button is visible (only on edit page)"""
        try:
            return self.get_delete_button().is_visible(timeout=1000)
        except:
            return False
