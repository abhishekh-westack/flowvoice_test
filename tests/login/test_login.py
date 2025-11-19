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
    
    with pytest.raises(AssertionError, match="Login failed"):
        login_flow.complete_login(
            email=user["email"],
            otp_code=user["otp"]
        )


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


@allure.feature("Authentication")
@allure.story("OTP Page")
@allure.title("Test OTP page elements")
@allure.severity(allure.severity_level.MINOR)
def test_otp_page_loads(login_flow, otp_page):
    """Test that OTP page loads and shows OTP field"""
    user = TEST_USERS["valid_user"]
    
    # Navigate to OTP page
    login_flow.login_email_only(email=user["email"])
    
    # Verify on OTP page
    assert otp_page.is_on_otp_page(), "Should be on OTP page"
    
    # Verify OTP field is visible
    otp_field = otp_page.get_otp_field()
    assert otp_field.is_visible(), "OTP field should be visible"
