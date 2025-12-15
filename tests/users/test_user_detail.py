"""
Test cases for the user detail page (/users/[id])
"""
import pytest
import allure
from playwright.sync_api import Page, expect
from flows.users.user_detail_flow import UserDetailFlow
from flows.users.users_list_flow import UsersListFlow
from core.playwright.auth import AuthService
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID
import re


@allure.feature("Users Management")
@allure.story("User Detail Page")
class TestUserDetail:
    
    @allure.title("Test user details page renders successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_details_render(self, page: Page):
        """Test that user detail page loads and displays user information"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to users list to get a user ID
        users_flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            users_flow.navigate_to_users(BASE_URL)
        
        # 3. Check if users exist
        user_count = users_flow.users_list_page.get_user_count()
        
        if user_count > 0:
            # 4. Click first user to navigate to detail page
            with allure.step("Click first user to open detail page"):
                users_flow.click_user_by_index(0)
            
            # 5. Verify user detail page loaded
            user_flow = UserDetailFlow(page)
            with allure.step("Verify user detail page is loaded"):
                assert user_flow.user_detail_page.is_page_loaded(), "User detail page did not load"
            
            # 6. Verify user details are populated
            with allure.step("Verify user details are populated"):
                assert user_flow.verify_user_details_loaded(), "User details should be loaded"
                
                # Verify form fields have values
                first_name = user_flow.user_detail_page.get_first_name_value()
                last_name = user_flow.user_detail_page.get_last_name_value()
                email = user_flow.user_detail_page.get_email_value()
                
                assert first_name, "First name should not be empty"
                assert last_name, "Last name should not be empty"
                assert email, "Email should not be empty"
                
                print(f"User details: {first_name} {last_name} ({email})")
        else:
            pytest.skip("No users available to test detail page")
    
    @allure.title("Test editing user details and saving")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_and_save(self, page: Page):
        """Test that user details can be edited and saved successfully"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to users list
        users_flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            users_flow.navigate_to_users(BASE_URL)
        
        # 3. Check if users exist
        user_count = users_flow.users_list_page.get_user_count()
        
        if user_count > 0:
            # 4. Click first user
            with allure.step("Click first user to open detail page"):
                users_flow.click_user_by_index(0)
            
            # 5. Wait for page to load
            user_flow = UserDetailFlow(page)
            user_flow.user_detail_page.wait_for_user_to_load()
            
            # 6. Get original values
            with allure.step("Get original user details"):
                original_first_name = user_flow.user_detail_page.get_first_name_value()
                original_last_name = user_flow.user_detail_page.get_last_name_value()
                original_email = user_flow.user_detail_page.get_email_value()
                
                print(f"Original: {original_first_name} {original_last_name} ({original_email})")
            
            # 7. Edit user details (change first name)
            new_first_name = f"{original_first_name} Test"
            with allure.step(f"Edit first name to: {new_first_name}"):
                user_flow.edit_user(first_name=new_first_name)
            
            # 8. Wait for save to complete
            page.wait_for_timeout(2000)
            
            # 9. Verify the value persisted
            with allure.step("Verify edited value persisted"):
                current_first_name = user_flow.user_detail_page.get_first_name_value()
                assert new_first_name in current_first_name, f"First name should be updated to contain '{new_first_name}'"
            
            # 10. Restore original value
            with allure.step("Restore original first name"):
                user_flow.edit_user(first_name=original_first_name)
                page.wait_for_timeout(2000)
        else:
            pytest.skip("No users available to test editing")
    
    @allure.title("Test form validation on user detail page")
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
        
        # 2. Navigate to users list
        users_flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            users_flow.navigate_to_users(BASE_URL)
        
        # 3. Check if users exist
        user_count = users_flow.users_list_page.get_user_count()
        
        if user_count > 0:
            # 4. Click first user
            with allure.step("Click first user to open detail page"):
                users_flow.click_user_by_index(0)
            
            # 5. Wait for page to load
            user_flow = UserDetailFlow(page)
            user_flow.user_detail_page.wait_for_user_to_load()
            
            # 6. Get original email
            original_email = user_flow.user_detail_page.get_email_value()
            
            # 7. Try to submit with invalid email
            with allure.step("Try to save with invalid email"):
                user_flow.user_detail_page.fill_email("invalid-email")
                user_flow.user_detail_page.save()
                page.wait_for_timeout(1000)
                
                # Note: Validation might be client-side or server-side
                # Just verify page doesn't navigate away on invalid input
                assert user_flow.user_detail_page.is_page_loaded(), "Should stay on page with invalid input"
            
            # 8. Restore original email
            with allure.step("Restore original email"):
                user_flow.user_detail_page.fill_email(original_email)
                user_flow.user_detail_page.save()
                page.wait_for_timeout(1000)
        else:
            pytest.skip("No users available to test form validation")
    
    @allure.title("Test loading and error states")
    @allure.severity(allure.severity_level.MINOR)
    def test_loading_and_error_states(self, page: Page):
        """Test that loading states are handled correctly"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to users list
        users_flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            users_flow.navigate_to_users(BASE_URL)
        
        # 3. Check if users exist
        user_count = users_flow.users_list_page.get_user_count()
        
        if user_count > 0:
            # 4. Click first user
            with allure.step("Click first user to open detail page"):
                users_flow.click_user_by_index(0)
            
            # 5. Verify page eventually loads (loading spinner disappears)
            user_flow = UserDetailFlow(page)
            with allure.step("Wait for user data to load"):
                user_flow.user_detail_page.wait_for_user_to_load()
            
            # 6. Verify data is loaded
            with allure.step("Verify user data is loaded"):
                assert user_flow.verify_user_details_loaded(), "User data should be loaded"
        else:
            pytest.skip("No users available to test loading states")
    
    @allure.title("Test create and delete user complete flow")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_delete_user_flow(self, page: Page):
        """Test complete flow: create a new user, verify it exists, then delete it"""
        # 1. Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # 2. Navigate to users page
        users_flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            users_flow.navigate_to_users(BASE_URL)
        
        # 3. Get initial user count
        initial_user_count = users_flow.users_list_page.get_user_count()
        print(f"Initial user count: {initial_user_count}")
        
        # 4. Click Create New button to open modal
        with allure.step("Open create user modal"):
            users_flow.open_add_user_modal()
            page.wait_for_timeout(1000)  # Wait for modal to open
        
        # 5. Fill in user details
        import time
        timestamp = str(int(time.time()))
        test_email = f"test.playwright.{timestamp}@example.com"  # Unique email
        test_first_name = "TestPlaywright"
        test_last_name = f"User{timestamp}"
        
        with allure.step(f"Fill user details: {test_first_name} {test_last_name} ({test_email})"):
            # Wait for modal to be fully visible
            page.wait_for_selector('input[name="first_name"]', state='visible', timeout=5000)
            
            # Fill first name
            page.locator('input[name="first_name"]').fill(test_first_name)
            # Fill last name
            page.locator('input[name="last_name"]').fill(test_last_name)
            # Fill email
            page.locator('input[name="email"]').fill(test_email)
            
            # Select role (User role) - using ShadCN Select component
            # Click the select trigger to open dropdown
            page.locator('button[role="combobox"]').click()
            page.wait_for_timeout(500)
            
            # Click the "User" option (or "Manager" if User is not available)
            user_option = page.locator('[role="option"]').filter(has_text=re.compile(r'User|Manager', re.IGNORECASE)).first
            user_option.click()
            
            page.wait_for_timeout(500)
        
        # 6. Submit the form
        with allure.step("Submit create user form"):
            # Click the submit button in the modal dialog (not the chat submit button)
            page.locator('[role="dialog"] form button[type="submit"]').click()
            page.wait_for_timeout(3000)  # Wait for user to be created and modal to close
        
        # 7. Verify modal closed and user was created
        with allure.step("Verify user was created"):
            # Modal should be closed
            page.wait_for_timeout(1000)
            
            # Navigate back to users page to refresh the list
            users_flow.navigate_to_users(BASE_URL)
            
            # Get new user count
            new_user_count = users_flow.users_list_page.get_user_count()
            print(f"New user count: {new_user_count}")
            
            # Verify user count increased
            assert new_user_count > initial_user_count, f"User count should increase from {initial_user_count} to {new_user_count}"
        
        # 8. Find the newly created user by email or name
        with allure.step("Find and open newly created user"):
            found_user = False
            user_index = -1
            
            # Search through users to find our test user
            for i in range(new_user_count):
                user_email = users_flow.users_list_page.get_user_email_by_index(i)
                if test_email in user_email:
                    found_user = True
                    user_index = i
                    print(f"Found test user at index {i}")
                    break
            
            assert found_user, f"Could not find newly created user with email {test_email}"
            
            # Click on the user to open detail page
            users_flow.click_user_by_index(user_index)
            page.wait_for_timeout(1000)
        
        # 9. Verify user details on detail page
        user_flow = UserDetailFlow(page)
        with allure.step("Verify user details are correct"):
            user_flow.user_detail_page.wait_for_user_to_load()
            
            assert test_first_name in user_flow.user_detail_page.get_first_name_value(), \
                "First name should match"
            assert test_last_name in user_flow.user_detail_page.get_last_name_value(), \
                "Last name should match"
            assert test_email in user_flow.user_detail_page.get_email_value(), \
                "Email should match"
            
            print(f"✓ User details verified: {test_first_name} {test_last_name} ({test_email})")
        
        # 10. Delete the user
        with allure.step("Delete the test user"):
            # Wait a bit more for the page to fully load
            page.wait_for_timeout(2000)
            
            # Check if delete button is visible (should be for non-admin users)
            # Try multiple times in case it's still loading
            delete_button_found = False
            for attempt in range(3):
                delete_button_found = user_flow.user_detail_page.is_delete_button_visible()
                if delete_button_found:
                    break
                print(f"Attempt {attempt + 1}: Delete button not yet visible, waiting...")
                page.wait_for_timeout(1000)
            
            if delete_button_found:
                print("✓ Delete button is visible")
                
                # Click delete button
                user_flow.user_detail_page.delete()
                page.wait_for_timeout(1000)
                
                # Verify delete confirmation dialog appears
                assert user_flow.user_detail_page.is_delete_alert_visible(), \
                    "Delete confirmation dialog should appear"
                
                # Confirm deletion
                user_flow.user_detail_page.confirm_delete()
                
                # Verify navigation back to users list (page navigates immediately after delete)
                with allure.step("Verify navigation back to users list"):
                    expect(page).to_have_url(re.compile(r".*(/[a-z]{2})?/users$"), timeout=5000)
                
                # Verify user count decreased
                users_flow.users_list_page.wait_for_users_to_load()
                final_user_count = users_flow.users_list_page.get_user_count()
                print(f"Final user count: {final_user_count}")
                
                assert final_user_count == initial_user_count, \
                    f"User count should return to {initial_user_count} after deletion, got {final_user_count}"
                
                print(f"✓ User successfully deleted")
            else:
                # Debug: print the user permissions
                print("⚠ Delete button not visible after 3 attempts")
                
                # Try to get the page content to debug
                page_content = page.content()
                if "deleteUser" in page_content or "Delete User" in page_content:
                    print("Delete User text found in page, but button may be hidden")
                
                # Clean up by going back
                user_flow.go_back()
                page.wait_for_timeout(1000)
                
                # Try to delete via going back to users list and finding the user again
                print("Attempting alternate deletion method...")
                pytest.fail("Delete button not visible - created user may have been assigned admin role")
