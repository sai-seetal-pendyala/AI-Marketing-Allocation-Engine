"""
Generates preliminary visualizations for the MAX 507 project proposal.
Each chart maps to one of the five analytical questions in the proposal.
Output: PNG files saved to the assets/ folder.
Run from the project root: python code/02_generate_visualizations.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
import os

os.makedirs("assets", exist_ok=True)

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "Arial", "Helvetica"],
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9,
    "figure.facecolor": "white",
    "axes.facecolor": "#f9f9fb",
    "axes.edgecolor": "#cccccc",
    "grid.color": "#e6e6e6",
})

PALETTE = {
    "Search": "#4285F4",
    "Social Media": "#E1306C",
    "Display": "#FBBC05",
    "Digital Video": "#EA4335",
    "Retail Media": "#34A853",
    "Digital Audio": "#9B59B6",
    "Podcast": "#9B59B6",
}

NAPS_COLORS = {
    "Scale": "#27ae60",
    "Test": "#2980b9",
    "Hold": "#f39c12",
    "Reduce": "#e74c3c",
}

# ================================================================
# LOAD DATA
# ================================================================
iab = pd.read_csv("data/dataset1_iab_advertising_revenue_2020_2024.csv")
semrush = pd.read_csv("data/dataset2_semrush_ai_overviews_2025.csv")
semrush_ind = pd.read_csv("data/dataset2b_semrush_aio_by_industry.csv")
gartner = pd.read_csv("data/dataset3a_gartner_cmo_spend_2025.csv")
scenario = pd.read_csv("data/dataset4_allocation_pressure_model.csv")


# ================================================================
# VISUALIZATION 1 — Question 1
# Channel Revenue Trajectories (2020–2024)
# ================================================================
def viz1_channel_revenue():
    fig, ax = plt.subplots(figsize=(10, 5.5))

    core_channels = ["Search", "Social Media", "Display", "Digital Video", "Retail Media"]
    for ch in core_channels:
        ch_data = iab[iab["Channel"] == ch].sort_values("Year")
        ax.plot(ch_data["Year"], ch_data["Revenue_Billions"],
                marker="o", linewidth=2.3, markersize=6,
                color=PALETTE.get(ch, "#666"), label=ch, zorder=3)
        last = ch_data.iloc[-1]
        ax.annotate(f"${last['Revenue_Billions']:.0f}B",
                    xy=(last["Year"], last["Revenue_Billions"]),
                    xytext=(8, 0), textcoords="offset points",
                    fontsize=8.5, fontweight="bold",
                    color=PALETTE.get(ch, "#666"), va="center")

    ax.axvspan(2023.3, 2024.7, alpha=0.07, color="#e74c3c", zorder=0)
    ax.text(2023.85, 108, "GenAI era", fontsize=8, color="#e74c3c",
            fontstyle="italic", alpha=0.7)

    ax.set_title("Q1: Where Is Advertising Money Flowing? — U.S. Digital Ad Revenue by Channel",
                 fontweight="bold", pad=12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue ($ Billions)")
    ax.set_xticks([2020, 2021, 2022, 2023, 2024])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}B"))
    ax.legend(loc="upper left", framealpha=0.9)
    ax.set_xlim(2019.7, 2024.8)

    fig.text(0.5, -0.02,
             "Source: IAB/PwC Internet Advertising Revenue Reports (2020–2024). Total U.S. market grew from $139.8B to $258.6B.",
             ha="center", fontsize=7.5, color="#888888")

    plt.tight_layout()
    fig.savefig("assets/viz1_channel_revenue_trajectory.png", bbox_inches="tight")
    plt.close()
    print("  Saved assets/viz1_channel_revenue_trajectory.png")


# ================================================================
# VISUALIZATION 2 — Question 2
# The Efficiency-to-Outcome Gap
# ================================================================
def viz2_efficiency_gap():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5),
                                    gridspec_kw={"width_ratios": [1.3, 1]})

    # LEFT: Divergence bar chart
    metrics = ["Time efficiency\ngains", "Cost efficiency\ngains",
               "Content capacity\nincrease"]
    efficiency_vals = [49, 40, 27]
    outcome_val = 27
    gap_vals = [v - outcome_val for v in efficiency_vals]

    y_pos = np.arange(len(metrics))
    bars_eff = ax1.barh(y_pos, efficiency_vals, height=0.55,
                         color="#3498db", alpha=0.85, label="% CMOs reporting efficiency gain")
    bars_outcome = ax1.barh(y_pos, [-outcome_val]*len(metrics), height=0.55,
                             color="#27ae60", alpha=0.85, label="% reporting business outcomes (27%)")

    for i, (e, o) in enumerate(zip(efficiency_vals, [outcome_val]*3)):
        ax1.text(e + 1, i, f"{e}%", va="center", fontsize=9, fontweight="bold", color="#2c3e50")
        ax1.text(-o - 1.5, i, f"{o}%", va="center", fontsize=9, fontweight="bold",
                 color="#2c3e50", ha="right")

    ax1.axvline(x=0, color="#2c3e50", linewidth=1.2)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(metrics)
    ax1.set_xlim(-45, 60)
    ax1.set_xlabel("← Business Outcomes          Efficiency Gains →")
    ax1.set_title("Q2: The Efficiency-to-Outcome Gap",
                  fontweight="bold", pad=10)
    ax1.legend(loc="lower right", fontsize=7.5, framealpha=0.9)

    gap_annotation = ax1.annotate(
        "22-point\ngap",
        xy=(38, 0), xytext=(50, 0.7),
        fontsize=10, fontweight="bold", color="#e74c3c",
        arrowprops=dict(arrowstyle="->", color="#e74c3c", lw=1.5),
        ha="center")

    # RIGHT: AI adoption growth waterfall
    categories = ["Marketing\nbudget\n(% of rev)", "AI time\nsavings", "AI cost\nsavings",
                  "Cut agency\nspend", "Cut labor\ncosts"]
    values = [7.7, 49, 40, -39, -39]
    colors_wf = ["#3498db", "#27ae60", "#27ae60", "#e74c3c", "#e74c3c"]

    bars = ax2.bar(range(len(categories)), [abs(v) for v in values],
                   color=colors_wf, alpha=0.85, width=0.6, edgecolor="white", linewidth=1)

    for i, (v, b) in enumerate(zip(values, bars)):
        label = f"{v}%" if v > 0 else f"{v}%"
        ax2.text(b.get_x() + b.get_width()/2, abs(v) + 1.2, label,
                ha="center", fontsize=8.5, fontweight="bold",
                color="#2c3e50")

    ax2.set_xticks(range(len(categories)))
    ax2.set_xticklabels(categories, fontsize=8)
    ax2.set_ylabel("Percentage (%)")
    ax2.set_title("Where CMOs Are Placing Their Bets",
                  fontweight="bold", pad=10)
    ax2.set_ylim(0, 60)

    fig.text(0.5, -0.03,
             "Sources: Gartner 2025 CMO Spend Survey | CMO Survey Spring 2025 (Duke/Deloitte, n=281)",
             ha="center", fontsize=7.5, color="#888888")

    plt.tight_layout()
    fig.savefig("assets/viz2_efficiency_outcome_gap.png", bbox_inches="tight")
    plt.close()
    print("  Saved assets/viz2_efficiency_outcome_gap.png")


# ================================================================
# VISUALIZATION 3 — Question 3
# AI Overview Intent Migration + Industry Exposure
# ================================================================
def viz3_ai_overview_exposure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5),
                                    gridspec_kw={"width_ratios": [1.2, 1]})

    # LEFT: Stacked area — intent migration over time
    months = pd.to_datetime(semrush["Month"])
    month_labels = [m.strftime("%b") for m in months]

    info = semrush["Informational_Intent_Pct"].values
    comm = semrush["Commercial_Intent_Pct"].values
    trans = semrush["Transactional_Intent_Pct"].values
    nav = semrush["Navigational_Intent_Pct"].values

    ax1.fill_between(range(len(months)), 0, info, alpha=0.7, color="#3498db", label="Informational")
    ax1.fill_between(range(len(months)), info, info + comm, alpha=0.7, color="#e67e22", label="Commercial")
    ax1.fill_between(range(len(months)), info + comm, info + comm + trans,
                     alpha=0.7, color="#e74c3c", label="Transactional")
    ax1.fill_between(range(len(months)), info + comm + trans, info + comm + trans + nav,
                     alpha=0.7, color="#9b59b6", label="Navigational")

    ax1_twin = ax1.twinx()
    ax1_twin.plot(range(len(months)), semrush["AIO_Prevalence_Pct"].values,
                  color="#2c3e50", linewidth=2.5, marker="D", markersize=5,
                  linestyle="--", label="AIO Prevalence %", zorder=5)
    ax1_twin.set_ylabel("AI Overview Prevalence (%)", color="#2c3e50")
    ax1_twin.set_ylim(0, 35)
    ax1_twin.tick_params(axis="y", labelcolor="#2c3e50")

    ax1.annotate("91.3%\ninformational", xy=(0, 91.3), xytext=(1.5, 75),
                fontsize=7.5, color="#2471a3", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2471a3", lw=1))
    ax1.annotate("57.1%\ninformational", xy=(9, 57.1), xytext=(7.5, 42),
                fontsize=7.5, color="#2471a3", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2471a3", lw=1))

    ax1.set_xticks(range(len(months)))
    ax1.set_xticklabels(month_labels, rotation=45)
    ax1.set_ylabel("Intent Distribution (%)")
    ax1.set_ylim(0, 105)
    ax1.set_title("Q3: AI Overviews Are Moving Down the Funnel",
                  fontweight="bold", pad=10)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right",
               fontsize=7, framealpha=0.9)

    # RIGHT: Industry exposure horizontal bars
    top_industries = semrush_ind.sort_values("AIO_Saturation_Nov2025_Pct", ascending=True).tail(12)

    colors_ind = []
    for v in top_industries["AIO_Saturation_Nov2025_Pct"]:
        if v >= 15:
            colors_ind.append("#e74c3c")
        elif v >= 10:
            colors_ind.append("#f39c12")
        else:
            colors_ind.append("#27ae60")

    bars = ax2.barh(range(len(top_industries)), top_industries["AIO_Saturation_Nov2025_Pct"],
                    color=colors_ind, alpha=0.85, height=0.65, edgecolor="white", linewidth=0.8)

    for i, (v, ind) in enumerate(zip(top_industries["AIO_Saturation_Nov2025_Pct"],
                                      top_industries["Industry"])):
        ax2.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=8, fontweight="bold", color="#2c3e50")

    ax2.set_yticks(range(len(top_industries)))
    ax2.set_yticklabels(top_industries["Industry"], fontsize=8.5)
    ax2.set_xlabel("AI Overview Saturation (% of keywords)")
    ax2.set_title("Industry Exposure to AI Overviews",
                  fontweight="bold", pad=10)
    ax2.set_xlim(0, 32)

    ax2.axvline(x=15.69, color="#2c3e50", linewidth=1, linestyle=":", alpha=0.5)
    ax2.text(16.2, 0.3, "Avg:\n15.7%", fontsize=7, color="#2c3e50", fontstyle="italic")

    fig.text(0.5, -0.03,
             "Source: SEMrush AI Overviews Study (10M+ keywords, Jan–Nov 2025) — semrush.com/blog/semrush-ai-overviews-study/",
             ha="center", fontsize=7.5, color="#888888")

    plt.tight_layout()
    fig.savefig("assets/viz3_ai_overview_exposure.png", bbox_inches="tight")
    plt.close()
    print("  Saved assets/viz3_ai_overview_exposure.png")


# ================================================================
# VISUALIZATION 4 — Question 4
# Net Allocation Pressure — Quadrant Scatter Plot
# ================================================================
def viz4_allocation_quadrant():
    fig, ax = plt.subplots(figsize=(10, 7))

    baseline = scenario[
        (scenario["Scenario"] == "Baseline") &
        (scenario["Industry"] == "Tech/Software") &
        (scenario["Company_Size"] == "Mid-Market")
    ].copy()

    positive_pressure = baseline["MMI_Score"] + baseline["AELI_Score"]
    negative_pressure = baseline["ADEI_Score"]
    bubble_size = baseline["Share_2024_Pct"] * 12

    for _, row in baseline.iterrows():
        pp = row["MMI_Score"] + row["AELI_Score"]
        np_ = row["ADEI_Score"]
        cls = row["Allocation_Classification"]
        color = NAPS_COLORS[cls]
        size = row["Share_2024_Pct"] * 12

        ax.scatter(pp, np_, s=size, c=color, alpha=0.8, edgecolors="white",
                   linewidth=1.5, zorder=5)

        offset_y = 3 if np_ > 30 else -5
        ax.annotate(row["Channel"], xy=(pp, np_),
                   xytext=(0, offset_y), textcoords="offset points",
                   fontsize=8, fontweight="bold", ha="center", color="#2c3e50",
                   zorder=6)

    # Quadrant lines
    ax.axhline(y=45, color="#bdc3c7", linewidth=1.2, linestyle="--", zorder=1)
    ax.axvline(x=100, color="#bdc3c7", linewidth=1.2, linestyle="--", zorder=1)

    # Quadrant labels
    ax.text(145, 85, "TEST\nHigh potential,\nhigh risk", fontsize=9, color="#2980b9",
            fontstyle="italic", ha="center", alpha=0.6, fontweight="bold")
    ax.text(60, 85, "REDUCE\nLow potential,\nhigh risk", fontsize=9, color="#e74c3c",
            fontstyle="italic", ha="center", alpha=0.6, fontweight="bold")
    ax.text(145, 10, "SCALE\nHigh potential,\nlow risk", fontsize=9, color="#27ae60",
            fontstyle="italic", ha="center", alpha=0.6, fontweight="bold")
    ax.text(60, 10, "HOLD\nLow potential,\nlow risk", fontsize=9, color="#f39c12",
            fontstyle="italic", ha="center", alpha=0.6, fontweight="bold")

    ax.set_xlabel("← Low Potential          Positive Pressure (MMI + AELI)          High Potential →",
                  fontsize=10, labelpad=8)
    ax.set_ylabel("← Low Risk          Negative Pressure (ADEI)          High Risk →",
                  fontsize=10, labelpad=8)
    ax.set_title("Q4: Net Allocation Pressure — Which Channels to Scale, Test, Hold, or Reduce?",
                 fontweight="bold", fontsize=12, pad=14)

    # Legend for classification
    for cls, color in NAPS_COLORS.items():
        ax.scatter([], [], s=80, c=color, label=cls, edgecolors="white", linewidth=1)
    ax.legend(title="Classification", loc="upper left", framealpha=0.9, fontsize=8.5)

    ax.set_xlim(40, 180)
    ax.set_ylim(-5, 100)

    fig.text(0.5, -0.02,
             "Baseline scenario | Tech/Software | Mid-Market | Bubble size = channel market share (IAB 2024)\n"
             "NAPS = (MMI + AELI) − ADEI | Sources: IAB, SEMrush, Gartner, CMO Survey",
             ha="center", fontsize=7.5, color="#888888")

    plt.tight_layout()
    fig.savefig("assets/viz4_allocation_quadrant.png", bbox_inches="tight")
    plt.close()
    print("  Saved assets/viz4_allocation_quadrant.png")


# ================================================================
# VISUALIZATION 5 — Question 5
# Scenario Comparison — How Allocations Shift Under Different Futures
# ================================================================
def viz5_scenario_shifts():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5),
                                    gridspec_kw={"width_ratios": [1.2, 1]})

    # LEFT: NAPS by channel across key scenarios
    key_scenarios = ["Baseline", "High_AI_Disruption", "Very_High_AI_Disruption",
                     "Low_AI_Disruption", "High_AI_Efficiency", "Low_AI_Efficiency"]
    scenario_labels = {
        "Baseline": "Baseline",
        "High_AI_Disruption": "High AI\nDisruption",
        "Very_High_AI_Disruption": "Very High AI\nDisruption",
        "Low_AI_Disruption": "Low AI\nDisruption",
        "High_AI_Efficiency": "High AI\nEfficiency",
        "Low_AI_Efficiency": "Low AI\nEfficiency",
    }

    focus_channels = ["Organic Search", "Paid Social", "Email", "Content / Blog"]
    channel_colors_naps = {
        "Organic Search": "#4285F4",
        "Paid Social": "#E1306C",
        "Email": "#f39c12",
        "Content / Blog": "#27ae60",
    }

    for ch in focus_channels:
        means = []
        for sc in key_scenarios:
            subset = scenario[(scenario["Scenario"] == sc) & (scenario["Channel"] == ch)]
            means.append(subset["NAPS_Score"].mean())
        ax1.plot(range(len(key_scenarios)), means, marker="o", linewidth=2,
                markersize=6, label=ch, color=channel_colors_naps[ch])

    ax1.axhline(y=75, color="#27ae60", linewidth=0.8, linestyle=":", alpha=0.5)
    ax1.axhline(y=55, color="#2980b9", linewidth=0.8, linestyle=":", alpha=0.5)
    ax1.axhline(y=35, color="#e74c3c", linewidth=0.8, linestyle=":", alpha=0.5)

    ax1.text(5.15, 76, "Scale", fontsize=7, color="#27ae60", fontstyle="italic")
    ax1.text(5.15, 56, "Test", fontsize=7, color="#2980b9", fontstyle="italic")
    ax1.text(5.15, 36, "Hold", fontsize=7, color="#e74c3c", fontstyle="italic")
    ax1.text(5.15, 25, "Reduce", fontsize=7, color="#e74c3c", fontstyle="italic", alpha=0.7)

    ax1.set_xticks(range(len(key_scenarios)))
    ax1.set_xticklabels([scenario_labels[s] for s in key_scenarios], fontsize=7.5)
    ax1.set_ylabel("NAPS Score (0–100)")
    ax1.set_title("Q5: How Do Allocations Shift Under Different Futures?",
                  fontweight="bold", pad=10)
    ax1.legend(loc="lower left", fontsize=8, framealpha=0.9)
    ax1.set_ylim(15, 90)

    # RIGHT: Classification distribution across scenarios
    class_order = ["Scale", "Test", "Hold", "Reduce"]
    comparison_scenarios = ["Baseline", "High_AI_Disruption", "Very_High_AI_Disruption", "Best_Case", "Worst_Case"]
    comp_labels = ["Baseline", "High AI\nDisruption", "Very High\nDisruption", "Best\nCase", "Worst\nCase"]

    bottom = np.zeros(len(comparison_scenarios))
    for cls in class_order:
        counts = []
        for sc in comparison_scenarios:
            subset = scenario[scenario["Scenario"] == sc]
            total = len(subset)
            cls_count = len(subset[subset["Allocation_Classification"] == cls])
            counts.append(cls_count / total * 100)
        ax2.bar(range(len(comparison_scenarios)), counts, bottom=bottom,
                color=NAPS_COLORS[cls], label=cls, width=0.6, alpha=0.85,
                edgecolor="white", linewidth=0.8)
        bottom += np.array(counts)

    ax2.set_xticks(range(len(comparison_scenarios)))
    ax2.set_xticklabels(comp_labels, fontsize=8)
    ax2.set_ylabel("% of Channel × Industry × Size Combinations")
    ax2.set_title("Classification Distribution by Scenario",
                  fontweight="bold", pad=10)
    ax2.legend(loc="upper right", fontsize=8, framealpha=0.9)
    ax2.set_ylim(0, 105)

    fig.text(0.5, -0.03,
             "Scenario engine adjusts ADEI (disruption), AELI (efficiency), and MMI (market) multipliers.\n"
             "Source: Allocation Pressure Model (derived from IAB, SEMrush, Gartner/CMO Survey data)",
             ha="center", fontsize=7.5, color="#888888")

    plt.tight_layout()
    fig.savefig("assets/viz5_scenario_comparison.png", bbox_inches="tight")
    plt.close()
    print("  Saved assets/viz5_scenario_comparison.png")


# ================================================================
# BONUS: Channel Exposure Heatmap
# ================================================================
def viz_bonus_channel_heatmap():
    fig, ax = plt.subplots(figsize=(8, 5))

    channels_list = ["Organic Search", "Content / Blog", "Paid Search (PPC/SEM)",
                     "Digital Video", "Retail Media", "Organic Social",
                     "Paid Social", "Email"]
    intents = ["Informational", "Commercial", "Transactional", "Navigational", "Non-Search"]

    exposure_map = {
        "Organic Search":        [0.9, 0.5, 0.2, 0.3, 0.0],
        "Content / Blog":        [0.95, 0.4, 0.1, 0.1, 0.0],
        "Paid Search (PPC/SEM)": [0.3, 0.8, 0.7, 0.5, 0.0],
        "Digital Video":         [0.2, 0.2, 0.1, 0.1, 0.6],
        "Retail Media":          [0.05, 0.1, 0.3, 0.05, 0.7],
        "Organic Social":        [0.05, 0.1, 0.05, 0.05, 0.9],
        "Paid Social":           [0.0, 0.05, 0.05, 0.0, 0.95],
        "Email":                 [0.0, 0.0, 0.0, 0.0, 1.0],
    }

    data = np.array([exposure_map[ch] for ch in channels_list])

    cmap = sns.diverging_palette(145, 10, s=90, l=50, as_cmap=True)
    sns.heatmap(data, annot=True, fmt=".0%",
                xticklabels=intents, yticklabels=channels_list,
                cmap="YlOrRd", vmin=0, vmax=1,
                linewidths=1.5, linecolor="white",
                cbar_kws={"label": "Exposure Level", "shrink": 0.8},
                ax=ax)

    ax.set_title("Channel Exposure to AI-Mediated Discovery Disruption\nby Primary Query Intent Dependency",
                 fontweight="bold", pad=12, fontsize=11)
    ax.set_xlabel("Query Intent Type")
    ax.set_ylabel("")

    fig.text(0.5, -0.02,
             "High values (dark) = channel heavily depends on that query type in search. Non-Search = channel operates outside Google ecosystem.\n"
             "AI Overviews expanding from Informational → Commercial (SEMrush 2025). Channels in Non-Search column are structurally insulated.",
             ha="center", fontsize=7, color="#888888")

    plt.tight_layout()
    fig.savefig("assets/viz_bonus_channel_exposure_heatmap.png", bbox_inches="tight")
    plt.close()
    print("  Saved assets/viz_bonus_channel_exposure_heatmap.png")


# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Generating proposal visualizations...\n")
    viz1_channel_revenue()
    viz2_efficiency_gap()
    viz3_ai_overview_exposure()
    viz4_allocation_quadrant()
    viz5_scenario_shifts()
    viz_bonus_channel_heatmap()
    print("\nAll visualizations saved to assets/ folder.")
