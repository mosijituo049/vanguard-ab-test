# Vanguard A/B Test — Digital Process Redesign

## Project Overview

Vanguard, a US-based investment management company, ran an A/B test from **March 15, 2017 to June 20, 2017** to evaluate whether a redesigned online process — featuring a more modern UI and timely in-context prompts — improved client completion rates compared to the traditional process.

This project analyzes the experiment data to answer the central question:

> **Did the new UI lead to higher process completion rates?**

- **Control Group**: clients used Vanguard's traditional online process
- **Test Group**: clients used the redesigned digital interface

Both groups navigated the same five-step journey: `start → step_1 → step_2 → step_3 → confirm`.

## Data Sources

Three datasets were provided (sourced from Vanguard's internal experiment data):

| Dataset | File | Description |
|---|---|---|
| Client Profiles | `df_final_demo` | Demographics: age, gender, tenure, account balance, number of accounts, calls/logons in last 6 months |
| Digital Footprints | `df_final_web_data` (pt_1 + pt_2) | Step-by-step trace of client interactions, merged into one dataset |
| Experiment Roster | `df_final_experiment_clients` | Maps each client to their assigned variation (Control / Test) |

[Add: original data source links here]

## Data Cleaning & Preparation

- Merged the two web-data parts (pt_1, pt_2) into a single chronological journey table
- Standardized column names and converted `date_time` to proper datetime format
- Mapped `process_step` to an ordinal `step_num` (start=0 → confirm=4) to detect step direction
- Derived `duration_sec` (time spent on each step) and a `transition_type` field (forward, backward, same step, skip, end of session)
- Flagged backward transitions as **errors**
- Joined the client/web data with the experiment roster on `client_id` to tag each record with its `Variation` (Control/Test)
- Removed client journey records not associated with an experiment variation (~57% of raw web logs were from clients not enrolled in the experiment)
- Missing demographic values affected under 0.03% of clients in both groups — negligible

## Key Performance Indicators (KPIs)

1. **Completion Rate** — proportion of clients reaching the `confirm` step
2. **Time Spent per Step** — average/median active time on each step (excluding error transitions)
3. **Error Rate** — proportion of step transitions that moved backward (a later step → an earlier step)

## Key Findings

### Experiment Evaluation
- **Sample size**: Control = 23,526 clients, Test = 26,961 clients (Test group ~14.6% larger — a mild deviation from a clean 50/50 split)
- **Age & tenure balance**: Control and Test groups are nearly identical in average age (~47.2–47.5 years) and tenure (~150–151 months) — randomization appears sound aside from the group-size difference
- **Gender balance**: closely matched across groups (~32% female in both)

### Completion Rate
- Control: **65.6%**
- Test: **69.3%**
- Absolute lift: **+3.7 percentage points**, statistically significant (p < 0.001, two-proportion Z-test)

### Cost-Effectiveness Threshold
- Vanguard's pre-defined threshold for a cost-justified redesign was a **5 pp lift**
- The observed lift (95% CI ≈ 2.9%–4.5%) falls **below** this threshold
- Result: statistically significant improvement, but does **not** clear the cost-effectiveness bar on its own

### Time Spent per Step
- Test group was notably **faster** on Step 1 and the Confirm step
- Test group was **slightly slower** on Step 2 (possibly due to new in-context prompts requiring more attention)
- Step 3 was roughly comparable between groups
- All step-level differences were statistically significant (t-tests, p < 0.05)

### Error Rate
- Control: ~16.6% of transitions were backward steps
- Test: ~20.0% of transitions were backward steps
- Difference statistically significant (chi-square test, p < 0.001) — the new UI may introduce some additional navigation friction despite higher overall completion

### Segmentation by Age
- All age segments improved under the new design
- Largest absolute lift: clients aged **60+** (+5.8 pp)
- Smallest lift: clients aged **40–60** (+2.2 pp), though still positive
- Clients under 40 saw a +4.8 pp lift

## Conclusion & Recommendations

The redesigned digital interface is a **directionally and statistically significant improvement**, but on completion rate alone it does not yet meet Vanguard's cost-effectiveness threshold.

**Recommendations:**
- Roll out the redesign, paired with targeted UX fixes for Step 2 and the elevated error rate, to push the lift above the 5% threshold
- Re-run or extend the experiment with an even Control/Test split and longer duration to validate results and capture seasonal effects
- Prioritize the 60+ segment in further UX testing, given the largest observed gains
- Collect additional data: session-level satisfaction/NPS scores, device/browser type, and explicit drop-off reasons

## Repository Structure

```
vanguard-ab-test/
├── notebooks/
│   ├── vanguard_ab_test.ipynb
│   ├── load_data.py
│   ├── duration_analysis.ipynb
│   ├── transition_analysis.ipynb
│   ├── funnel_analysis.ipynb
│   ├── testing_irene.ipynb
│   └── irene_tableau_prep.ipynb
├── src/
│   └── functions.py
├── data/
│   └── [cleaned/processed data exports]
├── README.md
└── requirements.txt
```

## Tools & Libraries

- **Python**: pandas, NumPy, Matplotlib, Seaborn, SciPy (hypothesis testing)
- **Tableau Public**: interactive dashboards for KPI visualization

## Tableau Dashboard

Interactive dashboards (KPI overview, demographic drill-down, and client journey funnel) are available on Tableau Public:

🔗 [Vanguard A/B Test Dashboard](https://public.tableau.com/views/VANGUARD_AB_DASHBOARD/Dashboard2?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)


## Presentation

🔗 [Project Presentation Slides](#) — *[Add Google Slides link here]*

## Authors

- Irene Fafian
- Zhiwen ??


