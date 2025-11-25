import allure
from flows.assistant.create_assistant_flow import CreateAssistantFlow
from core.playwright.auth import AuthService
from playwright.sync_api import expect
from config.env import BASE_URL
from config.env import LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID
import re
@allure.story("Assistant Creation")
@allure.title("Create a new assistant successfully")
LOGIN_EMAIL = LOGIN_EMAIL
LOGIN_CODE = LOGIN_CODE
LOGIN_COMPANY_ID = LOGIN_COMPANY_ID

def test_create_assistant(page):
    # 1. Login via API
    auth = AuthService()
    token = auth.login(
        email=LOGIN_EMAIL,
        code=LOGIN_CODE,
        company_id=LOGIN_COMPANY_ID
    )

    # 2. Inject token into Playwright browser
    auth.inject_token(page, token)

    base_url = BASE_URL

    # 3. Now continue with assistant flow
    flow = CreateAssistantFlow(page)

    with allure.step("Create a new Voice assistant"):
        random_name = flow.create_assistant(base_url, type_name="voice")

    # CORRECT URL CHECK
    with allure.step("Verify page redirects to assistant details page"):
        pattern = re.compile(r".*/assistants/[A-Za-z0-9]+$")
        expect(page).to_have_url(pattern)

    with allure.step("Verify name appears on details page"):
        expect(page.locator("input[name='name']")).to_have_value(random_name)