import os as os
import numpy as np
import pandas as pd
dir_path = os.path.dirname(os.path.realpath(__file__))
files = {
    "power_divider": "example",
    "line_coupler": "example",
    "isolator": "example",
}
files = {k: os.path.join(dir_path, rf"{v}.csv") for k, v in files.items()}
data = lambda n: (np.array(pd.read_csv(files[n], skipinitialspace=True)["trace"]), np.array(pd.read_csv(files[n], skipinitialspace=True)["f"]))


import matplotlib.pyplot as plt
import scienceplots 
plt.style.use(['science','ieee'])


for keys, value in files.items():
    fig, ax = plt.subplots()
    dat, f = data(keys)
    ax.plot(f, dat)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("S11 [dB]")
    ax.set_title("SNR")
    ax.legend()
    fig.savefig(f"{os.path.join(dir_path, rf"{keys}_SNR")}.svg", transparent=True)