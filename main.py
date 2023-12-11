import glob
import os
import subprocess
import textwrap

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams["figure.dpi"] = 200
mpl.rcParams["figure.figsize"] = (8, 9)
mpl.rcParams["figure.subplot.left"] = 0.05
mpl.rcParams["figure.subplot.right"] = 0.95
mpl.rcParams["figure.subplot.bottom"] = 0.1
mpl.rcParams["figure.subplot.top"] = 0.9


def load_features(file_path="features.txt"):
    try:
        with open(file_path) as file:
            lines = file.readlines()
            # Optionally, remove newline characters
            lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def draw_grid(dim, n, total):
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # horizontal
    for j in range(2 * dim + 1):
        if j % 2:
            linewidth = 1
            linecolor = "gray"
            linestyle = "dotted"
        else:
            linewidth = 1.5
            linecolor = "black"
            linestyle = "solid"
        ax.axhline(
            j / (2 * dim), color=linecolor, linewidth=linewidth, linestyle=linestyle
        )

    # vertical
    for i in range(dim + 1):
        ax.axvline(i / dim, color="black", linewidth=1.5)

    # Remove axis and axis titles
    ax.axis("off")

    # text
    features = np.random.choice(load_features(), size=25, replace=False)
    for row in range(dim):
        for col in range(dim):
            if (long_string := textwrap.fill(features[(row) * dim + (col)], 20)).count(
                "\n"
            ) > 4:
                raise OverflowError(
                    f"{repr(long_string)} wraps to more than 5 lines, so it doesn't fit!"
                )
            ax.text(
                row / dim + 1 / (2 * dim),
                col / dim + 1 / (4 * dim),
                textwrap.fill(features[(row) * dim + (col)], 20),
                ha="center",
                va="center",
                fontsize="small",
            )
    rules = (
        "Rules: Fill 5 tiles on a line; maximum one person per row, column or diagonal"
    )
    prize = "Come up to us to collect a big prize!"
    fs = "large"
    ax.text(0.5, 1.025, rules, fontsize=fs, va="bottom", ha="center")
    ax.text(0.5, -0.025, prize, fontsize=fs, va="top", ha="center")
    fig.savefig(
        os.path.join("figs", "0" * (len(str(total)) - len(str(n))) + str(n) + ".pdf"),
        format="pdf",
        dpi=200,
    )
    plt.close()


def verify_featrues():
    for feat in load_features():
        if (long_string := textwrap.fill(feat, 20)).count("\n") > 4:
            raise OverflowError(
                f"{repr(long_string)} wraps to more than 5 lines, so it doesn't fit!"
            )


def make_single_pdf(total) -> None:
    prompt = input(
        "Do you wish to comine all the output image files to a single PDF? [y/N]: "
    ).lower()
    if prompt == "y":
        files = [
            os.path.join(
                "figs", "0" * (len(str(total)) - len(str(n))) + str(n) + ".pdf"
            )
            for n in range(1, total + 1)
        ]
        subprocess.call(["pdftk", *files, "cat", "output", "figs/out.pdf"])
        subprocess.call(
            ["pdfjam", "--outfile", "figs/a4.pdf", "--paper", "a4paper", "figs/out.pdf"]
        )


def main(n=25, dim=5):
    verify_featrues()
    files = glob.glob("figs/*")
    for f in files:
        os.remove(f)
    for i in range(n):
        draw_grid(dim, i + 1, n)
    make_single_pdf(n)


if __name__ == "__main__":
    main(n=80, dim=5)
