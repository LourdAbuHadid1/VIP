# Make sure that the CSV has the expected columns:
#"Compound Name" → to filter for acetaminophen
#"Sample Type" → to separate standards vs samples
#"Sample Name" → for total vs filtrate
#"Concentration (µg/mL)" → known concentrations of standards
#"Peak Area" → HPLC peak areas

import pandas as pd
import matplotlib.pyplot as plt
from linear_regression import fit_linear

# Step 1: Load HPLC data
data = pd.read_csv("hplc_data.csv") #change name if needed

# Step 2: Extract only pure Acetaminophen
acet_data = data[data["Compound Name"].str.strip().str.lower() == "acetaminophen"]

# Step 3: Separate standards vs. samples
standards = acet_data[acet_data["Sample Type"] == "Standard"]
samples = acet_data[acet_data["Sample Type"] != "Standard"]

# Step 4: Prepare calibration data
x = standards["Concentration (µg/mL)"].astype(float).tolist()
y = standards["Peak Area"].astype(float).tolist()

# Step 5: Fit the calibration curve
m, b, r2 = fit_linear(x, y)
print(f"Slope: {m:.4f}, Intercept: {b:.4f}, R²: {r2:.4f}")

# Step 6: Calculate concentrations for unknown samples
samples["Calculated Concentration (µg/mL)"] = (samples["Peak Area"] - b) / m

# Step 7: Compute unbound fraction and percent penetration

total = samples[samples["Sample Name"].str.contains("Total", case=False)]["Calculated Concentration (µg/mL)"].mean()
filtrate = samples[samples["Sample Name"].str.contains("Filtrate", case=False)]["Calculated Concentration (µg/mL)"].mean()

f_u = filtrate / total
penetration = f_u * 100

print(f"Unbound fraction: {f_u:.4f}")
print(f"Percent penetration: {penetration:.2f}%")

# Plot Calibrtaion Curve
plt.scatter(x, y, label="Standards")
plt.plot(x, [m*xi + b for xi in x], color='red', label="Fit")
plt.xlabel("Concentration (µg/mL)")
plt.ylabel("Peak Area")
plt.title("Calibration Curve - Acetaminophen")
plt.legend()
plt.show()
