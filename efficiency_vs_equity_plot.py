import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# CONFIG:
# ----------------------------
KPI_PATH = r"C:\Users\alfri\OneDrive\Desktop\Tesi\Fico Xpress\kpi_results.csv"

# Se vuoi filtrare una singola istanza base (lascia None per usare TUTTE le istanze nel file)
# Esempio: "P100_T10_R4_M4_D5_S12"
INSTANCE_BASE = "P100_T10_R4_M4_D5_S12"   # oppure None

# Se vuoi filtrare un run specifico (lascia None per usare TUTTI i run)
RUN = None  # es. "1" oppure None

# ----------------------------
# Load KPI file (sep=';' e senza header)
# ----------------------------
cols = [
    "scenario_name", "input_file", "obj_val", "best_bound", "gap",
    "time_s", "scheduled_patients", "pct_patients_scheduled",
    "scheduled_sessions", "requested_sessions", "pct_sessions_scheduled",
    "global_utilization", "fairness_gap_util", "cv_util"
]

df = pd.read_csv(KPI_PATH, sep=";", header=None, names=cols)

# pulizia spazi
df["scenario_name"] = df["scenario_name"].astype(str).str.strip()
df["input_file"] = df["input_file"].astype(str).str.strip()

# cast numerici
for c in cols[2:]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# tieni solo scenari validi
valid_scen = {"A_CoCmanual", "B_noCoC", "C_CoCall"}
df = df[df["scenario_name"].isin(valid_scen)].copy()

# ----------------------------
# Filtri opzionali
# ----------------------------
# filtro istanza base (prima del _run.dat)
if INSTANCE_BASE is not None:
    df = df[df["input_file"].str.startswith(INSTANCE_BASE + "_")].copy()

# filtro run (numero prima di .dat)
if RUN is not None:
    df = df[df["input_file"].str.endswith(f"_{RUN}.dat")].copy()

# estrai run per etichettare i punti (ultimo numero prima di .dat)
df["run"] = df["input_file"].str.extract(r"_(\d+)\.dat$")[0]

# ----------------------------
# Scatter: Efficienza vs Equità
# Efficienza = global_utilization (x)
# Equità = cv_util (y)  (più basso = più equo)
# ----------------------------
scenario_labels = {
    "A_CoCmanual": "Scenario A (CoC manuali)",
    "B_noCoC": "Scenario B (No CoC)",
    "C_CoCall": "Scenario C (CoC totale)"
}

# marker diversi per scenario (così anche in stampa B/N si distingue)
markers = {
    "A_CoCmanual": "o",
    "B_noCoC": "s",
    "C_CoCall": "^"
}

fig, ax = plt.subplots(figsize=(8, 6))

for scen in ["A_CoCmanual", "B_noCoC", "C_CoCall"]:
    sub = df[df["scenario_name"] == scen]
    ax.scatter(
        sub["global_utilization"],
        sub["cv_util"],
        marker=markers[scen],
        s=70,
        alpha=0.85,
        label=scenario_labels[scen]
    )

    # etichetta run vicino ai punti (opzionale)
    for _, row in sub.iterrows():
        if pd.notna(row["run"]):
            ax.text(
                row["global_utilization"] + 0.004,
                row["cv_util"] + 0.002,
                str(row["run"]),
                fontsize=8
            )

ax.set_xlabel("Efficienza operativa: Global utilization")
ax.set_ylabel("Equità: Fairness CV (utilization)  ↓ = più equo")
ax.set_title("Efficienza vs Equità (punti = run, marker = scenario)")
ax.grid(True, alpha=0.3)
ax.legend()

# (opzionale) limiti automatici un po' “morbidi”
xmin, xmax = df["global_utilization"].min(), df["global_utilization"].max()
ymin, ymax = df["cv_util"].min(), df["cv_util"].max()
ax.set_xlim(xmin - 0.03, xmax + 0.03)
ax.set_ylim(max(0, ymin - 0.03), ymax + 0.03)

plt.tight_layout()
plt.show()
