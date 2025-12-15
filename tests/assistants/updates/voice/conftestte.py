import pytest
import requests
from core.playwright.auth import AuthService
from config.env import BASE_API, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID, ASSISTANT_TYPE_VOICE_ID

@pytest.fixture(scope="package", autouse=True)
def check_assistant_exists():
    """
    Fixture to check if the voice assistant exists before running any tests in this package.
    If the assistant is not found (404), all tests in this package will be skipped.
    """
    print("\n[Fixture] Checking if assistant exists...")
    
    auth = AuthService()
    try:
        # Login to get token
        token = auth.login(
            email=LOGIN_EMAIL,
            code=LOGIN_CODE,
            company_id=LOGIN_COMPANY_ID
        )
        
        # Check assistant existence
        url = f"{BASE_API}/assistants/{ASSISTANT_TYPE_VOICE_ID}"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 404:
            pytest.skip(f"Assistant with ID {ASSISTANT_TYPE_VOICE_ID} not found. Skipping tests.")
        elif response.status_code != 200:
            print(f"Warning: Could not verify assistant existence. Status: {response.status_code}, Response: {response.text}")
            # We don't skip here to allow tests to fail naturally if there's a different issue
            
    except Exception as e:
        print(f"Warning: Failed to check assistant existence: {e}")
        # We don't skip here to allow tests to fail naturally if there's a login issue
