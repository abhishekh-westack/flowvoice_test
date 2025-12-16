"""
Flow for contact form page actions
"""
from playwright.sync_api import Page
import allure
from pages.contacts.contact_form_page import ContactFormPage

class ContactFormFlow:
    """High-level flow for contact form page (new/edit)"""
    
    def __init__(self, page: Page):
        self.page = page
        self.contact_form_page = ContactFormPage(page)
    
    @allure.step("Navigate to new contact page")
    def navigate_to_new_contact(self, base_url: str):
        """Navigate to new contact page"""
        self.contact_form_page.navigate_to_new_contact(base_url)
        return self
    
    @allure.step("Navigate to edit contact page: {contact_id}")
    def navigate_to_edit_contact(self, base_url: str, contact_id: str):
        """Navigate to edit contact page"""
        self.contact_form_page.navigate_to_edit_contact(base_url, contact_id)
        self.contact_form_page.wait_for_contact_to_load()
        return self
    
    @allure.step("Create contact: {first_name} {last_name}")
    def create_contact(self, first_name: str, last_name: str, email: str = "", phone: str = ""):
        """Fill and submit new contact form"""
        self.contact_form_page.fill_first_name(first_name)
        self.contact_form_page.fill_last_name(last_name)
        if email:
            self.contact_form_page.fill_email(email)
        if phone:
            self.contact_form_page.fill_phone(phone)
        
        self.contact_form_page.save()
        self.page.wait_for_timeout(1500)  # Wait for save to complete
        return self
    
    @allure.step("Edit contact")
    def edit_contact(self, first_name: str = None, last_name: str = None, email: str = None, phone: str = None):
        """Edit contact details and save"""
        if first_name is not None:
            self.contact_form_page.fill_first_name(first_name)
        if last_name is not None:
            self.contact_form_page.fill_last_name(last_name)
        if email is not None:
            self.contact_form_page.fill_email(email)
        if phone is not None:
            self.contact_form_page.fill_phone(phone)
        
        self.contact_form_page.save()
        self.page.wait_for_timeout(1500)  # Wait for save to complete
        return self
    
    @allure.step("Delete contact")
    def delete_contact(self):
        """Delete contact and confirm"""
        self.contact_form_page.delete()
        self.page.wait_for_timeout(500)  # Wait for alert to appear
        
        if self.contact_form_page.is_delete_alert_visible():
            self.contact_form_page.confirm_delete()
            self.page.wait_for_timeout(1500)  # Wait for deletion to complete
        
        return self
    
    @allure.step("Verify contact details loaded")
    def verify_contact_details_loaded(self) -> bool:
        """Verify that contact details are loaded on the page"""
        return (
            self.contact_form_page.get_first_name_value() != "" and
            self.contact_form_page.get_last_name_value() != ""
        )
    
    @allure.step("Go back to contacts list")
    def go_back(self):
        """Click back button to return to contacts list"""
        self.contact_form_page.click_back()
        return self
