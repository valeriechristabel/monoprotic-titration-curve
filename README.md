# Project — Interactive Monoprotic Acid‑Base Titration Simulator

## Summary

This repository contains an interactive Python program that simulates and visualizes monoprotic acid–base titration curves, where both the analyte and the titrant participate in single-proton acid-base reaction. So it assumes a 1:1 stoichiometric relationship between acid and base. Polyprotic aics, polybasic bases, and titrants that release multiple protons or hydroxide ions per formula unit are not modeled. 

The app computes pH as titrant volume is added to an analyte and provides an interactive Matplotlib-based UI (sliders, radio buttons, color map) so users can explore titrations of strong and weak acids and bases.

Key features
- Simulates titration curves for combinations of monoprotic strong/weak acids and strong/weak bases.
- Interactive UI: analyte/titrant selection, concentration/volume sliders, Ka/Kb (log scale) sliders, reset button.
- Color-coded scatter plot of pH vs titrant volume and optional pH=7 guide line.
- Numerical safeguards are implemented to ensure stable and physically meaningful pH calculations. These include protection against taking logarithms of zero, avoiding division by zero in buffer equations, constraining calculated pH values to the realistic range of 0–14, and maintaining smooth behavior near equivalence points where concentrations become extremely small.
---

## Contents

- `titration.py` — the main Python script that performs the pH calculations and launches the interactive titration simulator.
  - `acid_base_titration(...)`: implements the chemical equations and numerical methods used to calculate pH during titration. It calculates the moles of acid and base, determines whether the system is before, at, or after the equivalence point, and computes pH using strong acid–strong base formulas, the Henderson–Hasselbalch equation for weak acid/base buffer regions, and hydrolysis equations at the equivalence point.
  - `make_titration_app()`: builds the interactive visualization, including the pH–volume plot and user interface controls such as sliders, radio buttons, and a reset button.
- `README.md` — documentation describing the principles, usage, program structure, limitations, and enhancements of the program.

---

## Principles and Functions of the Program 

This program implements approximate acid–base titration calculations using stoichiometry and classical acid–base equilibrium approximations. The code covers four principal analyte/titrant cases:

- Strong acid titrated with strong base
- Strong base titrated with strong acid
- Weak acid titrated with strong base
- Weak base titrated with strong acid

Chemical principles and equations used:

1. Neutralization (strong acid + strong base, instantaneous):
   - Example: HCl + NaOH → NaCl + H2O
   - Moles of H+ (from strong acid) and OH− (from strong base) react 1:1. After reaction, excess [H+] or [OH−] is computed by dividing excess moles by total solution volume.
   - pH = −log10([H+]) for acidic excess.
   - pOH = −log10([OH−]); pH = 14 − pOH for basic excess.
   - At exact stoichiometric equivalence pH ≈ 7.0 (assuming Kw = 1×10−14, T ≈ 25 °C).

2. Weak acid (HA) titration with strong base:
   - HA ⇌ H+ + A−
   - Ka = [H+][A−]/[HA]
   - Buffer region (before equivalence) is modeled using Henderson–Hasselbalch:
     - pH = pKa + log10([A−]/[HA]) where [A−] formed = moles_titrant; [HA] remaining = moles_initial − moles_titrant
   - At equivalence (weak acid titrated by strong base), the conjugate base (A−) hydrolyzes:
     - A− + H2O ⇌ HA + OH−, Kb = Kw / Ka
     - [OH−] ≈ sqrt(Kb × [A−]) (approximation used by the code)
     - pH = 14 − pOH where pOH = −log10([OH−])
  - After equivalence 
    - [OH−]= mole excess/total volume
    - pH = 14 − pOH where pOH = −log10([OH−])

3. Weak base (B) titration with strong acid:
   - B + H+ ⇌ BH+
   - Use analogous Henderson–Hasselbalch for pOH:
     - pOH = pKb + log10([B]/[BH+])
   - At equivalence BH+ hydrolyzes to produce H+:
     - BH+ ⇌ B + H+, Ka_eff = Kw / Kb
     - [H+] ≈ sqrt(Ka_eff × [BH+]) → pH = −log10([H+]) (approximation)
  - After equivalence, excess H+ from titrant dominates:
    - [H+] = mole excess/total volume 
    - pH = −log10([H+])

4. Same-type combinations (analyte and titrant both acidic or both basic) (is not part of the real chemistry titration, to prevent errors only):
   - The code gracefully handles adding strong acids to acid solutions or strong bases to base solutions by summing contributions to [H+] or [OH−] using simple approximations:
     - For acids: total [H+] ≈ [H+ from weak/strong analyte] + [H+ from added titrant]
     - For bases: total [OH−] similarly aggregated.

