import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button

# ----------------------------
# Titration calculation logic
# ----------------------------
def acid_base_titration(conc_analyte, vol_analyte_ml, conc_titrant,
                        analyte_type="weak_acid", titrant_type="strong_base",
                        Ka=1e-5, Kb=1e-5,
                        v_min=0, v_max=100, n_points=400):
    """
    Return (volumes_mL, pH_values) for given parameters.
    - conc_* in M, vol_analyte_ml in mL, conc_titrant in M.
    - analyte_type: 'strong_acid', 'weak_acid', 'strong_base', 'weak_base'
    - titrant_type: 'strong_acid' or 'strong_base'
    """
    volumes = np.linspace(v_min, v_max, n_points)
    pH_list = []

    moles_init_analyte = conc_analyte * (vol_analyte_ml / 1000.0)  # moles

    for v_ml in volumes:
        moles_titrant = conc_titrant * (v_ml / 1000.0)
        total_vol_L = (vol_analyte_ml + v_ml) / 1000.0

        # Helper clamp to avoid log(0)
        def safe_log10(x):
            return np.log10(max(x, 1e-20))

        # STRONG ACID (analyte) titrated with STRONG BASE (titrant)
        if analyte_type == "strong_acid" and titrant_type == "strong_base":
            if moles_init_analyte > moles_titrant:  # excess H+
                [H] = [(moles_init_analyte - moles_titrant) / total_vol_L]
                pH = -safe_log10(H)
            elif moles_titrant > moles_init_analyte:  # excess OH-
                [OH] = [(moles_titrant - moles_init_analyte) / total_vol_L]
                pOH = -safe_log10(OH)
                pH = 14.0 - pOH
            else:  # exact equivalence
                pH = 7.0

        # STRONG BASE (analyte) titrated with STRONG ACID (titrant)
        elif analyte_type == "strong_base" and titrant_type == "strong_acid":
            if moles_init_analyte > moles_titrant:  # excess OH-
                [OH] = [(moles_init_analyte - moles_titrant) / total_vol_L]
                pOH = -safe_log10(OH)
                pH = 14.0 - pOH
            elif moles_titrant > moles_init_analyte:  # excess H+
                [H] = [(moles_titrant - moles_init_analyte) / total_vol_L]
                pH = -safe_log10(H)
            else:
                pH = 7.0

        # WEAK ACID titrated by STRONG BASE
        elif analyte_type == "weak_acid" and titrant_type == "strong_base":
            if moles_titrant < moles_init_analyte:  # buffer region (HA/A-)
                HA_remaining = moles_init_analyte - moles_titrant
                A_minus = moles_titrant
                # Henderson-Hasselbalch: pH = pKa + log([A-]/[HA])
                pKa = -safe_log10(Ka)
                # avoid zero division
                ratio = (A_minus / max(HA_remaining, 1e-20))
                pH = pKa + safe_log10(ratio)
            elif abs(moles_titrant - moles_init_analyte) < 1e-30:  # equivalence
                A_minus_conc = moles_titrant / total_vol_L
                Kb_eff = 1e-14 / max(Ka, 1e-30)
                # base hydrolysis: [OH-] ~ sqrt(Kb * [A-])
                OH = np.sqrt(max(Kb_eff * A_minus_conc, 0.0))
                pOH = -safe_log10(OH)
                pH = 14.0 - pOH
            else:  # after equivalence: excess OH-
                OH_excess = (moles_titrant - moles_init_analyte) / total_vol_L
                pOH = -safe_log10(OH_excess)
                pH = 14.0 - pOH

        # WEAK BASE titrated by STRONG ACID
        elif analyte_type == "weak_base" and titrant_type == "strong_acid":
            if moles_titrant < moles_init_analyte:  # buffer region (B/BH+)
                B_remaining = moles_init_analyte - moles_titrant
                BH_plus = moles_titrant
                pKb = -safe_log10(Kb)
                ratio = (B_remaining / max(BH_plus, 1e-20))
                pOH = pKb + safe_log10(ratio)
                pH = 14.0 - pOH
            elif abs(moles_titrant - moles_init_analyte) < 1e-30:  # equivalence
                BH_conc = moles_titrant / total_vol_L
                Ka_eff = 1e-14 / max(Kb, 1e-30)
                H = np.sqrt(max(Ka_eff * BH_conc, 0.0))
                pH = -safe_log10(H)
            else:  # after equivalence: excess H+
                H_excess = (moles_titrant - moles_init_analyte) / total_vol_L
                pH = -safe_log10(H_excess)

        else:
            pH = 7.0

        # Ensure pH is a finite number and clip to [0,14] for display
        if not np.isfinite(pH):
            pH = 7.0
        pH = float(np.clip(pH, 0.0, 14.0))
        pH_list.append(pH)

    return volumes, np.array(pH_list)


