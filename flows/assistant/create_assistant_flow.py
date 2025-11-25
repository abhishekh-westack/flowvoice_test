from pages.assistant.assistants_page import AssistantsPage
import uuid
from playwright.sync_api import expect
import re
class CreateAssistantFlow:
    """Flow for creating a new assistant"""

    def __init__(self, page):
        self.page = page
        self.assistants_page = AssistantsPage(page)

    def create_assistant(self, base_url: str, type_name: str = "voice"):
        """Complete end-to-end assistant creation"""

        # Step 1: Open Assistants page
        self.assistants_page.open(base_url)

        # Step 2: Open modal
        self.assistants_page.click_create_new()
        self.assistants_page.wait_for_create_modal()

        # Step 3: Select type
        self.page.locator(f"div[role='dialog'] #{type_name}").click()
        # self.page.locator(f"#{type_name}").click()
        # Step 4: Enter random name
        random_name = f"Auto-{uuid.uuid4().hex[:6]}"
        self.assistants_page.enter_name(random_name)

         # Step 5: Submit
        self.assistants_page.submit_create()

        # Step 6: Wait for SPA navigation to assistant detail page
        pattern = re.compile(r".*/assistants/[A-Za-z0-9]+$")
        self.page.wait_for_url(pattern, timeout=10000)

        expect(self.page).to_have_url(pattern)

        print(f"Created assistant with name: {random_name}")
        return random_name