Numerical measures and safeguards:
- All logs use a helper clamp `safe_log10(x)` that prevents computing log(0) by clamping the argument to a small positive floor (1e−20).
- pH values are clipped to [0, 14] for display stability.
- Equivalence tests use a small tolerance for floating point comparisons.

Approximations / assumptions
- Ideal solution behavior (no activity coefficients).
- Mono‑protic acids/bases only.
- Temperature fixed at ~25 °C; Kw assumed ≈ 1×10−14.
- No ionic strength corrections.
- Approximations like Henderson–Hasselbalch and sqrt-based hydrolysis estimates are used rather than full numerical equilibrium solutions (see Limitations & Improvements).

---

## How to Use It 

Prerequisites
- Python 3.8+ (recommended)
- NumPy
- Matplotlib

Install dependencies (example)
- pip install numpy matplotlib

Run the interactive app
- From the repository directory:
  - python titration.py
  - (or) python3 titration.py

UI controls
- Radio buttons (left): select analyte type (strong_acid, weak_acid, strong_base, weak_base).
- Radio buttons (left, below): select titrant type (strong_base or strong_acid).
- Sliders (bottom/right):
  - Analyte Conc (M): initial concentration of the analyte (molarity).
  - Analyte Vol (mL): starting volume of the analyte (mL).
  - Titrant Conc (M): concentration of titrant.
  - log10(Ka) and log10(Kb): pKa/pKb controls (appear only when relevant).
- Reset button: returns all sliders and selections to their initial defaults.
- The plotted curve updates immediately as you move sliders or change analyte/titrant types.
- Colorbar indicates pH value for each point on the titration curve.

Example scenarios to try
- Strong acid (0.1 M HCl, 50 mL) titrated with 0.1 M NaOH.
- Weak acid (pKa ≈ 5) at 0.10 M, 50 mL, titrated with 0.10 M strong base: see buffer region and equivalence pH > 7.
- Weak base titrated with strong acid: pH starts >7 and approaches lower pH after equivalence.

---

## Program Architecture

The code is structured in two main layers:

1. Calculation layer
- Function: acid_base_titration(conc_analyte, vol_analyte_ml, conc_titrant, analyte_type, titrant_type, Ka, Kb, v_min, v_max, n_points)
  - Inputs: concentrations (M), volumes (mL), Ka/Kb, analyte/titrant types, and plotting range/resolution.
  - Outputs: (volumes_array, pH_array)
  - Responsibilities:
    - Compute initial moles of analyte.
    - Iterate over titrant volumes and compute added moles.
    - Select the correct chemical formula depending on analyte/titrant type (strong/weak).
    - Compute pH using: strong acid/base formula, Henderson–Hasselbalch equation, or hydrolysis at equivalence.
    - Apply numeric safeguards for stability.

2. UI & Visualization layer
- Function: make_titration_app()
  - Builds Matplotlib figure and axes, scatter plot and line plot, colorbar.
  - Adds interactive widgets (Slider, radio buttons, reset button). 
  - Updates the plot dynamically when user changes inputs.
  -Manages dynamic visibility of Ka/Kb sliders depending on analyte/titrant type

Separation of concerns
- The calculation function is pure (no plotting) so it can be reused or tested independently.
- UI code is responsible for user interaction and presentation.

---

## Development Process

- Goal: Develop an educational, interactive titration simulator that is simple to run, visually intuitive, and allows exploration of different monoprotic acid–base systems.

- Initial implementation:
  - The program started as a basic calculation tool with manual input/output. Users had to enter concentrations, volumes, and analyte/titrant types each time.  
  - This produced correct strong/strong titration curves, but repeatedly entering values was inefficient and cumbersome.  

- Enhancing interactivity: 
  - To make the program more user-friendly, sliders were introduced for analyte concentration, volume, and titrant concentration, allowing dynamic adjustment without restarting the program.  
  - For weak acids and bases, Ka/Kb sliders(logarithmic scale) were added, enabling quick exploration of different acid/base strengths.  

- Adding chemical realism: 
  - Implemented Henderson–Hasselbalch equation  for buffer regions before equivalence: directly relates pH to the ratio ([A−]/[HA]) or ([B]/[BH+])
  - At equivalence, used the hydrolysis approximation [OH−] ≈ sqrt(Kb × [A−]) or [H+] ≈ sqrt(Kb × [BH+]) to compute pH from conjugate species.  

- Numerical challenges and resolutions: 
  - Logarithm of zero errors when pH is extremely high or low: solved by implementing `safe_log10` with clamping to 1×10⁻²⁰.  
  - Exact equivalence detection: small tolerance values used to identify equivalence point reliably.  
  - Performance issues with large data points: optimized updates by mutating scatter and line plot objects instead of redrawing everything.  
  - Same-type additions (acid+acid or base+base) were handled using a simple additive approximation for [H⁺] or [OH⁻] to avoid crashes and maintain reasonable outputs.

