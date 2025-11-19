from pages.assistant.assistants_page import AssistantsPage
import uuid

class CreateAssistantFlow:
    """Flow for creating a new assistant"""

    def __init__(self, page):
        self.page = page
        self.assistants_page = AssistantsPage(page)

    def create_assistant(self, base_url: str, type_name: str = "Voice"):
        """Complete end-to-end assistant creation"""

        # Step 1: Open Assistants page
        self.assistants_page.open(base_url)

        # Step 2: Open modal
        self.assistants_page.click_create_new()
        self.assistants_page.wait_for_create_modal()

        # Step 3: Select type
        self.assistants_page.select_type(type_name)

        # Step 4: Enter random name
        random_name = f"Auto-{uuid.uuid4().hex[:6]}"
        self.assistants_page.enter_name(random_name)

        # Step 5: Click Create
        self.assistants_page.submit_create()

        return random_name
