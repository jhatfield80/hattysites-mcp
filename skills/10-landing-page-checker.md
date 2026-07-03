---
name: hatty-landing-page-checker
description: Hatty.ai landing page analysis for ads across Google and Meta including load time, UX, and conversion rate issues with dollar impact
version: 1.0.0
author: Hatty.ai
tier: premium
schedule: "0 7 * * 4"
---

# Hatty.ai - Landing Page Checker

When triggered, use both Google Ads and Meta Ads MCP connectors to audit landing pages.

## 1. Map Ads to Landing Pages
- Pull all active ads from Google Ads via google_get_ad_performance
- Pull all active Meta ad sets via meta_get_audience_data
- Extract all destination URLs from both platforms
- Strip UTM parameters and group unique pages
- Calculate total monthly ad spend driving to each unique landing page URL
- Focus analysis on pages receiving more than $500 per month in ad spend

## 2. Analyze Each Landing Page
For pages with significant spend, evaluate:

Technical performance:
- Page load time target: under 2 seconds is good, 2-4 is warning, over 4 is critical
- Mobile friendliness: does it load and display correctly on mobile?
- HTTPS: is the page secure?

Message match:
- Does the main headline on the page match the intent of the ad that sent traffic there?
- Is there a clear and prominent call to action above the fold?
- Does the page address the specific offer or claim made in the ad?

Conversion friction:
- If there is a form: how many fields does it have? Over 7 is critical, 5-7 is warning
- Is there a clear value proposition in the first 3 seconds?
- Are there trust signals (reviews, certifications, guarantees) visible?

## 3. Issue Severity Rating
CRITICAL - Fix before next week:
- Page load over 4 seconds
- Broken page or 404 error
- No CTA visible above the fold
- Form with over 7 fields
- Complete mismatch between ad copy and page headline

WARNING - Fix within 2 weeks:
- Page load 2-4 seconds
- Headline mismatch (similar but not aligned)
- Weak or generic value proposition
- Mobile display issues (minor)

MINOR - Fix when possible:
- Small UX improvements
- Trust signal additions

## 4. Dollar Impact Calculation
For each Critical issue:
- Estimated conversion rate impact: load over 4s loses 25-40% of conversions, broken page loses 100%, no CTA above fold loses 15-25%, form over 7 fields loses 20-35%
- Monthly revenue impact = monthly spend to this page x estimated conversion rate loss x average conversion value

## 5. Output Format

---
HATTY.AI LANDING PAGE CHECKER REPORT
Client: [client name]
Analysis Date: [today's date]
Pages analyzed: X (those receiving over $500/month in ad spend)
---

EXECUTIVE SUMMARY
Landing pages analyzed: X
Critical issues found: X (losing estimated $X/month in conversions)
Warning issues: X

CRITICAL LANDING PAGES - FIX BEFORE NEXT WEEK
[For each, ranked by dollar impact:]

Page: [URL]
Ad spend sending to this page: $X/month
Issues found:
  - [Issue 1]: [specific problem]
  - [Issue 2]: [specific problem]
Estimated conversion rate loss: X%
Estimated monthly revenue impact: $X
Specific fixes:
  1. [Exact fix with expected improvement]
  2. [Next fix]

WARNING LANDING PAGES - FIX WITHIN 2 WEEKS
[Same format, briefer]

TOP PERFORMING PAGES (benchmarks)
[List the 2-3 pages that are doing well and what makes them work]

TOTAL ESTIMATED MONTHLY REVENUE LOST: $X
PROJECTED IMPROVEMENT IF ALL CRITICAL FIXED: $X/month

---
Powered by Hatty.ai | mcp.hattysites.com
---
