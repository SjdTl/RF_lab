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
files = {k: os.path.join(dir_path, rf"{v}.csv") for k, v in files.items()}
data = lambda n: np.array(pd.read_csv(files[n], skipinitialspace=True, skiprows=6, skipfooter=2)['S11(DB)'])
# To Perform the offline calibration (only one port) using the commands from Appendix A acquire the RAW 
# (i.e., uncalibrated) data of the three standards and pass it to the script below with the following # convention:
Gm1 = data("open_uncorrected") #(Open measurement data from your lab measurement to be imported in Matlab)
Gm2 = data("short_uncorrected") #(Short measurement data from your lab measurement to be imported in Matlab)
Gm3 = data("load_uncorrected") #(Load measurement data from your lab measurement to be imported in Matlab)
# THIS IS WHAT YOU MEASURE WITH THE CORRECTION OFF
# To use the equation below use the following convention:
G1 = 1 # Gamma_ref_P2 (This is the open standard)
G2 = -1 # Gamma_ref_P1 (This is the short standard)
G3 = 0 # Gamma_ref_P3 (This is the load standard)

# THIS IS WHAT YOU MEASURE WITH THE CORRECTION ON
# Compute the error terms with the expressions:
ed = (G3*Gm3*G1*Gm2-G3*Gm3*Gm1*G2+G2*Gm2*Gm1*G3-
Gm2*G1*Gm1*G3+Gm3*G1*Gm1*G2-Gm3*G1*G2*Gm2)/(-
G3*Gm3*G2+G3*G2*Gm2-G1*Gm1*G3+G1*Gm1*G2+G1*G3*Gm3-
G1*G2*Gm2)
es=-(-G3*Gm2+Gm3*G2-G1*Gm3+G1*Gm2+Gm1*G3-Gm1*G2)/(-
G3*Gm3*G2+G3*G2*Gm2-G1*Gm1*G3+G1*Gm1*G2+G1*G3*Gm3-
G1*G2*Gm2)
Delta=-(-Gm2*Gm1*G2+Gm3*G2*Gm2+Gm3*Gm1*G3-
Gm2*G3*Gm3+Gm2*G1*Gm1-Gm3*G1*Gm1)/(-
G3*Gm3*G2+G3*G2*Gm2-G1*Gm1*G3+G1*Gm1*G2+G1*G3*Gm3-
G1*G2*Gm2)

et=ed*es-Delta
# Gamma Correction Procedure.
S11RAW = pd.read_csv(files["independent_load_uncorrected"], skiprows=6, skipfooter=2, skipinitialspace=True)
f = np.array(S11RAW["Freq(Hz)"])
S11RAW = np.array(S11RAW["S11(DB)"])
S11_corrected=(S11RAW-ed)/(S11RAW*es-Delta)
# Note: When performing the computation for the error term make sure you are using all consistent
# variable format (all raw or all column). When you need to transpose take care that you are dealing with
# complex number then the proper command in Matalb is:
# X.' is the non-conjugate transpose.

S11_ref = data("independent_load_corrected")
import matplotlib.pyplot as plt
import scienceplots 
plt.style.use(['science','ieee'])

fig, ax = plt.subplots()
# ax.plot(f, S11_ref, label="Reference data")
ax.plot(f, S11_corrected, 'o', label="Offline corrected")

ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("S11 [dB]")
ax.set_title("Verification")
ax.legend()
fig.savefig(f"{os.path.join(dir_path, "verification")}.svg", transparent=True)

fig, ax = plt.subplots()
ax.plot(f, np.abs(S11_corrected - S11_ref))
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("|S11-S11ref| [dB]")
ax.set_title("Verification")
fig.savefig(f"{os.path.join(dir_path, "verification_difference")}.svg", transparent=True)