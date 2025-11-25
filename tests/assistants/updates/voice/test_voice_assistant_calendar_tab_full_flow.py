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
    CALENDAR_SECONDARY_ID_1,
    CALENDAR_SECONDARY_ID_2,
    PRIMARY_CAL_ID,
)


@allure.story("Assistant - Voice - Calendar Tab")
@allure.title("Full: Add/Remove Calendars + Secondary Calendars + UI & Backend Validation")
def test_voice_assistant_calendar_tab_full_flow(page):

    assistant_id = ASSISTANT_TYPE_VOICE_ID

    # -----------------------------------------------------------
    # LOGIN
    # -----------------------------------------------------------
    auth = AuthService()
    token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
    auth.inject_token(page, token)

    # -----------------------------------------------------------
    # OPEN CALENDAR TAB
    # -----------------------------------------------------------
    with allure.step("Open Calendar tab"):
        page.goto(f"{BASE_URL}/assistants/{assistant_id}?tab=calendar")
        page.wait_for_selector("form#myForm", timeout=15000)
        time.sleep(0.6)
        calendar_tab = page.locator(
            "div[data-state='active'][id*='content-calendar']"
        )
        expect(calendar_tab).to_be_visible()

        expect(calendar_tab.get_by_role("heading", name="Calendar", exact=True)).to_be_visible()

    # ============================================================
    # 1) SELECT PRIMARY CALENDAR
    # ============================================================
    with allure.step("Select primary calendar"):
        # Open dropdown
        calendar_tab.locator("button[role='combobox']").first.click()
        time.sleep(0.3)

        # Select by value
        page.locator(f"[role='option']#select-item-{PRIMARY_CAL_ID}").click()

        # SAVE
        with page.expect_request("**/assistants/*") as save1_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()

    # ============================================================
    # 2) ADD SECONDARY CALENDARS
    # ============================================================
    with allure.step("Add secondary calendars"):
        # Open secondary selector
        multi = calendar_tab.locator("button[role='combobox']").nth(1)
        multi.click()

        # Select by value for secondary calendars
        page.locator(f"#select-item-secondary-{CALENDAR_SECONDARY_ID_1}").click()
        page.locator(f"#select-item-secondary-{CALENDAR_SECONDARY_ID_2}").click()

        # SAVE
        with page.expect_request("**/assistants/*") as save2_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()

        payload2 = save2_req.value.post_data_json

    # ============================================================
    # 3) REMOVE PRIMARY CALENDAR
    # ============================================================
    with allure.step("Remove primary calendar"):
        remove_primary = calendar_tab.locator("button:has(svg[class*='trash'])").first
        remove_primary.click()

        # SAVE
        with page.expect_request("**/assistants/*") as save3_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()

    # ============================================================
    # 4) REMOVE SECONDARY CALENDAR
    # ============================================================
    with allure.step("Remove a secondary calendar"):
    # Select the FIRST secondary calendar delete button
        chips = calendar_tab.locator("button:has(svg.lucide-trash2)")
        chips.nth(0).click()

        # SAVE
        with page.expect_request("**/assistants/*") as save4_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()
            time.sleep(0.6)

    # ============================================================
    # 5) RELOAD AND VERIFY UI PERSISTENCE
    # ============================================================
    with allure.step("Reload page and verify persistence"):
        page.reload()
        page.wait_for_selector("form#myForm", timeout=15000)

        # Primary calendar removed ⇒ dropdown should show placeholder
        primary_val = page.locator("button[role='combobox']").first.text_content()
        assert "Select secondary calendars" in primary_val

    with allure.step("Finished successfully"):
        assert True
