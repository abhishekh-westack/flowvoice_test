"""
Test cases for contact form pages (/contacts/new and /contacts/edit)
"""
import pytest
import allure
from playwright.sync_api import Page, expect
from flows.contacts.contact_form_flow import ContactFormFlow
from flows.contacts.contacts_list_flow import ContactsListFlow
from core.playwright.auth import AuthService
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID
import re
import time


@allure.feature("Contacts Management")
@allure.story("Contact Form")
class TestContactForm:
    
    @allure.title("Test new contact page renders successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_new_contact_page_renders(self, page: Page):
        """Test that new contact page loads correctly"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to new contact page
        flow = ContactFormFlow(page)
        with allure.step("Navigate to new contact page"):
            flow.navigate_to_new_contact(BASE_URL)
        
        # 3. Verify page loaded
        with allure.step("Verify new contact page is loaded"):
            assert flow.contact_form_page.is_new_page_loaded(), "New contact page did not load"
        
        # 4. Verify form fields are present
        with allure.step("Verify form fields are present"):
            expect(flow.contact_form_page.get_first_name_input()).to_be_visible()
            expect(flow.contact_form_page.get_last_name_input()).to_be_visible()
            expect(flow.contact_form_page.get_email_input()).to_be_visible()
            expect(flow.contact_form_page.get_phone_input()).to_be_visible()
            expect(flow.contact_form_page.get_save_button()).to_be_visible()
    
    @allure.title("Test edit contact page renders successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_contact_page_renders(self, page: Page):
        """Test that edit contact page loads and displays contact information"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to contacts list to get a contact
        contacts_flow = ContactsListFlow(page)
        with allure.step("Navigate to contacts page"):
            contacts_flow.navigate_to_contacts(BASE_URL)
        
        # 3. Check if contacts exist
        contact_count = contacts_flow.contacts_list_page.get_contact_count()
        
        if contact_count > 0:
            # 4. Click first contact to navigate to edit page
            with allure.step("Click first contact to open edit page"):
                contacts_flow.click_contact_by_index(0)
            
            # 5. Verify edit page loaded
            form_flow = ContactFormFlow(page)
            with allure.step("Verify edit contact page is loaded"):
                assert form_flow.contact_form_page.is_edit_page_loaded(), "Edit contact page did not load"
            
            # 6. Verify contact details are populated
            with allure.step("Verify contact details are populated"):
                form_flow.contact_form_page.wait_for_contact_to_load()
                assert form_flow.verify_contact_details_loaded(), "Contact details should be loaded"
                
                first_name = form_flow.contact_form_page.get_first_name_value()
                last_name = form_flow.contact_form_page.get_last_name_value()
                phone = form_flow.contact_form_page.get_phone_value()
                
                assert first_name, "First name should not be empty"
                assert last_name, "Last name should not be empty"
                assert phone, "Phone number should not be empty"
                
                print(f"Contact details: {first_name} {last_name} | Phone: {phone}")
        else:
            pytest.skip("No contacts available to test edit page")
    
    @allure.title("Test form validation on new contact page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_validation(self, page: Page):
        """Test that form validation works correctly"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to new contact page
        flow = ContactFormFlow(page)
        with allure.step("Navigate to new contact page"):
            flow.navigate_to_new_contact(BASE_URL)
        
        # 3. Try to submit empty form
        with allure.step("Try to submit empty form"):
            flow.contact_form_page.save()
            page.wait_for_timeout(1000)
            
            # Verify page doesn't navigate (stays on form due to validation errors)
            assert flow.contact_form_page.is_new_page_loaded(), "Should stay on form with validation errors"
        
        # 4. Try to submit with invalid phone number
        with allure.step("Try to submit with invalid phone number"):
            flow.contact_form_page.fill_first_name("Test")
            flow.contact_form_page.fill_last_name("User")
            flow.contact_form_page.fill_phone("12345")  # Invalid format (missing +)
            flow.contact_form_page.save()
            page.wait_for_timeout(1000)
            
            # Should still be on the form
            assert flow.contact_form_page.is_new_page_loaded(), "Should stay on form with invalid phone"
    
    @allure.title("Test editing contact details")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_contact_and_save(self, page: Page):
        """Test that contact details can be edited and saved successfully"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to contacts list
        contacts_flow = ContactsListFlow(page)
        with allure.step("Navigate to contacts page"):
            contacts_flow.navigate_to_contacts(BASE_URL)
        
        # 3. Check if contacts exist
        contact_count = contacts_flow.contacts_list_page.get_contact_count()
        
        if contact_count > 0:
            # 4. Click first contact
            with allure.step("Click first contact to open edit page"):
                contacts_flow.click_contact_by_index(0)
            
            # 5. Wait for page to load
            form_flow = ContactFormFlow(page)
            form_flow.contact_form_page.wait_for_contact_to_load()
            
            # 6. Get original values
            with allure.step("Get original contact details"):
                original_first_name = form_flow.contact_form_page.get_first_name_value()
                original_last_name = form_flow.contact_form_page.get_last_name_value()
                original_email = form_flow.contact_form_page.get_email_value()
                
                print(f"Original: {original_first_name} {original_last_name} ({original_email})")
            
            # 7. Edit contact details (change email if empty, or add a suffix to first name)
            if not original_email or original_email.strip() == "":
                # Add an email if missing
                new_email = f"test.edit.{int(time.time())}@example.com"
                with allure.step(f"Add email: {new_email}"):
                    form_flow.edit_contact(email=new_email)
                
                # 8. Verify navigation back to contacts list
                with allure.step("Verify navigation back to contacts list"):
                    expect(page).to_have_url(re.compile(r".*(/[a-z]{2})?/contacts$"), timeout=5000)
                
                # 9. Navigate back to edit page to verify changes
                with allure.step("Navigate back to verify changes"):
                    contacts_flow.navigate_to_contacts(BASE_URL)
                    contacts_flow.click_contact_by_index(0)
                    form_flow.contact_form_page.wait_for_contact_to_load()
                    
                    current_email = form_flow.contact_form_page.get_email_value()
                    assert new_email in current_email, f"Email should be updated to '{new_email}'"
                
                # 10. Restore original value (empty)
                with allure.step("Restore original email"):
                    form_flow.edit_contact(email="")
            else:
                # Just verify we can save without changes
                with allure.step("Save without changes"):
                    form_flow.contact_form_page.save()
                    page.wait_for_timeout(1500)
                
                # Verify navigation back to contacts list
                with allure.step("Verify navigation back to contacts list"):
                    expect(page).to_have_url(re.compile(r".*(/[a-z]{2})?/contacts$"), timeout=5000)
        else:
            pytest.skip("No contacts available to test editing")
    
    @allure.title("Test create and delete contact flow")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_delete_contact_flow(self, page: Page):
        """Test creating a new contact and then deleting it"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to contacts page and get initial count
        contacts_flow = ContactsListFlow(page)
        with allure.step("Navigate to contacts page"):
            contacts_flow.navigate_to_contacts(BASE_URL)
        
        initial_contact_count = contacts_flow.contacts_list_page.get_contact_count()
        print(f"Initial contact count: {initial_contact_count}")
        
        # 3. Navigate to new contact page
        form_flow = ContactFormFlow(page)
        with allure.step("Navigate to new contact page"):
            form_flow.navigate_to_new_contact(BASE_URL)
        
        # 4. Create a new contact with unique data
        timestamp = int(time.time())
        test_first_name = f"TestContact"
        test_last_name = f"Playwright{timestamp}"
        test_email = f"test.contact.{timestamp}@example.com"
        test_phone = f"+1234567{timestamp % 1000:03d}"  # Valid E.164 format
        
        with allure.step(f"Create new contact: {test_first_name} {test_last_name}"):
            form_flow.create_contact(
                first_name=test_first_name,
                last_name=test_last_name,
                email=test_email,
                phone=test_phone
            )
        
        # 5. Verify navigation back to contacts list
        with allure.step("Verify navigation back to contacts list after creation"):
            expect(page).to_have_url(re.compile(r".*(/[a-z]{2})?/contacts$"), timeout=5000)
        
        # 6. Verify contact count increased
        with allure.step("Verify contact was added"):
            contacts_flow.contacts_list_page.wait_for_contacts_to_load()
            new_contact_count = contacts_flow.contacts_list_page.get_contact_count()
            print(f"New contact count: {new_contact_count}")
            
            assert new_contact_count == initial_contact_count + 1, \
                f"Contact count should increase by 1, expected {initial_contact_count + 1}, got {new_contact_count}"
        
        # 7. Find the newly created contact by searching through the list
        with allure.step("Find the newly created contact"):
            found_contact_index = None
            for i in range(new_contact_count):
                name = contacts_flow.contacts_list_page.get_contact_name_by_index(i)
                if test_first_name in name and test_last_name in name:
                    found_contact_index = i
                    print(f"Found test contact at index {i}")
                    break
            
            assert found_contact_index is not None, "Could not find the newly created contact"
        
        # 8. Click on the contact to open edit page
        with allure.step("Open the newly created contact for editing"):
            contacts_flow.click_contact_by_index(found_contact_index)
        
        # 9. Verify contact details are correct
        with allure.step("Verify contact details are correct"):
            form_flow.contact_form_page.wait_for_contact_to_load()
            
            assert test_first_name in form_flow.contact_form_page.get_first_name_value(), \
                "First name should match"
            assert test_last_name in form_flow.contact_form_page.get_last_name_value(), \
                "Last name should match"
            assert test_email in form_flow.contact_form_page.get_email_value(), \
                "Email should match"
            assert test_phone in form_flow.contact_form_page.get_phone_value(), \
                "Phone should match"
            
            print(f"✓ Contact details verified: {test_first_name} {test_last_name} ({test_email})")
        
        # 10. Delete the contact
        with allure.step("Delete the test contact"):
            page.wait_for_timeout(1000)
            
            # Verify delete button is visible
            assert form_flow.contact_form_page.is_delete_button_visible(), \
                "Delete button should be visible"
            
            # Delete the contact
            form_flow.delete_contact()
            
            # Verify navigation back to contacts list
            with allure.step("Verify navigation back to contacts list after deletion"):
                expect(page).to_have_url(re.compile(r".*(/[a-z]{2})?/contacts$"), timeout=5000)
            
            # Verify contact count decreased
            contacts_flow.contacts_list_page.wait_for_contacts_to_load()
            final_contact_count = contacts_flow.contacts_list_page.get_contact_count()
            print(f"Final contact count: {final_contact_count}")
            
            assert final_contact_count == initial_contact_count, \
                f"Contact count should return to {initial_contact_count} after deletion, got {final_contact_count}"
            
            print(f"✓ Contact successfully deleted")
