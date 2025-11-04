import os as os
import numpy as np
from scipy.fft import fft, fftfreq, fftshift
import pandas as pd

import matplotlib.pyplot as plt
import scienceplots 
plt.style.use(['science','ieee'])


dir_path = os.path.dirname(os.path.realpath(__file__))
files = {
    "Low SNR": "Low_SNR",
    "Medium SNR": "Mid_SNR",
    "High SNR": "High_SNR",
}
files = {k: os.path.join(dir_path, rf"{v}.csv") for k, v in files.items()}

fs = 1000000000

for name in files.keys():
    data = pd.read_csv(files[name], skipinitialspace=True, skiprows=7, skipfooter=3, engine="python")
    S22 = (np.array(data["S22 (DB)"]), np.array(data["S22 (DEG)"]))
    a22 = (np.array(data["a2,2 (DB)"]), np.array(data["a2,2 (DEG)"]))
    b12 = (np.array(data["b1,2 (DB)"]), np.array(data["b1,2 (DEG)"]))
    t = np.array(data["Time(s)"])

    S22 = 10**(S22[0]/20) * np.exp(1j * S22[1])
    a22 = 10**(a22[0]/20) * np.exp(1j * a22[1])
    b12 = 10**(b12[0]/20) * np.exp(1j * b12[1])

    N = np.size(t)
    T = (t[-1]-t[0]) / N
    S22f = fftshift(fft(S22))
    a22f = fftshift(fft(a22))
    b12f = fftshift(fft(b12))
    f = fftshift(fftfreq(N, T))

    fig, ax = plt.subplots(1,2, figsize=(6,3))
    std = np.std(20*np.log10(np.abs(S22)))
    # ax[0].plot(t*1e3, 20*np.log10(np.abs(S22)), label=rf"S22: $\sigma = {std*1e3:.1f}m$")
    ax[0].plot(t*1e3, 20*np.log10(np.abs(S22)), label=rf"S22")
    ax[0].plot(t*1e3, 20*np.log10(np.abs(a22)), label="a2,2")
    ax[0].plot(t*1e3, 20*np.log10(np.abs(b12)), label="b1,2")
    
    ax[0].set_xlabel("Time [ms]")
    ax[0].set_ylabel("Magnitude [dB]")
    
    ax[1].plot(f, 20*np.log10(np.abs(S22f)), label="S22")
    ax[1].plot(f, 20*np.log10(np.abs(a22f)), label="a2,2")
    ax[1].plot(f, 20*np.log10(np.abs(b12f)), label="b1,2")

    ax[1].set_xlabel("Frequency [Hz]")
    ax[1].set_ylabel("Magnitude [dB]")

    ax[0].legend(loc="center left")
    ax[0].set_ylim(-115, 5)
    ax[1].set_ylim(-100, 50)
    ax[0].set_title("Time domain")
    ax[1].set_title("Frequency domain")
    fig.suptitle(name)
    plt.tight_layout()

    savename = name.replace(" ", "_")

    fig.savefig(f"{os.path.join(dir_path, rf"{savename}")}.svg", transparent=True)