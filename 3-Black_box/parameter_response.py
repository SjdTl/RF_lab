import os as os
import numpy as np
from scipy.fft import fft, fftfreq, fftshift, ifft
import pandas as pd

import matplotlib.pyplot as plt
import scienceplots 
plt.style.use(['science','ieee'])

options = {
    "Block" : "3_Block.csv",
    "Cylinder" : "3_Cilinder.csv",
    "Four_outputs" : "3_4Output.csv",
}

dir_path = os.path.dirname(os.path.realpath(__file__))

for name in options.keys():
    data = pd.read_csv(os.path.join(dir_path, os.path.join(options[name])), 
                    skipinitialspace=True, skiprows=6, skipfooter=3, engine="python")
    S = [[0,0,0], [0,0,0], [0,0,0]]
    fig, ax = plt.subplots(1,2, figsize=(7,3))
    f = np.array(data["Freq(Hz)"])
    for a in [1,2]:
        for b in [1,2]:
            S_val = (np.array(data[rf"S{a}{b}(DB)"]), np.array(data[rf"S{a}{b}(DEG)"]))
            S[a][b] = 10**(S_val[0]/20) * np.exp(1j * S_val[1])
            ax[0].plot(f*1e-9, 20*np.log10(np.abs(S[a][b])), label=rf"S{a}{b}")
            ax[1].plot(f*1e-9, np.unwrap(np.angle(S[a][b])), label=rf"S{a}{b}")


    # N = 5
    # to_derive = np.convolve(np.unwrap(np.angle(S21)), np.ones(N)/N, mode='same')

    ax[0].set_xlabel("Frequency [GHz]")
    ax[1].set_xlabel("Frequency [GHz]")
    ax[0].set_ylabel("Magnitude [dB]")
    ax[1].set_ylabel("Angle [rad]")
    # ax[1].set_xlim(2,2.5)
    ax[0].legend()
    ax[1].legend()
    ax[0].set_title("Magnitude response")
    ax[1].set_title("Phase response")
    plt.suptitle(f"Reponse of the `{name}\'")
    plt.tight_layout()


    fig.savefig(f"{os.path.join(dir_path, rf"{name}")}.svg", transparent=True)