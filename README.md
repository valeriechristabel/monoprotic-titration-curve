# Project — Interactive Monoprotic Acid‑Base Titration Simulator

## Summary In short

This repository contains an interactive Python program that simulates and visualizes monoprotic acid–base titration curves, where both the analyte and the titrant participate in single-proton acid-base reaction. So it assumes a 1:1 stoichiometric relationship between acid and base. Polyprotic aics, polybasic bases, and titrants that release multiple protons or hydroxide ions per formula unit are not modeled. 

The app computes pH as titrant volume is added to an analyte and provides an interactive Matplotlib-based UI (sliders, radio buttons, color map) so users can explore titrations of strong and weak acids and bases.

---

## Principles and Functions of the Program

This program simulates monoprotic acid–base titrations using classical stoichiometry and acid–base equilibrium theory.  
All calculations assume a 1:1 reaction between acid and base, meaning one mole of acid reacts with one mole of base.  
Polyprotic acids and bases are not modeled.

---

1. Stoichiometry and Volume 

Initial moles of analyte:
n_analyte = C_analyte × V_analyte

Moles of titrant added:
n_titrant = C_titrant × V_titrant

Total solution volume:
V_total = V_analyte + V_titrant

Because the system is monoprotic, neutralization always follows:
H⁺ + OH⁻ → H₂O

At each added titrant volume, the program determines:
- which species is in excess,
- its concentration after dilution,
- and the resulting pH.

---

2. Strong Acid – Strong Base Titration

Strong acids and strong bases are assumed to dissociate completely.

Before equivalence (excess H⁺):
[H⁺] = (n_acid − n_base) / V_total  
pH = −log₁₀([H⁺])

After equivalence (excess OH⁻):
[OH⁻] = (n_base − n_acid) / V_total  
pOH = −log₁₀([OH⁻])  
pH = 14 − pOH

At equivalence:
pH ≈ 7 (assuming Kw = 1.0 × 10⁻¹⁴ at 25 °C)

---

3. Weak Acid – Strong Base Titration

Weak acids dissociate partially:
HA ⇌ H⁺ + A⁻  
Ka = [H⁺][A⁻] / [HA]

Buffer Region (Before Equivalence)
Both HA and A⁻ are present, so the Henderson–Hasselbalch equation is used:
pH = pKa + log₁₀([A⁻]/[HA])

Where:
- [A⁻] is proportional to moles of base added
- [HA] is the remaining weak acid

At Equivalence
All HA has been converted to A⁻.  
The conjugate base hydrolyzes with water:
A⁻ + H₂O ⇌ HA + OH⁻

Kb is calculated from:
Kb = Kw / Ka

Hydroxide concentration is approximated as:
[OH⁻] ≈ √(Kb × C_A⁻)

Then:
pOH = −log₁₀([OH⁻])  
pH = 14 − pOH

This causes the equivalence-point pH to be greater than 7.

---

4. Weak Base – Strong Acid Titration
Weak bases react as:
B + H⁺ ⇌ BH⁺  
Kb = [BH⁺][OH⁻] / [B]

Buffer Region (Before Equivalence)
The Henderson–Hasselbalch form for bases is used:
pOH = pKb + log₁₀([B]/[BH⁺])  
pH = 14 − pOH

At Equivalence
Only the conjugate acid BH⁺ remains:
BH⁺ ⇌ B + H⁺

An effective Ka is calculated:
Ka = Kw / Kb

Hydrogen ion concentration is approximated as:
[H⁺] ≈ √(Ka × C_BH⁺)

Then:
pH = −log₁₀([H⁺])

This results in pH < 7 at equivalence.

---

5. Same-Type Additions (Error Prevention)
Although not true titrations, the program can handle:
- acid + acid
- base + base

To prevent numerical errors, concentrations are added directly:
- Acids: total [H⁺] = analyte contribution + titrant contribution
- Bases: total [OH⁻] = analyte contribution + titrant contribution

This ensures the program does not crash during invalid input combinations.

---

6. Mathematical and Numerical Safeguards

To ensure stability and smooth visualization:
- Logarithms are protected using:
  log₁₀(x) → log₁₀(max(x, 1×10⁻²⁰))
- pH values are clipped to the range 0–14
- Small tolerances are used to detect equivalence points reliably

---

7. Purpose of Approximations

Solving full equilibrium equations at every titrant volume requires nonlinear numerical methods and is computationally expensive.

Instead, the program uses:
- Stoichiometric calculations
- Henderson–Hasselbalch equations
- Square-root hydrolysis approximations

These methods are standard in chemistry and provide fast, stable, and educationally meaningful results for an interactive simulator.

---

## How to Use It 

Run the program
- Execute the Python script
- A window will open showing a pH vs. titrant volume graph with control panels on the side.

Select the analyte and the titrant
- Use the radio buttons to choose:
  - The analyte (solution in the flask):
    - strong_acid, weak_acid, strong_base, or weak_base
  - The titrant (solution being added):
    - strong_acid, or strong_base
