---
name: hatty-search-terms-cleanup
description: Hatty.ai Google Ads search term mining for waste elimination and negative keyword generation
version: 1.0.0
author: Hatty.ai
tier: pro,premium
schedule: "0 7 * * 1"
---

# Hatty.ai - Search Terms Cleanup

When triggered, use the connected Google Ads MCP to mine search terms for waste and opportunities.

## 1. Pull Search Terms Data
Use google_get_search_terms (days: 30) to get all search terms from the last 30 days.
Include: query text, clicks, spend, conversions, CPA, match type that triggered it.

## 2. Categorize Every Term
Apply these categories to every term with spend:

WASTE - Add as negative immediately:
  Spend over $50 AND zero conversions in 30 days

LOW QUALITY - Add as negative:
  Converting at more than 2x the client target CPA

UNDERDEVELOPED - Promote to exact match keyword:
  Converting at under 50% of target CPA AND fewer than 100 clicks (scale these)

IRRELEVANT - Add as campaign-level negative:
  Queries clearly unrelated to the business based on industry context

PERFORMING - Leave as is:
  Converting within target CPA range with sufficient volume

## 3. Generate Negative Keyword Lists
Create ready-to-import negative keyword lists:
- Campaign-level negatives: broad irrelevant terms
- Ad group-level negatives: specific waste terms
- Account-level negatives: universal irrelevance

Format each list as a plain text list ready to copy into Google Ads Editor.

## 4. Calculate Impact
- Total wasted spend in last 30 days
- Projected monthly savings if all waste removed
- Number of terms to promote to exact match
- Estimated conversion gain from scaling underdeveloped terms

## 5. Output Format

---
HATTY.AI SEARCH TERMS CLEANUP REPORT
Client: [client name]
Period: Last 30 days
Generated: [today's date]
---

EXECUTIVE SUMMARY
Total search terms analyzed: X
Wasted spend identified: $X (X% of total spend)
Terms to add as negatives: X
Terms to promote as new keywords: X
Net monthly savings potential: $X

TOP 20 WASTEFUL SEARCH TERMS
[Table: Query | Spend | Clicks | Conversions | Action]

TOP 10 TERMS TO PROMOTE TO KEYWORDS
[Table: Query | Spend | Conversions | CPA | Recommended Bid]

NEGATIVE KEYWORD LISTS (ready to import)

Campaign-Level Negatives:
[one term per line]

Account-Level Negatives:
[one term per line]

MONTHLY SAVINGS PROJECTION
If all waste removed: $X saved per month
If all underdeveloped terms scaled: +X estimated conversions per month

---
Powered by Hatty.ai | mcp.hattysites.com
---
