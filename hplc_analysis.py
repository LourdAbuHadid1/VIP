import pandas as pd
import matplotlib.pyplot as plt
from linear_regression import fit_linear
import glob
import re

# Adjust RT window to match acetaminophen peak
RT_MIN = 2.4
RT_MAX = 2.6
concentrations = [0, 10, 20, 40, 60]  # µg/mL

def extract_areas(run_pattern):
    areas = []

    # Get all matching files
    files = glob.glob(run_pattern)
    if not files:
        print("No files found with pattern:", run_pattern)
        return []

    # Sort files by the concentration number in the filename
    def extract_number(filename):
        match = re.search(r'conc(\d+)', filename)
        return int(match.group(1)) if match else -1

    files = sorted(files, key=extract_number)
    print("Files found (sorted):", files)

    for f in files:
        df = pd.read_csv(f)
        # Filter peaks inside the RT window for acetaminophen
        filtered = df[(df['RetTime [min]'] >= RT_MIN) & (df['RetTime [min]'] <= RT_MAX)]
        if not filtered.empty:
            area = filtered['Area [mAU * s]'].iloc[0]
        else:
            area = 0  # handle missing peak
        areas.append(area)

    return areas

areas_run1 = extract_areas("HPLC_Run1_conc*.csv")
print("Extracted areas:", areas_run1)
print("Number of areas:", len(areas_run1))

if len(areas_run1) != len(concentrations):
    raise ValueError("Number of areas does not match number of concentrations!")

m, b, r2 = fit_linear(concentrations, areas_run1)

print("\n--- Run 1 ---")
print(f"Slope: {m:.4f}, Intercept: {b:.4f}, R²: {r2:.4f}")

plt.figure(figsize=(8,5))
plt.scatter(concentrations, areas_run1, label="Run 1 Data", color="blue")
x_vals = sorted(concentrations)
plt.plot(x_vals, [m*x + b for x in x_vals], '--', color='red', label="Run 1 Fit")
plt.xlabel("Concentration (µg/mL)")
plt.ylabel("Peak Area (mAU·s)")
plt.title("Calibration Curve - Acetaminophen (Run 1)")
plt.legend()
plt.tight_layout()
plt.show()
