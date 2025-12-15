# API Endpoints for Test Execution

You can trigger individual test files via FastAPI endpoints. Each endpoint will start the corresponding pytest run and return a status response.

## Available Endpoints

- `POST /test-login` — Runs login tests
- `POST /test-assistant-creation` — Runs assistant creation test
- `POST /test-voice-type` — Runs all voice assistant tab tests
- `POST /test-create-assistant-all-types` — Runs all types assistant creation test
- `POST /test-update-assistant-basic` — Runs assistant update test
- `POST /test-delete-assistant` — Runs assistant deletion test
- `POST /test-whatsapp-general-tab` — Runs WhatsApp general tab test
- `POST /test-chatbot-general-tab` — Runs Chatbot general tab test
- `POST /test-sms-general-tab` — Runs SMS general tab test

## Usage Example
Send a POST request to the desired endpoint:
```
curl -X POST http://localhost:8000/test-login
```

Each endpoint will respond with `{ "test_started": true }` when the test is triggered.

---
For more details, see `scripts/test_runner_api.py`.
