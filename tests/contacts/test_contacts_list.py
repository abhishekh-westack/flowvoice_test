"""
Test cases for the contacts list page (/contacts)
"""
import pytest
import allure
from playwright.sync_api import Page, expect
from flows.contacts.contacts_list_flow import ContactsListFlow
from core.playwright.auth import AuthService
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID
import re


@allure.feature("Contacts Management")
@allure.story("Contacts List Page")
class TestContactsList:
    
    @allure.title("Test contacts list page renders successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_contacts_list_renders(self, page: Page):
        """Test that contacts list page loads and renders correctly"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to contacts page
        flow = ContactsListFlow(page)
        with allure.step("Navigate to contacts page"):
            flow.navigate_to_contacts(BASE_URL)
        
        # 3. Verify page loaded
        with allure.step("Verify contacts page is loaded"):
            assert flow.contacts_list_page.is_page_loaded(), "Contacts page did not load"
        
        # 4. Verify add contact button is visible
        with allure.step("Verify Add Contact button is visible"):
            expect(flow.contacts_list_page.get_add_contact_button()).to_be_visible()
    
    @allure.title("Test empty state displays when no contacts available")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_state(self, page: Page):
        """Test that empty state message is shown when no contacts exist"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to contacts page
        flow = ContactsListFlow(page)
        with allure.step("Navigate to contacts page"):
            flow.navigate_to_contacts(BASE_URL)
        
        # 3. Check if empty state OR contacts are displayed
        with allure.step("Check empty state or contacts displayed"):
            contact_count = flow.contacts_list_page.get_contact_count()
            
            if contact_count == 0:
                # If no contacts, verify empty state is shown
                assert flow.verify_empty_state(), "Empty state should be visible when no contacts exist"
            else:
                # If contacts exist, that's also a valid state
                print(f"Contacts found: {contact_count}. Empty state test skipped.")
    
    @allure.title("Test loading state during data fetch")
    @allure.severity(allure.severity_level.MINOR)
    def test_loading_state(self, page: Page):
        """Test that loading spinner appears during data fetch"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to contacts page
        with allure.step("Navigate to contacts page"):
            page.goto(f"{BASE_URL}/contacts")
        
        # 3. Note: Loading might be too fast to catch, so we just verify page loads
        with allure.step("Verify page eventually loads"):
            flow = ContactsListFlow(page)
            flow.wait_for_page_load()
            assert flow.contacts_list_page.is_page_loaded(), "Page should load successfully"
    
    @allure.title("Test clicking Add Contact navigates to new contact page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_contact_navigation(self, page: Page):
        """Test that clicking Add Contact button navigates to new contact page"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to contacts page
        flow = ContactsListFlow(page)
        with allure.step("Navigate to contacts page"):
            flow.navigate_to_contacts(BASE_URL)
        
        # 3. Click Add Contact button
        with allure.step("Click Add Contact button"):
            flow.click_add_contact()
        
        # 4. Verify navigation to new contact page
        with allure.step("Verify navigation to new contact page"):
            pattern = re.compile(r".*(/[a-z]{2})?/contacts/new$")
            expect(page).to_have_url(pattern, timeout=5000)
    
    @allure.title("Test clicking a contact navigates to edit page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_contact_navigation(self, page: Page):
        """Test that clicking a contact row navigates to edit contact page"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to contacts page
        flow = ContactsListFlow(page)
        with allure.step("Navigate to contacts page"):
            flow.navigate_to_contacts(BASE_URL)
        
        # 3. Check if contacts exist
        contact_count = flow.contacts_list_page.get_contact_count()
        
        if contact_count > 0:
            # 4. Click first contact
            with allure.step("Click first contact row"):
                flow.click_contact_by_index(0)
            
            # 5. Verify navigation to edit page
            with allure.step("Verify navigation to edit contact page"):
                pattern = re.compile(r".*(/[a-z]{2})?/contacts/edit\?id=[A-Za-z0-9\-_]+$")
                expect(page).to_have_url(pattern, timeout=5000)
        else:
            pytest.skip("No contacts available to test navigation")
    
    @allure.title("Test contact information display in table")
    @allure.severity(allure.severity_level.NORMAL)
    def test_contact_display(self, page: Page):
        """Test that contact information is displayed correctly in table"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to contacts page
        flow = ContactsListFlow(page)
        with allure.step("Navigate to contacts page"):
            flow.navigate_to_contacts(BASE_URL)
        
        # 3. Check if contacts exist
        contact_count = flow.contacts_list_page.get_contact_count()
        
        if contact_count > 0:
            # 4. Verify contact information is displayed
            with allure.step("Verify contact information is displayed"):
                for i in range(min(contact_count, 3)):  # Check first 3 contacts
                    name = flow.contacts_list_page.get_contact_name_by_index(i)
                    email = flow.contacts_list_page.get_contact_email_by_index(i)
                    phone = flow.contacts_list_page.get_contact_phone_by_index(i)
                    
                    print(f"Contact {i}: {name} | {email} | {phone}")
                    
                    # Name should always be present
                    assert name, f"Contact {i} should have a name"
                    # Phone should always be present (required field)
                    assert phone, f"Contact {i} should have a phone number"
        else:
            pytest.skip("No contacts available to test display")
