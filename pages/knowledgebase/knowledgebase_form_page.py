"""
Page Object Model for Knowledge Base Form Page (Create/Edit)
Handles all interactions with the knowledge base create and edit pages
"""
from playwright.sync_api import Page, expect
import allure
import re
from config.env import BASE_URL


class KnowledgeBaseFormPage:
    """Page object for knowledge base create/edit form page"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = BASE_URL
        
        # Locators
        self._title_input = 'input[placeholder*="title"], input[placeholder*="Title"]'
        self._section_name_inputs = 'input[placeholder*="section name"], input[placeholder*="Section name"]'
        self._save_button = 'button:has-text("save"), button:has-text("saving")'
        self._back_button = 'button.p-2:has(svg)'  # Button with ChevronLeft icon
        self._add_section_button = 'button:has-text("Create New")'  # Translated from create_new
        self._remove_section_buttons = 'button:has-text("Remove Section")'  # Translated from Remove_section
        self._delete_button = 'button:has-text("Delete")'
        self._loading_indicator = '[data-testid="loading"], .animate-spin'
        self._editor = '.ProseMirror, [contenteditable="true"]'
        self._sections = '.border.p-4.rounded-md'
        self._title_error = 'text=Title is required'
        self._section_name_error = 'text=Section name is required'
        self._content_error = 'text=Content cannot be empty'
        
        # URL type specific fields
        self._url_input = 'input[placeholder*="url"], input[placeholder*="URL"]'
        self._frequency_select = 'select'
        self._prompt_textarea = 'textarea[placeholder*="prompt"], textarea[placeholder*="AI"]'
        self._last_checked_badge = 'text=Last Checked'
        
        # Delete confirmation
        self._confirm_delete = 'button:has-text("Continue")'
        self._cancel_delete = 'button:has-text("Cancel")'
        
    @allure.step("Navigate to create knowledge base page")
    def navigate_to_create(self, base_url: str = None, type: str = "article"):
        """Navigate to the create knowledge base page"""
        if base_url is None:
            base_url = self.base_url
        url = f"{base_url}/knowledgebase/create?type={type}"
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        
    @allure.step("Navigate to edit knowledge base page: {entry_id}")
    def navigate_to_edit(self, entry_id: str, base_url: str = None):
        """Navigate to the edit knowledge base page"""
        if base_url is None:
            base_url = self.base_url
        url = f"{base_url}/knowledgebase/edit/{entry_id}"
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        
    @allure.step("Wait for page to load")
    def wait_for_page_load(self):
        """Wait for the page to finish loading"""
        # Wait for loading indicator to disappear
        try:
            self.page.wait_for_selector(self._loading_indicator, state="hidden", timeout=10000)
        except:
            pass  # Loading indicator might not appear for create page
            
    @allure.step("Fill title: {title}")
    def fill_title(self, title: str):
        """Fill the title field"""
        self.page.fill(self._title_input, title)
        
    @allure.step("Get title value")
    def get_title_value(self):
        """Get the current title value"""
        return self.page.input_value(self._title_input)
        
    @allure.step("Fill section name at index {index}: {name}")
    def fill_section_name(self, name: str, index: int = 0):
        """Fill a section name field"""
        section_inputs = self.page.locator(self._section_name_inputs).all()
        if len(section_inputs) > index:
            section_inputs[index].fill(name)
            
    @allure.step("Get section name at index {index}")
    def get_section_name(self, index: int = 0):
        """Get a section name value"""
        section_inputs = self.page.locator(self._section_name_inputs).all()
        if len(section_inputs) > index:
            return section_inputs[index].input_value()
        return ""
        
    @allure.step("Fill section content at index {index}")
    def fill_section_content(self, content: str, index: int = 0):
        """Fill section content in the editor"""
        editors = self.page.locator(self._editor).all()
        if len(editors) > index:
            editors[index].click()
            editors[index].fill(content)
            
    @allure.step("Click save button")
    def click_save_button(self):
        """Click the save button"""
        self.page.click(self._save_button)
        self.page.wait_for_timeout(1000)  # Wait for save to complete
        
    @allure.step("Click back button")
    def click_back_button(self):
        """Click the back button"""
        self.page.click(self._back_button)
        
    @allure.step("Click add section button")
    def click_add_section_button(self):
        """Click the add new section button"""
        self.page.click(self._add_section_button)
        
    @allure.step("Click remove section button at index {index}")
    def click_remove_section_button(self, index: int = 0):
        """Click remove section button"""
        remove_buttons = self.page.locator(self._remove_section_buttons).all()
        if len(remove_buttons) > index:
            remove_buttons[index].click()
            
    @allure.step("Get section count")
    def get_section_count(self):
        """Get the number of sections"""
        return self.page.locator(self._sections).count()
        
    @allure.step("Click delete button")
    def click_delete_button(self):
        """Click the delete button (edit page only)"""
        self.page.click(self._delete_button)
        
    @allure.step("Confirm delete")
    def confirm_delete(self):
        """Confirm deletion in the alert dialog"""
        self.page.wait_for_selector(self._confirm_delete, state="visible", timeout=5000)
        self.page.click(self._confirm_delete, force=True)
        self.page.wait_for_timeout(1000)
        
    @allure.step("Cancel delete")
    def cancel_delete(self):
        """Cancel deletion in the alert dialog"""
        self.page.click(self._cancel_delete)
        
    @allure.step("Check if title error is visible")
    def is_title_error_visible(self):
        """Check if title validation error is visible"""
        return self.page.locator(self._title_error).is_visible()
        
    @allure.step("Check if section name error is visible")
    def is_section_name_error_visible(self):
        """Check if section name validation error is visible"""
        return self.page.locator(self._section_name_error).is_visible()
        
    @allure.step("Check if content error is visible")
    def is_content_error_visible(self):
        """Check if content validation error is visible"""
        return self.page.locator(self._content_error).is_visible()
        
    # URL type specific methods
    @allure.step("Fill URL: {url}")
    def fill_url(self, url: str):
        """Fill the URL field (URL type only)"""
        self.page.fill(self._url_input, url)
        
    @allure.step("Get URL value")
    def get_url_value(self):
        """Get the current URL value"""
        return self.page.input_value(self._url_input)
        
    @allure.step("Select frequency: {frequency}")
    def select_frequency(self, frequency: str):
        """Select scrape frequency (URL type only)"""
        self.page.select_option(self._frequency_select, frequency)
        
    @allure.step("Get selected frequency")
    def get_selected_frequency(self):
        """Get the selected frequency value"""
        return self.page.input_value(self._frequency_select)
        
    @allure.step("Fill prompt: {prompt}")
    def fill_prompt(self, prompt: str):
        """Fill the ChatGPT prompt field (URL type only)"""
        self.page.fill(self._prompt_textarea, prompt)
        
    @allure.step("Get prompt value")
    def get_prompt_value(self):
        """Get the current prompt value"""
        return self.page.input_value(self._prompt_textarea)
        
    @allure.step("Check if last checked badge is visible")
    def is_last_checked_visible(self):
        """Check if last checked badge is visible (URL type only)"""
        return self.page.locator(self._last_checked_badge).is_visible()
        
    @allure.step("Get save button")
    def get_save_button(self):
        """Get the save button element"""
        return self.page.locator(self._save_button)
        
    @allure.step("Get delete button")
    def get_delete_button(self):
        """Get the delete button element"""
        return self.page.locator(self._delete_button)
        
    @allure.step("Verify URL is on create page")
    def verify_on_create_page(self):
        """Verify that we're on the create page"""
        expect(self.page).to_have_url(re.compile(r".*/knowledgebase/create.*"))
        
    @allure.step("Verify URL is on edit page")
    def verify_on_edit_page(self):
        """Verify that we're on the edit page"""
        expect(self.page).to_have_url(re.compile(r".*/knowledgebase/edit/[A-Za-z0-9\-_]+$"))
        
    @allure.step("Verify URL is on list page")
    def verify_on_list_page(self):
        """Verify that we navigated back to the list page"""
        expect(self.page).to_have_url(re.compile(r".*/knowledgebase$"))
