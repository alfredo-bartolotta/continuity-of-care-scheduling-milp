
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ----------------------------
# CONFIG: cambia SOLO qui
# ----------------------------
BASE_PATH = r"C:\Users\alfri\OneDrive\Desktop\Tesi\Fico Xpress"
RUN = "8"  # cambia qui il run 

SLOTS_PER_DAY = 12
N_DAYS = 5

# Scegli quali scenari visualizzare (1, 2 o 3)
# - Solo uno: ["A"]
# - Solo due: ["A", "C"]
# - Tutti e tre: ["A", "B", "C"]
SELECTED = ["A", "B", "C"]

# ----------------------------
# File per scenario (stesso RUN)
# ----------------------------
scenario_def = {
    "A": ("Scenario A – CoC manual", f"sol_A_CoCmanual_P100_T10_R4_M4_D5_S12_{RUN}.dat.csv"),
    "B": ("Scenario B – No CoC",      f"sol_B_noCoC_P100_T10_R4_M4_D5_S12_{RUN}.dat.csv"),
    "C": ("Scenario C – CoC total",  f"sol_C_CoCall_P100_T10_R4_M4_D5_S12_{RUN}.dat.csv"),
}

# Colori per session_type
colors = {1: '#3498db', 2: '#e74c3c'}

def load_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    # Normalizza nome colonna terapista se nel file è "Terapist"
    if "Therapist" not in df.columns and "Terapist" in df.columns:
        df = df.rename(columns={"Terapist": "Therapist"})

    needed = ["Patients", "Therapist", "session_type", "Day", "Time_slot"]
    for c in needed:
        if c not in df.columns:
            raise ValueError(f"Colonna mancante nel file {os.path.basename(path)}: '{c}'")
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=needed)
    df[needed] = df[needed].astype(int)
    return df

def plot_gantt_patients(ax, df, title):
    patients = sorted(df["Patients"].unique())

    for _, row in df.iterrows():
        y = patients.index(row["Patients"])
        x = (row["Day"] - 1) * SLOTS_PER_DAY + row["Time_slot"]
        ax.barh(
            y, width=0.8, left=x, height=0.6,
            color=colors.get(row["session_type"], "#7f8c8d"),
            edgecolor="black", linewidth=0.5
        )

    ax.set_yticks(range(len(patients)))
    ax.set_yticklabels([f"P{p}" for p in patients], fontsize=7)
    ax.set_xlabel("Time (Day × Slot)")
    ax.set_ylabel("Patients")
    ax.set_title(title, fontsize=12, fontweight="bold")

    for d in range(1, N_DAYS + 1):
        ax.axvline(x=d*SLOTS_PER_DAY + 0.5, color="gray", linestyle="--", alpha=0.4)
        ax.text(d*SLOTS_PER_DAY - (SLOTS_PER_DAY/2), len(patients) + 0.6, f"Day {d}",
                ha="center", fontsize=8)

    ax.set_xlim(0, N_DAYS*SLOTS_PER_DAY + 1)
    ax.set_ylim(-0.5, len(patients) + 1.0)

def plot_gantt_therapists(ax, df, title):
    therapists = sorted(df["Therapist"].unique())

    for _, row in df.iterrows():
        y = therapists.index(row["Therapist"])
        x = (row["Day"] - 1) * SLOTS_PER_DAY + row["Time_slot"]
        ax.barh(
            y, width=0.8, left=x, height=0.6,
            color=colors.get(row["session_type"], "#7f8c8d"),
            edgecolor="black", linewidth=0.5
        )

    ax.set_yticks(range(len(therapists)))
    ax.set_yticklabels([f"T{t}" for t in therapists], fontsize=9)
    ax.set_xlabel("Time (Day × Slot)")
    ax.set_ylabel("Physiotherapists")
    ax.set_title(title, fontsize=12, fontweight="bold")

    for d in range(1, N_DAYS + 1):
        ax.axvline(x=d*SLOTS_PER_DAY + 0.5, color="gray", linestyle="--", alpha=0.4)
        ax.text(d*SLOTS_PER_DAY - (SLOTS_PER_DAY/2), len(therapists) + 0.2, f"Day {d}",
                ha="center", fontsize=8)

    ax.set_xlim(0, N_DAYS*SLOTS_PER_DAY + 1)
    ax.set_ylim(-0.5, len(therapists) + 0.6)

# ----------------------------
# Carica i dataset selezionati
# ----------------------------
data = {}
for code in SELECTED:
    if code not in scenario_def:
        raise ValueError(f"Codice scenario non valido in SELECTED: '{code}'. Usa solo A, B, C.")
    scen_title, filename = scenario_def[code]
    path = os.path.join(BASE_PATH, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File non trovato per '{scen_title}':\n{path}")
    data[scen_title] = load_df(path)

# ----------------------------
# Plot: n righe (scenari) x 2 colonne (pazienti, terapisti)
# ----------------------------
n = len(data)
fig, axes = plt.subplots(n, 2, figsize=(18, 5*n), constrained_layout=True)

# se n==1, axes non è una matrice 2D: lo normalizzo
if n == 1:
    axes = np.array([axes])

if n == 1:
    fig.suptitle(f"{list(data.keys())[0]} – Run {RUN}", fontsize=18, fontweight="bold")
else:
    fig.suptitle(f"Confronto scenari – Run {RUN}", fontsize=18, fontweight="bold")

for row_idx, (scen_title, df) in enumerate(data.items()):
    plot_gantt_patients(axes[row_idx, 0], df, f"{scen_title} | Patients")
    plot_gantt_therapists(axes[row_idx, 1], df, f"{scen_title} | Physiotherapists")

# Legenda comune
handles = [plt.Rectangle((0, 0), 1, 1, color=c, ec="black") for c in colors.values()]
fig.legend(handles, ["Session Type 1", "Session Type 2"],
           loc="upper center", ncol=2, fontsize=11, frameon=True)

# Salvataggio
sel_str = "".join(SELECTED)
out_name = f"gantt_{sel_str}_run{RUN}.png"
out_path = os.path.join(BASE_PATH, out_name)
plt.savefig(out_path, dpi=150, bbox_inches="tight")
plt.show()

print(f" Figura salvata: {out_path}")