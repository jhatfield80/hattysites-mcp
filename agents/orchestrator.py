"""
Hatty.ai Agent Orchestrator - orchestrator.py
Runs all 10 skills automatically on schedule for all clients.
No human trigger needed - fully agentic.

Usage: python agents/orchestrator.py
"""

import asyncio
import logging
import os
import sys
import yaml
from pathlib import Path
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.agent_runner import AgentRunner
from agents.client_manager import ClientManager

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [Hatty.ai Orchestrator] %(levelname)s %(message)s"
)
logger = logging.getLogger("hatty-orchestrator")

CONFIG_DIR = Path(os.getenv("HATTY_CONFIG_DIR", "./config"))
SKILLS_DIR = Path(os.getenv("HATTY_SKILLS_DIR", "./skills"))


def load_schedules() -> dict:
    with open(CONFIG_DIR / "schedules.yaml") as f:
        return yaml.safe_load(f)


def load_clients() -> list[dict]:
    with open(CONFIG_DIR / "clients.yaml") as f:
        data = yaml.safe_load(f)
        return [c for c in data.get("clients", []) if c.get("active", True)]


class HattyOrchestrator:
    """
    Agentic orchestrator that runs all Hatty.ai skills automatically.
    Reads schedules from config/schedules.yaml and runs each skill
    across all eligible clients on the defined cron schedule.
    """

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.runner = AgentRunner()
        self.client_manager = ClientManager()
        self.schedules_config = load_schedules()
        self.clients = load_clients()
        logger.info(f"Orchestrator initialized with {len(self.clients)} active clients")

    def setup_schedules(self):
        """Register all automated jobs from schedules.yaml."""
        for schedule in self.schedules_config.get("schedules", []):
            skill_name = schedule["skill"]
            cron = schedule["cron"]
            tiers = schedule.get("tiers", ["all"])
            description = schedule.get("description", skill_name)

            self.scheduler.add_job(
                func=self.run_skill_for_all_clients,
                trigger=CronTrigger.from_crontab(cron),
                args=[skill_name, tiers],
                id=f"hatty_{skill_name}",
                name=f"Hatty.ai: {description}",
                replace_existing=True,
                misfire_grace_time=3600,  # Allow 1 hour late run if server was down
            )
            logger.info(f"Scheduled: {skill_name} | cron: {cron} | tiers: {tiers}")

    async def run_skill_for_all_clients(self, skill_name: str, tiers: list[str]):
        """Run a skill across all eligible clients (concurrently, capped)."""
        eligible = [
            c for c in self.clients
            if c.get("tier") in tiers or "all" in tiers
        ]

        if not eligible:
            logger.info(f"No eligible clients for {skill_name} (tiers: {tiers})")
            return

        logger.info(f"Running {skill_name} for {len(eligible)} clients...")

        settings = self.schedules_config.get("settings", {})
        max_concurrent = settings.get("max_concurrent_clients", 5)

        # Run in batches to avoid API rate limits
        for i in range(0, len(eligible), max_concurrent):
            batch = eligible[i:i + max_concurrent]
            tasks = [self.run_skill_for_client(skill_name, client) for client in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            success = sum(1 for r in results if not isinstance(r, Exception))
            failed = [(batch[j]["id"], str(results[j])) for j in range(len(results)) if isinstance(results[j], Exception)]

            if failed:
                for client_id, error in failed:
                    logger.error(f"  FAILED: {client_id} | {error}")

            logger.info(f"Batch {i//max_concurrent + 1}: {success}/{len(batch)} succeeded")

    async def run_skill_for_client(self, skill_name: str, client: dict):
        """Run a single skill for a single client and deliver the report."""
        client_id = client["id"]
        logger.info(f"  Running {skill_name} for {client_id} ({client['name']})")

        skill_path = SKILLS_DIR / f"{skill_name}.md"
        if not skill_path.exists():
            raise FileNotFoundError(f"Skill file not found: {skill_path}")

        skill_content = skill_path.read_text()

        context = {
            "client_id": client_id,
            "client_name": client["name"],
            "customer_id": client.get("google_customer_id", ""),
            "ad_account_id": client.get("meta_ad_account_id", ""),
            "property_id": client.get("ga4_property_id", ""),
            "industry": client.get("industry", "general"),
            "target_cpa": client.get("target_cpa"),
            "target_roas": client.get("target_roas"),
            "monthly_budget": client.get("monthly_budget"),
        }

        report = await self.runner.run(
            skill=skill_content,
            context=context,
            skill_name=skill_name,
        )

        await self.deliver_report(client=client, skill_name=skill_name, report=report)
        logger.info(f"  Done: {skill_name} for {client_id}")

    async def deliver_report(self, client: dict, skill_name: str, report: str):
        """Send the report via configured delivery channels."""
        delivery = client.get("delivery", {})
        report_title = skill_name.replace("-", " ").replace("_", " ").title()
        subject = f"Hatty.ai | {report_title} | {client['name']} | {datetime.now().strftime('%b %d, %Y')}"

        if delivery.get("email"):
            try:
                from server.utils.email_sender import send_report_email
                await send_report_email(
                    to=delivery["email"],
                    subject=subject,
                    markdown_body=report,
                    client_name=client["name"],
                )
                logger.info(f"  Email sent to {delivery['email']}")
            except Exception as e:
                logger.error(f"  Email delivery failed: {e}")

        if delivery.get("slack_webhook"):
            try:
                import httpx
                async with httpx.AsyncClient() as http:
                    await http.post(delivery["slack_webhook"], json={
                        "text": f"*{subject}*",
                        "blocks": [
                            {"type": "section", "text": {"type": "mrkdwn", "text": f"*{subject}*"}},
                            {"type": "section", "text": {"type": "mrkdwn", "text": report[:2800] + "..." if len(report) > 2800 else report}},
                        ]
                    })
                logger.info(f"  Slack notification sent")
            except Exception as e:
                logger.error(f"  Slack delivery failed: {e}")

        if delivery.get("webhook_url"):
            try:
                import httpx
                async with httpx.AsyncClient() as http:
                    await http.post(delivery["webhook_url"], json={
                        "client_id": client["id"],
                        "client_name": client["name"],
                        "skill": skill_name,
                        "report": report,
                        "generated_at": datetime.utcnow().isoformat() + "Z",
                    })
                logger.info(f"  Webhook delivered")
            except Exception as e:
                logger.error(f"  Webhook delivery failed: {e}")

    async def start(self):
        """Start the orchestrator."""
        logger.info("Hatty.ai Orchestrator starting...")
        logger.info(f"Loaded {len(self.clients)} active clients")
        self.setup_schedules()
        self.scheduler.start()
        logger.info("Orchestrator running. All skills scheduled. Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Orchestrator shutting down...")
            self.scheduler.shutdown(wait=True)
            logger.info("Orchestrator stopped.")


if __name__ == "__main__":
    orchestrator = HattyOrchestrator()
    asyncio.run(orchestrator.start())
