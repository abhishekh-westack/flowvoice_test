import requests
import json
from playwright.sync_api import Page
from config.env import BASE_API, DOMAIN

class AuthService:
    BASE_API = BASE_API

    def login(self, email: str, code: str, company_id: str):
        """Login using auth/email/finish API"""

        url = f"{BASE_API}/auth/email/finish"
        payload = {
            "Email": email,
            "Code": code,
            "CompanyID": company_id,
        }

        print("Login URL:", url)
        print("Payload:", payload)

        res = requests.post(url, json=payload)

        print("Status:", res.status_code)
        print("Raw Response:", res.text)

        if res.status_code != 200:
            raise Exception(f"Login failed: {res.text}")

        try:
            data = res.json()
        except json.JSONDecodeError:
            raise Exception("API did not return valid JSON")

        # UPDATED EXTRACTION
        print("Parsed Response JSON:", data)
        token = data.get("data", {}).get("token")

        if not token:
            raise Exception("Access token not found in API response")

        print("\n✅ Token extracted successfully")
        return token
    
    def inject_token(self, page: Page, token: str):
        domain = DOMAIN
        # domain = "app.dev.getflowvoice.com"
        """Inject ACCESS_TOKEN cookie"""
        page.context.add_cookies([
            {
                "name": "ACCESS_TOKEN",
                "value": token,
                "domain": domain,
                "path": "/",
                "httpOnly": False,
                "secure": True,
                "sameSite": "Lax",
            }
        ])

