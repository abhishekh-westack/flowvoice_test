import re
from playwright.sync_api import expect

class DeleteAssistantFlow:

    def __init__(self, page):
        self.page = page

    def delete_assistant(self, assistant_name):
        """Delete an assistant from its details page"""

        # Step 1: Click Delete button
        delete_btn = self.page.get_by_role("button", name="Delete")
        delete_btn.click()

        # Step 2: Wait for confirmation modal
        expect(self.page.get_by_text("Are you absolutely sure?")).to_be_visible()

        # Step 3: Click Continue
        self.page.get_by_role("button", name="Continue").click()

        # Step 4: Wait for redirect back to assistant list
        self.page.wait_for_url(re.compile(r".*/assistants$"), timeout=10000)

        expect(self.page).to_have_url(re.compile(r".*/assistants$"))
