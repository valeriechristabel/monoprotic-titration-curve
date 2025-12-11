# # import numpy as np
# # import matplotlib.pyplot as plt

# # def acid_base_titration(conc_analyte, vol_analyte, conc_titrant, max_vol_titrant=100, points=200,
# #                         analyte_type="strong_acid", titrant_type="strong_base", Ka=None, Kb=None):
# #     """
# #     General acid-base titration simulator.
# #     analyte_type: "strong_acid", "weak_acid", "strong_base", "weak_base"
# #     titrant_type: "strong_base" or "strong_acid"
# #     Ka: required for weak acids
# #     Kb: required for weak bases
# #     """
# #     volumes = np.linspace(0, max_vol_titrant, points)
# #     pH_values = []
# #     moles_analyte = conc_analyte * (vol_analyte/1000)

# #     for v in volumes:
# #         moles_titrant = conc_titrant * (v/1000)
# #         total_vol = (vol_analyte + v)/1000

# #         # Strong acid vs strong base
# #         if analyte_type == "strong_acid" and titrant_type == "strong_base":
# #             if moles_analyte > moles_titrant:
# #                 conc_H = (moles_analyte - moles_titrant) / total_vol
# #                 pH = -np.log10(conc_H)
# #             elif moles_titrant > moles_analyte:
# #                 conc_OH = (moles_titrant - moles_analyte) / total_vol
# #                 pOH = -np.log10(conc_OH)
# #                 pH = 14 - pOH
# #             else:
# #                 pH = 7.0

# #         # Strong base vs strong acid
# #         elif analyte_type == "strong_base" and titrant_type == "strong_acid":
# #             if moles_analyte > moles_titrant:
# #                 conc_OH = (moles_analyte - moles_titrant) / total_vol
# #                 pOH = -np.log10(conc_OH)
# #                 pH = 14 - pOH
# #             elif moles_titrant > moles_analyte:
# #                 conc_H = (moles_titrant - moles_analyte) / total_vol
# #                 pH = -np.log10(conc_H)
# #             else:
# #                 pH = 7.0

# #         # Weak acid vs strong base
# #         elif analyte_type == "weak_acid" and titrant_type == "strong_base":
# #             if moles_titrant < moles_analyte:  # buffer region
# #                 ratio = moles_titrant / (moles_analyte - moles_titrant) if moles_titrant > 0 else 0.0001
# #                 pH = -np.log10(Ka) + np.log10(ratio)
# #             elif moles_titrant == moles_analyte:  # equivalence
# #                 conc_A_minus = moles_titrant / total_vol
# #                 Kb = 1e-14 / Ka
# #                 OH = np.sqrt(Kb * conc_A_minus)
# #                 pOH = -np.log10(OH)
# #                 pH = 14 - pOH
# #             else:  # after equivalence
# #                 excess_OH = (moles_titrant - moles_analyte) / total_vol
# #                 pOH = -np.log10(excess_OH)
# #                 pH = 14 - pOH

# #         # Weak base vs strong acid
# #         elif analyte_type == "weak_base" and titrant_type == "strong_acid":
# #             if moles_titrant < moles_analyte:  # buffer region
# #                 ratio = (moles_analyte - moles_titrant) / moles_titrant if moles_titrant > 0 else 1000
# #                 pOH = -np.log10(Kb) + np.log10(ratio)
# #                 pH = 14 - pOH
# #             elif moles_titrant == moles_analyte:  # equivalence
# #                 conc_BH_plus = moles_titrant / total_vol
# #                 Ka = 1e-14 / Kb
# #                 H = np.sqrt(Ka * conc_BH_plus)
# #                 pH = -np.log10(H)
# #             else:  # after equivalence
# #                 excess_H = (moles_titrant - moles_analyte) / total_vol
# #                 pH = -np.log10(excess_H)

# #         else:
# #             pH = 7.0

# #         pH_values.append(pH)

# #     return volumes, np.array(pH_values)