- The graph immediately updates to show the corresponding titration curve.

Adjust concentrations and volume
- Use sliders to change:
  - Analyte concentration (M)
  - Analyte volume (mL)
  - Titrant concentration (M)
- As you move the sliders, the program recalculates:
  - Initial moles of analyte
  - Moles of titrant added
  - Resulting pH at each titrant volume
- The curve updates in real time, so you can see how each parameter affects the titration.

Adjust Ka or Kb (only for weak species)
- If you select a weak acid, a log₁₀(Ka) slider appears.
- If you select a weak base, a log₁₀(Kb) slider appears.
- The slider value represents the exponent:
  - For example, log₁₀(Ka) = −5 means Ka = 10⁻⁵.
- Changing Ka or Kb affects:
  - Buffer region slope
  - Equivalence-point pH
  - Overall shape of the titration curve

Interpret the graph
- X-axis: Volume of titrant added (mL)
- Y-axis: pH
- The curve shows:
  - Initial pH
  - Buffer region (for weak systems)
  - Equivalence point
  - Excess titrant region
- Points are color-coded by pH, making acidic and basic regions easy to identify.
- For strong acid–strong base titration, a dashed pH = 7 reference line appears automatically.

Reset the simulation
- Click the Reset button to return all sliders and selections to their default values.
- This allows quick comparison between different titration setups.

Example scenarios to try
- Strong acid (0.1 M HCl, 50 mL) titrated with 0.1 M NaOH.
- Weak acid (pKa ≈ 5) at 0.10 M, 50 mL, titrated with 0.10 M strong base: see buffer region and equivalence pH > 7.
- Weak base titrated with strong acid: pH starts >7 and approaches lower pH after equivalence.

---

## Program Architecture

The program is organized into two main layers, each with distinct responsibilities:

1. Calculation Layer
Function: `acid_base_titration(...)`  
Purpose: Compute pH values for a range of titrant volumes using chemical principles.  

Inputs: 
- Analyte concentration and volume  
- Titrant concentration  
- Analyte/titrant type (strong/weak acid/base)  
- Ka or Kb (for weak species)  
- Titrant volume range and resolution  

Outputs:
- Arrays of titrant volumes  
- Corresponding pH values  

Responsibilities and Principles:
1. Stoichiometry: Compute initial moles of analyte (moles = concentration × volume).  
2. Strong acid–strong base: Compute excess H⁺ or OH⁻ after 1:1 neutralization;  
   pH = −log10([H⁺]) or pH = 14 − pOH.  
3. Weak acid titration: 
   - Buffer region: Henderson–Hasselbalch equation:  
     `pH = pKa + log10([A−]/[HA])`  
   - Equivalence point: Hydrolysis of conjugate base:  
     `[OH−] ≈ sqrt(Kb × [A−])`, pH = 14 − pOH.  
   - Excess titrant: Compute pH from remaining OH⁻.  
4. Weak base titration: Analogous to weak acid, using pOH and hydrolysis of conjugate acid.  
5. Same-type combinations (acid + acid, base + base): Approximate total [H⁺] or [OH−] to avoid program errors.  
6. Numeric safeguards: log inputs, constrain pH to 0–14, and use tolerances near equivalence points.  

---

2. User Interface & Visualization Layer
Function: `make_titration_app()`  
Purpose: Provide an interactive interface for exploring titration curves.  

Responsibilities:  
- Build the Matplotlib figure and axes  
- Create scatter and line plots for pH vs titrant volume  
- Add interactive widgets:  
  - Sliders for concentrations and volume  
  - Logarithmic Ka/Kb sliders for weak species  
  - Radio buttons for analyte/titrant selection  
  - Reset button  
- Dynamically update the plot when parameters change  
- Show or hide Ka/Kb sliders depending on analyte/titrant type  
- Apply color mapping to pH values along the curve  

---

Separation of Concerns
- The calculation layer is independent of plotting, making it reusable or testable separately.  
- The UI layer handles user interaction and presentation, keeping the program responsive and educational.

---

## Development Process

Goal: Develop an educational, interactive titration simulator that is easy to run, visually intuitive, and allows exploration of different monoprotic acid–base systems.

Initial Implementation:
The program began as a basic calculation tool with manual input/output. Users had to enter concentrations, volumes, and analyte/titrant types each time. While it produced correct strong/strong titration curves, manual input was inefficient.

What I added:  
- Sliders for analyte concentration, analyte volume, and titrant concentration to make the program interactive.  
- Ka/Kb sliders (logarithmic scale) for weak acids and bases.  
- Buffer-region calculations for weak acids/bases using the Henderson–Hasselbalch equation.  
- Equivalence-point hydrolysis calculations ([OH⁻] ≈ √(Kb × [A⁻]) or [H⁺] ≈ √(Ka × [BH⁺])) to model conjugate base/acid behavior.  
- Color-coded pH mapping, a pH = 7 guide line for strong/strong titrations, and a reset button for usability.

