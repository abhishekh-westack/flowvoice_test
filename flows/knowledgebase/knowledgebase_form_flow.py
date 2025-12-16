"""
Flow Object for Knowledge Base Form (Create/Edit)
Combines page actions into complete user workflows
"""
from pages.knowledgebase.knowledgebase_form_page import KnowledgeBaseFormPage
from playwright.sync_api import Page
import allure
from config.env import BASE_URL


class KnowledgeBaseFormFlow:
    """Flow object for knowledge base form operations"""
    
    def __init__(self, page: Page):
        self.page = page
        self.form_page = KnowledgeBaseFormPage(page)
        
    @allure.step("Create article entry with title: {title}")
    def create_article_entry(self, title: str, sections: list, base_url: str = None):
        """
        Create a new article entry
        sections: list of dicts with 'name' and 'content' keys
        """
        if base_url is None:
            base_url = BASE_URL
        self.form_page.navigate_to_create(base_url=base_url, type="article")
        self.form_page.wait_for_page_load()
        
        # Fill title
        self.form_page.fill_title(title)
        
        # Fill sections
        for i, section in enumerate(sections):
            if i > 0:  # Add section if not the first one
                self.form_page.click_add_section_button()
                self.page.wait_for_timeout(500)
                
            self.form_page.fill_section_name(section['name'], i)
            self.form_page.fill_section_content(section['content'], i)
            
        # Save
        self.form_page.click_save_button()
        self.page.wait_for_timeout(2000)  # Wait for save to complete
        
    @allure.step("Create URL entry with title: {title}")
    def create_url_entry(self, title: str, url: str, frequency: str = "24", prompt: str = "", base_url: str = None):
        """
        Create a new URL entry
        """
        if base_url is None:
            base_url = BASE_URL
        self.form_page.navigate_to_create(base_url=base_url, type="url")
        self.form_page.wait_for_page_load()
        
        # Fill fields
        self.form_page.fill_title(title)
        self.form_page.fill_url(url)
        self.form_page.select_frequency(frequency)
        if prompt:
            self.form_page.fill_prompt(prompt)
            
        # Save
        self.form_page.click_save_button()
        self.page.wait_for_timeout(2000)  # Wait for save to complete
        
    @allure.step("Edit entry title to: {new_title}")
    def edit_entry_title(self, entry_id: str, new_title: str, base_url: str = None):
        """Edit an entry's title"""
        if base_url is None:
            base_url = BASE_URL
        self.form_page.navigate_to_edit(entry_id, base_url=base_url)
        self.form_page.wait_for_page_load()
        
        self.form_page.fill_title(new_title)
        self.form_page.click_save_button()
        self.page.wait_for_timeout(2000)
        
    @allure.step("Edit entry and add section")
    def edit_and_add_section(self, entry_id: str, section_name: str, section_content: str, base_url: str = None):
        """Edit an entry and add a new section"""
        if base_url is None:
            base_url = BASE_URL
        self.form_page.navigate_to_edit(entry_id, base_url=base_url)
        self.form_page.wait_for_page_load()
        
        # Get current section count
        current_count = self.form_page.get_section_count()
        
        # Add new section
        self.form_page.click_add_section_button()
        self.page.wait_for_timeout(500)
        
        # Fill new section
        self.form_page.fill_section_name(section_name, current_count)
        self.form_page.fill_section_content(section_content, current_count)
        
        # Save
        self.form_page.click_save_button()
        self.page.wait_for_timeout(2000)
        
    @allure.step("Delete entry")
    def delete_entry(self, entry_id: str, base_url: str = None):
        """Delete a knowledge base entry"""
        if base_url is None:
            base_url = BASE_URL
        self.form_page.navigate_to_edit(entry_id, base_url=base_url)
        self.form_page.wait_for_page_load()
        
        self.form_page.click_delete_button()
        self.form_page.confirm_delete()
        self.page.wait_for_timeout(2000)
        
    @allure.step("Verify entry details match")
    def verify_entry_details(self, entry_id: str, expected_title: str, expected_section_count: int = None, base_url: str = None):
        """Verify entry details on edit page"""
        if base_url is None:
            base_url = BASE_URL
        self.form_page.navigate_to_edit(entry_id, base_url=base_url)
        self.form_page.wait_for_page_load()
        
        # Verify title
        actual_title = self.form_page.get_title_value()
        assert actual_title == expected_title, f"Expected title '{expected_title}', got '{actual_title}'"
        
        # Verify section count if provided
        if expected_section_count is not None:
            actual_count = self.form_page.get_section_count()
            assert actual_count == expected_section_count, f"Expected {expected_section_count} sections, got {actual_count}"
            
    @allure.step("Verify validation errors are shown")
    def verify_validation_errors(self):
        """Verify that validation errors are shown when required fields are empty"""
        # Try to save without filling required fields
        self.form_page.click_save_button()
        self.page.wait_for_timeout(500)
        
        # Check for validation errors
        has_errors = (
            self.form_page.is_title_error_visible() or
            self.form_page.is_section_name_error_visible() or
            self.form_page.is_content_error_visible()
        )
        
        return has_errors
        
    @allure.step("Navigate back to list")
    def navigate_back_to_list(self):
        """Navigate back to the knowledge base list page"""
        self.form_page.click_back_button()
        self.page.wait_for_timeout(1000)