# # # --- Example Usage ---
# # atype = input("Enter analyte type (strong_acid, weak_acid, strong_base, weak_base): ").strip()
# # ttype = input("Enter titrant type (strong_base or strong_acid): ").strip()
# # conc_analyte = float(input("Enter analyte concentration (M): "))
# # vol_analyte = float(input("Enter analyte volume (mL): "))
# # conc_titrant = float(input("Enter titrant concentration (M): "))

# # Ka = None
# # Kb = None
# # if atype == "weak_acid":
# #     Ka = float(input("Enter Ka value for weak acid: "))
# # elif atype == "weak_base":
# #     Kb = float(input("Enter Kb value for weak base: "))

# # volumes, pH_values = acid_base_titration(conc_analyte, vol_analyte, conc_titrant,
# #                                          analyte_type=atype, titrant_type=ttype, Ka=Ka, Kb=Kb)



# # plt.figure(figsize=(8,6))
# # plt.plot(volumes, pH_values, label=f"{atype} vs {ttype}")
# # plt.axhline(7, color='gray', linestyle='--', label="Neutral pH")
# # plt.xlabel("Volume of titrant added (mL)")
# # plt.ylabel("pH")
# # plt.title("pH Titration Curve Simulator")
# # plt.legend()
# # plt.grid(True)
# # plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# from matplotlib.cm import get_cmap

# def acid_base_titration(conc_analyte, vol_analyte, conc_titrant, max_vol_titrant=100, points=200,
#                         analyte_type="strong_acid", titrant_type="strong_base", Ka=None, Kb=None):
#     volumes = np.linspace(0, max_vol_titrant, points)
#     pH_values = []
#     moles_analyte = conc_analyte * (vol_analyte/1000)

#     for v in volumes:
#         moles_titrant = conc_titrant * (v/1000)
#         total_vol = (vol_analyte + v)/1000

#         # Strong acid vs strong base
#         if analyte_type == "strong_acid" and titrant_type == "strong_base":
#             if moles_analyte > moles_titrant:
#                 conc_H = (moles_analyte - moles_titrant) / total_vol
#                 pH = -np.log10(conc_H)
#             elif moles_titrant > moles_analyte:
#                 conc_OH = (moles_titrant - moles_analyte) / total_vol
#                 pOH = -np.log10(conc_OH)
#                 pH = 14 - pOH
#             else:
#                 pH = 7.0

#         # Strong base vs strong acid
#         elif analyte_type == "strong_base" and titrant_type == "strong_acid":
#             if moles_analyte > moles_titrant:
#                 conc_OH = (moles_analyte - moles_titrant) / total_vol
#                 pOH = -np.log10(conc_OH)
#                 pH = 14 - pOH
#             elif moles_titrant > moles_analyte:
#                 conc_H = (moles_titrant - moles_analyte) / total_vol
#                 pH = -np.log10(conc_H)
#             else:
#                 pH = 7.0

#         # Weak acid vs strong base
#         elif analyte_type == "weak_acid" and titrant_type == "strong_base":
#             if moles_titrant < moles_analyte:  # buffer region
#                 ratio = moles_titrant / (moles_analyte - moles_titrant) if moles_titrant > 0 else 0.0001
#                 pH = -np.log10(Ka) + np.log10(ratio)
#             elif moles_titrant == moles_analyte:  # equivalence
#                 conc_A_minus = moles_titrant / total_vol
#                 Kb = 1e-14 / Ka
#                 OH = np.sqrt(Kb * conc_A_minus)
#                 pOH = -np.log10(OH)
#                 pH = 14 - pOH
#             else:  # after equivalence
#                 excess_OH = (moles_titrant - moles_analyte) / total_vol
#                 pOH = -np.log10(excess_OH)
#                 pH = 14 - pOH

