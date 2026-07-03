---
name: hatty-quality-score-optimizer
description: Hatty.ai Google Ads Quality Score audit with component-level diagnosis and savings calculation
version: 1.0.0
author: Hatty.ai
tier: pro,premium
schedule: "0 6 * * 2"
---

# Hatty.ai - Quality Score Optimizer

When triggered, use the connected Google Ads MCP to audit and fix Quality Score issues.

## 1. QS Audit
Use google_get_quality_scores to pull all keywords with QS data. Group into tiers:
- CRITICAL (QS 1-3): Paying 3-5x expected CPC. Immediate action required.
- LOW (QS 4-5): Paying 1.5-2x expected CPC. Fix within 2 weeks.
- MODERATE (QS 6-7): Near expected CPC. Monitor and improve.
- GOOD (QS 8-10): Paying below expected CPC. Protect these.

## 2. Component Breakdown
For each Critical and Low keyword, identify the weak component:
- Expected CTR: Below Average means the ad is not expected to get enough clicks
- Ad Relevance: Below Average means the ad copy does not match keyword intent
- Landing Page Experience: Below Average means the page does not satisfy search intent

## 3. Specific Fixes by Component
When Expected CTR is weak:
  Write 3 specific alternative headline variations for this keyword
  Suggest adding the keyword in the headline if it is not there
  Recommend testing a stronger call to action

When Ad Relevance is weak:
  Recommend splitting the keyword into its own dedicated ad group
  Write a specific ad headline that includes the keyword phrase
  Identify which existing ad group it should move to

When Landing Page is weak:
  Flag the specific URL being used
  Identify the mismatch between ad copy and page content
  Recommend a more relevant landing page if one exists in the account

## 4. CPC Impact Calculation
For each keyword group:
- Calculate the estimated CPC premium being paid vs. QS 7 baseline
- QS multipliers: QS 3 = 3x CPC, QS 4 = 2x CPC, QS 5 = 1.5x CPC, QS 6 = 1.2x CPC
- Monthly savings = current spend x (1 - 1/QS multiplier)
- Total account savings if all Critical reach QS 7

## 5. Output Format

---
HATTY.AI QUALITY SCORE OPTIMIZER REPORT
Client: [client name]
Analysis Date: [today's date]
---

EXECUTIVE SUMMARY
Critical keywords (QS 1-3): X keywords | Monthly cost of low QS: $X
Total savings potential if fixed: $X/month

CRITICAL KEYWORDS - FIX IMMEDIATELY
[Table sorted by dollar impact: Keyword | Campaign | QS | Weak Component | Monthly Extra Spend | Fix Required]

For each critical keyword, include the specific fix:
Keyword: [keyword]
Campaign: [campaign name]
QS: X | Weak Component: [component]
Extra CPC paid: $X vs. QS7 baseline
Specific fix: [exact action with example copy if relevant]

LOW QS KEYWORDS - FIX THIS WEEK
[Table: Keyword | QS | Component | Monthly Impact | Action]

TOTAL SAVINGS SUMMARY
If all Critical keywords reach QS 7: Save $X/month
If all Low keywords reach QS 7: Save additional $X/month
Total monthly savings potential: $X

NEXT STEPS
1. [Action 1 with specific implementation detail]
2. [Action 2]
3. [Review timeline]

---
Powered by Hatty.ai | mcp.hattysites.com
---
