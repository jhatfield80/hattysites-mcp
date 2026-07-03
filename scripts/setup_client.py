"""
Hatty.ai Client Onboarding Script - setup_client.py
Run this script to connect a new client account to Hatty.ai.

Usage:
  python scripts/setup_client.py --client acme-corp --platform google
  python scripts/setup_client.py --client acme-corp --platform meta
  python scripts/setup_client.py --client acme-corp --platform all
  python scripts/setup_client.py --status
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from server.auth import AuthManager


def setup_google(client_id: str, auth: AuthManager):
    """Run Google OAuth2 flow for a client."""
    client_secrets = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "google_client_secrets.json")
    
    if not Path(client_secrets).exists():
        print(f"Error: {client_secrets} not found.")
        print("Download it from Google Cloud Console > APIs & Services > Credentials")
        sys.exit(1)
    
    print(f"Starting Google OAuth for client: {client_id}")
    print("A browser window will open. Sign in with the Google account that has access to this client Google Ads account.")
    print()
    
    creds = auth.run_google_oauth_flow(client_id, client_secrets)
    print(f"Google OAuth complete for {client_id}")
    print(f"Credentials saved to credentials/{client_id}_google.json")
    return creds


def setup_meta(client_id: str, auth: AuthManager):
    """Save a Meta long-lived access token for a client."""
    print(f"Setting up Meta Ads for client: {client_id}")
    print()
    print("To get a Meta long-lived access token:")
    print("  1. Go to https://developers.facebook.com/tools/explorer/")
    print("  2. Select your Meta App")
    print("  3. Generate a User Token with ads_read, ads_management permissions")
    print("  4. Exchange for a long-lived token (valid 60 days)")
    print()
    
    access_token = input("Paste Meta long-lived access token: ").strip()
    
    if not access_token:
        print("Error: No token provided.")
        sys.exit(1)
    
    # Token expires in 60 days
    expires_at = time.time() + (60 * 24 * 3600)
    auth.save_meta_token(client_id, access_token, expires_at)
    
    print(f"Meta token saved for {client_id}")
    print(f"Token saved to credentials/{client_id}_meta.json")
    print(f"Token expires in ~60 days. Set a reminder to refresh it.")


def show_status(auth: AuthManager):
    """Show all onboarded clients and their connection status."""
    from agents.client_manager import ClientManager
    cm = ClientManager()
    status = cm.get_status()
    
    print(f"Hatty.ai Client Status ({status['total_clients']} active clients)")
    print("=" * 60)
    
    for c in status["clients"]:
        google_status = "connected" if c["google_connected"] else "NOT connected"
        meta_status = "connected" if c["meta_connected"] else "NOT connected"
        print(f"  {c['id']} ({c['name']})")
        print(f"    Tier: {c['tier']}")
        print(f"    Google: {google_status} | Meta: {meta_status}")
        print(f"    Delivery: {', '.join(c['delivery']) or 'none configured'}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Hatty.ai Client Onboarding")
    parser.add_argument("--client", help="Client ID (must match clients.yaml)")
    parser.add_argument("--platform", choices=["google", "meta", "all"], help="Platform to connect")
    parser.add_argument("--status", action="store_true", help="Show all client connection status")
    args = parser.parse_args()
    
    auth = AuthManager()
    
    if args.status:
        show_status(auth)
        return
    
    if not args.client:
        parser.print_help()
        sys.exit(1)
    
    if not args.platform:
        parser.print_help()
        sys.exit(1)
    
    client_id = args.client
    
    if args.platform in ("google", "all"):
        setup_google(client_id, auth)
        print()
    
    if args.platform in ("meta", "all"):
        setup_meta(client_id, auth)
        print()
    
    print(f"Onboarding complete for client: {client_id}")
    print(f"Next: Add {client_id} to config/clients.yaml if not already there.")


if __name__ == "__main__":
    main()
