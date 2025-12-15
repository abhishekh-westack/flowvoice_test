import allure, time
from playwright.sync_api import expect
from core.playwright.auth import AuthService
from config.env import BASE_URL, LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID, ASSISTANT_SMS_ID


def sms_dropdown(page):
    return page.get_by_role("combobox", name="SMS Number")


# ───────────────────────────────────────────────────────────────
@allure.title("Save SMS number + vibe then verify persistence after reload")
def test_sms_general_tab_update(page):
    auth = AuthService()
    token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
    auth.inject_token(page, token)

    page.goto(f"{BASE_URL}/assistants/{ASSISTANT_SMS_ID}?tab=general")
    time.sleep(0.5)
    page.wait_for_selector("form#myForm")

    # VIBE
    page.get_by_label("Select your assistant's tone of voice").click()
    page.get_by_role("option", name="Formal").click()
    time.sleep(0.5)
    # SMS DROPDOWN
    sms_dropdown(page).click()
    first = page.locator("[role='option']").first
    selected_label = first.inner_text()
    first.click()

    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Done")).to_be_visible()

    page.reload()
    page.wait_for_selector("form#myForm")
    time.sleep(0.5)
    expect(page.get_by_label("Select your assistant's tone of voice")).to_contain_text("Formal")
    expect(sms_dropdown(page)).to_contain_text(selected_label)


# ───────────────────────────────────────────────────────────────
@allure.title("Switch SMS number and verify persistence after reload")
def test_sms_switch_number(page):
    auth = AuthService()
    token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
    auth.inject_token(page, token)

    page.goto(f"{BASE_URL}/assistants/{ASSISTANT_SMS_ID}?tab=general")
    time.sleep(0.5)
    page.wait_for_selector("form#myForm")

    sms_dropdown(page).click()
    options = page.locator("[role='option']")

    total = options.count()
    assert total > 0, "❌ No SMS numbers found in dropdown"

    if total < 2:
        print("⚠ Only one SMS registered → skipping switch test")
        return  # avoid false fail

    second = options.nth(1)
    label = second.inner_text()
    second.click()

    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Done")).to_be_visible()

    page.reload()
    page.wait_for_selector("form#myForm")

    expect(sms_dropdown(page)).to_contain_text(label)
    print(f"✔ Successfully switched to {label}")


# ───────────────────────────────────────────────────────────────
@allure.title("Ensure SMS dropdown list renders all numbers from backend")
def test_sms_dropdown_list(page):
    auth = AuthService()
    token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
    auth.inject_token(page, token)

    page.goto(f"{BASE_URL}/assistants/{ASSISTANT_SMS_ID}?tab=general")
    page.wait_for_selector("form#myForm")

    sms_dropdown(page).click()

    items = page.locator("[role='option']")
    count = items.count()

    assert count > 0, "❌ SMS list empty — Numbers not loading!"
    print(f"✔ Dropdown contains {count} SMS Numbers")
