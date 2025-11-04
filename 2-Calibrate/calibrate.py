import os as os
import numpy as np
from scipy.fft import fft, fftfreq, fftshift
import pandas as pd

import matplotlib.pyplot as plt
import scienceplots 
plt.style.use(['science','ieee'])


dir_path = os.path.dirname(os.path.realpath(__file__))

data = pd.read_csv(os.path.join(dir_path, "2_Calibration.csv"), 
                   skipinitialspace=True, skiprows=6, skipfooter=3, engine="python")
S21_Mem = (np.array(data["S21_Mem(DB)"]), np.array(data["S21_Mem(DEG)"]))
S21 = (np.array(data["S21(DB)"]), np.array(data["S21(DEG)"]))
f = np.array(data["Freq(Hz)"])

S21_Mem = 10**(S21_Mem[0]/20) * np.exp(1j * S21_Mem[1])
S21 = 10**(S21[0]/20) * np.exp(1j * S21[1])

fig, ax = plt.subplots(figsize=(3,3))

# ax.plot(f*1e-9, 20*np.log10(np.abs(S21_Mem)), label="S21_Mem")
# ax.plot(f*1e-9, 20*np.log10(np.abs(S21)), label="S21")
ax.plot(f*1e-9, np.angle(S21_Mem), label="S21_Mem")
ax.plot(f*1e-9, np.angle(S21), label="S21")
# axt = ax.twinx()
# axt.plot(f, np.angle(S21))
# axt.plot(f, np.angle(S21_Mem))
ax.set_xlabel("Frequency [GHz]")
ax.set_ylabel("Magnitude [dB]")

ax.legend()
fig.suptitle("Calibration verification")
plt.tight_layout()


fig.savefig(f"{os.path.join(dir_path, rf"Calibration")}.svg", transparent=True)