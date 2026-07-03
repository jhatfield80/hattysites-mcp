---
name: hatty-conversion-tracking-validator
description: Hatty.ai conversion tracking validation for Google Ads and Meta Ads including pixel health, CAPI, and cross-platform consistency
version: 1.0.0
author: Hatty.ai
tier: pro,premium
schedule: "0 6 * * 4"
---

# Hatty.ai - Conversion Tracking Validator

When triggered, use both Google Ads and Meta Ads MCP connectors to validate all tracking.

## 1. Google Ads Conversion Tracking Checks
Use google_get_conversion_actions to pull all conversion actions. Check each one:
- Status: is it Active, Eligible, or Inactive?
- Conversions in last 30 days: if zero, flag as likely broken
- Counting type: is it using Every when it should use One (e.g., purchases should be One)
- Tag firing: is the tag verified as firing?
- Enhanced conversions: is enhanced conversion data enabled?

Also check:
- Are Google Ads conversions imported from GA4? If yes, verify the import is active.
- Is there a primary conversion action set for each campaign?

## 2. Meta Ads Pixel Checks
Use meta_get_pixel_events to check pixel health. For each pixel:
- Event status: is each key event (Purchase, Lead, Add to Cart) active and firing?
- Event match quality score: is it above 6? Below 6 means poor CAPI setup.
- Conversions API (CAPI): is server-side tracking deployed?
- Deduplication: is the pixel event ID matching the CAPI event ID for deduplication?
- Aggregated Event Measurement: is it configured correctly for iOS traffic?

## 3. Cross-Platform Consistency Check
Compare conversion volumes across platforms:
- Google Ads reported conversions vs GA4 conversions for the same event
- Meta pixel reported conversions vs actual backend conversions
- Flag any discrepancy over 20% as needing investigation
- Identify if different attribution windows are causing confusion (e.g., 7-day click vs 28-day click)

## 4. Common Issues to Flag
Check for these known problems:
- Duplicate conversion counting: same event firing twice
- Conversion lag not configured: campaigns optimizing without recent conversion data
- Missing value and currency parameters on purchase events
- View-through conversions inflating Meta numbers
- All-conversions vs conversions discrepancy in Google

## 5. Output Format

---
HATTY.AI CONVERSION TRACKING VALIDATION REPORT
Client: [client name]
Analysis Date: [today's date]
---

EXECUTIVE SUMMARY
Google Ads conversion actions reviewed: X
Meta pixel events reviewed: X
Critical issues found: X (fix today to stop wasted ad spend)
Warning issues found: X

CRITICAL ISSUES - FIX TODAY (These are costing you money right now)
[List with: Issue | Platform | Impact | Step-by-step fix]

WARNING ISSUES - FIX THIS WEEK
[List with: Issue | Platform | Impact | Fix]

GOOGLE ADS TRACKING STATUS
| Conversion Action | Status | 30-Day Conversions | Issue |
[Table]

META ADS TRACKING STATUS
| Event | Pixel Status | CAPI Status | Match Quality | Issue |
[Table]

CROSS-PLATFORM CONSISTENCY
Google Ads reports X conversions
Meta Ads reports X conversions
GA4 reports X conversions
Discrepancy: [explanation if over 20%]

RECOMMENDED FIXES (in priority order)
1. [Fix] - Fixes: [issue] - Estimated data improvement: [impact]
2. [Fix]
3. [Fix]

---
Powered by Hatty.ai | mcp.hattysites.com
---
