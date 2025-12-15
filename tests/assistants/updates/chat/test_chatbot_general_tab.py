import time
import allure
from playwright.sync_api import expect
from fixtures.page_fixtures import *
from core.playwright.auth import AuthService
from config.env import (
    BASE_URL,
    LOGIN_EMAIL,
    LOGIN_CODE,
    LOGIN_COMPANY_ID,
    ASSISTANT_CHAT_ID,
)

# ───────────────────────────────────────────────────────────────
# Locators
# ───────────────────────────────────────────────────────────────

def theme_light(page):
    return page.get_by_role("button", name="Light")

def theme_dark(page):
    return page.get_by_role("button", name="Dark")

def primary_color_input(page):
    return page.locator("#primary-color")

def accent_color_input(page):
    return page.locator("#accent-color").locator("..").locator("input[type='color']")

def header_title_input(page):
    return page.locator("#header-title")

def header_subtitle_input(page):
    return page.locator("#header-subtitle")

def welcome_message_input(page):
    return page.locator("#welcome-message")

def avatar_dropdown(page):
    return page.get_by_role("button", name="Microphone")

# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────

def set_controlled_input(locator, value):
    locator.click()
    locator.fill(value)
    locator.blur()
    expect(locator).to_have_value(value)

def wait_for_chatbot_hydration(page):
    """
    Chatbot UI hydrates AFTER backend responds with settings.
    We detect hydration using guaranteed-visible elements.
    """

    # Preview block appears only after hydration
    page.wait_for_selector("text=Live Preview", timeout=15000)
    page.wait_for_selector("text=Real-time widget preview", timeout=15000)

    # Inputs exist only after hydration
    page.wait_for_selector("#header-title", timeout=15000)
    page.wait_for_selector("#primary-color", timeout=15000)

    print("✓ Chatbot hydration complete")

# ───────────────────────────────────────────────────────────────
# MAIN TEST
# ───────────────────────────────────────────────────────────────

@allure.title("Chatbot: Update all chatbot fields and verify persistence (Hydration Safe)")
def test_chatbot_general_tab_update(page):
    # Authenticate
    auth = AuthService()
    token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
    auth.inject_token(page, token)

    # Open Chatbot General Tab
    page.goto(f"{BASE_URL}/assistants/{ASSISTANT_CHAT_ID}?tab=general")
    page.wait_for_selector("form#myForm")

    # ⭐ CRITICAL: wait for hydration BEFORE filling any inputs
    wait_for_chatbot_hydration(page)

    # ───────────────────────────
    # Update fields
    # ───────────────────────────

    theme_dark(page).click()

    set_controlled_input(primary_color_input(page), "#111111")
    set_controlled_input(accent_color_input(page), "#222222")

    set_controlled_input(header_title_input(page), "My Bot Title")
    set_controlled_input(header_subtitle_input(page), "My Subtitle")

    set_controlled_input(welcome_message_input(page), "Hello! I am your friendly chatbot.")

    # Save
    time.sleep(1)
    save_btn = page.get_by_role("button", name="Save")
    expect(save_btn).to_be_visible()
    save_btn.click()

    expect(page.get_by_text("Done")).to_be_visible()

    # ───────────────────────────
    # Reload & verify persistence
    # ───────────────────────────

    page.reload()
    page.wait_for_selector("form#myForm")
    wait_for_chatbot_hydration(page)

    expect(primary_color_input(page)).to_have_value("#111111")
    expect(accent_color_input(page)).to_have_value("#222222")
    expect(header_title_input(page)).to_have_value("My Bot Title")
    expect(header_subtitle_input(page)).to_have_value("My Subtitle")
    expect(welcome_message_input(page)).to_have_value("Hello! I am your friendly chatbot.")

# ----------------------------------------------------------------
# NOTE:
# The following tests are kept as comments (like in your original file).
# You can enable them and adapt them if you'd like; the main pattern to follow is:
# - Use set_controlled_input(...) after fill
# - Use page.route before clicking Save when asserting payloads
# - Use explicit waits for elements (#primary-color, #header-title, etc.)
# ----------------------------------------------------------------

