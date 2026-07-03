"""
Hatty.ai Client Manager - client_manager.py
Manages the client registry and provides helpers for
filtering clients by tier, industry, or platform availability.
"""

import yaml
import logging
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger("hatty-client-manager")
CONFIG_DIR = Path(os.getenv("HATTY_CONFIG_DIR", "./config"))
CREDENTIALS_DIR = Path(os.getenv("HATTY_CREDENTIALS_DIR", "./credentials"))


class ClientManager:
    """
    Manages client accounts loaded from config/clients.yaml.
    Provides filtering, validation, and status methods.
    """

    def __init__(self):
        self._clients = None

    @property
    def clients(self) -> list[dict]:
        if self._clients is None:
            self._clients = self._load_clients()
        return self._clients

    def _load_clients(self) -> list[dict]:
        clients_file = CONFIG_DIR / "clients.yaml"
        if not clients_file.exists():
            logger.warning("clients.yaml not found. No clients loaded.")
            return []
        with open(clients_file) as f:
            data = yaml.safe_load(f)
        all_clients = data.get("clients", [])
        active = [c for c in all_clients if c.get("active", True)]
        logger.info(f"Loaded {len(active)} active clients ({len(all_clients)} total)")
        return active

    def reload(self):
        self._clients = None

    def get_client(self, client_id: str) -> Optional[dict]:
        return next((c for c in self.clients if c["id"] == client_id), None)

    def get_clients_by_tier(self, tier: str) -> list[dict]:
        return [c for c in self.clients if c.get("tier") == tier]

    def get_clients_with_google(self) -> list[dict]:
        return [
            c for c in self.clients
            if (CREDENTIALS_DIR / f"{c['id']}_google.json").exists()
        ]

    def get_clients_with_meta(self) -> list[dict]:
        return [
            c for c in self.clients
            if (CREDENTIALS_DIR / f"{c['id']}_meta.json").exists()
        ]

    def get_status(self) -> dict:
        status = []
        for client in self.clients:
            has_google = (CREDENTIALS_DIR / f"{client['id']}_google.json").exists()
            has_meta = (CREDENTIALS_DIR / f"{client['id']}_meta.json").exists()
            status.append({
                "id": client["id"],
                "name": client["name"],
                "tier": client["tier"],
                "google_connected": has_google,
                "meta_connected": has_meta,
                "delivery": list(client.get("delivery", {}).keys()),
            })
        return {
            "total_clients": len(self.clients),
            "clients": status,
        }

    def list_all(self) -> list[str]:
        return [c["id"] for c in self.clients]
