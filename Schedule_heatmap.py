
import glob
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

BASE_PATH = r"C:\Users\alfri\OneDrive\Desktop\Tesi\Fico Xpress"

patterns = {
    "Scenario A – CoC manual": "sol_A_CoCmanual_P100_T10_R4_M4_D5_S12_8.dat.csv",
    "Scenario B – No CoC":      "sol_B_noCoC_P100_T10_R4_M4_D5_S12_8.dat.csv",
    "Scenario C – CoC total":  "sol_C_CoCall_P100_T10_R4_M4_D5_S12_8.dat.csv",
}

def load_df(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    # cast numerici (evita problemi strani)
    for c in ["Patients", "Day", "Time_slot"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["Patients", "Day", "Time_slot"])
    df[["Patients","Day","Time_slot"]] = df[["Patients","Day","Time_slot"]].astype(int)
    return df

def make_pivot(df):
    pv = df.pivot_table(
        index="Time_slot",
        columns="Day",
        values="Patients",
        aggfunc="count",
        fill_value=0
    )
    # ordina per chiarezza
    pv = pv.sort_index().sort_index(axis=1)
    return pv

def extract_run(filename):
 
    m = re.search(r"_(\d+)\.dat\.csv$", filename)
    return m.group(1) if m else "?"

pivots = {}
run_ids = {}   # <-- IMPORTANTISSIMO: run per scenario

for title, pattern in patterns.items():
    files = sorted(glob.glob(os.path.join(BASE_PATH, pattern)))
    if not files:
        raise FileNotFoundError(f"Nessun file trovato per {title}")

    chosen = files[0]  # oppure files[-1] se vuoi l'ultimo
    run_ids[title] = extract_run(os.path.basename(chosen))
    fname = os.path.basename(chosen)

    df = load_df(chosen)
    pivots[title] = make_pivot(df)
    run_ids[title] = extract_run(fname)

    print(f"{title}: uso {fname} | run {run_ids[title]}")

# allinea assi tra scenari
all_slots = sorted(set().union(*[p.index for p in pivots.values()]))
all_days  = sorted(set().union(*[p.columns for p in pivots.values()]))

for k in pivots:
    pivots[k] = pivots[k].reindex(index=all_slots, columns=all_days, fill_value=0)

vmin = min(pv.values.min() for pv in pivots.values())
vmax = max(pv.values.max() for pv in pivots.values())

fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)

last_im = None
for ax, (title, pv) in zip(axes, pivots.items()):
    data = pv.values

    last_im = ax.imshow(
        data,
        aspect="auto",
        cmap="YlGnBu",
        vmin=vmin,
        vmax=vmax
    )

    # assi: metti i VALORI reali (giorni e slot),
    ax.set_xlabel("Day")
    ax.set_ylabel("Time slot")

    ax.set_xticks(np.arange(len(all_days)))
    ax.set_xticklabels(all_days)

    ax.set_yticks(np.arange(len(all_slots)))
    ax.set_yticklabels(all_slots)

    # griglia visibile tra celle
    ax.set_xticks(np.arange(-0.5, len(all_days), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(all_slots), 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.6)
    ax.tick_params(which="minor", bottom=False, left=False)

    # titolo con run corretto per quello scenario
    ax.set_title(f"{title}\nRun {run_ids[title]}", fontsize=11)

    # numeri leggibili (bianco se cella scura)
    mid = (vmin + vmax) / 2.0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            ax.text(
                j, i, str(val),
                ha="center", va="center",
                fontsize=8,
                color="white" if val > mid else "black"
            )

fig.colorbar(last_im, ax=axes, shrink=0.85, label="Numero di sessioni")
plt.show()