"""
Flow Object for Knowledge Base List
Combines page actions into complete user workflows
"""
from pages.knowledgebase.knowledgebase_list_page import KnowledgeBaseListPage
from playwright.sync_api import Page
import allure
from config.env import BASE_URL


class KnowledgeBaseListFlow:
    """Flow object for knowledge base list operations"""
    
    def __init__(self, page: Page):
        self.page = page
        self.list_page = KnowledgeBaseListPage(page)
        
    @allure.step("Navigate to knowledge base list and wait for load")
    def navigate_and_wait(self, base_url: str = None):
        """Navigate to knowledge base list page and wait for it to load"""
        if base_url is None:
            base_url = BASE_URL
        self.list_page.navigate(base_url)
        self.list_page.wait_for_page_load()
        
    @allure.step("Create new article entry")
    def start_create_article(self):
        """Start creating a new article entry"""
        self.list_page.click_create_button()
        self.list_page.select_article_option()
        self.page.wait_for_timeout(1000)
        
    @allure.step("Create new web content entry")
    def start_create_web_content(self):
        """Start creating a new dynamic web content entry"""
        self.list_page.click_create_button()
        self.list_page.select_web_content_option()
        self.page.wait_for_timeout(1000)
        
    @allure.step("Create new URL entry")
    def start_create_url(self):
        """Start creating a new URL entry"""
        self.list_page.click_create_button()
        self.list_page.select_url_option()
        self.page.wait_for_timeout(1000)
        
    @allure.step("Search and verify entry: {title}")
    def search_and_verify(self, title: str):
        """Search for an entry and verify it exists"""
        self.list_page.search(title)
        return self.list_page.verify_entry_exists(title)
        
    @allure.step("Verify entry count is {expected_count}")
    def verify_entry_count(self, expected_count: int):
        """Verify the number of knowledge base entries"""
        actual_count = self.list_page.get_row_count()
        assert actual_count == expected_count, f"Expected {expected_count} entries, found {actual_count}"
        
    @allure.step("Verify entry with title exists: {title}")
    def verify_entry_with_title_exists(self, title: str):
        """Verify that an entry with the given title exists in the list"""
        titles = self.list_page.get_entry_titles()
        assert title in titles, f"Entry with title '{title}' not found in list"
        
    @allure.step("Open entry by title: {title}")
    def open_entry_by_title(self, title: str):
        """Open a knowledge base entry by clicking on its title"""
        self.list_page.click_entry_by_title(title)
        self.page.wait_for_timeout(1000)
