import os as os
import numpy as np
import pandas as pd
dir_path = os.path.dirname(os.path.realpath(__file__))
files = {
    "open_uncorrected" : "4_OFF_J2",
    "short_uncorrected" : "4_OFF_J1",
    "load_uncorrected" : "4_OFF_J3",
    "load_corrected" : "4_ON_J3",
    "short_corrected" : "4_ON_J1",
    "open_corrected" : "4_ON_J2",
    "independent_load_uncorrected" : "4_OFF_J4",
    "independent_load_corrected" : "4_ON_J4",
}

def get_data(name):
    db = np.array(pd.read_csv(files[name], skipinitialspace=True, skiprows=6, skipfooter=2, engine = "python")["S11(DB)"])
    deg = np.array(pd.read_csv(files[name], skipinitialspace=True, skiprows=6, skipfooter=2, engine = "python")["S11(DEG)"])
    return 10**(db/20.0) * np.exp(1j * np.deg2rad(deg))
def db(val):
    return 20 * np.log10(np.abs(val))

files = {k: os.path.join(dir_path, rf"{v}.csv") for k, v in files.items()}
# To Perform the offline calibration (only one port) using the commands from Appendix A acquire the RAW 
# (i.e., uncalibrated) data of the three standards and pass it to the script below with the following # convention:
Gm1 = get_data("open_uncorrected" )
Gm2 = get_data("short_uncorrected")
Gm3 = get_data("load_uncorrected" )
# THIS IS WHAT YOU MEASURE WITH THE CORRECTION OFF
# To use the equation below use the following convention:
G1 = 1 # Gamma_ref_P2 (This is the open standard)
G2 = -1 # Gamma_ref_P1 (This is the short standard)
G3 = 0 # Gamma_ref_P3 (This is the load standard)

# THIS IS WHAT YOU MEASURE WITH THE CORRECTION ON
# Compute the error terms with the expressions:
ed = (G3 * Gm3 * G1 * Gm2-G3 * Gm3 * Gm1 * G2+G2 * Gm2 * Gm1 * G3-
Gm2 * G1 * Gm1 * G3+Gm3 * G1 * Gm1 * G2-Gm3 * G1 * G2 * Gm2)/(-
G3 * Gm3 * G2+G3 * G2 * Gm2-G1 * Gm1 * G3+G1 * Gm1 * G2+G1 * G3 * Gm3-
G1 * G2 * Gm2)

es=-(-G3 * Gm2+Gm3 * G2-G1 * Gm3+G1 * Gm2+Gm1 * G3-Gm1 * G2)/(-
G3 * Gm3 * G2+G3 * G2 * Gm2-G1 * Gm1 * G3+G1 * Gm1 * G2+G1 * G3 * Gm3-
G1 * G2 * Gm2)

Delta=-(-Gm2 * Gm1 * G2+Gm3 * G2 * Gm2+Gm3 * Gm1 * G3-
Gm2 * G3 * Gm3+Gm2 * G1 * Gm1-Gm3 * G1 * Gm1)/(-
G3 * Gm3 * G2+G3 * G2 * Gm2-G1 * Gm1 * G3+G1 * Gm1 * G2+G1 * G3 * Gm3-
G1 * G2 * Gm2)

et=ed * es-Delta
# Gamma Correction Procedure.
S11RAW = get_data("independent_load_uncorrected")
f =  np.array(pd.read_csv(files["independent_load_uncorrected"], skipinitialspace=True, skiprows=6, skipfooter=2, engine = "python")["Freq(Hz)"])

S11_corrected=(S11RAW-ed)/(S11RAW * es - Delta)
# Note: When performing the computation for the error term make sure you are using all consistent
# variable format (all raw or all column). When you need to transpose take care that you are dealing with
# complex number then the proper command in Matalb is:
# X.' is the non-conjugate transpose.

S11_ref = get_data("independent_load_corrected")
import matplotlib.pyplot as plt
import scienceplots 
plt.style.use(['science','ieee'])

fig, ax = plt.subplots(1,2, figsize=(4.5,2.5))
ax[0].plot(f*1e-9, db(S11_ref), label="Reference data")
ax[0].plot(f*1e-9, db(S11_corrected), label="Offline corrected")

ax[0].set_xlabel("Frequency [GHz]")
ax[0].set_ylabel("S11 [dB]")
ax[0].set_title("Comparison")
ax[0].legend()

ax[1].plot(f*1e-9, np.abs(db(S11_corrected) - db(S11_ref)))
ax[1].set_xlabel("Frequency [GHz]")
ax[1].set_ylabel(r"$\vert$S11-S11ref$\vert$ [dB]")
ax[1].set_title("Difference")
plt.suptitle(f"Verification (magnitude)")
plt.tight_layout()
fig.savefig(f"{os.path.join(dir_path, "verification_db")}.svg", transparent=True)

fig, ax = plt.subplots(1,2, figsize=(4.5,2.5))
ax[0].plot(f*1e-9, np.unwrap(np.angle(S11_ref)), label="Reference data")
ax[0].plot(f*1e-9, np.unwrap(np.angle(S11_corrected)), label="Offline corrected")

ax[0].set_xlabel("Frequency [GHz]")
ax[0].set_ylabel("S11 [rad]")
ax[0].set_title("Comparison")
ax[0].legend()

ax[1].plot(f*1e-9, np.abs(np.unwrap(np.angle(S11_corrected)) - np.unwrap(np.angle(S11_ref))))
ax[1].set_xlabel("Frequency [GHz]")
ax[1].set_ylabel(r"$\vert$S11-S11ref$\vert$ [rad]")
ax[1].set_title("Difference")
plt.suptitle(f"Verification (angle)")
plt.tight_layout()
fig.savefig(f"{os.path.join(dir_path, "verification_deg")}.svg", transparent=True)