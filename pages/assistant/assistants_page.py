from pages.base_page import BasePage
from playwright.sync_api import expect

class AssistantsPage(BasePage):
    """Page object for the Assistants listing page"""

    CREATE_NEW_BUTTON = "button:has-text('Create New')"  # or use data-testid if available
    MODAL_TITLE = "text=Create New Assistant"
    TYPE_OPTION = "div[role='button']"   # You should replace with better selector! (e.g. data-testid)
    NAME_INPUT = "input[name=\"name\"]"
    CREATE_BUTTON = "button:has-text('Create New Assistant')"

    def open(self, base_url: str):
        self.navigate(f"{base_url}/assistants")

    def click_create_new(self):
        self.page.click(self.CREATE_NEW_BUTTON)

    def wait_for_create_modal(self):
        expect(self.page.locator(self.MODAL_TITLE)).to_be_visible()

    def select_type(self, type_name: str):
        self.page.get_by_text(type_name, exact=True).click()

    def enter_name(self, name: str):
        self.page.fill(self.NAME_INPUT, name)

    def submit_create(self):
        self.page.click(self.CREATE_BUTTON)
