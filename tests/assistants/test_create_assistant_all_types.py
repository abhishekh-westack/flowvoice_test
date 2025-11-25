import allure
import pytest
import re
from flows.assistant.create_assistant_flow import CreateAssistantFlow
from core.playwright.auth import AuthService
from playwright.sync_api import expect
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID

@allure.story("Assistant Creation")
@allure.title("Create assistant of each type")
@pytest.mark.parametrize(
    "type_name",
    ["voice", "whatsapp", "chatbot", "sms"],
    ids=["voice", "whatsapp", "chatbot", "sms"]
)
def test_create_assistant_all_types(page, type_name):

    # Login
    auth = AuthService()
    
    token = auth.login(
        email=LOGIN_EMAIL,
        code=LOGIN_CODE,
        company_id=LOGIN_COMPANY_ID
    )
    auth.inject_token(page, token)

    # Flow
    flow = CreateAssistantFlow(page)
    random_name = flow.create_assistant(BASE_URL, type_name=type_name)

    # Validate navigation
    pattern = re.compile(r".*/assistants/[A-Za-z0-9]+$")
    expect(page).to_have_url(pattern)

    # Validate name
    expect(page.locator("input[name='name']")).to_have_value(random_name)
