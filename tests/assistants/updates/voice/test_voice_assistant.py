import allure
import re
from playwright.sync_api import expect
from core.playwright.auth import AuthService
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID, ASSISTANT_VOICE_ID, ASSISTANT_NAME, ASSISTANT_TYPE_VOICE_ID, BASE_API
import time

@allure.story("Assistant - Voice - General Tab")
@allure.title("Update ALL General Tab fields for a Voice assistant")
def test_update_voice_assistant_general_tab(page):

    assistant_id = ASSISTANT_TYPE_VOICE_ID
    assistant_name = ASSISTANT_NAME

    # 1. Login via API
    auth = AuthService()
    token = auth.login(
        email=LOGIN_EMAIL,
        code=LOGIN_CODE,
        company_id=LOGIN_COMPANY_ID
    )
    auth.inject_token(page, token)

    # 2. Navigate directly to general tab
    with allure.step("Open assistant general tab"):
        page.goto(f"{BASE_URL}/assistants/{assistant_id}?tab=general")
        # Wait for form to load (data must be fetched first)
        page.wait_for_selector("form#myForm", timeout=15000)
        name_input = page.locator("input[name='name']")
        time.sleep(0.6)

        # Useful debug: print actual value before failing
        print("Actual input value:", name_input.input_value())

        # Assert correctly
        expect(name_input).to_be_visible()
        expect(name_input).to_have_value(assistant_name)

    # ----------- GENERAL TAB FILLING -------------

    with allure.step("Update language EN → DE"):
        page.get_by_label("Language").click()
        page.get_by_role("option", name="German").click()

    with allure.step("Update vibe Formal → Casual"):
        page.get_by_label("Select your assistant's tone of voice").click()
        page.get_by_role("option", name="Formal").click()

    with allure.step("Update voice to Sebastian"):
        # Your UI: voice radio cards → clickable divs
        page.get_by_text("Sebastian").click()

    with allure.step("Update greeting"):
        page.get_by_label("Greetings").fill("Hallo")

    with allure.step("Update goodbye"):
        goodbye = page.locator("input[name='goodbye']")
        expect(goodbye).to_be_visible()
        goodbye.fill("Tschüss")

    with allure.step("Update summary email"):
        page.get_by_label("Mail").fill("test@mail.com")

    # ----------- SAVE -------------

    with allure.step("Save assistant"):
        page.get_by_role("button", name="Save").click()

    # ----------- ASSERTIONS -------------

    with allure.step("Verify success toast"):
        expect(page.get_by_text("Done", exact=False)).to_be_visible()

    with allure.step("Reload page to verify UI saved values"):
        page.reload()
        page.wait_for_selector("form#myForm")

        expect(page.locator("input[name='greeting']")).to_have_value("Hallo")
        expect(page.locator("input[name='goodbye']")).to_have_value("Tschüss")
        expect(page.locator("input[name='SummaryEmail']")).to_have_value("test@mail.com")

        expect(page.get_by_label("Language")).to_contain_text("German")
        expect(page.get_by_text("Sebastian")).to_be_visible()