#         # Weak base vs strong acid
#         elif analyte_type == "weak_base" and titrant_type == "strong_acid":
#             if moles_titrant < moles_analyte:  # buffer region
#                 ratio = (moles_analyte - moles_titrant) / moles_titrant if moles_titrant > 0 else 1000
#                 pOH = -np.log10(Kb) + np.log10(ratio)
#                 pH = 14 - pOH
#             elif moles_titrant == moles_analyte:  # equivalence
#                 conc_BH_plus = moles_titrant / total_vol
#                 Ka = 1e-14 / Kb
#                 H = np.sqrt(Ka * conc_BH_plus)
#                 pH = -np.log10(H)
#             else:  # after equivalence
#                 excess_H = (moles_titrant - moles_analyte) / total_vol
#                 pH = -np.log10(excess_H)

#         else:
#             pH = 7.0

#         pH_values.append(pH)

#     return volumes, np.array(pH_values)

# # --- Example Usage ---
# atype = "weak_base"
# ttype = "strong_acid"
# conc_analyte = 0.1
# vol_analyte = 50
# conc_titrant = 0.1
# Kb = 1e-4

# volumes, pH_values = acid_base_titration(conc_analyte, vol_analyte, conc_titrant,
#                                          analyte_type=atype, titrant_type=ttype, Kb=Kb)

# # --- Plot Enhancements ---
# fig, ax = plt.subplots(figsize=(9,7))

# # Scatter plot with color-coded pH
# sc = ax.scatter(volumes, pH_values, c=pH_values, cmap='RdYlBu_r', s=20, label=f"{atype} vs {ttype}")

# # Equivalence point marker
# dpH = np.gradient(pH_values)
# eq_index = np.argmax(np.abs(dpH))
# eq_volume = volumes[eq_index]
# eq_pH = pH_values[eq_index]
# ax.axvline(eq_volume, color='purple', linestyle='--', label="Equivalence Point")
# ax.scatter(eq_volume, eq_pH, color='black', zorder=5)

# # Neutral line
# ax.axhline(7, color='gray', linestyle='--', label="Neutral pH")

# # Colorbar attached to scatter
# cbar = plt.colorbar(sc, ax=ax)
# cbar.set_label('pH Scale')

# # Annotations
# ax.text(eq_volume/2, 9, "Buffer Region", fontsize=10, color="darkgreen")
# ax.text(eq_volume, eq_pH+0.5, "Equivalence Point", fontsize=10, color="purple")
# ax.text(eq_volume+20, 3, "Excess Acid", fontsize=10, color="red")

# # Labels
# ax.set_xlabel("Volume of titrant added (mL)")
# ax.set_ylabel("pH")
# ax.set_title("Enhanced pH Titration Curve Simulator")
# ax.legend()
# ax.grid(True)

# plt.show()

import numpy as np
import matplotlib.pyplot as plt

