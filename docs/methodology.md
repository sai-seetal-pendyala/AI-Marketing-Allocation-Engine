# Methodology

---

## Analytical approach

The project does not build a predictive model. It builds a **decision framework** that integrates three public-data signals -- market momentum, AI efficiency leverage, and AI discovery exposure -- into a composite allocation score for each marketing channel.

The choice to use composite indexing rather than regression or classification modeling is deliberate. The underlying data comes from different sources at different granularities (IAB annual revenue, SEMrush monthly keyword data, Gartner/CMO Survey point-in-time metrics). There is no common unit of observation that would support a unified statistical model. Instead, the framework normalizes each signal to a 0--100 scale, combines them with transparent weighting, and lets the user adjust assumptions through scenario parameters.

This produces directional pressure classifications (Scale/Test/Hold/Reduce), not point estimates. The output is designed for a budget meeting, not a journal submission.

---

## Index construction


| Index                               | Source                         | Formula                                                                                      | Weight in NAPS     |
| ----------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------------- | ------------------ |
| Market Momentum Index (MMI)         | IAB/PwC 5-year channel revenue | 60% from CAGR (normalized 5--20% range), 40% from share shift                                | Positive component |
| AI Efficiency Leverage Index (AELI) | Gartner/CMO Survey             | 25% time efficiency + 25% cost efficiency + 50% outcome translation                          | Positive component |
| AI Discovery Exposure Index (ADEI)  | SEMrush AI Overviews           | 50% from AIO prevalence, 30% from intent migration velocity, 20% from search dependency flag | Negative component |


NAPS = (MMI + AELI) -- ADEI. Normalized to 0--100, then classified: Scale (75+), Test (55--74), Hold (35--54), Reduce (<35).

The 50% weight on outcome translation in AELI is the most consequential design choice. It penalizes channels where AI produces faster output but does not improve business results -- which is the central thesis of the project.

---

## Assumptions and limitations

**Data limitations:**

- IAB reports are annual aggregates. They show where money flows but not whether it flows profitably.
- SEMrush data covers 10M+ keywords but is published as monthly aggregates, not individual keyword data. Eleven months is enough for trend detection but not time-series forecasting.
- The CMO Survey has 281 respondents. Cross-tabulations by industry and company size produce small cell sizes (10--20 per cell). Patterns are directional, not statistically robust.
- CAC benchmarks from FirstPageSage are used for calibration, not as model inputs. They are based on their own client data and may not generalize.

**Framework limitations:**

- The weighting of MMI vs. AELI vs. ADEI involves subjective choices. A different weighting scheme would produce different classifications for borderline channels.
- Scenario variants use fixed multipliers (e.g., 1.5x for "High AI Disruption"). Real-world disruption does not scale linearly.
- The framework treats each channel independently. In reality, reallocating budget from Reduce channels to Scale channels affects competitive dynamics in those channels.

---

## With more time and data

1. **Add channel-level AI efficiency data.** The CMO Survey reports efficiency gains at the function level, not the channel level. Channel-specific AI ROI data would sharpen the AELI score.
2. **Incorporate CTR and conversion rate data** from Google Search Console and analytics platforms to validate the ADEI scores against actual performance metrics.
3. **Build a Bayesian updating mechanism** that adjusts the index weights based on observed allocation outcomes -- channels classified as Scale that underperform should reduce the MMI weight; channels classified as Reduce that outperform should reduce the ADEI weight.
4. **Extend the scenario engine** to model competitive dynamics: if 60% of advertisers shift budget from search to social, social CPMs rise and the Scale classification weakens.
5. **Add a temporal dimension** to the scenario model so users can project NAPS scores 6--12 months forward based on trend extrapolation from SEMrush and IAB data.