# @allure.title("Chatbot: Theme toggle (Light/Dark) works correctly")
# def test_chatbot_theme_toggle(page):
#     auth = AuthService()
#     token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
#     auth.inject_token(page, token)
#
#     page.goto(f"{BASE_URL}/assistants/{ASSISTANT_CHAT_ID}?tab=general")
#     page.wait_for_selector("form#myForm")
#
#     theme_dark(page).click()
#     time.sleep(0.2)
#     theme_light(page).click()
#     time.sleep(0.2)
#
#     page.get_by_role("button", name="Save").click()
#     expect(page.get_by_text("Done")).to_be_visible()
#
#     page.reload()
#     page.wait_for_selector("form#myForm")
#     # Asserting class might be implementation-specific; prefer checking persisted value/state if available
#     expect(theme_light(page)).to_be_visible()
#
#
# @allure.title("Chatbot: Color fields accept hex values")
# def test_chatbot_color_hex_validation(page):
#     auth = AuthService()
#     token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
#     auth.inject_token(page, token)
#
#     page.goto(f"{BASE_URL}/assistants/{ASSISTANT_CHAT_ID}?tab=general")
#     page.wait_for_selector("form#myForm")
#
#     set_controlled_input(primary_color_input(page), "#abcdef")
#     set_controlled_input(accent_color_input(page), "#123456")
#
#     page.get_by_role("button", name="Save").click()
#     expect(page.get_by_text("Done")).to_be_visible()
#
#     page.reload()
#     page.wait_for_selector("form#myForm")
#     expect(primary_color_input(page)).to_have_value("#abcdef")
#     expect(accent_color_input(page)).to_have_value("#123456")
#
#
# @allure.title("Chatbot: Verify backend payload only includes chatbot-specific keys")
# def test_chatbot_payload_structure(page):
#     auth = AuthService()
#     token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
#     auth.inject_token(page, token)
#
#     page.goto(f"{BASE_URL}/assistants/{ASSISTANT_CHAT_ID}?tab=general")
#     page.wait_for_selector("form#myForm")
#
#     set_controlled_input(primary_color_input(page), "#333333")
#
#     def validate(route, request):
#         body = request.post_data_json
#
#         # Required chatbot keys
#         assert "ChatTheme" in body
#         assert "ChatPrimaryColor" in body
#         assert "ChatAccentColor" in body
#         assert "ChatHeaderTitle" in body
#         assert "ChatHeaderSubtitle" in body
#         assert "ChatAvatar" in body
#         assert "ChatWelcomeMessage" in body
#
#         # Ensure voice-only keys do NOT exist
#         assert "Voice" not in body
#         assert "Language" not in body
#         assert "Forwarders" not in body
#
#         # Ensure SMS/WhatsApp fields do NOT exist
#         assert "SmsNumber" not in body
#         assert "WhatsAppChannelID" not in body
#
#         route.continue_()
#
#     page.route("**/assistants/*", validate)
#
#     page.get_by_role("button", name="Save").click()
#     expect(page.get_by_text("Done")).to_be_visible()
#
#
# @allure.title("Chatbot: Avatar dropdown opens and options appear")
# def test_chatbot_avatar_dropdown(page):
#     auth = AuthService()
#     token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
#     auth.inject_token(page, token)
#
#     page.goto(f"{BASE_URL}/assistants/{ASSISTANT_CHAT_ID}?tab=general")
#     page.wait_for_selector("form#myForm")
#
#     avatar_dropdown(page).click()
#     expect(page.get_by_role("dialog")).to_be_visible()
#
#
# @allure.title("Chatbot: Reset All Settings resets fields to default")
# def test_chatbot_reset_button(page):
#     auth = AuthService()
#     token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
#     auth.inject_token(page, token)
#
#     page.goto(f"{BASE_URL}/assistants/{ASSISTANT_CHAT_ID}?tab=general")
#     page.wait_for_selector("form#myForm")
#
#     header_title_input(page).fill("Temp Title")
#     page.get_by_role("button", name="Reset All Settings").click()
#     time.sleep(0.5)
#
#     expect(header_title_input(page)).to_have_value("")
#
#
# @allure.title("Chatbot: Integration tab renders embed code")
# def test_chatbot_integration_tab(page):
#     auth = AuthService()
#     token = auth.login(LOGIN_EMAIL, LOGIN_CODE, LOGIN_COMPANY_ID)
#     auth.inject_token(page, token)
#
#     page.goto(f"{BASE_URL}/assistants/{ASSISTANT_CHAT_ID}?tab=integrate")
#     page.wait_for_selector("form#myForm")
#
#     expect(page.get_by_text("Integration Guide")).to_be_visible()
#     expect(page.locator("code")).to_be_visible()
