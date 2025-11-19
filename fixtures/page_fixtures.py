# fixtures/page_fixtures.py
import pytest
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from flows.login_flow import LoginFlow


@pytest.fixture
def login_page(page):
    """Fixture to provide LoginPage instance"""
    return LoginPage(page)


@pytest.fixture
def otp_page(page):
    """Fixture to provide OTPPage instance"""
    return OTPPage(page)


@pytest.fixture
def login_flow(page):
    """Fixture to provide LoginFlow instance"""
    return LoginFlow(page)
