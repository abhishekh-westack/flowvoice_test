import allure
import time
from playwright.sync_api import expect
from core.playwright.auth import AuthService
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID, ASSISTANT_WHATSAPP_ID   # <--- new ID

@allure.story("Assistant - WhatsApp - General Tab")
@allure.title("Update WhatsApp Channel & Vibe and Validate Persistence")
def test_update_whatsapp_general_tab(page):

    assistant_id = ASSISTANT_WHATSAPP_ID

    # ----------------- LOGIN SETUP (same as voice test) -----------------
    auth = AuthService()
    token = auth.login(
        email=LOGIN_EMAIL,
        code=LOGIN_CODE,
        company_id=LOGIN_COMPANY_ID
    )
    auth.inject_token(page, token)

    # ----------------- PAGE OPEN -----------------
    with allure.step("Navigate to General tab for WhatsApp assistant"):
        page.goto(f"{BASE_URL}/assistants/{assistant_id}?tab=general")
        page.wait_for_selector("form#myForm", timeout=15000)
        time.sleep(0.6)

    # ----------------- FORM FILLING -----------------

    with allure.step("Select Vibe 'humorous'"):
        page.get_by_label("Select your assistant's tone of voice").click()
        page.get_by_role("option", name="Humorous").click()

    with allure.step("Select WhatsApp channel from dropdown"):
        page.get_by_label("WhatsApp Channel").click()

        # select first option dynamically if multiple exist
        first_option = page.locator("[role=option]").first
        selected_channel = first_option.inner_text()

        first_option.click()
        print("Selected WhatsApp Channel:", selected_channel)

    # ----------------- SAVE -----------------

    with allure.step("Save assistant"):
        page.get_by_role("button", name="Save").click()

    with allure.step("Verify success toast"):
        expect(page.get_by_text("Done", exact=False)).to_be_visible()

    # ----------------- RELOAD + ASSERT -----------------

    with allure.step("Reload & verify values persisted"):
        page.reload()
        page.wait_for_selector("form#myForm", timeout=15000)

        expect(page.get_by_label("Select your assistant's tone of voice")).to_contain_text("Humorous")
        expect(page.get_by_label("WhatsApp Channel")).to_contain_text(selected_channel)

        print("✔ WhatsApp config saved & persisted successfully")
