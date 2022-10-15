#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import re

parts = {
    "core": 73308,
    "packages": 146887,
    "all": 73308 + 146887,
}

pat = r"(\d+) chars:\s+(?:\d+) files changed, (\d+) insertions\(\+\), (\d+) deletions\(\-\)"

dfs = []
for name, total_lines in parts.items():
    with open(f"{name}.dat", "w") as dat:
        dat.write("chars,lines\n")
        for line in open(f"{name}.txt"):
            match = re.match(pat, line)
            if match:
                chars, added, deleted = [int(x) for x in match.groups()]
                dat.write("%d,%d\n" % (chars, (total_lines + added - deleted)))

    df = pd.read_csv(f"{name}.dat").set_index("chars").rename(columns={"lines": name})
    #    df[name] = (df[name] - total_lines) / total_lines * 100
    dfs.append(df)

df = pd.concat(dfs)

df.plot()
plt.title("Blackening Spack")
plt.xlabel("Columns")
plt.ylabel("Lines")

for lim in [80, 88, 99]:
    plt.axvline(x=lim, linestyle="dotted")
    plt.text(lim + 0.5, 10000, str(lim), rotation=45)

for name, total_lines in parts.items():
    plt.axhline(y=total_lines, linestyle="dotted")
    plt.text(121, total_lines + 5000, total_lines, ha="right")

# plt.axhline(y=0, color="black")
plt.ylim(bottom=0)
plt.savefig(f"plot.pdf")
plt.savefig(f"plot.png", dpi=110)
