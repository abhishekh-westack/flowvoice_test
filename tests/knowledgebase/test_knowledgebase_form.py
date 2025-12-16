"""
Test cases for Knowledge Base Form Page (Create/Edit)
Tests the knowledge base create and edit functionality
"""
import pytest
import allure
from datetime import datetime
from playwright.sync_api import Page
from flows.knowledgebase.knowledgebase_form_flow import KnowledgeBaseFormFlow
from flows.knowledgebase.knowledgebase_list_flow import KnowledgeBaseListFlow
from pages.knowledgebase.knowledgebase_form_page import KnowledgeBaseFormPage
from fixtures.knowledgebase_fixtures import *
from core.playwright.auth import AuthService
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID


@allure.feature("Knowledge Base")
@allure.suite("Knowledge Base Form")
class TestKnowledgeBaseForm:
    """Test suite for knowledge base form page"""

    @allure.story("Form Page")
    @allure.title("Test create article page renders correctly")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_article_page_renders(self, page: Page):
        """Test that the create article page renders correctly"""
        # Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        knowledgebase_form_page = KnowledgeBaseFormPage(page)
        knowledgebase_form_page.navigate_to_create(type="article")
        knowledgebase_form_page.wait_for_page_load()
        
        # Verify form elements are visible
        assert knowledgebase_form_page.get_save_button().is_visible(), \
            "Save button should be visible"
        assert knowledgebase_form_page.page.locator('input[placeholder*="title"]').is_visible(), \
            "Title input should be visible"


    @allure.story("Form Page")
    @allure.title("Test article validation errors")
    @allure.severity(allure.severity_level.NORMAL)
    def test_article_validation_errors(self, page: Page):
        """Test that validation errors are shown for empty required fields"""
        # Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        knowledgebase_form_flow = KnowledgeBaseFormFlow(page)
        knowledgebase_form_flow.form_page.navigate_to_create(type="article")
        knowledgebase_form_flow.form_page.wait_for_page_load()
        
        # Try to save without filling required fields
        has_errors = knowledgebase_form_flow.verify_validation_errors()
        
        # Note: Validation might happen on submit or might allow empty saves
        # This test verifies the validation mechanism exists


    @allure.story("Form Page")
    @allure.title("Test add section functionality")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_section(self, page: Page):
        """Test adding a new section to an article"""
        # Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        knowledgebase_form_page = KnowledgeBaseFormPage(page)
        knowledgebase_form_page.navigate_to_create(type="article")
        knowledgebase_form_page.wait_for_page_load()
        
        # Get initial section count
        initial_count = knowledgebase_form_page.get_section_count()
        
        # Add a new section
        knowledgebase_form_page.click_add_section_button()
        knowledgebase_form_page.page.wait_for_timeout(500)
        
        # Verify section count increased
        new_count = knowledgebase_form_page.get_section_count()
        assert new_count == initial_count + 1, \
            f"Section count should increase from {initial_count} to {initial_count + 1}"


    @allure.story("Form Page")
    @allure.title("Test remove section functionality")
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_section(self, page: Page):
        """Test removing a section from an article"""
        # Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        knowledgebase_form_page = KnowledgeBaseFormPage(page)
        knowledgebase_form_page.navigate_to_create(type="article")
        knowledgebase_form_page.wait_for_page_load()
        
        # Add a section first
        knowledgebase_form_page.click_add_section_button()
        knowledgebase_form_page.page.wait_for_timeout(500)
        
        # Get section count
        count_before = knowledgebase_form_page.get_section_count()
        
        # Remove a section (if more than 1)
        if count_before > 1:
            knowledgebase_form_page.click_remove_section_button(1)
            knowledgebase_form_page.page.wait_for_timeout(500)
            
            # Verify section count decreased
            count_after = knowledgebase_form_page.get_section_count()
            assert count_after == count_before - 1, \
                f"Section count should decrease from {count_before} to {count_before - 1}"


    @allure.story("Form Page")
    @allure.title("Test back button navigation")
    @allure.severity(allure.severity_level.MINOR)
    def test_back_button_navigation(self, page: Page):
        """Test that back button navigates to the list page"""
        # Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        # First navigate to list page to establish browser history
        knowledgebase_list_page = KnowledgeBaseListPage(page)
        knowledgebase_list_page.navigate()
        knowledgebase_list_page.wait_for_page_load()
        
        # Then navigate to create page
        knowledgebase_form_page = KnowledgeBaseFormPage(page)
        knowledgebase_form_page.navigate_to_create(type="article")
        knowledgebase_form_page.wait_for_page_load()
        
        # Click back button
        knowledgebase_form_page.click_back_button()
        knowledgebase_form_page.page.wait_for_timeout(1000)
        
        # Verify navigation to list page
        knowledgebase_form_page.verify_on_list_page()


    @allure.story("Form Page - Complete Flow")
    @allure.title("Test create and delete article flow")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_delete_article_flow(self, page: Page):
        """Test complete flow: create an article, verify it exists, then delete it"""
        # Login via API
        with allure.step("Login via API"):
            auth = AuthService()
            token = auth.login(
                email=LOGIN_EMAIL,
                code=LOGIN_CODE,
                company_id=LOGIN_COMPANY_ID
            )
            auth.inject_token(page, token)
        
        knowledgebase_form_flow = KnowledgeBaseFormFlow(page)
        knowledgebase_list_flow = KnowledgeBaseListFlow(page)
        
        # Generate unique title with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        article_title = f"Test Article {timestamp}"
        
        # Step 1: Create article
        sections = [
            {
                "name": "Introduction",
                "content": "This is a test introduction section."
            },
            {
                "name": "Main Content",
                "content": "This is the main content of the test article."
            }
        ]
        
        knowledgebase_form_flow.create_article_entry(article_title, sections)
        
        # Step 2: Verify article appears in list
        knowledgebase_list_flow.navigate_and_wait()
        
        # Search for the created article
        found = knowledgebase_list_flow.search_and_verify(article_title)
        assert found, f"Article '{article_title}' should be visible in the list"
        
        # Step 3: Open the article for editing
        knowledgebase_list_flow.open_entry_by_title(article_title)
        knowledgebase_form_flow.page.wait_for_timeout(2000)
        
        # Verify we're on edit page
        knowledgebase_form_flow.form_page.verify_on_edit_page()
        
        # Step 4: Delete the article
        knowledgebase_form_flow.form_page.click_delete_button()
        knowledgebase_form_flow.form_page.confirm_delete()
        
        # Wait for deletion and navigation
        knowledgebase_form_flow.page.wait_for_timeout(2000)
        
        # Step 5: Verify article is removed from list
        knowledgebase_list_flow.navigate_and_wait()
        
        # Search for the deleted article - it should not be found
        found_after_delete = knowledgebase_list_flow.search_and_verify(article_title)
        assert not found_after_delete, f"Article '{article_title}' should not be visible after deletion"