def acid_base_titration(conc_analyte, vol_analyte, conc_titrant, max_vol_titrant=100, points=200,
                        analyte_type="strong_acid", titrant_type="strong_base", Ka=None, Kb=None):
    volumes = np.linspace(0, max_vol_titrant, points)
    pH_values = []
    moles_analyte = conc_analyte * (vol_analyte/1000)

    for v in volumes:
        moles_titrant = conc_titrant * (v/1000)
        total_vol = (vol_analyte + v)/1000

        # Strong acid vs strong base
        if analyte_type == "strong_acid" and titrant_type == "strong_base":
            if moles_analyte > moles_titrant:
                conc_H = (moles_analyte - moles_titrant) / total_vol
                pH = -np.log10(conc_H)
            elif moles_titrant > moles_analyte:
                conc_OH = (moles_titrant - moles_analyte) / total_vol
                pOH = -np.log10(conc_OH)
                pH = 14 - pOH
            else:
                pH = 7.0

        # Strong base vs strong acid
        elif analyte_type == "strong_base" and titrant_type == "strong_acid":
            if moles_analyte > moles_titrant:
                conc_OH = (moles_analyte - moles_titrant) / total_vol
                pOH = -np.log10(conc_OH)
                pH = 14 - pOH
            elif moles_titrant > moles_analyte:
                conc_H = (moles_titrant - moles_analyte) / total_vol
                pH = -np.log10(conc_H)
            else:
                pH = 7.0

        # Weak acid vs strong base
        elif analyte_type == "weak_acid" and titrant_type == "strong_base":
            if moles_titrant < moles_analyte:  # buffer region
                ratio = moles_titrant / (moles_analyte - moles_titrant) if moles_titrant > 0 else 0.0001
                pH = -np.log10(Ka) + np.log10(ratio)
            elif moles_titrant == moles_analyte:  # equivalence
                conc_A_minus = moles_titrant / total_vol
                Kb = 1e-14 / Ka
                OH = np.sqrt(Kb * conc_A_minus)
                pOH = -np.log10(OH)
                pH = 14 - pOH
            else:  # after equivalence
                excess_OH = (moles_titrant - moles_analyte) / total_vol
                pOH = -np.log10(excess_OH)
                pH = 14 - pOH

        # Weak base vs strong acid
        elif analyte_type == "weak_base" and titrant_type == "strong_acid":
            if moles_titrant < moles_analyte:  # buffer region
                ratio = (moles_analyte - moles_titrant) / moles_titrant if moles_titrant > 0 else 1000
                pOH = -np.log10(Kb) + np.log10(ratio)
                pH = 14 - pOH
            elif moles_titrant == moles_analyte:  # equivalence
                conc_BH_plus = moles_titrant / total_vol
                Ka = 1e-14 / Kb
                H = np.sqrt(Ka * conc_BH_plus)
                pH = -np.log10(H)
            else:  # after equivalence
                excess_H = (moles_titrant - moles_analyte) / total_vol
                pH = -np.log10(excess_H)

        else:
            pH = 7.0

        pH_values.append(pH)

    return volumes, np.array(pH_values)

# --- Interactive User Input ---
atype = input("Enter analyte type (strong_acid, weak_acid, strong_base, weak_base): ").strip()
ttype = input("Enter titrant type (strong_base or strong_acid): ").strip()
conc_analyte = float(input("Enter analyte concentration (M): "))
vol_analyte = float(input("Enter analyte volume (mL): "))
conc_titrant = float(input("Enter titrant concentration (M): "))

Ka = None
Kb = None
if atype == "weak_acid":
    Ka = float(input("Enter Ka value for weak acid: "))
elif atype == "weak_base":
    Kb = float(input("Enter Kb value for weak base: "))

volumes, pH_values = acid_base_titration(conc_analyte, vol_analyte, conc_titrant,
                                         analyte_type=atype, titrant_type=ttype, Ka=Ka, Kb=Kb)

# --- Plot Enhancements ---
fig, ax = plt.subplots(figsize=(9,7))

# Scatter plot with color-coded pH
sc = ax.scatter(volumes, pH_values, c=pH_values, cmap='RdYlBu_r', s=20, label=f"{atype} vs {ttype}")

# Equivalence point marker
dpH = np.gradient(pH_values)
eq_index = np.argmax(np.abs(dpH))
eq_volume = volumes[eq_index]
eq_pH = pH_values[eq_index]
ax.axvline(eq_volume, color='purple', linestyle='--', label="Equivalence Point")
ax.scatter(eq_volume, eq_pH, color='black', zorder=5)

# Neutral line
ax.axhline(7, color='gray', linestyle='--', label="Neutral pH")

# Colorbar attached to scatter
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('pH Scale')

# Annotations
ax.text(eq_volume/2, max(pH_values)-2, "Buffer Region", fontsize=10, color="darkgreen")
ax.text(eq_volume, eq_pH+0.5, "Equivalence Point", fontsize=10, color="purple")
ax.text(eq_volume+20, min(pH_values)+1, "Excess Titrant", fontsize=10, color="red")

# Labels
ax.set_xlabel("Volume of titrant added (mL)")
ax.set_ylabel("pH")
ax.set_title("Interactive pH Titration Curve Simulator")
ax.legend()
ax.grid(True)

plt.show()