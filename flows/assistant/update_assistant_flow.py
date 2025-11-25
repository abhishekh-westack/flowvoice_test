import re
from playwright.sync_api import expect

class UpdateAssistantFlow:

    def __init__(self, page):
        self.page = page

    def update_basic_fields(self, new_name, new_description):
        """Update name and description fields on assistant detail page"""

        # Step 1: Fill Name
        name_input = self.page.locator("input[name='name']")
        name_input.fill(new_name)

        # Step 2: Fill Description
        desc_input = self.page.locator("input[name='description']")
        desc_input.fill(new_description)

        # Step 3: Click Save
        self.page.get_by_role("button", name="Save").click()

        # Wait for API + UI state to update
        self.page.wait_for_timeout(1500)

        # Step 4: Reload the page to confirm persistence
        self.page.reload()

        # Step 5: Assertions
        expect(self.page.locator("input[name='name']")).to_have_value(new_name)
        expect(self.page.locator("input[name='description']")).to_have_value(new_description)

        return True
