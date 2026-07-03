"""
Hatty.ai Agent Runner - agent_runner.py
Executes Claude skills against the Hatty.ai MCP server.
This is the brain of the agentic loop.
"""

import os
import logging
from pathlib import Path
import anthropic

logger = logging.getLogger("hatty-agent-runner")


class AgentRunner:
    """
    Executes Hatty.ai skills using Claude as the AI agent.
    Connects to the MCP server to pull live ad account data.
    """

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ["ANTHROPIC_API_KEY"]
        )
        self.model = os.getenv("HATTY_CLAUDE_MODEL", "claude-opus-4-5")
        self.mcp_server_url = os.getenv("HATTY_MCP_URL", "https://mcp.hattysites.com/mcp")
        logger.info(f"AgentRunner ready | Model: {self.model}")

    def _build_system_prompt(self, context: dict) -> str:
        client_name = context["client_name"]
        industry = context.get("industry", "general")
        target_cpa = context.get("target_cpa", "not set")
        target_roas = context.get("target_roas", "not set")
        monthly_budget = context.get("monthly_budget", "not set")
        customer_id = context.get("customer_id", "not connected")
        ad_account_id = context.get("ad_account_id", "not connected")
        client_id = context["client_id"]
        from datetime import datetime
        date_str = datetime.now().strftime("%B %d, %Y")

        return (
            f"You are Hatty.ai, an expert paid media analyst and AI agent.\n"
            f"Client: {client_name} | Industry: {industry}\n"
            f"Target CPA: ${target_cpa} | Target ROAS: {target_roas}x | Budget: ${monthly_budget}/mo\n"
            f"Google Ads ID: {customer_id} | Meta Account: {ad_account_id}\n"
            f"Hatty.ai Client ID: {client_id} | Date: {date_str}\n\n"
            "RULES:\n"
            "- Always include specific dollar amounts\n"
            "- Flag Critical issues first sorted by dollar impact\n"
            "- Write for CMO/CEO audience not PPC technician\n"
            "- Never say optimize - say specifically what to do\n"
            "- Every recommendation must have expected outcome\n"
            "- Format as clean markdown ready for email"
        )

    def _build_user_prompt(self, skill_name: str) -> str:
        triggers = {
            "01-google-ads-weekly-audit": "Run the weekly Google Ads audit for this account.",
            "02-meta-creative-fatigue": "Check Meta Ads for creative fatigue in the last 14 days.",
            "03-cross-platform-roas": "Compare last 30 days ROAS across Google Ads and Meta Ads.",
            "04-search-terms-cleanup": "Clean up Google Ads search terms for the last 30 days.",
            "05-quality-score-optimizer": "Optimize Quality Scores across this Google Ads account.",
            "06-audience-overlap-detector": "Detect audience overlap across this Meta Ads account.",
            "07-budget-reallocator": "Reallocate ad budget based on last 30 days performance.",
            "08-weekly-exec-report": "Write the weekly executive ad performance report for last week.",
            "09-conversion-tracking-validator": "Validate conversion tracking across Google Ads and Meta Ads.",
            "10-landing-page-checker": "Check all landing pages this account ads point to.",
        }
        return triggers.get(skill_name, f"Run the {skill_name} analysis for this account.")

    async def run(self, skill: str, context: dict, skill_name: str) -> str:
        """Execute a skill as a Claude agentic loop. Returns the final markdown report."""
        logger.info(f"Running {skill_name} for {context['client_id']}")

        system_prompt = skill + "\n\n---\n\n" + self._build_system_prompt(context)
        user_prompt = self._build_user_prompt(skill_name)
        messages = [{"role": "user", "content": user_prompt}]

        for iteration in range(10):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8096,
                system=system_prompt,
                messages=messages,
            )

            text_parts = [b.text for b in response.content if hasattr(b, "text")]
            full_text = "\n".join(text_parts)

            if response.stop_reason == "end_turn":
                logger.info(f"Complete: {skill_name} ({len(full_text)} chars)")
                return full_text

            messages.append({"role": "assistant", "content": response.content})

            tool_uses = [b for b in response.content if b.type == "tool_use"]
            if not tool_uses:
                return full_text

        logger.warning(f"Max iterations reached for: {skill_name}")
        return full_text
