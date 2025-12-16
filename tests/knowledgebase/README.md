# Knowledge Base Test Suite

This directory contains automated tests for the Knowledge Base feature using Playwright and pytest.

## Test Structure

### Page Objects (`pages/knowledgebase/`)
- `knowledgebase_list_page.py` - Page object for the knowledge base list page
- `knowledgebase_form_page.py` - Page object for create/edit forms

### Flow Objects (`flows/knowledgebase/`)
- `knowledgebase_list_flow.py` - User workflows for list operations
- `knowledgebase_form_flow.py` - User workflows for form operations

### Test Files
- `test_knowledgebase_list.py` - Tests for knowledge base list page (6 tests)
- `test_knowledgebase_form.py` - Tests for create/edit forms (6 tests)

### Fixtures (`fixtures/`)
- `knowledgebase_fixtures.py` - Reusable fixtures for knowledge base testing

## Test Coverage

### List Page Tests (`test_knowledgebase_list.py`)
1. ✅ `test_knowledgebase_list_renders` - Verify list page renders correctly
2. ✅ `test_knowledgebase_empty_state` - Verify empty state when no entries exist
3. ✅ `test_knowledgebase_loading_state` - Verify loading state
4. ✅ `test_knowledgebase_create_dropdown` - Verify create dropdown options
5. ✅ `test_navigate_to_create_article` - Verify navigation to create page
6. ✅ `test_knowledgebase_entry_types` - Verify entry types are displayed correctly

### Form Page Tests (`test_knowledgebase_form.py`)
1. ✅ `test_create_article_page_renders` - Verify create page renders correctly
2. ✅ `test_article_validation_errors` - Verify validation for required fields
3. ✅ `test_add_section` - Verify adding new sections
4. ✅ `test_remove_section` - Verify removing sections
5. ✅ `test_back_button_navigation` - Verify back navigation
6. ✅ `test_create_and_delete_article_flow` - Complete create and delete flow

## Knowledge Base Features Tested

### Entry Types
- ✅ Article entries (text-based with sections)
- ✅ Dynamic Web Content entries
- ✅ URL entries (with scraping configuration)

### CRUD Operations
- ✅ Create new entries
- ✅ View/List entries
- ✅ Edit existing entries
- ✅ Delete entries

### Form Functionality
- ✅ Multi-section articles
- ✅ Add/remove sections
- ✅ Rich text editor integration
- ✅ URL configuration (for URL type)
- ✅ Scrape frequency selection
- ✅ ChatGPT prompt configuration

### Validation
- ✅ Title validation
- ✅ Section name validation
- ✅ Content validation
- ✅ URL validation (for URL type)

## Running the Tests

### Run all knowledge base tests:
```bash
pytest tests/knowledgebase/ -v
```

### Run specific test file:
```bash
pytest tests/knowledgebase/test_knowledgebase_list.py -v
pytest tests/knowledgebase/test_knowledgebase_form.py -v
```

### Run specific test:
```bash
pytest tests/knowledgebase/test_knowledgebase_form.py::test_create_and_delete_article_flow -v
```

### Run with Allure report:
```bash
pytest tests/knowledgebase/ --alluredir=allure-results
allure serve allure-results
```

## Test Data

### Sample Article
```python
{
    "title": "Test Article",
    "sections": [
        {
            "name": "Introduction",
            "content": "This is the introduction section."
        },
        {
            "name": "Main Content",
            "content": "This is the main content section."
        }
    ]
}
```

### Sample URL Entry
```python
{
    "title": "Test URL Entry",
    "url": "https://example.com",
    "frequency": "24",  # hours
    "prompt": "Extract the main content from this page."
}
```

## Key Locators

### List Page
- Create button: `button:has-text("New Knowledge Base Entry")`
- Table rows: `table tbody tr`
- Empty state: `text=No Knowledge Base entries found`

### Form Page
- Title input: `input[placeholder*="title"]`
- Section name input: `input[placeholder*="section name"]`
- Save button: `button:has-text("Save")`
- Add section button: `button:has-text("Add New Section")`
- Delete button: `button:has-text("Delete")`

## Notes

- Tests use authenticated_page fixture for logged-in state
- All tests include Allure reporting annotations
- Create-and-delete flow ensures cleanup after testing
- Tests handle both article and URL entry types
- Validation tests verify form error handling
