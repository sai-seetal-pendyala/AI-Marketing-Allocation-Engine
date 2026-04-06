"""
Dataset 4: Allocation Pressure Scenario Model Generator
========================================================
Generates the scenario layer for the AI Marketing Allocation Engine project.

This script combines three indices derived from public datasets into a composite
allocation framework with scenario variants:
  - Market Momentum Index (MMI) from IAB/PwC data
  - AI Efficiency Leverage Index (AELI) from Gartner/CMO Survey data
  - AI Discovery Exposure Index (ADEI) from SEMrush AI Overviews data

Output: data/dataset4_allocation_pressure_model.csv
Run from the project root: python code/01_generate_scenario_model.py

All calibration sources are documented inline.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# ============================================================
# STEP 1: Define channel taxonomy and base scores
# ============================================================

channels = {
    "Organic Search": {
        "iab_channel": "Search",
        "iab_cagr_5yr": 11.8,        # Search: $59B (2020) -> $102.9B (2024) ~11.8% CAGR
        "iab_share_2024": 39.8,
        "iab_share_2020": 42.2,
        "ai_efficiency_time_pct": 55,  # High - SEO content heavily AI-assisted
        "ai_efficiency_cost_pct": 50,
        "ai_outcome_translation_pct": 20,  # Low - gains absorbed by channel headwinds
        "aio_prevalence_pct": 15.69,  # SEMrush Nov 2025 average
        "primary_intent": "Informational",
        "intent_aio_growth_velocity": 0.8,  # Moderate - informational declining in share
        "search_dependent": True,
        "b2b_cac": 1216,  # Average of Thought Leadership SEO ($647) and Basic SEO ($1786)
        "b2c_cac": 750,   # Average of $298 and $1201
    },
    "Paid Search (PPC/SEM)": {
        "iab_channel": "Search",
        "iab_cagr_5yr": 11.8,
        "iab_share_2024": 39.8,
        "iab_share_2020": 42.2,
        "ai_efficiency_time_pct": 50,
        "ai_efficiency_cost_pct": 45,
        "ai_outcome_translation_pct": 35,  # Higher - paid has clearer attribution
        "aio_prevalence_pct": 10.0,  # Lower - ads still shown alongside AIOs (25% of AIO SERPs now show ads)
        "primary_intent": "Commercial",
        "intent_aio_growth_velocity": 1.2,  # Growing - commercial AIOs rising fast
        "search_dependent": True,
        "b2b_cac": 802,
        "b2c_cac": 290,
    },
    "Paid Social": {
        "iab_channel": "Social Media",
        "iab_cagr_5yr": 16.4,  # Social: $41.5B (2020) -> $88.8B (2024) ~16.4% CAGR
        "iab_share_2024": 34.3,
        "iab_share_2020": 29.7,
        "ai_efficiency_time_pct": 52,
        "ai_efficiency_cost_pct": 42,
        "ai_outcome_translation_pct": 38,
        "aio_prevalence_pct": 0.0,  # Not in search ecosystem
        "primary_intent": "Non-Search",
        "intent_aio_growth_velocity": 0.0,
        "search_dependent": False,
        "b2b_cac": 982,   # LinkedIn Ads proxy
        "b2c_cac": 230,   # Facebook Ads
    },
    "Organic Social": {
        "iab_channel": "Social Media",
        "iab_cagr_5yr": 16.4,
        "iab_share_2024": 34.3,
        "iab_share_2020": 29.7,
        "ai_efficiency_time_pct": 48,
        "ai_efficiency_cost_pct": 55,  # High - AI generates social content cheaply
        "ai_outcome_translation_pct": 25,  # Organic social reach declining (pay-to-play)
        "aio_prevalence_pct": 0.0,
        "primary_intent": "Non-Search",
        "intent_aio_growth_velocity": 0.0,
        "search_dependent": False,
        "b2b_cac": 658,
        "b2c_cac": 212,
    },
    "Email": {
        "iab_channel": "Direct/Email",
        "iab_cagr_5yr": 5.0,  # Stable, mature channel
        "iab_share_2024": 3.0,  # Small share of ad market but huge owned channel
        "iab_share_2020": 3.5,
        "ai_efficiency_time_pct": 55,
        "ai_efficiency_cost_pct": 60,  # Very high - AI personalizes at scale
        "ai_outcome_translation_pct": 45,  # Highest - email has direct attribution
        "aio_prevalence_pct": 0.0,  # Completely insulated from search disruption
        "primary_intent": "Non-Search",
        "intent_aio_growth_velocity": 0.0,
        "search_dependent": False,
        "b2b_cac": 510,
        "b2c_cac": 287,
    },
    "Content / Blog": {
        "iab_channel": "Display",
        "iab_cagr_5yr": 15.5,  # Display: $36.2B -> $74.3B ~15.5% CAGR
        "iab_share_2024": 28.7,
        "iab_share_2020": 25.9,
        "ai_efficiency_time_pct": 60,  # Highest - blog content is AI's sweet spot
        "ai_efficiency_cost_pct": 65,
        "ai_outcome_translation_pct": 18,  # Lowest - content saturation kills returns
        "aio_prevalence_pct": 20.0,  # High - informational queries hit hardest
        "primary_intent": "Informational",
        "intent_aio_growth_velocity": 0.8,
        "search_dependent": True,
        "b2b_cac": 1254,
        "b2c_cac": 890,
    },
    "Digital Video": {
        "iab_channel": "Digital Video",
        "iab_cagr_5yr": 18.8,  # Video: $26.2B -> $62.1B ~18.8% CAGR
        "iab_share_2024": 24.0,
        "iab_share_2020": 18.7,
        "ai_efficiency_time_pct": 35,  # Lower - video AI tools less mature
        "ai_efficiency_cost_pct": 30,
        "ai_outcome_translation_pct": 30,
        "aio_prevalence_pct": 5.0,  # Low - video carousels sometimes appear with AIOs
        "primary_intent": "Mixed",
        "intent_aio_growth_velocity": 0.3,
        "search_dependent": False,  # Primarily platform-native (YouTube, TikTok)
        "b2b_cac": 815,
        "b2c_cac": 301,
    },
    "Retail Media": {
        "iab_channel": "Retail Media",
        "iab_cagr_5yr": 17.5,  # Retail Media: ~$24B (2020 est) -> $53.7B (2024)
        "iab_share_2024": 20.8,
        "iab_share_2020": 17.2,
        "ai_efficiency_time_pct": 40,
        "ai_efficiency_cost_pct": 35,
        "ai_outcome_translation_pct": 42,  # High - closed-loop measurement
        "aio_prevalence_pct": 2.5,  # Very low - Shopping has lowest AIO rate
        "primary_intent": "Transactional",
        "intent_aio_growth_velocity": 0.5,
        "search_dependent": False,  # Platform-native (Amazon, Walmart)
        "b2b_cac": None,
        "b2c_cac": 290,  # Comparable to PPC
    },
}

# ============================================================
# STEP 2: Compute the three indices for each channel
# ============================================================

def compute_mmi(channel_data):
    """Market Momentum Index (0-100). Based on IAB 5-year CAGR and share trajectory."""
    cagr = channel_data["iab_cagr_5yr"]
    share_shift = channel_data["iab_share_2024"] - channel_data["iab_share_2020"]
    cagr_score = min(max((cagr - 5.0) / (20.0 - 5.0) * 60, 0), 60)
    share_score = min(max((share_shift - (-3.0)) / (6.0 - (-3.0)) * 40, 0), 40)
    return round(cagr_score + share_score, 1)

def compute_aeli(channel_data):
    """AI Efficiency Leverage Index (0-100). Weighted: outcome translation gets 50% weight."""
    time_eff = channel_data["ai_efficiency_time_pct"]
    cost_eff = channel_data["ai_efficiency_cost_pct"]
    outcome = channel_data["ai_outcome_translation_pct"]
    raw = (time_eff * 0.25 + cost_eff * 0.25 + outcome * 0.50)
    return round(min(max(raw / 0.55, 0), 100), 1)  # Normalize so max ~100

def compute_adei(channel_data):
    """AI Discovery Exposure Index (0-100). Based on AIO prevalence and intent growth velocity."""
    prevalence = channel_data["aio_prevalence_pct"]
    velocity = channel_data["intent_aio_growth_velocity"]
    is_search = 1.0 if channel_data["search_dependent"] else 0.0
    raw = (prevalence / 25.0 * 50) + (velocity / 1.5 * 30) + (is_search * 20)
    return round(min(max(raw, 0), 100), 1)

records = []
for ch_name, ch_data in channels.items():
    mmi = compute_mmi(ch_data)
    aeli = compute_aeli(ch_data)
    adei = compute_adei(ch_data)
    records.append({
        "Channel": ch_name,
        "IAB_Channel_Group": ch_data["iab_channel"],
        "MMI_Score": mmi,
        "AELI_Score": aeli,
        "ADEI_Score": adei,
        "CAGR_5yr_Pct": ch_data["iab_cagr_5yr"],
        "Share_2024_Pct": ch_data["iab_share_2024"],
        "Share_Shift_Pct": round(ch_data["iab_share_2024"] - ch_data["iab_share_2020"], 1),
        "AI_Time_Efficiency_Pct": ch_data["ai_efficiency_time_pct"],
        "AI_Cost_Efficiency_Pct": ch_data["ai_efficiency_cost_pct"],
        "AI_Outcome_Translation_Pct": ch_data["ai_outcome_translation_pct"],
        "AIO_Prevalence_Pct": ch_data["aio_prevalence_pct"],
        "Primary_Query_Intent": ch_data["primary_intent"],
        "Search_Dependent": ch_data["search_dependent"],
        "B2B_CAC_USD": ch_data["b2b_cac"],
        "B2C_CAC_USD": ch_data["b2c_cac"],
    })

channel_base = pd.DataFrame(records)

# ============================================================
# STEP 3: Generate scenario variants
# ============================================================

scenarios = {
    "Baseline": {"adei_mult": 1.0, "aeli_mult": 1.0, "mmi_mult": 1.0},
    "High_AI_Disruption": {"adei_mult": 1.5, "aeli_mult": 1.0, "mmi_mult": 1.0},
    "Very_High_AI_Disruption": {"adei_mult": 2.0, "aeli_mult": 1.0, "mmi_mult": 1.0},
    "Low_AI_Disruption": {"adei_mult": 0.6, "aeli_mult": 1.0, "mmi_mult": 1.0},
    "High_AI_Efficiency": {"adei_mult": 1.0, "aeli_mult": 1.25, "mmi_mult": 1.0},
    "Low_AI_Efficiency": {"adei_mult": 1.0, "aeli_mult": 0.75, "mmi_mult": 1.0},
    "Bull_Market": {"adei_mult": 1.0, "aeli_mult": 1.0, "mmi_mult": 1.15},
    "Bear_Market": {"adei_mult": 1.0, "aeli_mult": 1.0, "mmi_mult": 0.85},
    "Worst_Case": {"adei_mult": 2.0, "aeli_mult": 0.75, "mmi_mult": 0.85},
    "Best_Case": {"adei_mult": 0.6, "aeli_mult": 1.25, "mmi_mult": 1.15},
}

industries = [
    "Tech/Software", "Healthcare", "Financial Services",
    "Retail/E-commerce", "Professional Services", "Consumer Brands"
]

company_sizes = ["SMB", "Mid-Market", "Enterprise"]

# Industry modifiers (how much each industry amplifies or dampens each index)
industry_mods = {
    "Tech/Software":        {"mmi_mod": 1.10, "aeli_mod": 1.15, "adei_mod": 1.05},
    "Healthcare":           {"mmi_mod": 0.95, "aeli_mod": 0.90, "adei_mod": 1.10},
    "Financial Services":   {"mmi_mod": 1.00, "aeli_mod": 0.95, "adei_mod": 0.90},
    "Retail/E-commerce":    {"mmi_mod": 1.05, "aeli_mod": 1.05, "adei_mod": 0.80},
    "Professional Services":{"mmi_mod": 0.90, "aeli_mod": 1.00, "adei_mod": 1.00},
    "Consumer Brands":      {"mmi_mod": 1.00, "aeli_mod": 0.95, "adei_mod": 0.95},
}

# Company size modifiers
size_mods = {
    "SMB":        {"aeli_mod": 0.85, "adei_sensitivity": 1.10},
    "Mid-Market": {"aeli_mod": 1.00, "adei_sensitivity": 1.00},
    "Enterprise": {"aeli_mod": 1.15, "adei_sensitivity": 0.90},
}

def normalize_naps(raw_naps, min_raw=-40, max_raw=210):
    """Normalize raw NAPS to 0-100 scale for consistent classification."""
    return max(0, min(100, (raw_naps - min_raw) / (max_raw - min_raw) * 100))

def classify_naps(naps_normalized):
    if naps_normalized >= 75:
        return "Scale"
    elif naps_normalized >= 55:
        return "Test"
    elif naps_normalized >= 35:
        return "Hold"
    else:
        return "Reduce"

def confidence_band(channel_data, scenario_name):
    if scenario_name == "Baseline":
        return "High"
    elif "Very_High" in scenario_name or "Worst" in scenario_name or "Best" in scenario_name:
        return "Low"
    else:
        return "Medium"

all_rows = []

for scenario_name, s_params in scenarios.items():
    for _, ch_row in channel_base.iterrows():
        for industry in industries:
            for size in company_sizes:
                i_mod = industry_mods[industry]
                s_mod = size_mods[size]

                adj_mmi = min(ch_row["MMI_Score"] * s_params["mmi_mult"] * i_mod["mmi_mod"], 100)
                adj_aeli = min(ch_row["AELI_Score"] * s_params["aeli_mult"] * i_mod["aeli_mod"] * s_mod["aeli_mod"], 100)
                adj_adei = min(ch_row["ADEI_Score"] * s_params["adei_mult"] * i_mod["adei_mod"] * s_mod["adei_sensitivity"], 100)

                noise = np.random.normal(0, 1.5)
                naps_raw = (adj_mmi + adj_aeli) - adj_adei + noise
                naps = round(normalize_naps(naps_raw), 2)

                classification = classify_naps(naps)
                conf = confidence_band(ch_row, scenario_name)

                all_rows.append({
                    "Channel": ch_row["Channel"],
                    "Industry": industry,
                    "Company_Size": size,
                    "Scenario": scenario_name,
                    "MMI_Score": round(adj_mmi, 2),
                    "AELI_Score": round(adj_aeli, 2),
                    "ADEI_Score": round(adj_adei, 2),
                    "NAPS_Score": naps,
                    "Allocation_Classification": classification,
                    "Confidence_Band": conf,
                    "IAB_Channel_Group": ch_row["IAB_Channel_Group"],
                    "Primary_Query_Intent": ch_row["Primary_Query_Intent"],
                    "Search_Dependent": ch_row["Search_Dependent"],
                    "B2B_CAC_USD": ch_row["B2B_CAC_USD"],
                    "B2C_CAC_USD": ch_row["B2C_CAC_USD"],
                    "AI_Time_Efficiency_Pct": ch_row["AI_Time_Efficiency_Pct"],
                    "AI_Cost_Efficiency_Pct": ch_row["AI_Cost_Efficiency_Pct"],
                    "AI_Outcome_Translation_Pct": ch_row["AI_Outcome_Translation_Pct"],
                    "AIO_Prevalence_Pct": ch_row["AIO_Prevalence_Pct"],
                    "CAGR_5yr_Pct": ch_row["CAGR_5yr_Pct"],
                    "Share_2024_Pct": ch_row["Share_2024_Pct"],
                })

df = pd.DataFrame(all_rows)

# ============================================================
# STEP 4: Validation
# ============================================================

assert df["NAPS_Score"].notna().all(), "Found NaN NAPS scores"
assert df["Allocation_Classification"].isin(["Scale", "Test", "Hold", "Reduce"]).all()
assert len(df) == len(channels) * len(scenarios) * len(industries) * len(company_sizes)

baseline = df[df["Scenario"] == "Baseline"]
print("\n=== VALIDATION SUMMARY ===")
print(f"Total records: {len(df)}")
print(f"Channels: {df['Channel'].nunique()}")
print(f"Scenarios: {df['Scenario'].nunique()}")
print(f"Industries: {df['Industry'].nunique()}")
print(f"Company sizes: {df['Company_Size'].nunique()}")
print(f"\nBaseline allocation distribution:")
print(baseline["Allocation_Classification"].value_counts().to_string())
print(f"\nNAPS score range: {df['NAPS_Score'].min():.1f} to {df['NAPS_Score'].max():.1f}")
print(f"Baseline NAPS mean: {baseline['NAPS_Score'].mean():.1f}")

print("\nBaseline NAPS by Channel (averaged across industry/size):")
ch_summary = baseline.groupby("Channel")["NAPS_Score"].mean().sort_values(ascending=False)
for ch, score in ch_summary.items():
    cls = classify_naps(score)
    print(f"  {ch:30s}  NAPS={score:6.1f}  -> {cls}")

# ============================================================
# STEP 5: Export
# ============================================================

output_path = "data/dataset4_allocation_pressure_model.csv"
df.to_csv(output_path, index=False)
print(f"\nExported {len(df)} records to {output_path}")
