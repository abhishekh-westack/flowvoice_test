# Page Object Model (POM) Structure

## Overview
This project uses the Page Object Model design pattern for better test maintainability and reusability.

## Directory Structure

```
tests/
├── pages/              # Page Objects (UI elements and actions)
│   ├── base_page.py    # Base class with common methods
│   ├── login_page.py   # Login page object
│   └── otp_page.py     # OTP page object
├── flows/              # Business flows (multi-page scenarios)
│   └── login_flow.py   # Complete login flow
├── fixtures/           # Test data and fixtures
│   ├── test_data.py    # Test data constants
│   └── page_fixtures.py # Page object fixtures
└── tests/              # Actual test files
    └── login/
        ├── test_login.py     # Original test (legacy)
        └── test_login_pom.py # Refactored POM tests
```

## Architecture

### 1. **Base Page** (`pages/base_page.py`)
- Common methods used by all pages
- Navigation, screenshots, waits
- Inherited by all page objects

### 2. **Page Objects** (`pages/`)
- Encapsulate UI elements (locators)
- Provide methods for user actions
- One class per page
- **Example**: `LoginPage`, `OTPPage`

### 3. **Flows** (`flows/`)
- High-level business scenarios
- Combine multiple page objects
- Orchestrate complex user journeys
- **Example**: `LoginFlow.complete_login()`

### 4. **Test Data** (`fixtures/test_data.py`)
- Centralized test data
- User credentials, test URLs, etc.
- Easy to maintain and update

### 5. **Fixtures** (`fixtures/page_fixtures.py`)
- Pytest fixtures for page objects
- Automatically inject dependencies
- Simplify test setup

## Usage Examples

### Simple Test (Using Page Object)
```python
def test_login_page_loads(login_page):
    login_page.navigate()
    assert login_page.get_email_field().is_visible()
```

### Complex Test (Using Flow)
```python
def test_login_success(login_flow):
    user = TEST_USERS["valid_user"]
    result = login_flow.complete_login(
        email=user["email"],
        otp_code=user["otp"]
    )
    assert result
```

### Custom Test (Mix Page Objects)
```python
def test_custom_scenario(login_page, otp_page):
    login_page.navigate()
    login_page.fill_email("test@example.com")
    login_page.click_submit()
    
    assert otp_page.is_on_otp_page()
    otp_page.fill_otp("1111")
```

## Benefits

✅ **Maintainability**: Change locator once, update all tests  
✅ **Reusability**: Share page objects across tests  
✅ **Readability**: Tests read like user stories  
✅ **Scalability**: Easy to add new pages/flows  
✅ **DRY Principle**: No duplicate code  

## Running Tests

### Run all tests
```bash
pytest
```

### Run only POM tests
```bash
pytest tests/login/test_login_pom.py
```

### Run with Allure report
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### Run specific test
```bash
pytest tests/login/test_login_pom.py::test_login_success -v
```

## Adding New Pages

1. **Create page object** in `pages/`
```python
# pages/dashboard_page.py
from pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._welcome_message = "h1.welcome"
    
    def get_welcome_message(self):
        return self.page.locator(self._welcome_message)
```

2. **Add fixture** in `fixtures/page_fixtures.py`
```python
@pytest.fixture
def dashboard_page(page):
    return DashboardPage(page)
```

3. **Use in tests**
```python
def test_dashboard(dashboard_page):
    dashboard_page.navigate()
    assert dashboard_page.get_welcome_message().is_visible()
```

## Adding New Flows

1. **Create flow** in `flows/`
```python
# flows/onboarding_flow.py
class OnboardingFlow:
    def __init__(self, page):
        self.page = page
        self.login_flow = LoginFlow(page)
        self.dashboard_page = DashboardPage(page)
    
    def complete_onboarding(self, email, otp):
        self.login_flow.complete_login(email, otp)
        self.dashboard_page.complete_profile()
```

2. **Add fixture** in `fixtures/page_fixtures.py`
```python
@pytest.fixture
def onboarding_flow(page):
    return OnboardingFlow(page)
```

3. **Use in tests**
```python
def test_onboarding(onboarding_flow):
    result = onboarding_flow.complete_onboarding(
        email="test@example.com",
        otp="1111"
    )
    assert result
```

## Best Practices

1. **Keep locators in page objects** - Never use raw locators in tests
2. **One assertion per test** - Tests should be focused
3. **Use flows for complex scenarios** - Don't duplicate multi-step logic
4. **Name methods clearly** - `fill_email()` not `fill_field_1()`
5. **Use Allure steps** - Makes reports more readable
6. **Centralize test data** - Update in one place

## Migration Guide

To migrate existing tests to POM:

1. Identify UI elements → Move to page objects
2. Identify actions → Create methods in page objects
3. Identify flows → Create flow objects
4. Update tests to use fixtures
5. Remove hardcoded locators and data

### Before (Old Test)
```python
def test_login(page):
    page.goto("https://app.dev.getflowvoice.com/en/login")
    page.locator('input[name="email"]').fill("test@example.com")
    page.get_by_role("button").click()
    # ... more code
```

### After (POM Test)
```python
def test_login(login_flow):
    user = TEST_USERS["valid_user"]
    result = login_flow.complete_login(user["email"], user["otp"])
    assert result
```

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'pages'`  
**Solution**: Make sure you're running pytest from the project root

**Issue**: Fixture not found  
**Solution**: Import fixtures in `conftest.py`

**Issue**: Tests are slow  
**Solution**: Use pytest-xdist for parallel execution

## Next Steps

- [ ] Add more page objects (Dashboard, Settings, etc.)
- [ ] Create more flows (Onboarding, Profile Update, etc.)
- [ ] Add API helper for test data setup
- [ ] Implement retry mechanism for flaky tests
- [ ] Add pytest-xdist for parallel execution
