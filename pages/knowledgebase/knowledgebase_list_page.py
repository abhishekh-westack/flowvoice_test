"""
Page Object Model for Knowledge Base List Page
Handles all interactions with the knowledge base list page
"""
from playwright.sync_api import Page, expect
import allure
from config.env import BASE_URL


class KnowledgeBaseListPage:
    """Page object for knowledge base list page"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = BASE_URL
        
        # Locators
        self._create_button = 'button:has-text("create_new"), button >> text=/create.*new/i'
        self._create_dropdown_trigger = 'button:has-text("create_new"), button >> text=/create.*new/i'
        self._article_option = 'a[href*="/knowledgebase/create?type=article"]'
        self._web_content_option = 'button:has-text("dynamic_web_content"), button:has-text("Dynamic Web Content")'
        self._url_option = 'button:has-text("url"), button:has-text("URL")'
        self._table = 'table'
        self._table_rows = 'table tbody tr'
        self._empty_state = 'text=/not.*found/i, text=/no.*knowledge.*base.*entries/i, h3:has-text("not_found")'
        self._loading_indicator = 'svg.animate-spin, [data-testid="loading"]'
        self._search_input = 'input[placeholder*="Search"]'
        self._title_cells = 'table tbody tr td:first-child .font-medium'
        self._type_cells = 'table tbody tr td:nth-child(2) span'
        
    @allure.step("Navigate to knowledge base list page")
    def navigate(self, base_url: str = None):
        """Navigate to the knowledge base list page"""
        if base_url is None:
            base_url = self.base_url
        url = f"{base_url}/knowledgebase"
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        
    @allure.step("Wait for page to load")
    def wait_for_page_load(self):
        """Wait for the page to finish loading"""
        # Wait for loading indicator to disappear
        self.page.wait_for_selector(self._loading_indicator, state="hidden", timeout=10000)
        
    @allure.step("Click create button")
    def click_create_button(self):
        """Click the create new knowledge base entry button"""
        self.page.click(self._create_dropdown_trigger)
        
    @allure.step("Select article option from dropdown")
    def select_article_option(self):
        """Select article option from create dropdown"""
        self.page.click(self._article_option)
        
    @allure.step("Select web content option from dropdown")
    def select_web_content_option(self):
        """Select dynamic web content option from create dropdown"""
        self.page.click(self._web_content_option)
        
    @allure.step("Select URL option from dropdown")
    def select_url_option(self):
        """Select URL option from create dropdown"""
        self.page.click(self._url_option)
        
    @allure.step("Get table element")
    def get_table(self):
        """Get the knowledge base table element"""
        return self.page.locator(self._table)
        
    @allure.step("Get all table rows")
    def get_all_rows(self):
        """Get all knowledge base entries from the table"""
        return self.page.locator(self._table_rows).all()
        
    @allure.step("Get row count")
    def get_row_count(self):
        """Get the count of knowledge base entries"""
        return self.page.locator(self._table_rows).count()
        
    @allure.step("Check if empty state is visible")
    def is_empty_state_visible(self):
        """Check if the empty state message is displayed"""
        return self.page.locator(self._empty_state).is_visible()
        
    @allure.step("Check if loading indicator is visible")
    def is_loading(self):
        """Check if the loading indicator is visible"""
        return self.page.locator(self._loading_indicator).is_visible()
        
    @allure.step("Search for knowledge base entry: {search_text}")
    def search(self, search_text: str):
        """Search for knowledge base entries"""
        if self.page.locator(self._search_input).is_visible():
            self.page.fill(self._search_input, search_text)
            self.page.wait_for_timeout(500)  # Wait for search to filter
            
    @allure.step("Click on entry with title: {title}")
    def click_entry_by_title(self, title: str):
        """Click on a knowledge base entry by its title (row is clickable)"""
        row = self.page.locator(f'table tbody tr:has(.font-medium:has-text("{title}"))')
        row.click()
            
    @allure.step("Get entry titles")
    def get_entry_titles(self):
        """Get all entry titles from the table"""
        title_elements = self.page.locator(self._title_cells).all()
        return [elem.text_content().strip() for elem in title_elements]
        
    @allure.step("Get entry types")
    def get_entry_types(self):
        """Get all entry types from the table"""
        type_elements = self.page.locator(self._type_cells).all()
        return [elem.text_content().strip() for elem in type_elements]
        
    @allure.step("Click on entry with title: {title}")
    def click_entry_by_title(self, title: str):
        """Click on a knowledge base entry by its title (row is clickable)"""
        row = self.page.locator(f'table tbody tr:has(.font-medium:has-text("{title}"))')
        row.click()
        
    @allure.step("Verify entry exists with title: {title}")
    def verify_entry_exists(self, title: str):
        """Verify that an entry with the given title exists"""
        entry = self.page.locator(f'.font-medium:has-text("{title}")')
        return entry.is_visible()
        
    @allure.step("Get create button")
    def get_create_button(self):
        """Get the create button element"""
        return self.page.locator(self._create_button)
        
    @allure.step("Wait for table to be visible")
    def wait_for_table(self):
        """Wait for the table to be visible"""
        self.page.wait_for_selector(self._table, state="visible", timeout=10000)
