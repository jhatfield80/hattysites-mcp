"""
Hatty.ai MCP Server - auth.py
OAuth manager for Google and Meta API credentials.
"""

import json
import os
import logging
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger("hatty-auth")
CREDENTIALS_DIR = Path(os.getenv("HATTY_CREDENTIALS_DIR", "./credentials"))
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/adwords",
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/webmasters.readonly",
]


class AuthManager:
    def __init__(self):
        CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)

    def get_google_credentials(self, client_id: str) -> Credentials:
        cred_file = CREDENTIALS_DIR / f"{client_id}_google.json"
        if not cred_file.exists():
            raise FileNotFoundError(
                f"No Google credentials for '{client_id}'. "
                f"Run: python scripts/setup_client.py --client {client_id} --platform google"
            )
        creds = Credentials.from_authorized_user_file(str(cred_file), GOOGLE_SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(cred_file, "w") as f:
                f.write(creds.to_json())
        return creds

    def get_meta_token(self, client_id: str) -> str:
        token_file = CREDENTIALS_DIR / f"{client_id}_meta.json"
        if not token_file.exists():
            raise FileNotFoundError(
                f"No Meta token for '{client_id}'. "
                f"Run: python scripts/setup_client.py --client {client_id} --platform meta"
            )
        with open(token_file) as f:
            data = json.load(f)
        expires_at = data.get("expires_at", 0)
        days_left = (expires_at - time.time()) / 86400
        if days_left < 7:
            logger.warning(f"Meta token for '{client_id}' expires in {days_left:.0f} days!")
        return data["access_token"]

    def save_meta_token(self, client_id: str, access_token: str, expires_at: float):
        token_file = CREDENTIALS_DIR / f"{client_id}_meta.json"
        with open(token_file, "w") as f:
            json.dump({"access_token": access_token, "expires_at": expires_at}, f)

    def run_google_oauth_flow(self, client_id: str, client_secrets_file: str) -> Credentials:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, GOOGLE_SCOPES)
        creds = flow.run_local_server(port=0)
        cred_file = CREDENTIALS_DIR / f"{client_id}_google.json"
        with open(cred_file, "w") as f:
            f.write(creds.to_json())
        return creds

    def list_clients(self) -> list[str]:
        ids = set()
        for f in CREDENTIALS_DIR.glob("*_google.json"):
            ids.add(f.stem.replace("_google", ""))
        for f in CREDENTIALS_DIR.glob("*_meta.json"):
            ids.add(f.stem.replace("_meta", ""))
        return sorted(ids)