# ----------------------------
# Plot + interactive widgets
# ----------------------------
def make_titration_app():
    # Initial parameters
    analyte_type = "weak_acid"
    titrant_type = "strong_base"
    conc_analyte = 0.10  # M
    vol_analyte_ml = 50.0  # mL
    conc_titrant = 0.10  # M
    Ka_init = 1e-5
    Kb_init = 1e-5

    # Plot setup
    fig, ax = plt.subplots(figsize=(9, 6))
    plt.subplots_adjust(left=0.28, bottom=0.38)
    ax.set_xlabel("Volume titrant added (mL)")
    ax.set_ylabel("pH")
    ax.set_ylim(0, 14)
    ax.set_xlim(0, 100)
    ax.set_title(f"Titration: {analyte_type} (analyte) vs {titrant_type} (titrant)")

    # initial data
    vols, pHvals = acid_base_titration(conc_analyte, vol_analyte_ml, conc_titrant,
                                      analyte_type=analyte_type, titrant_type=titrant_type,
                                      Ka=Ka_init, Kb=Kb_init)

    sc = ax.scatter(vols, pHvals, c=pHvals, cmap="RdYlBu_r", s=18)
    line, = ax.plot(vols, pHvals, alpha=0.6)  # connecting line for nicer look
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("pH")

    # Horizontal pH=7 line (initially show only if both strong)
    pH7_line = ax.axhline(7.0, linestyle="--", linewidth=1.0, color="gray", visible=False)

    # ----------------------------
    # UI axes (sliders / radios)
    # ----------------------------
    axcolor = "lightgoldenrodyellow"
    slider_h = 0.03
    pad_left = 0.30

    # Concentration + volume sliders
    ax_concA = plt.axes([pad_left, 0.28, 0.50, slider_h], facecolor=axcolor)
    ax_volA  = plt.axes([pad_left, 0.22, 0.50, slider_h], facecolor=axcolor)
    ax_concT = plt.axes([pad_left, 0.16, 0.50, slider_h], facecolor=axcolor)

    s_concA = Slider(ax_concA, "Analyte Conc (M)", 0.005, 1.0, valinit=conc_analyte)
    s_concT = Slider(ax_concT, "Titrant Conc (M)", 0.005, 1.0, valinit=conc_titrant)

    # Ka/Kb sliders (log-exponent sliders). create axes but visibility managed.
    ax_Ka    = plt.axes([pad_left, 0.10, 0.50, slider_h], facecolor=axcolor)
    ax_Kb    = plt.axes([pad_left, 0.04, 0.50, slider_h], facecolor=axcolor)

    # Slider values are exponents for 10^x so we cover typical weak ranges
    s_Ka = Slider(ax_Ka, "log10(Ka)", -10.0, -2.0, valinit=np.log10(Ka_init))
    s_Kb = Slider(ax_Kb, "log10(Kb)", -10.0, -2.0, valinit=np.log10(Kb_init))
    
    # Radio buttons for analyte and titrant types (smaller size)
    rax1 = plt.axes([0.03, 0.67, 0.15, 0.18], facecolor=axcolor)
    radio_analyte = RadioButtons(rax1, 
    ('strong_acid', 'weak_acid', 'strong_base', 'weak_base'), active=1)
    
    rax2 = plt.axes([0.03, 0.52, 0.15, 0.13], facecolor=axcolor)
    radio_titrant = RadioButtons(rax2, ('strong_base', 'strong_acid'), active=0)
    
    # Smaller Reset button
    bax = plt.axes([0.03, 0.42, 0.12, 0.04])
    button_reset = Button(bax, "Reset", color=axcolor, hovercolor='0.9')


    # ----------------------------
    # Helper: Toggle Ka/Kb visibility depending on weak/strong selection
    # ----------------------------
    def toggle_ka_kb_visibility():
        atype = radio_analyte.value_selected
        ttype = radio_titrant.value_selected

        # Ka visible only if analyte is weak acid
        ka_visible = (atype == "weak_acid")
        ax_Ka.set_visible(ka_visible)
        s_Ka.ax.set_visible(ka_visible)  # slider internals

        # Kb visible only if analyte is weak base OR if titrant is weak base (rare)
        # We want Kb slider visible if either species involved requires Kb: (weak_base analyte) OR (weak_base titrant)
        kb_visible = (atype == "weak_base") or (ttype == "weak_base")
        ax_Kb.set_visible(kb_visible)
        s_Kb.ax.set_visible(kb_visible)

        # If Ka/Kb not visible, we still set values but they won't show
        fig.canvas.draw_idle()

    # initial toggle
    toggle_ka_kb_visibility()

    # ----------------------------
    # Update function (recompute + redraw)
    # ----------------------------
    def update_plot(event=None):
        atype = radio_analyte.value_selected
        ttype = radio_titrant.value_selected

        concA = s_concA.val
        volA = s_volA.val
        concT = s_concT.val

        Ka = 10.0 ** s_Ka.val
        Kb = 10.0 ** s_Kb.val

        vols, pHvals = acid_base_titration(concA, volA, concT,
                                          analyte_type=atype, titrant_type=ttype,
                                          Ka=Ka, Kb=Kb, v_min=0, v_max=100, n_points=600)

        # update scatter and line
        sc.set_offsets(np.column_stack((vols, pHvals)))
        sc.set_array(pHvals)
        line.set_data(vols, pHvals)

        # update title
        ax.set_title(f"Titration: {atype} (analyte) vs {ttype} (titrant)")

        # show pH=7 line only if both are strong
        if (atype in ("strong_acid",) and ttype in ("strong_base",)) or \
           (atype in ("strong_base",) and ttype in ("strong_acid",)):
            pH7_line.set_visible(True)
        else:
            pH7_line.set_visible(False)

        # re-draw
        ax.relim()
        ax.autoscale_view(scalex=False, scaley=False)  # keep x-range fixed
        fig.canvas.draw_idle()

    # ----------------------------
    # Connect widgets to update
    # ----------------------------
    s_concA.on_changed(update_plot)
    s_volA.on_changed(update_plot)
    s_concT.on_changed(update_plot)
    s_Ka.on_changed(update_plot)
    s_Kb.on_changed(update_plot)

    radio_analyte.on_clicked(lambda label: (toggle_ka_kb_visibility(), update_plot(None)))
    radio_titrant.on_clicked(lambda label: (toggle_ka_kb_visibility(), update_plot(None)))

    button_reset.on_clicked(lambda event: (s_concA.reset(), s_volA.reset(), s_concT.reset(),
                                          s_Ka.reset(), s_Kb.reset(), toggle_ka_kb_visibility(), update_plot(None)))

    # initial draw
    update_plot(None)

    plt.show()


if __name__ == "__main__":
    make_titration_app()
