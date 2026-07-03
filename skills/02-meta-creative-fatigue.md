---
name: hatty-meta-creative-fatigue
description: Hatty.ai automated Meta Ads creative fatigue detection using CTR decline, frequency, and CPM signals
version: 1.0.0
author: Hatty.ai
tier: pro,premium
schedule: "0 6 * * 1"
---

# Hatty.ai - Meta Creative Fatigue Detector

When triggered, use the connected Meta Ads MCP to detect fatigued ad creatives.

## 1. Pull Fatigue Signals
Use meta_get_ad_creative_performance (days: 14) to get data for all active ads.
For each active ad running for 7 or more days, analyze:
- CTR over last 7 days vs previous 7 days (pull both periods)
- Frequency (average impressions per unique user)
- CPM trend over last 14 days
- Conversion rate trend

## 2. Fatigue Scoring
Rate each ad as CRITICAL, WARNING, or OK:

CRITICAL - All three signals present:
  - CTR dropped more than 20% week-over-week
  - Frequency above 3.5
  - CPM rose more than 15%

WARNING - One or two signals:
  - CTR dropped 10-20% week-over-week
  - OR frequency between 2.5 and 3.5
  - OR CPM rose 5-15%

OK - All metrics stable or improving

## 3. Impact Estimation
For each CRITICAL ad:
- Calculate wasted spend since fatigue started (spend x CTR decline percentage)
- Project monthly cost if creative is not replaced
- Estimate audience saturation percentage

## 4. Creative Recommendations
For each fatigued ad:
- Identify what made the original creative work (hook, offer, visual type)
- Suggest 3 specific creative directions to test as replacements
- Recommend whether to pause immediately or refresh within 7 days
- Flag the top-performing creative from each campaign to use as benchmark

## 5. Output Format

---
HATTY.AI META CREATIVE FATIGUE REPORT
Client: [client name]
Period: Last 14 days
Generated: [today's date]
---

EXECUTIVE SUMMARY
Total active ads analyzed: X
CRITICAL (pause now): X ads wasting $X/month
WARNING (refresh this week): X ads
Healthy: X ads

CRITICAL ADS - PAUSE IMMEDIATELY
[Table: Ad Name | CTR Change | Frequency | CPM Change | Wasted Spend | Action]

WARNING ADS - REFRESH THIS WEEK
[Table: Ad Name | CTR Change | Frequency | Action]

TOP PERFORMING CREATIVES (benchmarks for replacement)
[List top 3 with what's working]

CREATIVE REPLACEMENT RECOMMENDATIONS
For each Critical ad: 3 specific creative directions to test

TOTAL WASTED SPEND THIS MONTH: $X
PROJECTED SAVINGS IF FIXED: $X/month

---
Powered by Hatty.ai | mcp.hattysites.com
---
