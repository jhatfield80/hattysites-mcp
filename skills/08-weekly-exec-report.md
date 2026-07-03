---
name: hatty-weekly-exec-report
description: Hatty.ai automated weekly executive ad performance report for CEO/CMO delivery across Google and Meta
version: 1.0.0
author: Hatty.ai
tier: basic,pro,premium
schedule: "0 8 * * 1"
---

# Hatty.ai - Weekly Executive Report

When triggered, use both Google Ads and Meta Ads MCP connectors to generate a stakeholder-ready weekly report.

## 1. Pull Performance Data
- Google Ads: google_get_campaign_performance (days: 7) and previous 7 days for comparison
- Meta Ads: meta_get_campaign_performance (days: 7) and previous 7 days for comparison
- Combine into blended view across both platforms
- Calculate: total spend, total conversions, total revenue, blended CPA, blended ROAS

## 2. Find the Stories
Identify for the report:
- The single biggest win this week (what drove the most improvement)
- The single biggest concern this week (what declined the most)
- The most important action item for next week

## 3. Writing Style Rules
These are absolute requirements for this report:
- Maximum 1 page when printed. Be ruthlessly concise.
- Write for a CEO or CMO, not a PPC analyst. No jargon.
- Never say "optimize," "leverage," "synergy," or "learnings." Say what specifically happened.
- Always include dollar amounts. Never percentages alone.
- Always name the specific platform (Google or Meta) for each metric.
- Every action item must have an expected outcome and an owner.
- Tone: professional, direct, confident. Like a trusted advisor giving a verbal briefing.

## 4. Output Format
Use this exact format. Do not add extra sections.

---
HATTY.AI WEEKLY PERFORMANCE REPORT
[Client Name]
Week of [Monday date] to [Sunday date]
---

EXECUTIVE SUMMARY
[Three sentences maximum. Sentence 1: total spend and direction vs last week. Sentence 2: conversions and revenue with trend. Sentence 3: the single most important finding this week.]

KEY METRICS
| Metric | This Week | Last Week | Change |
| Total Spend | $X | $X | +/-X% |
| Total Conversions | X | X | +/-X% |
| Total Revenue | $X | $X | +/-X% |
| Blended CPA | $X | $X | +/-X% |
| Blended ROAS | Xx | Xx | +/-X% |
| Google Spend | $X | $X | +/-X% |
| Google ROAS | Xx | Xx | +/-X% |
| Meta Spend | $X | $X | +/-X% |
| Meta ROAS | Xx | Xx | +/-X% |

TOP 3 WINS THIS WEEK
1. [Specific win. What campaign or platform. What happened. Dollar impact.]
2. [Second win with dollar impact]
3. [Third win with dollar impact]

TOP 3 CONCERNS THIS WEEK
1. [Specific concern. What campaign or platform. What happened. Dollar impact. Why it matters.]
2. [Second concern with dollar impact]
3. [Third concern with dollar impact]

5 ACTION ITEMS FOR NEXT WEEK
1. [Specific action] | Owner: [Marketing team/Agency] | Expected outcome: [specific result]
2. [Specific action] | Owner: [Marketing team/Agency] | Expected outcome: [specific result]
3. [Specific action] | Owner: [Marketing team/Agency] | Expected outcome: [specific result]
4. [Specific action] | Owner: [Marketing team/Agency] | Expected outcome: [specific result]
5. [Specific action] | Owner: [Marketing team/Agency] | Expected outcome: [specific result]

---
Report generated automatically by Hatty.ai
Questions? Contact your Hatty.ai account manager.
mcp.hattysites.com
---
