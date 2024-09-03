import os
from os.path import isfile, join
filelist = [f for f in os.listdir("./data") if isfile(join("./data", f))]
for filename in filelist:
    with open("./data/" + filename) as f:
        if "--undefined--" in f.read():
            print(filename)
import pandas
import math
import matplotlib.pyplot as plt
all_data = pandas.DataFrame()
for filename in filelist:
    data = pandas.read_csv("./data/" + filename, sep="   ", engine="python")
    data["Semitones"] = 12 * data["F0_Hz"].apply(
        lambda x: math.log(x / data["F0_Hz"].mean(), 2)
    )
    all_data = pandas.concat([all_data, data], ignore_index=True)
plt.figure(figsize=(10, 6))
for filename in filelist:
    data = pandas.read_csv("./data/" + filename, sep="   ", engine="python")
    data["Semitones"] = 12 * data["F0_Hz"].apply(
        lambda x: math.log(x / data["F0_Hz"].mean(), 2)
    )
    data["Cents"] = round(data["Semitones"] * 100).astype(int)
    data["ZScore"] = (data["Semitones"] - all_data["Semitones"].mean()) / all_data["Semitones"].std()
    data["Time"] = data["Time_s"] - data["Time_s"].min()
    plt.plot(data["Time"], data["ZScore"], label=filename)
plt.title("log z-Score contours")
plt.xlabel("Time (s)")
plt.ylabel("z-Score")
plt.legend(loc="upper right", fontsize='small')
plt.grid(True)
plt.savefig("./plot.png", dpi=300)