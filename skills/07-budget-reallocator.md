---
name: hatty-budget-reallocator
description: Hatty.ai cross-platform budget reallocation from underperforming campaigns to high-ROAS campaigns
version: 1.0.0
author: Hatty.ai
tier: premium
schedule: "0 6 * * 3"
---

# Hatty.ai - Budget Reallocator

When triggered, use both Google Ads and Meta Ads MCP connectors to optimize budget allocation.

## 1. Pull Campaign Performance
Use google_get_campaign_performance (days: 30) and meta_get_campaign_performance (days: 30).
For each campaign get: daily budget, actual spend, conversions, CPA, ROAS.
Exclude campaigns with fewer than 25 conversions (insufficient data for reallocation).

## 2. Categorize Campaigns
Calculate the account average ROAS across all campaigns. Then categorize:

SCALE (increase budget):
  ROAS above 150% of account average
  AND impression share lost to budget more than 15%

MAINTAIN (keep current budget):
  ROAS between 80% and 150% of account average

REDUCE (cut budget):
  ROAS between 50% and 80% of account average
  Reallocate this budget to Scale campaigns

PAUSE CANDIDATE (flag for review):
  ROAS below 50% of account average
  AND at least 50 conversions recorded (sufficient data to confirm underperformance)

## 3. Calculate Reallocation
The total budget shift must be budget-neutral. No new money added.
- For Reduce campaigns: propose cutting daily budget by 20-30%
- For Scale campaigns: propose increasing daily budget by 20-40%
- Cap increases at the impression share lost to budget to avoid waste
- Show exactly how much budget moves from where to where

## 4. Forecast Impact
For each proposed change:
- Expected conversion change based on historical CPA at that budget level
- Expected ROAS change for scaled campaigns
- Total account-level conversion improvement
- Total account-level ROAS improvement

IMPORTANT: Always recommend that a human review and approve changes before applying.
Never auto-execute budget changes.

## 5. Output Format

---
HATTY.AI BUDGET REALLOCATOR REPORT
Client: [client name]
Period: Based on last 30 days
Generated: [today's date]
Requires approval before implementation.
---

EXECUTIVE SUMMARY
Account average ROAS: Xx
Budget reallocation opportunity identified: $X/day
Expected ROAS improvement: +X% after reallocation
Expected additional conversions: +X/month

CAMPAIGNS TO SCALE (increase budget)
[Table: Campaign | Platform | Current Budget | Proposed Budget | Current ROAS | Expected ROAS | Reason]

CAMPAIGNS TO REDUCE (free up budget for scalers)
[Table: Campaign | Platform | Current Budget | Proposed Budget | Current ROAS | Reason]

CAMPAIGNS TO MONITOR (maintain)
[Brief list]

PAUSE CANDIDATES (human review required)
[Table: Campaign | Spend in 30d | Conversions | ROAS | Reason for concern]

BUDGET FLOW SUMMARY
Total budget freed from underperformers: $X/day
Total budget added to scalers: $X/day
Net budget change: $0 (reallocation only)

PROJECTED OUTCOME
Conversions this month (current): X
Conversions this month (after reallocation): X (+X%)
ROAS (current): Xx
ROAS (after reallocation): Xx (+X%)

ACTION REQUIRED
These changes require your approval before implementation.
Reply with APPROVED to implement, or ADJUSTED with specific changes.

---
Powered by Hatty.ai | mcp.hattysites.com
---
