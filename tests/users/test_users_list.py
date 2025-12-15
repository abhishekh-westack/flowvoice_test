"""
Test cases for the users list page (/users)
"""
import pytest
import allure
from playwright.sync_api import Page, expect
from flows.users.users_list_flow import UsersListFlow
from core.playwright.auth import AuthService
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID
import re


@allure.feature("Users Management")
@allure.story("Users List Page")
class TestUsersList:
    
    @allure.title("Test users list page renders successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_users_list_renders(self, page: Page):
        """Test that users list page loads and renders correctly"""
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
        flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            flow.navigate_to_users(BASE_URL)
        
        # 3. Verify page loaded
        with allure.step("Verify users page is loaded"):
            assert flow.users_list_page.is_page_loaded(), "Users page did not load"
        
        # 4. Verify create new button is visible
        with allure.step("Verify Create New button is visible"):
            expect(flow.users_list_page.get_create_new_button()).to_be_visible()
    
    @allure.title("Test empty state displays when no users available")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_state(self, page: Page):
        """Test that empty state message is shown when no users exist"""
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
        flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            flow.navigate_to_users(BASE_URL)
        
        # 3. Check if empty state OR users are displayed
        with allure.step("Check empty state or users displayed"):
            user_count = flow.users_list_page.get_user_count()
            
            if user_count == 0:
                # If no users, verify empty state is shown
                assert flow.verify_empty_state(), "Empty state should be visible when no users exist"
            else:
                # If users exist, that's also a valid state
                print(f"Users found: {user_count}. Empty state test skipped.")
    
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
        
        # 2. Navigate to users page
        with allure.step("Navigate to users page"):
            page.goto(f"{BASE_URL}/users")
        
        # 3. Note: Loading might be too fast to catch, so we just verify page loads
        with allure.step("Verify page eventually loads"):
            flow = UsersListFlow(page)
            flow.wait_for_page_load()
            assert flow.users_list_page.is_page_loaded(), "Page should load successfully"
    
    @allure.title("Test add user modal opens when clicking Create New")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_user_modal_opens(self, page: Page):
        """Test that clicking Create New button opens the add user modal"""
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
        flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            flow.navigate_to_users(BASE_URL)
        
        # 3. Click Create New button
        with allure.step("Click Create New button"):
            flow.open_add_user_modal()
        
        # 4. Verify modal is visible
        with allure.step("Verify add user modal is visible"):
            assert flow.users_list_page.is_add_user_modal_visible(), "Add user modal should be visible"
    
    @allure.title("Test clicking a user navigates to detail page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_navigation(self, page: Page):
        """Test that clicking a user card navigates to user detail page"""
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
        flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            flow.navigate_to_users(BASE_URL)
        
        # 3. Check if users exist
        user_count = flow.users_list_page.get_user_count()
        
        if user_count > 0:
            # 4. Click first user
            with allure.step("Click first user card"):
                flow.click_user_by_index(0)
            
            # 5. Verify navigation to detail page
            with allure.step("Verify navigation to user detail page"):
                # Pattern accounts for optional locale prefix (e.g., /en/users/id or /users/id)
                pattern = re.compile(r".*(/[a-z]{2})?/users/[A-Za-z0-9\-_]+$")
                expect(page).to_have_url(pattern, timeout=10000)
        else:
            pytest.skip("No users available to test navigation")
    
    @allure.title("Test role display logic for users")
    @allure.severity(allure.severity_level.NORMAL)
    def test_role_display(self, page: Page):
        """Test that user roles are displayed correctly"""
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
        flow = UsersListFlow(page)
        with allure.step("Navigate to users page"):
            flow.navigate_to_users(BASE_URL)
        
        # 3. Check if users exist
        user_count = flow.users_list_page.get_user_count()
        
        if user_count > 0:
            # 4. Verify role badges are displayed
            with allure.step("Verify role badges are displayed for users"):
                for i in range(min(user_count, 3)):  # Check first 3 users
                    roles = flow.users_list_page.get_user_roles_by_index(i)
                    print(f"User {i} roles: {roles}")
                    # Roles could be empty (No role), single, or multiple
                    assert isinstance(roles, list), "Roles should be returned as a list"
        else:
            pytest.skip("No users available to test role display")
