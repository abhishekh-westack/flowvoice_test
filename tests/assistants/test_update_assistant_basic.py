import allure
from core.playwright.auth import AuthService
from flows.assistant.create_assistant_flow import CreateAssistantFlow
from flows.assistant.update_assistant_flow import UpdateAssistantFlow
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID


@allure.story("Assistant Update")
@allure.title("Update basic assistant fields")
def test_update_assistant_basic(page):

    # Login
    auth = AuthService()
    token = auth.login(
        email=LOGIN_EMAIL,
        code=LOGIN_CODE,
        company_id=LOGIN_COMPANY_ID
    )
    auth.inject_token(page, token)

    # Create new assistant
    create_flow = CreateAssistantFlow(page)
    original_name = create_flow.create_assistant(BASE_URL, type_name="voice")

    # Prepare updated values
    updated_name = original_name + "_updated"
    updated_desc = "This is a new description"

    # Update using flow
    update_flow = UpdateAssistantFlow(page)
    update_flow.update_basic_fields(updated_name, updated_desc)
