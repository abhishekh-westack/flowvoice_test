# Users Management Tests

This directory contains comprehensive test coverage for the Users Management feature.

## Test Structure

### Page Objects (`pages/users/`)
- `users_list_page.py` - Page object for the users list page (`/users`)
- `user_detail_page.py` - Page object for the user detail page (`/users/[id]`)

### Flows (`flows/users/`)
- `users_list_flow.py` - High-level flow actions for users list page
- `user_detail_flow.py` - High-level flow actions for user detail page

### Tests (`tests/users/`)
- `test_users_list.py` - Test cases for users list page
- `test_user_detail.py` - Test cases for user detail page

### Fixtures (`fixtures/`)
- `users_fixtures.py` - Pytest fixtures for users tests

## Test Cases

### Users List Page Tests (`test_users_list.py`)

1. **test_users_list_renders** ✅
   - Verifies users list page loads correctly
   - Checks Create New button is visible
   - Severity: CRITICAL

2. **test_empty_state** ✅
   - Tests empty state message when no users exist
   - Severity: NORMAL

3. **test_loading_state** ✅
   - Verifies loading spinner behavior during data fetch
   - Severity: MINOR

4. **test_add_user_modal_opens** ✅
   - Tests that Create New button opens add user modal
   - Severity: NORMAL

5. **test_user_navigation** ✅
   - Verifies clicking a user navigates to detail page
   - Severity: CRITICAL

6. **test_role_display** ✅
   - Tests role badge display logic (single, multiple, no role)
   - Severity: NORMAL

### User Detail Page Tests (`test_user_detail.py`)

1. **test_user_details_render** ✅
   - Verifies user detail page loads with user information
   - Checks all form fields are populated
   - Severity: CRITICAL

2. **test_edit_user_and_save** ✅
   - Tests editing user details and saving changes
   - Verifies changes persist after save
   - Restores original values after test
   - Severity: CRITICAL

3. **test_form_validation** ✅
   - Tests form validation with invalid inputs
   - Verifies error handling
   - Severity: NORMAL

4. **test_delete_user** ✅
   - Tests delete functionality for non-admin users
   - Verifies delete confirmation dialog
   - Skips for admin users (no delete button)

5. **test_create_and_delete_user_flow** ✅
   - Creates a new user via the UI
   - Verifies user creation successful
   - Navigates to user detail page
   - Deletes the created user
   - Verifies successful deletion
   - Severity: CRITICAL

5. **test_loading_and_error_states** ✅
   - Tests loading spinner behavior
   - Verifies data loads correctly
   - Severity: MINOR

## Running the Tests

### Run all users tests
```bash
pytest tests/users/ -v
```

### Run specific test file
```bash
pytest tests/users/test_users_list.py -v
pytest tests/users/test_user_detail.py -v
```

### Run specific test
```bash
pytest tests/users/test_users_list.py::TestUsersList::test_users_list_renders -v
```

### Run with Allure reporting
```bash
pytest tests/users/ --alluredir=allure-results
allure serve allure-results
```

### Run with specific markers
```bash
pytest -m users -v
```

## Test Data Requirements

The tests use the following environment variables (from `.env`):
- `BASE_URL` - Base URL of the application
- `LOGIN_EMAIL` - Valid user email for authentication
- `LOGIN_CODE` - Valid OTP code for authentication
- `LOGIN_COMPANY_ID` - Company ID for authentication

## Key Features Tested

### Users List Page
- ✅ Page rendering and loading
- ✅ Empty state handling
- ✅ User card display
- ✅ Role badge display (single, multiple, no role)
- ✅ Create New button functionality
- ✅ Navigation to user detail page
- ✅ Loading states

### User Detail Page
- ✅ Page rendering with user data
- ✅ Form field population
- ✅ Edit and save functionality
- ✅ Form validation
- ✅ Delete functionality (non-admin users)
- ✅ Delete button visibility (hidden for admin)
- ✅ Back navigation
- ✅ Loading states
- ✅ Avatar display with initials

## Notes

- Tests use API-based authentication (faster than UI login)
- Tests are designed to be non-destructive (restore original values)
- Delete tests verify the flow but don't actually delete users
- Tests gracefully skip when no users are available
- Admin users are automatically detected and delete tests are skipped for them

## Future Enhancements

- Add tests for role selection in user detail page
- Add tests for user creation flow
- Add tests for bulk user operations
- Add tests for user search/filtering
- Add API mocking for more controlled test scenarios
