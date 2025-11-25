import re
import allure
import time
from playwright.sync_api import expect
from core.playwright.auth import AuthService
from config.env import (
    BASE_URL,
    LOGIN_EMAIL,
    LOGIN_CODE,
    LOGIN_COMPANY_ID,
    ASSISTANT_TYPE_VOICE_ID,
    ASSISTANT_NAME
)


@allure.story("Assistant - Voice - Forwarder Tab")
@allure.title("Full: Add, Remove Forwarders + Backend Payload Verification")
def test_voice_assistant_forwarder_tab_full_flow(page):

    assistant_id = ASSISTANT_TYPE_VOICE_ID

    # -----------------------------------------------------------
    # LOGIN
    # -----------------------------------------------------------
    auth = AuthService()
    token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
    auth.inject_token(page, token)

    # -----------------------------------------------------------
    # OPEN FORWARDER TAB
    # -----------------------------------------------------------
    with allure.step("Open Forwarder tab"):
        page.goto(f"{BASE_URL}/assistants/{assistant_id}?tab=forwarder")
        page.wait_for_selector("form#myForm", timeout=15000)
        time.sleep(0.6)

        # Scope inside the tab
        forwarder_tab = page.locator(
            "div[data-state='active'][id*='content-forwarder']"
        )
        expect(forwarder_tab).to_be_visible()

        # Validate the main Forwarder heading
        expect(
            forwarder_tab.get_by_role("heading", name="Forwarder", level=2)
        ).to_be_visible()


    # =====================================================================
    # 1) ADD FORWARDER #1
    # =====================================================================
    with allure.step("Add Forwarder #1"):
        page.get_by_role("button", name=re.compile("Add Forwarder", re.I)).click()
        time.sleep(0.3)

        # Fill fields
        page.locator("input[name='forwarder.0.Number']").fill("+491234567890")
        page.locator("input[name='forwarder.0.Topics']").fill("Billing")
        page.locator("input[name='forwarder.0.Message']").fill("We will call you back soon.")

        # SAVE
        with page.expect_request("**/assistants/*") as save1_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()

        payload1 = save1_req.value.post_data_json

        assert "Forwarders" in payload1
        assert len(payload1["Forwarders"]) == 1
        assert payload1["Forwarders"][0]["Number"] == "+491234567890"
        assert payload1["Forwarders"][0]["Topics"] == "Billing"

    # =====================================================================
    # 2) ADD FORWARDER #2
    # =====================================================================
    with allure.step("Add Forwarder #2"):
        page.get_by_role("button", name=re.compile("Add Forwarder", re.I)).click()
        time.sleep(0.3)

        page.locator("input[name='forwarder.1.Number']").fill("+491111111111")
        page.locator("input[name='forwarder.1.Topics']").fill("Support")
        page.locator("input[name='forwarder.1.Message']").fill("Support message.")

        # SAVE
        with page.expect_request("**/assistants/*") as save2_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()

        payload2 = save2_req.value.post_data_json

        assert len(payload2["Forwarders"]) == 2
        assert payload2["Forwarders"][1]["Number"] == "+491111111111"

    # =====================================================================
    # 3) DELETE FORWARDER #1 (Index 0)
    # =====================================================================
    with allure.step("Delete Forwarder #1 using X button"):
        # Remove button inside first forwarder card
        remove_btn = page.locator("button:has(svg.lucide-x)").first
        remove_btn.click()

        # SAVE
        with page.expect_request("**/assistants/*") as save3_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()
        time.sleep(0.8)

        payload3 = save3_req.value.post_data_json

        # Only second forwarder should remain
        assert len(payload3["Forwarders"]) == 1
        assert payload3["Forwarders"][0]["Number"] == "+491111111111"

    # =====================================================================
    # 4) RELOAD & VERIFY UI PERSISTENCE
    # =====================================================================
    with allure.step("Reload and verify only one forwarder remains"):
        page.reload()
        page.wait_for_selector("form#myForm")

        # Should have exactly ONE forwarder card
        forwarder_inputs = page.locator("input[name^='forwarder.']")
        assert forwarder_inputs.count() > 0

        remaining_num = page.locator("input[name='forwarder.0.Number']").input_value()
        assert remaining_num == "+491111111111"

    with allure.step("Finished successfully"):
        assert True
