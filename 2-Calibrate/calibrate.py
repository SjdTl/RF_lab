import os as os
import numpy as np
from scipy.fft import fft, fftfreq, fftshift, ifft
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

fig, ax = plt.subplots(figsize=(4,3))

# ax.plot(f*1e-9, 20*np.log10(np.abs(S21_Mem)), label="S21_Mem")
# ax.plot(f*1e-9, 20*np.log10(np.abs(S21)), label="S21")
# ax.plot(f*1e-9, np.angle(S21_Mem), label="S21_Mem")
ax.plot(f*1e-9, (np.angle(S21)), label="S21")

N = 5
to_derive = np.convolve(np.unwrap(np.angle(S21)), np.ones(N)/N, mode='same')
derivative = np.gradient(to_derive,np.mean(np.diff(f*1e-9)))

n = 0.05
N = np.size(f)
n = int(0.05 * N)
ax.plot(f[n:-n]*1e-9, derivative[n:-n], label="dS21/df", color="C1")
ax.hlines(np.mean(derivative[n:-n]), xmin=f[n]*1e-9, xmax=f[-n]*1e-9, color="C1", linestyles=":")
# axt = ax.twinx()
# axt.plot(f, np.angle(S21))
# axt.plot(f, np.angle(S21_Mem))
ax.set_xlabel("Frequency [GHz]")
ax.set_ylabel("Angle [rad]")
ax.set_ylim(-6,5)
ax.legend()
ax.set_title("Calibration verification")
plt.tight_layout()


fig.savefig(f"{os.path.join(dir_path, rf"Calibration")}.svg", transparent=True)