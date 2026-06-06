import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# CONFIG
# ----------------------------
KPI_PATH = r"C:\Users\alfri\OneDrive\Desktop\Tesi\Fico Xpress\kpi_results.csv"
RUN = "8"  # <-- cambia solo questo

SCEN_ORDER = ["A_CoCmanual", "B_noCoC", "C_CoCall"]

# KPI da confrontare
KPI_TO_PLOT = {
    "pct_patients_scheduled": "Patients scheduled (%)",
    "pct_sessions_scheduled": "Sessions scheduled (%)",
    "global_utilization": "Global utilization",
    "fairness_gap_util": "Fairness GAP",
    "cv_util": "Fairness GAP CV",
     "time_s": "Resolution time (s)"
}

# ----------------------------
# LOAD
# ----------------------------
cols = [
    "scenario_name", "input_file", "obj_val", "best_bound", "gap",
    "time_s", "scheduled_patients", "pct_patients_scheduled",
    "scheduled_sessions", "requested_sessions", "pct_sessions_scheduled",
    "global_utilization", "fairness_gap_util", "cv_util"
]

df = pd.read_csv(KPI_PATH, sep=";", header=None, names=cols)

# pulizia stringhe
df["scenario_name"] = df["scenario_name"].astype(str).str.strip()
df["input_file"] = df["input_file"].astype(str).str.strip()

# cast numerici
for c in cols[2:]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# ----------------------------
# FILTRO: stesso RUN
# ----------------------------
target_input = df["input_file"].str.endswith(f"_{RUN}.dat")
sub = df[target_input].copy()

# tieni solo A/B/C
sub = sub[sub["scenario_name"].isin(SCEN_ORDER)].copy()

# controllo
if len(sub) != 3:
    raise ValueError(
        f"Trovate {len(sub)} righe per run {RUN}. "
        f"Attese 3 (A, B, C)."
    )

sub["scenario_name"] = pd.Categorical(sub["scenario_name"], SCEN_ORDER, ordered=True)
sub = sub.sort_values("scenario_name")

# etichette
label_map = {
    "A_CoCmanual": "Scenario A\n(CoC manuali)",
    "B_noCoC":     "Scenario B\n(No CoC)",
    "C_CoCall":    "Scenario C\n(CoC totale)",
}
x_labels = [label_map[s] for s in sub["scenario_name"]]

# ----------------------------
# PLOT
# ----------------------------
n = len(KPI_TO_PLOT)
fig, axes = plt.subplots(1, n, figsize=(4.8*n, 4), constrained_layout=True)

if n == 1:
    axes = [axes]

for ax, (kpi, kpi_label) in zip(axes, KPI_TO_PLOT.items()):
    y = sub[kpi].values
    ax.bar(range(3), y)
    ax.set_xticks(range(3))
    ax.set_xticklabels(x_labels, fontsize=9)
    ax.set_title(kpi_label, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)

    for i, val in enumerate(y):
        ax.text(i, val, f"{val:.3f}", ha="center", va="bottom", fontsize=9)

fig.suptitle(f"Confronto KPI per scenario – Run {RUN}", fontsize=16, fontweight="bold")
plt.show()

