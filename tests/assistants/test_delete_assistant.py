import allure
import re
from flows.assistant.create_assistant_flow import CreateAssistantFlow
from flows.assistant.delete_assistant_flow import DeleteAssistantFlow
from core.playwright.auth import AuthService
from playwright.sync_api import expect
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID

@allure.story("Assistant Deletion")
@allure.title("Delete an assistant successfully")
def test_delete_assistant(page):

    # Login
    auth = AuthService()
    token = auth.login(
        email=LOGIN_EMAIL,
        code=LOGIN_CODE,
        company_id=LOGIN_COMPANY_ID
    )
    auth.inject_token(page, token)

    # Create assistant first
    create_flow = CreateAssistantFlow(page)
    random_name = create_flow.create_assistant(BASE_URL, type_name="voice")

    # Delete the assistant
    delete_flow = DeleteAssistantFlow(page)
    delete_flow.delete_assistant(random_name)

    # Verify deletion
    with allure.step("Verify assistant is removed from list"):
        deleted_id = random_name.lower()

        # The card MUST NOT exist
        expect(page.locator(f"#{deleted_id}")).not_to_be_visible()
