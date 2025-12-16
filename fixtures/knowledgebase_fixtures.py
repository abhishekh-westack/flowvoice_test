"""
Test fixtures for Knowledge Base tests
Provides reusable fixtures for knowledge base testing
"""
import pytest
from pages.knowledgebase.knowledgebase_list_page import KnowledgeBaseListPage
from pages.knowledgebase.knowledgebase_form_page import KnowledgeBaseFormPage
from flows.knowledgebase.knowledgebase_list_flow import KnowledgeBaseListFlow
from flows.knowledgebase.knowledgebase_form_flow import KnowledgeBaseFormFlow


@pytest.fixture
def knowledgebase_list_page(page):
    """Fixture for knowledge base list page object"""
    return KnowledgeBaseListPage(page)


@pytest.fixture
def knowledgebase_form_page(page):
    """Fixture for knowledge base form page object"""
    return KnowledgeBaseFormPage(page)


@pytest.fixture
def knowledgebase_list_flow(page):
    """Fixture for knowledge base list flow object"""
    return KnowledgeBaseListFlow(page)


@pytest.fixture
def knowledgebase_form_flow(page):
    """Fixture for knowledge base form flow object"""
    return KnowledgeBaseFormFlow(page)


# Test data fixtures
@pytest.fixture
def sample_article_data():
    """Sample data for creating an article"""
    return {
        "title": "Test Article",
        "sections": [
            {
                "name": "Introduction",
                "content": "This is the introduction section of the test article."
            },
            {
                "name": "Main Content",
                "content": "This is the main content section with detailed information."
            }
        ]
    }


@pytest.fixture
def sample_url_data():
    """Sample data for creating a URL entry"""
    return {
        "title": "Test URL Entry",
        "url": "https://example.com",
        "frequency": "24",
        "prompt": "Extract the main content and key points from this page."
    }
