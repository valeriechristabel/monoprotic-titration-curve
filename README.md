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
- Points are color-coded by pH, making acidic and basic regions easy to identify.
- For strong acid–strong base titration, a dashed pH = 7 reference line appears automatically.

Reset the simulation
- Click the Reset button to return all sliders and selections to their default values.
- This allows quick comparison between different titration setups.

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

Goal:
- Develop an educational, interactive titration simulator.
- Ensure it is easy to run, visually intuitive, and allows exploration of various monoprotic acid–base systems.

Initial Implementation:
- Started as a basic calculation tool with manual input/output.
- Users had to enter concentrations, volumes, and analyte/titrant types each time.
- Produced correct strong/strong titration curves, but manual input was inefficient.

Enhancements Added:
- Sliders for analyte concentration, analyte volume, and titrant concentration to make the program interactive.
- Ka/Kb sliders (logarithmic scale) for weak acids and bases.
- Buffer-region calculations for weak acids/bases using the Henderson–Hasselbalch equation.
- Equivalence-point hydrolysis calculations ([OH⁻] ≈ √(Kb × [A⁻]) or [H⁺] ≈ √(Ka × [BH⁺])) to model conjugate base/acid behavior.
- Color-coded pH mapping, a pH = 7 guide line for strong/strong titrations, and a reset button for usability.
- Visualization of buffer regions and equivalence points.

Difficulties Encountered:
- Modeling weak acids and bases accurately required chemical knowledge and careful mathematical implementation.
- Exact equilibrium calculations were slow and complex, making real-time interaction challenging.
- Numerical issues such as log(0) or extremely small equivalence-point concentrations caused errors.
- Many bugs appeared during implementation, especially with buffer regions: sliders sometimes became unresponsive.
- Ka/Kb sliders would appear incorrectly (e.g., showing both weak acid and weak base simultaneously).
- Weak base + strong acid titration curves were initially not smooth.
- Acid + acid and base + base titration curves were unrealistic at first and had to be adjusted to reflect neutral pH behavior.
- Adding or revising functionality occasionally caused the reset button to disappear, requiring careful readjustment.

How These Were Resolved:
- Implemented approximations for faster calculations:
    - Henderson–Hasselbalch for buffer regions.
    - Square-root hydrolysis for equivalence points.
- Added numerical safeguards:
    - safe_log10 to prevent errors from very small numbers or zero.
    - Small tolerances to detect the equivalence point accurately despite rounding errors.
    - Clipped pH values to the realistic range of 0–14.
- Updated scatter points and line data dynamically instead of redrawing the whole graph, keeping the UI responsive.
- Iteratively debugged and revised:
    - Corrected slider behavior for buffer regions.
    - Fixed Ka/Kb slider visibility issues.
    - Smoothed weak base + strong acid curves.
    - Adjusted acid + acid and base + base curves to realistic neutral pH.
    - Ensured the reset button worked correctly after multiple revisions.

---

## Sources and References

Primary References Used:
- Textbooks and Standard Chemistry References:
  - Cengage Chemistry Textbooks: Acid–base equilibria, neutralization stoichiometry, Henderson–Hasselbalch equation, hydrolysis approximations.   

LLM:
  - Used as a development aid to suggest calculation approaches, numerical safeguards, UI improvements, and code structuring.  
  - All suggestions were reviewed, adapted, and implemented with added numeric stability and user interface enhancements.  
  - GitHub Copilot: Assisted in making readme file

Modifications and Original Contributions: 
- Code Implementation: The actual calculation function (`acid_base_titration(...)`)
- Numerical Safeguards: Added `safe_log10`, small equivalence tolerances, and pH clipping for stability.  
- Hydrolysis Approximations: Implemented a square-root approximation for weak acid/base equivalence points to simplify calculations while keeping chemical realism.  
- Add the buffer region area, and the equivalence point

Summary: 
The theoretical foundations come from standard chemistry references, while all code-level implementations, UI design, and numerical improvements are original contributions. LLM was used only as an advisory tool to suggest strategies.

---

## Program Modifications and Enhancements

To improve both the practicality and distinctiveness of the titration simulator, several modifications and enhancements were made beyond a basic acid–base calculation program. These efforts focus on interactivity, numerical stability, chemical realism, and educational usability.

1. Interactive Parameter Control

Instead of requiring users to repeatedly enter numerical values through the console, the program was enhanced with interactive UI sliders for:
- Analyte concentration and volume  
- Titrant concentration  
- Acid/base strength (Ka or Kb)

Ka and Kb sliders were implemented on a logarithmic scale because equilibrium constants span many orders of magnitude in real chemistry. This allows users to intuitively explore how changing acid or base strength affects the titration curve in real time, making the program more practical for learning and demonstrations.

---

2. Support for Multiple Titration Types

The program was extended to correctly handle multiple titration systems:
- Strong acid–strong base  
- Weak acid–strong base  
- Weak base–strong acid  
- Same-type additions (acid + acid, base + base)

This enhancement makes the program more distinctive by allowing users to compare different titration behaviors within a single application.

---

3. Stoichiometry-First Calculation Strategy

The program always performs stoichiometric mole balance calculations before applying equilibrium chemistry:
1. Calculate initial moles of analyte and added titrant.
2. Determine which species is in excess.
3. Identify whether the system is before equivalence, at equivalence, or after equivalence.
4. Apply the appropriate pH calculation model.

This mirrors real chemical problem-solving and improves both correctness and educational clarity.

---

4. Chemical Realism with Computational Efficiency

To model weak acid and weak base titrations realistically while keeping the program responsive:
- The Henderson–Hasselbalch equation is used in buffer regions before equivalence.
- At the equivalence point, hydrolysis approximations are applied using square-root expressions such as  
  `[OH⁻] ≈ √(Kb × [A⁻])` or `[H⁺] ≈ √(Ka × [BH⁺])`.

Implementing these calculations was challenging: adding buffer-region and equivalence-point visualization initially caused the figure to freeze or the sliders to become unresponsive. Weak base + strong acid curves were not smooth and required careful debugging and iterative adjustment.  

---

5. Numerical Stability and Error Prevention

Several numerical safeguards were implemented:
- A `safe_log10` function prevents logarithm-of-zero errors by clamping very small concentrations.
- Small tolerance values ensure reliable detection of equivalence points.
- pH values are clipped to the physically meaningful range of 0–14.

Despite these measures, errors occurred during implementation: updating the plot sometimes failed, sliders would not respond, and curves could display unrealistic spikes. Each issue required careful step-by-step debugging.

---

6. Visualization and Performance Optimization

To improve visualization quality and performance:
- The titration curve is color-coded by pH to distinguish acidic, neutral, and basic regions.
- A pH = 7 reference line is shown for strong acid–strong base titrations.
- Buffer regions and equivalence points are highlighted on the plot.
- Plot performance is optimized by updating existing line and scatter objects instead of redrawing the entire plot.

Even with these optimizations, ensuring smooth real-time updates while showing all features (buffer region, equivalence point, Ka/Kb sliders) required multiple revisions and careful management of plot objects.

---

7. User Experience Improvements

Additional enhancements include:
- Dynamic visibility of Ka/Kb sliders based on the selected titration type.
- A reset button to quickly restore default parameters.
- Clear separation between chemical calculations, UI logic, and plotting logic for easier maintenance and explanation.
- Extensive debugging to fix slider freezing, curve smoothing, and plotting errors.

This process also involves help with LLM, especially to solve the error part, and make the code well structured. 
LLM chat : https://copilot.microsoft.com/shares/EBnhyhwfWsr65Yn5EXMwR
