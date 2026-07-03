---
name: hatty-audience-overlap-detector
description: Hatty.ai Meta Ads audience overlap detection to prevent internal auction competition and CPM inflation
version: 1.0.0
author: Hatty.ai
tier: premium
schedule: "0 7 * * 2"
---

# Hatty.ai - Audience Overlap Detector

When triggered, use the connected Meta Ads MCP to detect audience overlap causing internal competition.

## 1. Pull Targeting Data
Use meta_get_audience_data to get all active ad sets spending more than $50 per day.
For each ad set collect:
- Age range and gender targeting
- Geographic targeting (countries, regions, cities)
- Interest targeting layers
- Custom audience IDs
- Lookalike audience sources and percentage ranges
- Exclusion audiences currently applied

## 2. Overlap Detection
Compare all active ad sets against each other. Flag overlap when any of these conditions are met:
- Same custom audience is included in both ad sets without exclusions
- Same lookalike source audience at any percentage range
- Overlapping interest targeting plus same geography plus same age range
- No exclusion audiences separating them

Rate overlap severity:
- SEVERE: Same custom audiences with no exclusions (direct cannibalization)
- HIGH: Same lookalike source with overlapping geo and age
- MODERATE: Significant interest overlap with same audience parameters
- LOW: Minor demographic overlap only

## 3. CPM Impact Estimation
For each overlap pair:
- Severe overlap CPM inflation estimate: 20-30%
- High overlap CPM inflation estimate: 15-20%
- Moderate overlap CPM inflation estimate: 10-15%
- Wasted spend = (combined daily spend of overlapping pair) x (overlap severity percentage) x 30

## 4. Consolidation Plan
For each overlap cluster:
- Recommend which ad set to keep based on highest ROAS
- Identify which ad sets to pause or merge
- Write specific exclusion audience instructions to prevent future overlap
- Recommend structure for clean prospecting versus retargeting separation

## 5. Output Format

---
HATTY.AI AUDIENCE OVERLAP DETECTOR REPORT
Client: [client name]
Analysis Date: [today's date]
Account: [Meta ad account ID]
---

EXECUTIVE SUMMARY
Active ad sets analyzed: X
Overlap clusters found: X
Estimated CPM inflation from overlap: X%
Monthly wasted spend from overlap: $X

SEVERE OVERLAP (Pause or Merge Now)
[For each pair: Ad Set A vs Ad Set B | Overlap Type | Combined Spend | CPM Inflation | Wasted $/mo | Action]

HIGH OVERLAP (Fix This Week)
[Same format]

CONSOLIDATION PLAN
Cluster 1: [Ad Set names]
  Keep: [Which ad set and why - it has highest ROAS]
  Pause: [Which ad sets]
  Add these exclusions to the surviving ad set:
    [Specific exclusion audience instructions]

PROJECTED IMPROVEMENTS
After fixing all severe and high overlaps:
- Expected CPM reduction: -X%
- Expected additional reach at same budget: +X%
- Monthly savings: $X

---
Powered by Hatty.ai | mcp.hattysites.com
---
