# hplc_analysis_unbound.py

import pandas as pd
import matplotlib.pyplot as plt
import glob
import re
import numpy as np
from linear_regression import fit_linear  # your existing linear regression function

# === PARAMETERS ===
concentrations = [0, 10, 20, 40, 60]  # µg/mL
RT_MAX = 4.0  # consider all peaks up to 4 min for unbound fraction

# === FUNCTIONS ===

def extract_unbound_fraction(run_pattern, rt_max=RT_MAX):
    """
    For each CSV in run_pattern, compute:
    tallest peak area / total area (for all peaks with RetTime <= rt_max)
    """
    fractions = []
    files = sorted(glob.glob(run_pattern), key=lambda f: int(re.search(r'conc(\d+)', f).group(1)))
    print(f"Files for pattern {run_pattern}: {files}")
    for f in files:
        df = pd.read_csv(f)
        filtered = df[df['RetTime [min]'] <= rt_max]
        if not filtered.empty:
            tallest = filtered['Area [mAU * s]'].max()
            total = filtered['Area [mAU * s]'].sum()
            frac = tallest / total if total > 0 else 0.0
        else:
            frac = 0.0
        fractions.append(frac)
    return np.array(fractions, dtype=float)

# === EXTRACT DATA ===
unbound_run1 = extract_unbound_fraction("HPLC_Run1_conc*.csv")
unbound_run2 = extract_unbound_fraction("HPLC_Run2_conc*.csv")

# Sanity check
if len(unbound_run1) != len(concentrations) or len(unbound_run2) != len(concentrations):
    raise ValueError("Mismatch: number of files vs number of concentrations.")

# === AVERAGE RUNS ===
avg_unbound = (unbound_run1 + unbound_run2) / 2.0

# === LINEAR FIT ===
m, b, r2 = fit_linear(concentrations, avg_unbound)

# === OUTPUT RESULTS ===
print("\n--- RESULTS ---")
print("Unbound Run1:", unbound_run1)
print("Unbound Run2:", unbound_run2)
print("Average Unbound Fraction:", avg_unbound)
print(f"Slope = {m:.4f}, Intercept = {b:.4f}, R² = {r2:.4f}")

# === PLOT ===
plt.figure(figsize=(8,5))
plt.scatter(concentrations, unbound_run1, label="Run 1", color="orange")
plt.scatter(concentrations, unbound_run2, label="Run 2", color="blue")
plt.scatter(concentrations, avg_unbound, label="Average", color="green", marker='x', s=80)
x_vals = sorted(concentrations)
plt.plot(x_vals, [m*x + b for x in x_vals], '--', color='red', label="Fit (average)")
plt.xlabel("Concentration (µg/mL)")
plt.ylabel("Unbound Fraction (tallest peak / total area ≤ 4 min)")
plt.title("Unbound Fraction Calibration Curve")
plt.legend()
plt.tight_layout()
plt.show()
