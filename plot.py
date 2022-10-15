#!/usr/bin/env python3

import glob
import re

import matplotlib.pyplot as plt


data_dir = "2022-07-black"


def get_code_lines(filename):
    with open(filename) as f:
        for line in f:
            if line.startswith("Python"):
                _, files, blank, comments, code = line.split()
                return int(code)


def get_series(glob_expression):
    result = []

    for filename in glob.glob(glob_expression):
        match = re.search(glob_expression.replace("*", r'(\d+)'), filename)
        if not match:
            raise RuntimeError("invalid filename: " + filename)
        cols = int(match.group(1))
        result.append((cols, get_code_lines(filename)))

    return sorted(result)



label_height = 5000
col_pad = .5

baseline_all = get_code_lines(f"{data_dir}/logs/cloc.all.txt")
baseline_packages = get_code_lines(f"{data_dir}/logs/cloc.packages.txt")
baseline_core = get_code_lines(f"{data_dir}/logs/cloc.core.txt")

cols_all, lines_all = zip(*get_series(f"{data_dir}/logs/cloc.all.*.txt"))
cols_packages, lines_packages = zip(*get_series(f"{data_dir}/logs/cloc.packages.*.txt"))
cols_core, lines_core = zip(*get_series(f"{data_dir}/logs/cloc.core.*.txt"))

# plot of core, packages, all
plt.figure()

plt.axhline(baseline_all, label=None, linestyle="dotted")
plt.axhline(baseline_packages, label=None, linestyle="dotted")
plt.axhline(baseline_core, label=None, linestyle="dotted")

plt.text(116, baseline_all + label_height, str(baseline_all))
plt.text(116, baseline_packages + label_height, str(baseline_packages))
plt.text(116, baseline_core + label_height, str(baseline_core))

plt.axvline(80, label=None, linestyle="dotted")
plt.axvline(88, label=None, linestyle="dotted")
plt.axvline(99, label=None, linestyle="dotted")

plt.text(80 + col_pad, label_height, "80")
plt.text(88 + col_pad, label_height, "88")
plt.text(99 + col_pad, label_height, "99")

plt.plot(cols_all, lines_all, label="all")
plt.plot(cols_packages, lines_packages, label="packages")
plt.plot(cols_core, lines_core, label="core")

plt.legend(loc="upper right")
plt.ylim(bottom=0)

plt.ylabel("Lines of code")
plt.xlabel("Black column limit")
plt.savefig("all-lines.pdf")

# plot of just core
plt.figure()
label_height = 1000

# right axis on core is a percentage
#ax_left = plt.gca()
#ax_right = ax_left.twinx()

#def convert_ax_left_to_percent(ax_left):
#    y1, y2 = ax_left.get_ylim()
#    ax_right.set_ylim(
#        (y1 - baseline_core) / baseline_core * 100,
#        (y2 - baseline_core) / baseline_core * 100
#    )
#    ax_right.figure.canvas.draw()

#ax_left.callbacks.connect("ylim_changed", convert_ax_left_to_percent)


plt.axhline(baseline_core, label=None, linestyle="dotted")
plt.text(116, baseline_core + label_height, str(baseline_core))

plt.axvline(80, label=None, linestyle="dotted")
plt.axvline(88, label=None, linestyle="dotted")
plt.axvline(99, label=None, linestyle="dotted")

plt.text(80 + col_pad, label_height, "80")
plt.text(88 + col_pad, label_height, "88")
plt.text(99 + col_pad, label_height, "99")

plt.plot(cols_core, lines_core, label="core")

plt.legend(loc="upper right")

plt.ylabel("Lines of code")
plt.xlabel("Black column limit")
plt.savefig("core-lines.pdf")
