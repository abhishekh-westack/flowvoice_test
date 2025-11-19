import allure
from core.playwright.auth import AuthService
from playwright.sync_api import expect

@allure.story("Authentication")
@allure.title("Verify API Login & Cookie Injection")
def test_auth_service_login_and_cookie(page):
    auth = AuthService()

    with allure.step("Call login API and fetch token"):
        token = auth.login(
            email="abhishekh.ojha@westack.ai",
            code="1234",
            company_id="company1_id"
        )
        assert token is not None
        assert len(token) > 10  # basic sanity check

    with allure.step("Inject cookie into Playwright context"):
        auth.inject_token(page, token)

    with allure.step("Validate ACCESS_TOKEN cookie exists"):
        cookies = page.context.cookies()
        access_cookie = next((c for c in cookies if c["name"] == "ACCESS_TOKEN"), None)

        assert access_cookie is not None, "ACCESS_TOKEN cookie was not set!"
        assert access_cookie["value"] == token
        assert access_cookie["domain"] == "app.dev.getflowvoice.com"
