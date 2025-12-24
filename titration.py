import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button  # tambahkan Button

def acid_base_titration(conc_analyte, vol_analyte_ml, conc_titrant,
                        analyte_type="weak_acid", titrant_type="strong_base",
                        Ka=1e-5, Kb=1e-5, v_min=0, v_max=100, n_points=400):

    volumes = np.linspace(v_min, v_max, n_points)
    pH_list = []
    moles_init = conc_analyte * vol_analyte_ml / 1000

    def safe_log(x): return np.log10(max(x, 1e-20))

    for v in volumes:
        moles_t = conc_titrant * v / 1000
        V = (vol_analyte_ml + v) / 1000

        if analyte_type == "strong_acid" and titrant_type == "strong_base":
            if moles_init > moles_t: pH = -safe_log((moles_init - moles_t)/V)
            elif moles_t > moles_init: pH = 14 + safe_log((moles_t - moles_init)/V)
            else: pH = 7
        elif analyte_type == "strong_base" and titrant_type == "strong_acid":
            if moles_init > moles_t: pH = 14 + safe_log((moles_init - moles_t)/V)
            elif moles_t > moles_init: pH = -safe_log((moles_t - moles_init)/V)
            else: pH = 7
        elif analyte_type == "weak_acid" and titrant_type == "strong_base":
            if moles_t < moles_init:
                pKa = -safe_log(Ka)
                pH = pKa + safe_log(moles_t/(moles_init - moles_t))
            elif np.isclose(moles_t, moles_init):
                Kb_eff = 1e-14 / Ka
                OH = np.sqrt(Kb_eff * (moles_t / V))
                pH = 14 + safe_log(OH)
            else: pH = 14 + safe_log((moles_t - moles_init)/V)
        elif analyte_type == "weak_base" and titrant_type == "strong_acid":
            if moles_t < moles_init:
                pKb = -safe_log(Kb)
                pOH = pKb + safe_log(moles_t/(moles_init - moles_t))
                pH = 14 - pOH
            elif np.isclose(moles_t, moles_init):
                Ka_eff = 1e-14 / Kb
                H = np.sqrt(Ka_eff * (moles_t / V))
                pH = -safe_log(H)
            else: pH = -safe_log((moles_t - moles_init)/V)
        else: pH = 7

        pH_list.append(np.clip(pH,0,14))
    return volumes, np.array(pH_list)


def make_titration_app():
    fig, ax = plt.subplots(figsize=(9,6))
    plt.subplots_adjust(left=0.28, bottom=0.38)
    ax.set_xlim(0,100); ax.set_ylim(0,14)
    ax.set_xlabel("Volume titrant (mL)"); ax.set_ylabel("")
    ax.set_title("Monoprotic Acid-Base Titration")
    
    vols, pHvals = acid_base_titration(0.1,50,0.1)
    sc = ax.scatter(vols,pHvals,c=pHvals,cmap="RdYlBu_r",s=18)
    line, = ax.plot(vols,pHvals)
    plt.colorbar(sc, ax=ax).set_label("pH")

    pH7 = ax.axhline(7, ls="--", color="gray", visible=False)
    eq_line = ax.axvline(0, ls="--", color="purple", visible=False)
    eq_text = ax.text(0,7.5,"Equivalence", color="purple", ha="center", visible=False)
    buffer_patch = ax.axvspan(0,0, color="green", alpha=0.12, visible=False)
    buffer_text = ax.text(0,6,"Buffer Region", color="darkgreen", ha="center", visible=False)

    axcolor = "lightgoldenrodyellow"
    s_concA = Slider(plt.axes([0.3,0.28,0.5,0.03], facecolor=axcolor),"Analyte M",0.01,1,valinit=0.1)
    s_volA  = Slider(plt.axes([0.3,0.22,0.5,0.03], facecolor=axcolor),"Analyte mL",5,200,valinit=50)
    s_concT = Slider(plt.axes([0.3,0.16,0.5,0.03], facecolor=axcolor),"Titrant M",0.01,1,valinit=0.1)
    s_Ka    = Slider(plt.axes([0.3,0.10,0.5,0.03], facecolor=axcolor),"log Ka",-10,-2,valinit=-5)
    s_Kb    = Slider(plt.axes([0.3,0.04,0.5,0.03], facecolor=axcolor),"log Kb",-10,-2,valinit=-5)

    radio_a = RadioButtons(plt.axes([0.03,0.65,0.2,0.2], facecolor=axcolor),
                           ["strong_acid","weak_acid","strong_base","weak_base"],1)
    radio_t = RadioButtons(plt.axes([0.03,0.52,0.2,0.12], facecolor=axcolor),
                           ["strong_base","strong_acid"],0)

    # ===== Reset Button =====
    reset_ax = plt.axes([0.03, 0.42, 0.12, 0.04])
    button_reset = Button(reset_ax, "Reset", color=axcolor, hovercolor='0.9')
    def reset(event):
        s_concA.reset()
        s_volA.reset()
        s_concT.reset()
        s_Ka.reset()
        s_Kb.reset()
        radio_a.set_active(1)  # weak_acid default
        radio_t.set_active(0)  # strong_base default
    button_reset.on_clicked(reset)
    # ===== End Reset Button =====

    def toggle_Ka_Kb():
        at = radio_a.value_selected
        s_Ka.ax.set_visible(at=="weak_acid")
        s_Kb.ax.set_visible(at=="weak_base")
        fig.canvas.draw_idle()

    def update(_=None):
        toggle_Ka_Kb()
        at = radio_a.value_selected
        tt = radio_t.value_selected

        vols, pHvals = acid_base_titration(
            s_concA.val, s_volA.val, s_concT.val,
            at, tt, 10**s_Ka.val, 10**s_Kb.val
        )

        sc.set_offsets(np.c_[vols,pHvals])
        sc.set_array(pHvals)
        line.set_data(vols,pHvals)

        eq = (s_concA.val*s_volA.val)/s_concT.val
        eq_line.set_xdata([eq, eq]); eq_line.set_visible(True)
        eq_text.set_position((eq,7.5)); eq_text.set_visible(True)

        pH7.set_visible((at=="strong_acid" and tt=="strong_base") or (at=="strong_base" and tt=="strong_acid"))

        if at in ("weak_acid","weak_base"):
            buffer_patch.set_x(0.1*eq)
            buffer_patch.set_width(0.8*eq)
            buffer_patch.set_visible(True)
            buffer_text.set_position((0.5*eq + 0.1*eq,6))
            buffer_text.set_visible(True)
        else:
            buffer_patch.set_visible(False)
            buffer_text.set_visible(False)

        fig.canvas.draw_idle()

    for s in (s_concA,s_volA,s_concT,s_Ka,s_Kb):
        s.on_changed(update)
    radio_a.on_clicked(update)
    radio_t.on_clicked(update)
    update()
    plt.show()

if __name__=="__main__":
    make_titration_app()
