# Hatty.ai MCP Server

Agentic Google Ads and Meta Ads automation powering mcp.hattysites.com

## What This Is

The Hatty.ai MCP Server is a fully agentic Model Context Protocol (MCP) server that connects Claude AI to your clients Google Ads and Meta Ads accounts. It runs 10 automated skills on a schedule and delivers reports directly to clients via email, Slack, or webhook. No human needed after setup.

## Architecture

mcp.hattysites.com runs:
- MCP Server using FastAPI and MCP Protocol with connectors for Google Ads API v17, Meta Marketing API v19, GA4, and Search Console
- Agentic Orchestrator using APScheduler for cron-based multi-client automation and report delivery via Email, Slack, or Webhook
- 10 Hatty.ai Skill files that Claude executes autonomously
- Claude Agent Runner via Anthropic API executing claude-opus-4-5

## Project Structure

hattysites-mcp/
  server/
    main.py - MCP server entry point
    auth.py - OAuth manager for Google and Meta
    connectors/ - google_ads.py, meta_ads.py, ga4.py, search_console.py
    tools/ - google_tools.py, meta_tools.py, cross_platform_tools.py
    utils/ - report_formatter.py, email_sender.py
  agents/
    orchestrator.py - Cron scheduler that runs all skills automatically
    agent_runner.py - Claude API agentic loop
    client_manager.py - Multi-client account registry
  skills/
    01-google-ads-weekly-audit.md
    02-meta-creative-fatigue.md
    03-cross-platform-roas.md
    04-search-terms-cleanup.md
    05-quality-score-optimizer.md
    06-audience-overlap-detector.md
    07-budget-reallocator.md
    08-weekly-exec-report.md
    09-conversion-tracking-validator.md
    10-landing-page-checker.md
  config/
    clients.yaml - Client account registry
    schedules.yaml - Automation schedules
  scripts/
    setup_client.py - OAuth onboarding per client
  .env.example
  docker-compose.yml
  Dockerfile
  requirements.txt

## Quick Start

1. Clone the repo and install: pip install -r requirements.txt
2. Copy .env.example to .env and fill in API keys
3. Run setup_client.py to onboard each client via OAuth
4. Edit config/clients.yaml with account IDs and delivery settings
5. Start the MCP server: python server/main.py
6. Start the orchestrator: python agents/orchestrator.py

## Docker Deployment for mcp.hattysites.com

Run: docker-compose up -d
This starts both the MCP server and orchestrator with auto-restart.

## Connecting to Claude

1. Open Claude Settings and go to Custom Connectors
2. Click Add and enter: https://mcp.hattysites.com/mcp
3. Authorize via OAuth
Claude will then have live access to all connected client ad accounts.

## The 10 Hatty.ai Skills

01. Google Ads Weekly Audit - Monday 6am - Pro and Premium tiers
02. Meta Creative Fatigue Detector - Monday 6am - Pro and Premium tiers
03. Cross-Platform ROAS Analyzer - Monday 7am - Premium tier only
04. Search Terms Cleanup - Monday 7am - Pro and Premium tiers
05. Quality Score Optimizer - Tuesday 6am - Pro and Premium tiers
06. Audience Overlap Detector - Tuesday 7am - Premium tier only
07. Budget Reallocator - Wednesday 6am - Premium tier only
08. Weekly Executive Report - Monday 8am - Basic, Pro, and Premium tiers
09. Conversion Tracking Validator - Thursday 6am - Pro and Premium tiers
10. Landing Page Checker - Thursday 7am - Premium tier only

## Client Service Tiers

Basic: Weekly Executive Report only (entry-level reporting clients)
Pro: Audit, Fatigue Detection, Search Terms, Quality Score, Tracking, and Executive Report
Premium: All 10 Skills (full-service automation)

## Required API Credentials

- Google Ads Developer Token (Google Ads API access)
- Google OAuth Client ID and Secret (per-client authentication)
- Meta App ID and Secret (Meta Marketing API access)
- Anthropic API Key (Claude agent execution)
- SendGrid API Key, optional (email report delivery)

## Security

- Client credentials stored in credentials/ which is gitignored and never committed
- Google OAuth tokens auto-refresh on expiry
- Meta tokens are long-lived with 60-day rotation reminder built into orchestrator
- All report generation happens server-side
- MCP server requires OAuth to connect

## IMPORTANT - Do Not Touch the API Repo

This is a completely separate service from api.hattysites.com.
Do NOT make changes to the hattysites-licensing repository.
This MCP server deploys independently to mcp.hattysites.com.

---
Built by Hatty.ai - https://Hatty.ai
AI-powered marketing automation for agencies.