Why it was challenging:  
- Modeling weak acids and bases accurately requires chemical knowledge and careful math.  
- Exact equilibrium calculations are slow and complex, making real-time interaction difficult.  
- Numerical issues such as log(0) or tiny equivalence-point concentrations could cause errors.

How I solved it:  
- Implemented approximations: Henderson–Hasselbalch for buffer regions, and square-root hydrolysis for equivalence points.  
- Added numerical safeguards to ensure stable calculations:
  - `safe_log10` prevents errors when taking the logarithm of very small numbers or zero.
  - Small tolerances help accurately detect the equivalence point despite tiny rounding differences.
  - pH values are clipped to the realistic range of 0–14 to avoid unphysical results.
- Instead of clearing and redrawing the entire graph each time a slider is moved, the program updates the existing scatter points and line with the new data.
- This keeps the UI responsive even when many points are plotted, making the titration curve update smoothly in real time.

---

## Sources and References

Primary References Used:
- Textbooks and Standard Chemistry References:
  - Cengage Chemistry Textbooks: Acid–base equilibria, neutralization stoichiometry, Henderson–Hasselbalch equation, hydrolysis approximations.  
  - Wikipedia: "Acid–base reaction", "Henderson–Hasselbalch equation", "Titration (chemistry)".  

- ChatGPT (GPT-4):
  - Used as a development aid to suggest calculation approaches, numerical safeguards, UI improvements, and code structuring.  
  - All suggestions were reviewed, adapted, and implemented with added numeric stability and user interface enhancements.  

Modifications and Original Contributions: 
- Code Implementation: The actual calculation function (`acid_base_titration(...)`), UI (`make_titration_app()`), plotting, color mapping, and slider behavior were written by the author.  
- Numerical Safeguards: Added `safe_log10`, small equivalence tolerances, and pH clipping for stability.  
- Interactive Enhancements: Logarithmic Ka/Kb sliders, dynamic visibility, Reset button, and color-coded pH curves.  
- Hydrolysis Approximations: Implemented a square-root approximation for weak acid/base equivalence points to simplify calculations while keeping chemical realism.  

Summary: 
The theoretical foundations come from standard chemistry references, while all code-level implementations, UI design, and numerical improvements are original contributions. ChatGPT was used only as an advisory tool to suggest strategies.

---

## Modifications, Enhancements, and Attribution 

The program is based on standard chemistry principles from textbooks, Cengage. 
- Neutralization stoichiometry: H⁺ + OH⁻ → H₂O  
- Weak acid/base equilibria: HA ⇌ H⁺ + A⁻, B + H⁺ ⇌ BH⁺  
- Henderson–Hasselbalch equation for buffer regions  
- Hydrolysis approximation at equivalence: [OH⁻] ≈ √(Kb × [A⁻]) or [H⁺] ≈ √(Ka × [BH⁺])

My contributions / modifications
- Implementation of a flexible, single function `acid_base_titration(...)` that covers all main analyte/titrant types with branch logic.
- Interactive Matplotlib UI (`make_titration_app`) with:
  - Sliders for concentrations and volumes, remove the input output.
  - Log-scale sliders for Ka/Kb for weak species
  - Radio buttons for analyte/titrant selection with dynamic control visibility.
  - Color-mapped scatter with line trace for pH curves
  - Reset button for quick return to defaults
- Numerical robustness:
  - safe_log10 clamping, pH clipping, and tolerances for equivalence detection.
- Practical UX touches:
  - Hide Ka/Kb sliders unless relevant.
  - Show pH=7 guide line for strong/strong titration only.
  - Increased default point density for smoother curves.
- Documented the code and made it self-contained to be easily run by learners.

Which parts were changed from reference material
- The code implementation, UI design, numeric guards, plotting, and interactivity are original contributions by the author.  
- Any suggestions from ChatGPT were adapted and enhanced with numeric safeguards, UI polish, and behavior tuning.
- Any suggestions drawn from ChatGPT were adapted and implemented with additional numeric safeguards, UI polish, and behavior tuning.

Detailed list of enhancements (why they were made)
- Log10 Ka/Kb sliders: Makes it intuitive to adjust dissociation constants spanning many orders of magnitude.
- Color mapping by pH: Improves immediate visual interpretation of regions (acidic vs basic).
- Numeric guards: Prevent runtime errors (log(0), divide-by-zero) when exploring extreme parameter ranges.
- Dynamic UI visibility: Reduces confusion by only presenting Ka/Kb when applicable.
- Approximate hydrolysis computations at equivalence: When a weak acid is titrated with a strong base, at the equivalence point all the weak acid has reacted, forming its conjugate base. This conjugate base reacts slightly with water, producing OH⁻ ions, making the solution basic.

Similarly, when a weak base is titrated with a strong acid, the conjugate acid forms H⁺ ions, making the solution acidic.

Calculating the exact pH would require solving a complex equilibrium equation for every titrant volume, which is slow and impractical for an interactive program.
The program approximates the pH at the equivalence point using a simple square-root formula instead of solving the full equilibrium equation. This keeps the simulation smooth, responsive, and educational.

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
