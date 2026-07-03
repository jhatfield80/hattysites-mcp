---
name: hatty-cross-platform-roas
description: Hatty.ai cross-platform ROAS comparison across Google Ads and Meta Ads with budget reallocation recommendations
version: 1.0.0
author: Hatty.ai
tier: premium
schedule: "0 7 * * 1"
---

# Hatty.ai - Cross-Platform ROAS Analyzer

When triggered, use both Google Ads and Meta Ads MCP connectors to compare performance.

## 1. Pull Matched 30-Day Data
- Google Ads: use google_get_campaign_performance (days: 30) for spend, conversions, revenue, CPA, ROAS
- Meta Ads: use meta_get_campaign_performance (days: 30) for spend, conversions, revenue, CPA, ROAS
- Pull previous 30 days for trend comparison on both platforms
- Segment by funnel stage where possible (prospecting, retargeting, brand)

## 2. Platform Comparison
Build a side-by-side comparison showing:
- Total spend on each platform
- Conversions and revenue from each platform
- Blended CPA and ROAS on each platform
- Week-over-week trend for each metric
- Share of total budget on each platform

## 3. Attribution Overlap Detection
Flag these common issues:
- Retargeting overlap: both platforms targeting the same users in retargeting
- Brand vs non-brand imbalance: one platform taking disproportionate brand credit
- Last-click over-attribution: identify if one platform is claiming conversions the other platform drove
- Frequency mismatch: users seeing ads on both platforms creating burnout

## 4. Budget Reallocation Logic
Apply these rules:
- If Google ROAS exceeds Meta ROAS by more than 30%: recommend shifting 15-20% of Meta budget to Google
- If Meta ROAS exceeds Google ROAS by more than 30%: recommend shifting 15-20% of Google budget to Meta
- If platforms are within 20% of each other: recommend funnel-stage optimization instead
- Always include expected ROAS impact of the recommended shift
- Never recommend total elimination of either platform

## 5. Output Format

---
HATTY.AI CROSS-PLATFORM ROAS REPORT
Client: [client name]
Period: Last 30 days
Generated: [today's date]
---

EXECUTIVE SUMMARY
[2-3 sentences. Which platform is winning, by how much, and the single biggest opportunity.]

PLATFORM COMPARISON
| Metric | Google Ads | Meta Ads | Winner |
| Spend | $X | $X | - |
| Conversions | X | X | |
| Revenue | $X | $X | |
| CPA | $X | $X | |
| ROAS | Xx | Xx | |
| Trend (vs last 30d) | +/-% | +/-% | |

ATTRIBUTION ISSUES FOUND
[List any overlap or attribution problems with dollar impact]

BUDGET REALLOCATION RECOMMENDATION
Current allocation: Google $X (X%) / Meta $X (X%)
Recommended: Google $X (X%) / Meta $X (X%)
Expected ROAS improvement: +X%
Expected additional conversions per month: +X
Confidence level: High / Medium / Low (based on data volume)

IMPLEMENTATION STEPS
1. [Specific step with exact campaign/budget change]
2. [Next step]
3. [Monitor metric to confirm success]

---
Powered by Hatty.ai | mcp.hattysites.com
---
