# fixtures/test_data.py
"""
Test data for various test scenarios
"""

# User credentials
TEST_USERS = {
    "valid_user": {
        "email": "abhishekh.ojha@westack.ai",
        "otp": "1111",
        "description": "Valid user for successful login"
    },
    "invalid_email": {
        "email": "invalid@example.com",
        "otp": "1111",
        "description": "Invalid email that doesn't exist"
    },
    "invalid_format": {
        "email": "notanemail",
        "otp": "1111",
        "description": "Invalid email format"
    },
}

# OTP codes
OTP_CODES = {
    "valid": "1111",
    "invalid": "0000",
    "expired": "9999",
}

# URLs for testing
TEST_URLS = {
    "login": "/login",
    "otp": "/login/otp",
    "dashboard": "/dashboard",
}