- UI polishing and visualization:  
  - Ka/Kb sliders are logarithmic because these constants span many orders of magnitude.  
  - Added color-coded pH mapping along the titration curve for better visual distinction of regions (e.g., buffer, equivalence, excess titrant).  
  - Added pH = 7 guide line for strong acid + strong base titrations.  
  - Dynamic visibility of Ka/Kb sliders and a reset button were included to improve usability and reduce clutter.  

---

## Sources and References 

Primary references used to design and validate the program logic:
- ChatGPT (GPT-4) — used as a development aid to suggest calculation approaches, approximations, and UI design patterns. (Assistance noted in this README.)
- Fundamental chemistry texts:
  - Wikipedia: "Acid–base reaction", "Henderson–Hasselbalch equation", "Titration (chemistry)".
- Standard constants:
  - Kw ≈ 1.0 × 10−14 (assumed at 25 °C).

Acknowledgement of GPT use
- This project used ChatGPT (GPT-4) as an assistant to help draft equations, suggest calculation, implemented from the chemistry equation. GPT's role was advisory.

---

## Modifications, Enhancements, and Attribution 

Base ideas from references
- Chemical theory (Henderson–Hasselbalch, equilibrium hydrolysis approximations, neutralization stoichiometry) are standard textbook material; these are the theoretical foundations used.

My contributions / modifications
- Implementation of a flexible, single function `acid_base_titration(...)` that covers all main analyte/titrant types with branch logic.
- Interactive Matplotlib UI (`make_titration_app`) with:
  - Sliders for concentrations and volumes.
  - Log-scale sliders for Ka/Kb.
  - Radio buttons for analyte/titrant selection and dynamic control visibility.
  - Color-mapped scatter with line trace and autoscaling.
  - Reset button and efficient plot updates by mutating artists.
- Numerical robustness:
  - safe_log10 clamping, pH clipping, and tolerances for equivalence detection.
- Practical UX touches:
  - Hide Ka/Kb sliders unless relevant.
  - Show pH=7 guide line for strong/strong titration only.
  - Increased default point density for smoother curves.
- Documented the code and made it self-contained to be easily run by learners.

Which parts were changed from reference material
- The theoretical formulas are from standard chemistry sources (Henderson–Hasselbalch, Ka/Kb relationships). The code-level implementation, UI design, numerical guards, and plotting details are original contributions by the author.

- Any suggestions drawn from ChatGPT were adapted and implemented with additional numeric safeguards, UI polish, and behavior tuning.

Detailed list of enhancements (why they were made)
- Log10 Ka/Kb sliders: Makes it intuitive to adjust dissociation constants spanning many orders of magnitude.
- Color mapping by pH: Improves immediate visual interpretation of regions (acidic vs basic).
- Numeric guards: Prevent runtime errors (log(0), divide-by-zero) when exploring extreme parameter ranges.
- Dynamic UI visibility: Reduces confusion by only presenting Ka/Kb when applicable.
- Approximate hydrolysis computations at equivalence: Gives instant, reasonable equivalence pH estimates for weak analytes without a full nonlinear solve (practical for an interactive demo).

---

## Limitations and Possible Improvements

Limitations
- Uses simplified approximations for weak species at equivalence (sqrt approximation); may be less accurate for very concentrated solutions or when Ka/Kb are extreme.
- Mono‑protic acids/bases only; polyprotic species are not handled.
- No activity coefficient / ionic strength corrections.
- Temperature fixed (Kw = 1e−14) — pH values will differ with temperature changes.
- No file export (CSV) of computed curves (can be added).

Suggested improvements
- Replace approximate equilibrium steps with a full numerical equilibrium solver (solve mass/balance and charge balance equations with a root finder) for higher accuracy.
- Support polyprotic acids/bases and mixtures.
- Add export functionality (CSV/PNG).
- Add unit tests and automated CI to validate calculation branches.
- Add a web UI (e.g., using Plotly Dash or Streamlit) for easier distribution.

---

## Examples and Quick Tests

Example: strong acid titration
- conc_analyte = 0.10 M (HCl), vol_analyte_ml = 50 mL, conc_titrant = 0.10 M (NaOH)
- Expect pH near 1 at start → steep rise near 25 mL (equivalence) → pH ≈ 7 at equivalence → then basic plateau.

Example: weak acid titration (pKa = 5)
- Set log10(Ka) = −5 (Ka = 1e−5), conc_analyte = 0.10 M, vol_analyte = 50 mL, conc_titrant = 0.10 M
- Expect buffer region where pH ≈ pKa (around pH 5) when A− and HA concentrations are comparable, and pH at equivalence > 7.

---
