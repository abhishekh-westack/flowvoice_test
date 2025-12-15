# tests/login/test_login_pom.py
"""
Refactored login tests using Page Object Model
"""
import pytest
import allure
from fixtures.test_data import TEST_USERS, OTP_CODES


@allure.feature("Authentication")
@allure.story("Login Flow")
@allure.title("Test successful login with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_success(login_flow):
    """Test successful login with valid email and OTP"""
    user = TEST_USERS["valid_user"]
    
    result = login_flow.complete_login(
        email=user["email"],
        otp_code=user["otp"]
    )
    
    assert result, "Login should be successful"


@allure.feature("Authentication")
@allure.story("Email Validation")
@allure.title("Test email validation with invalid email")
@allure.severity(allure.severity_level.NORMAL)
def test_login_invalid_email(login_flow):
    """Test that invalid email shows error message"""
    user = TEST_USERS["invalid_email"]
    with pytest.raises(AssertionError) as excinfo:
        login_flow.complete_login(
            email=user["email"],
            otp_code=user["otp"]
        )
    # Assert the error message contains the backend error
    assert "User not found" in str(excinfo.value)


@allure.feature("Authentication")
@allure.story("Email Validation")
@allure.title("Test email-only flow (reach OTP page)")
@allure.severity(allure.severity_level.NORMAL)
def test_login_email_only(login_flow):
    """Test that valid email navigates to OTP page"""
    user = TEST_USERS["valid_user"]
    
    result = login_flow.login_email_only(email=user["email"])
    
    assert result, "Should navigate to OTP page with valid email"


@allure.feature("Authentication")
@allure.story("Login Page")
@allure.title("Test login page navigation")
@allure.severity(allure.severity_level.MINOR)
def test_login_page_loads(login_page):
    """Test that login page loads successfully"""
    login_page.navigate()
    
    # Verify email field is visible
    email_field = login_page.get_email_field()
    assert email_field.is_visible(), "Email field should be visible"
    
    # Verify submit button is visible
    submit_button = login_page.get_submit_button()
    assert submit_button.is_visible(), "Submit button should be visible"



# @allure.feature("Authentication")
# @allure.story("OTP Page")
# @allure.title("Test OTP rate limit error")
# @allure.severity(allure.severity_level.NORMAL)
# def test_otp_rate_limited(login_flow):
#     """Test that OTP rate limit error is shown"""
#     user = TEST_USERS["valid_user"]
#     # First request - should succeed and reach OTP page
#     login_flow.login_email_only(email=user["email"])
    
#     # Second request - navigate back to login and submit again to trigger rate limit
#     login_flow.login_page.navigate()
#     login_flow.login_page.submit_email(user["email"])
    
#     # Check for rate limit error
#     has_error, error_text = login_flow.login_page.check_for_errors()
#     assert has_error
#     assert "Please wait 3 minutes before requesting a new code" in error_text
