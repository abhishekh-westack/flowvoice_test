# pages/__init__.py
"""Page Object Models"""
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.otp_page import OTPPage

__all__ = ["BasePage", "LoginPage", "OTPPage"]
