import time
import allure
import re
from playwright.sync_api import expect
from core.playwright.auth import AuthService
from config.env import (
    BASE_URL,
    LOGIN_EMAIL,
    LOGIN_CODE,
    LOGIN_COMPANY_ID,
    ASSISTANT_TYPE_VOICE_ID,
    ASSISTANT_NAME,
    ASSISTANT_KNOWHOW_NAME
)


@allure.story("Assistant - Voice - KnowHow Tab")
@allure.title("Full: Update Instructions + Add/Remove Knowledge Bases + Backend & UI Verification")
def test_voice_assistant_knowhow_tab_full_flow(page):

    assistant_id = ASSISTANT_TYPE_VOICE_ID
    assistant_name = ASSISTANT_NAME

    # -----------------------------------------------------------
    # LOGIN
    # -----------------------------------------------------------
    auth = AuthService()
    token = auth.login(
        email=LOGIN_EMAIL,
        code=LOGIN_CODE,
        company_id=LOGIN_COMPANY_ID
    )
    auth.inject_token(page, token)

    # -----------------------------------------------------------
    # OPEN KNOW-HOW TAB
    # -----------------------------------------------------------
    with allure.step("Open Know-How tab"):
        page.goto(f"{BASE_URL}/assistants/{assistant_id}?tab=know")
        page.wait_for_selector("form#myForm", timeout=20000)
        time.sleep(0.6)

        expect(page.locator("input[name='name']")).to_have_value(assistant_name)

        # "Selected Knowledge Bases" heading exists
        expect(page.get_by_text("Select Knowledge Base", exact=False)).to_be_visible()

    # -----------------------------------------------------------
    # UPDATE INSTRUCTIONS (QUILL EDITOR)
    # -----------------------------------------------------------
    with allure.step("Update Knowledge Instructions"):
        editor = page.locator(".ql-editor").first
        expect(editor).to_be_visible()

        editor_handle = editor.element_handle()
        assert editor_handle is not None, "Quill editor handle is None"

        # CLEAR
        page.evaluate(
            "(el) => { el.innerHTML = ''; }",
            editor_handle
        )

        new_text = "Please answer questions about billing and pricing."

        # SET NEW INSTRUCTIONS
        page.evaluate(
            "(args) => { args.el.innerHTML = args.value; }",
            {"el": editor_handle, "value": new_text}
        )
        # SAVE → capture API payload
        with page.expect_request("**/assistants/*") as save_req:
            page.get_by_role("button", name=re.compile("save", re.I)).click()

        sent_payload = save_req.value.post_data_json

        assert sent_payload.get("Knowledge", "").strip() != ""
        assert new_text in sent_payload["Knowledge"]

        # SUCCESS TOAST
        expect(page.get_by_text("Done")).to_be_visible()

    # -----------------------------------------------------------
    # ADD KNOWLEDGE BASE
    # -----------------------------------------------------------
    with allure.step("Add a Knowledge Base (modal)"):
        page.get_by_role("button", name=re.compile("Add Knowledge Base", re.I)).click()
        page.wait_for_selector("[role='dialog']", timeout=10000)

        # SEARCH
        search_input = page.locator("[placeholder*='Search']").first
        search_input.fill(ASSISTANT_KNOWHOW_NAME)
        time.sleep(0.6)

        # Select the KB titled ASSISTANT_KNOWHOW_NAME
        kb_item = page.get_by_text(ASSISTANT_KNOWHOW_NAME, exact=False).first
        expect(kb_item).to_be_visible()
        kb_item.click()

        # SAVE & APPLY CHANGES
        save_btn = page.get_by_role("button", name=re.compile("Apply|Save", re.I)).last

        with page.expect_request("**/assistants/*") as kb_add_req:
            save_btn.click()

        payload_kb_add = kb_add_req.value.post_data_json
        knowledges = payload_kb_add.get("Knowledges", [])

        assert isinstance(knowledges, list)
        assert len(knowledges) >= 1

        added_kb_id = knowledges[0]
        kb_title = ASSISTANT_KNOWHOW_NAME

        # UI: KB card should appear
        expect(page.get_by_text(kb_title, exact=False).first).to_be_visible()

    # -----------------------------------------------------------
    # REMOVE KNOWLEDGE BASE
    # -----------------------------------------------------------
    with allure.step("Remove Knowledge Base"):
        # find card
        kb_card = page.locator(f"div:has-text('{kb_title}')").first
        expect(kb_card).to_be_visible()

        remove_btn = kb_card.locator("button:has(svg)").last
        remove_btn.click()

        expect(page.get_by_text("Are you absolutely sure?", exact=False)).to_be_visible()

        # confirm deletion / Continue button
        confirm = page.get_by_role("button", name=re.compile("Continue|Confirm|Yes", re.I))

        with page.expect_request("**/assistants/*") as kb_remove_req:
            confirm.click()

        payload_remove = kb_remove_req.value.post_data_json

        assert added_kb_id not in payload_remove.get("Knowledges", [])

        # UI removed
        time.sleep(0.6)
        assert page.locator(f"div:has-text('{added_kb_id}')").count() == 0

    # -----------------------------------------------------------
    # RELOAD PAGE → VERIFY PERSISTED DATA
    # -----------------------------------------------------------
    with allure.step("Reload page and verify persistence"):
        page.reload()
        page.wait_for_selector("form#myForm", timeout=15000)

        # Verify Instructions
        editor_after = page.locator(".ql-editor").first
        editor_el = editor_after.element_handle()
        content = editor_el.evaluate("el => el.innerText")
        assert "Please answer questions about billing and pricing." in content

        # ensure KB removed
        assert page.locator(f"div:has-text('{added_kb_id}')").count() == 0

    with allure.step("Finished successfully"):
        assert True
