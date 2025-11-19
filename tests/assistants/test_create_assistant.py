import allure
from flows.assistant.create_assistant_flow import CreateAssistantFlow
from core.playwright.auth import AuthService
from playwright.sync_api import expect
from config.env import BASE_URL
@allure.story("Assistant Creation")
@allure.title("Create a new assistant successfully")
def test_create_assistant(page):

    # 1. Login via API
    auth = AuthService()
    token = auth.login(
        email="abhishekh.ojha@westack.ai",
        code="1234",
        company_id="company1_id"
    )

    # 2. Inject token into Playwright browser
    auth.inject_token(page, token)

    base_url = BASE_URL

    # 3. Now continue with assistant flow
    flow = CreateAssistantFlow(page)

    with allure.step("Create a new Voice assistant"):
        random_name = flow.create_assistant(base_url, type_name="Voice")

    with allure.step("Verify page redirects to assistant details page"):
        expect(page).to_have_url(lambda url: "/assistants/" in url)

    with allure.step("Verify name appears on details page"):
        expect(page.get_by_text(random_name)).to_be_visible()