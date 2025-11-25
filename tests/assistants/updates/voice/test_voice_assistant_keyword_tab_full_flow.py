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
)


@allure.story("Assistant - Voice - Keywords Tab")
@allure.title("Full: Add/Remove Keywords + UI & Backend Validation")
def test_voice_assistant_keywords_tab_full_flow(page):

    assistant_id = ASSISTANT_TYPE_VOICE_ID

    # -----------------------------------------------------------
    # LOGIN
    # -----------------------------------------------------------
    auth = AuthService()
    token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
    auth.inject_token(page, token)

    # -----------------------------------------------------------
    # OPEN KEYWORDS TAB
    # -----------------------------------------------------------
    with allure.step("Open Keywords tab"):
        page.goto(f"{BASE_URL}/assistants/{assistant_id}?tab=keywords")
        page.wait_for_selector("form#myForm", timeout=15000)
        time.sleep(0.6)
        keywords_tab = page.locator("div[data-state='active'][id*='content-keywords']")
        expect(keywords_tab).to_be_visible()
        expect(keywords_tab.get_by_role("heading", name=re.compile("keywords", re.I))).to_be_visible()

    # ============================================================
    # 1) ADD KEYWORD #1
    # ============================================================
    with allure.step("Add first keyword"):
        add_btn = keywords_tab.get_by_role("button", name=re.compile("add keyword", re.I))
        add_btn.click()
        time.sleep(0.3)

        kw1 = keywords_tab.locator("input[name='keywords.0.Keyword']")
        ds1 = keywords_tab.locator("textarea[name='keywords.0.Description']")

        kw1.fill("billing support")
        ds1.fill("Handles all billing-related questions.")

        # SAVE
        with page.expect_request("**/assistants/*") as save_kw1_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()

        payload1 = save_kw1_req.value.post_data_json
        print("Payload after Keyword #1:", payload1)

        assert {"Keyword": "billing support", "Description": "Handles all billing-related questions."} in payload1["Keywords"]

    # ============================================================
    # 2) ADD KEYWORD #2
    # ============================================================
    with allure.step("Add second keyword"):
        add_btn.click()
        time.sleep(0.3)

        kw2 = keywords_tab.locator("input[name='keywords.1.Keyword']")
        ds2 = keywords_tab.locator("textarea[name='keywords.1.Description']")

        kw2.fill("technical help")
        ds2.fill("Assists with technical troubleshooting.")

        with page.expect_request("**/assistants/*") as save_kw2_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()

        payload2 = save_kw2_req.value.post_data_json
        print("Payload after Keyword #2:", payload2)

        assert {"Keyword": "technical help", "Description": "Assists with technical troubleshooting."} in payload2["Keywords"]

    # ============================================================
    # 3) REMOVE KEYWORD #1
    # ============================================================
    with allure.step("Remove first keyword"):
        # first keyword row has an 'X' icon remove button positioned absolutely
        remove_btn = keywords_tab.locator("button:has(svg.lucide-x)").first
        remove_btn.click()
        time.sleep(0.2)

        with page.expect_request("**/assistants/*") as save_remove_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()
        time.sleep(0.6)
        payload3 = save_remove_req.value.post_data_json
        print("Payload after removing Keyword #1:", payload3)

        keywords_after_remove = payload3.get("Keywords", [])
        assert not any(k["Keyword"] == "billing support" for k in keywords_after_remove)

    # ============================================================
    # 4) RELOAD + UI PERSISTENCE CHECK
    # ============================================================
    with allure.step("Reload page and verify persistence"):
        page.reload()
        page.wait_for_selector("form#myForm", timeout=15000)

        keywords_tab = page.locator("div[data-state='active'][id*='content-keywords']")
        expect(keywords_tab).to_be_visible()

        # Find keyword #2 input field
        kw2_input = keywords_tab.locator("input[name='keywords.0.Keyword']")

        # Assert its value persisted
        expect(kw2_input).to_have_value("technical help")
    with allure.step("Finished successfully"):
        assert True
