# Analyzing the Intersection of Housing Affordability and Transit Access for Hispanic Communities in Washington, D.C.

**Author**: Pablo Andre Espejo  
**Course**: URSP688Y – Urban Data Science & Smart Cities  
**Instructor**: Dr. Chester Harvey  
**Date**: May 11, 2025

[**Link to the Google Drive Containing all the Files**](https://drive.google.com/drive/folders/1e2nGDsZfV_kfSOfiPWKqfelK_zvqVgPR?usp=share_link)

[**Link to the Written Narrative**](https://drive.google.com/file/d/1IddFn6Mos7H1QWQB4awTcNUUQKMHhtWz/view?usp=sharing)

---

## Introduction

This project examines whether affordable housing and public transit in Washington, D.C. equitably serve Hispanic communities, who face rising displacement pressures and transportation barriers due to gentrification. Using spatial analysis and data visualization, it explores the mismatch between where Hispanic populations live, where affordable housing is built, and where high-frequency transit is available.

---

## Central Research Questions

1. How does the spatial distribution of affordable housing (by AMI tier) correlate with the Hispanic population at the census block group level?
2. To what extent do Hispanic-majority areas have access to high-frequency Metrorail and Metrobus service?

---

## Data Sources

- **Affordable Housing Projects** (Open Data DC, since 2015)
- **ACS 2023 Block Group Demographics** (NHGIS)
- **Transit Stop Frequency Shapefile** (Transit Service Frequency App)
- **D.C. Boundary** (Open Data DC)

---

## Methodology

### 4.1 Spatial Joins & Calculations
Each census block group was enriched with:
- Total & Hispanic population
- Affordable housing unit counts by AMI tier (≤30%, 31–50%, 51–60%, 61–80%, ≥81%)
- Transit stop frequency
- Calculated Hispanic percentage & affordable housing ratios

### 4.2 Bivariate Choropleth Mapping
Variables were grouped into 3 tiers (low, medium, high) using **Natural Breaks (Jenks)** and combined into 3x3 bivariate classes to visualize overlaps and mismatches.

---

## Results

### 5.1 Affordable Housing

- **Few areas** had both high Hispanic populations and high affordable housing counts.
- Most common:  
  - High Hispanic, **Low** affordable housing  
  - Low Hispanic, **High** affordable housing

#### 5.1.1 Distribution by AMI Tier
- Slight alignment for ≤30% AMI units
- Weak or negative overlap for 31–80% AMI units
- Near-zero presence of ≥81% AMI units in Hispanic areas

### 5.2 Transit Access

#### 5.2.1 Rail
- High-Hispanic areas had **limited to no Metrorail access**
- Raises equity concerns due to exclusion from faster, reliable modes

#### 5.2.2 Bus
- Bus service more available, but **inconsistent in quality and frequency**
- No strong statistical correlation with Hispanic population share

---

## Conclusions

- **Housing Mismatch**: Affordable housing, especially mid-tier (31–80% AMI), is not concentrated in Hispanic neighborhoods, limiting upward mobility and stability.
- **Transportation Exclusion**: Metrorail investment favors wealthier, whiter areas, forcing Hispanic residents to rely on slower, less frequent buses.

### Overall:
There is a **persistent spatial mismatch** between affordable housing, transit access, and the needs of D.C.’s Hispanic communities.

---

## Limitations

- Time mismatch between transit and housing data
- Ecological fallacy from census aggregation
- Correlation ≠ causation
- Access vs. proximity distinction

---

## Future Work

- Longitudinal studies on housing distribution trends
- Qualitative interviews with Hispanic residents
- Better transit service quality metrics
- Comparison with similar cities (e.g., Boston, SF)

---
