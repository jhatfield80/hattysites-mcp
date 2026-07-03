---
name: hatty-google-ads-weekly-audit
description: Hatty.ai automated weekly Google Ads audit covering waste, quality score, and conversion tracking
version: 1.0.0
author: Hatty.ai
tier: pro,premium
schedule: "0 6 * * 1"
---

# Hatty.ai - Google Ads Weekly Audit

When triggered, use the connected Google Ads MCP to run a comprehensive weekly audit.

## 1. Account Health Check
- Pull last 7 days of campaign performance via google_get_campaign_performance (days: 7)
- Pull previous 7 days for comparison
- Calculate account-level spend, conversions, CPA, ROAS
- Flag any metric that changed more than 20% week-over-week
- Identify the single biggest driver of change (positive or negative)

## 2. Wasted Spend Detection
- Pull search terms via google_get_search_terms (days: 30)
- Find all terms with spend over $50 and zero conversions
- Calculate total wasted spend
- Categorize as exact negatives or phrase negatives
- Estimate monthly savings if all waste removed

## 3. Quality Score Audit
- Pull keyword QS data via google_get_quality_scores
- Group into Critical (QS 1-3), Low (QS 4-5), Moderate (QS 6-7), Good (QS 8-10)
- For each underperforming keyword identify weak component: CTR, Ad Relevance, or Landing Page
- Calculate the CPC penalty each client is paying vs. QS 7 baseline
- Estimate monthly savings if all Critical and Low keywords reach QS 7

## 4. Structural Issues
- Pull ad performance via google_get_ad_performance
- Flag ad groups with more than 20 keywords
- Flag campaigns with fewer than 3 active ads per ad group
- Flag any disapproved ads with the disapproval reason

## 5. Conversion Tracking Quick Check
- Pull conversion actions via google_get_conversion_actions
- Flag any conversion action with zero conversions in last 30 days (likely broken)
- Flag any action using count-every when it should be count-one

## 6. Report Format

Use this exact structure for the output:

---
HATTY.AI WEEKLY GOOGLE ADS AUDIT
Client: [client name]
Period: [date range]
Generated: [today's date]
---

EXECUTIVE SUMMARY
[3 bullet points max. Total spend, blended CPA/ROAS, and the single most important finding.]

CRITICAL ISSUES (Fix This Week)
[List sorted by dollar impact. Each item: issue description, dollar amount affected, specific action.]

KEY METRICS
| Metric | This Week | Last Week | Change |
[Include: Spend, Conversions, CPA, ROAS, CTR, Avg CPC]

WASTED SPEND
Total identified: $X
Top 10 wasteful search terms: [table with term, spend, clicks, conversions]
Estimated monthly savings if fixed: $X

QUALITY SCORE BREAKDOWN
Critical (QS 1-3): X keywords paying avg $X extra per click
Low (QS 4-5): X keywords
Monthly savings potential: $X

TOP 5 ACTIONS FOR THIS WEEK
1. [Action] - Expected impact: $X
2. [Action] - Expected impact: $X
3. [Action] - Expected impact: $X
4. [Action] - Expected impact: $X
5. [Action] - Expected impact: $X

---
Powered by Hatty.ai | mcp.hattysites.com
---

Rules:
- Always include dollar amounts not just percentages
- Always specify which campaign each issue belongs to
- Never say "consider optimizing" - say exactly what to do
- Write for a CMO, not a PPC manager
