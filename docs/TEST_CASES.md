# Test Case Documentation

This document describes the current automated test cases in the project.

## Authentication & Login

### test_login_success
- Verifies successful login with valid email and OTP.
- Asserts navigation to dashboard after OTP submission.

### test_login_invalid_email
- Verifies error handling for invalid email.
- Asserts error message contains "User not found".

### test_login_email_only
- Verifies navigation to OTP page with valid email.
- Asserts OTP page is reached.

### test_otp_rate_limited
- Verifies OTP rate limit error is shown when requesting OTP too frequently.
- Asserts error message contains "Please wait 3 minutes before requesting a new code".

### test_login_page_loads
- Verifies login page loads successfully.
- Asserts email field and submit button are visible.

### test_otp_page_loads
- Verifies OTP page loads and OTP field is visible.
- Asserts OTP field is visible on OTP page.

## Assistant Flows (Voice Type)
- Calendar tab: Add/remove primary and secondary calendars, verify persistence.
- Forwarder tab: Add/remove forwarders, verify backend payloads.
- Keywords tab: Add/remove keywords, verify UI and backend.
- KnowHow tab: Update instructions, add/remove knowledge bases, verify persistence.
- General tab: Update all general fields, verify backend and UI.

## Error Handling
- All tests assert for correct error messages and UI feedback (popups, banners, Toastify notifications).
- Rate limit, invalid credentials, and navigation errors are covered.

---

For details on each test, see the corresponding files in `tests/login/`, `tests/assistants/`, and `tests/flows/`.
