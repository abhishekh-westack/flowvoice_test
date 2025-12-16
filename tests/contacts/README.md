# Contacts Management Tests

This directory contains comprehensive test coverage for the Contacts Management feature.

## Test Structure

### Page Objects (`pages/contacts/`)
- `contacts_list_page.py` - Page object for the contacts list page (`/contacts`)
- `contact_form_page.py` - Page object for contact form pages (`/contacts/new` and `/contacts/edit`)

### Flows (`flows/contacts/`)
- `contacts_list_flow.py` - High-level flow actions for contacts list page
- `contact_form_flow.py` - High-level flow actions for contact form pages

### Tests (`tests/contacts/`)
- `test_contacts_list.py` - Test cases for contacts list page (6 tests)
- `test_contact_form.py` - Test cases for contact form pages (5 tests)

## Test Cases

### Contacts List Page Tests (`test_contacts_list.py`)

1. **test_contacts_list_renders** ✅
   - Verifies contacts list page loads correctly
   - Checks Add Contact button is visible
   - Severity: CRITICAL

2. **test_empty_state** ✅
   - Tests empty state message when no contacts exist
   - Severity: NORMAL

3. **test_loading_state** ✅
   - Verifies loading spinner behavior during data fetch
   - Severity: MINOR

4. **test_add_contact_navigation** ✅
   - Tests that Add Contact button navigates to new contact page
   - Severity: NORMAL

5. **test_contact_navigation** ✅
   - Verifies clicking a contact navigates to edit page
   - Severity: CRITICAL

6. **test_contact_display** ✅
   - Tests contact information display in table (name, email, phone)
   - Severity: NORMAL

### Contact Form Tests (`test_contact_form.py`)

1. **test_new_contact_page_renders** ✅
   - Verifies new contact page loads with form fields
   - Checks all required fields are present
   - Severity: CRITICAL

2. **test_edit_contact_page_renders** ✅
   - Verifies edit contact page loads with contact data
   - Checks form fields are populated
   - Severity: CRITICAL

3. **test_form_validation** ✅
   - Tests form validation with empty and invalid inputs
   - Verifies phone number validation (E.164 format)
   - Severity: NORMAL

4. **test_edit_contact_and_save** ✅
   - Tests editing contact details and saving changes
   - Verifies changes persist after save
   - Restores original values after test
   - Severity: CRITICAL

5. **test_create_and_delete_contact_flow** ✅
   - **Complete end-to-end test**
   - Creates a new contact with unique data
   - Verifies contact appears in list
   - Edits and verifies contact details
   - Deletes the contact
   - Verifies contact is removed from list
   - Severity: CRITICAL

## Running the Tests

### Run all contacts tests
```bash
pytest tests/contacts/ -v
```

### Run specific test file
```bash
pytest tests/contacts/test_contacts_list.py -v
pytest tests/contacts/test_contact_form.py -v
```

### Run specific test
```bash
pytest tests/contacts/test_contacts_list.py::TestContactsList::test_contacts_list_renders -v
pytest tests/contacts/test_contact_form.py::TestContactForm::test_create_and_delete_contact_flow -v
```

### Run with Allure reporting
```bash
pytest tests/contacts/ --alluredir=allure-results
allure serve allure-results
```

## Test Data Requirements

The tests use the following environment variables (from `.env`):
- `BASE_URL` - Base URL of the application
- `LOGIN_EMAIL` - Valid user email for authentication
- `LOGIN_CODE` - Valid OTP code for authentication
- `LOGIN_COMPANY_ID` - Company ID for authentication

## Key Features Tested

### Contacts List Page
- ✅ Page rendering and loading
- ✅ Empty state handling
- ✅ Contact table display
- ✅ Contact information (name, email, phone)
- ✅ Add Contact button functionality
- ✅ Navigation to edit page
- ✅ Loading states

### Contact Form (New/Edit)
- ✅ New contact form rendering
- ✅ Edit contact form rendering
- ✅ Form field population
- ✅ Create contact functionality
- ✅ Edit and save functionality
- ✅ Form validation (required fields, phone format)
- ✅ Delete functionality
- ✅ Back navigation
- ✅ Loading states

## Contact Form Validation

### Required Fields
- ✅ First Name (required)
- ✅ Last Name (required)
- ✅ Phone Number (required, E.164 format: `+[country code][number]`)

### Optional Fields
- Email (optional, but validated if provided)

### Phone Number Format
- Must start with `+`
- Must be in E.164 format (e.g., `+12345678901`)
- Validated on both client and server side

## Notes

- Tests use API-based authentication (faster than UI login)
- Tests are designed to be non-destructive (restore original values when editing)
- Create/delete tests use unique timestamps to avoid conflicts
- Tests gracefully skip when no contacts are available
- Phone numbers are validated to E.164 international format

## Test Statistics

- **Total Tests**: 11
- **Contacts List Tests**: 6
- **Contact Form Tests**: 5
- **Pass Rate**: 100% ✅

## Future Enhancements

- Add tests for bulk contact operations
- Add tests for contact search/filtering
- Add tests for CSV import/export
- Add tests for contact grouping/tagging
- Add API mocking for more controlled test scenarios
- Add tests for call button functionality
