import textwrap
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
mpl.rcParams['figure.dpi']= 200


def load_features(file_path="features.txt"):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Optionally, remove newline characters
            lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def draw_grid(n):
    fig, ax = plt.subplots(figsize=(n+1,n+1.3))
    ax.set_aspect('equal')  # Ensure the plot is a square
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)

    # horizontal
    for j in range(2*n + 1):
        if j%2:
            linewidth = 1
            linecolor = "gray"
            linestyle = "dotted"
        else:
            linewidth = 1.5
            linecolor = "black"
            linestyle = "solid"
        ax.axhline(j/(2*n),
                   color=linecolor,
                   linewidth=linewidth,
                   linestyle=linestyle)

    # vertical
    for i in range(n + 1):
        ax.axvline(i/n, color='black', linewidth=1.5)

    # Remove axis and axis titles
    ax.axis('off')

    # text
    features = np.random.choice(load_features(),size=25,replace=False)
    for row in range(n):
        for col in range(n):
            if (long_string := textwrap.fill(features[(row) * n + (col)], 20)).count("\n") > 4:
                raise OverflowError(f"{repr(long_string)} wraps to more than 5 lines, so it doesn't fit!")
            ax.text(row/n+1/(2*n),
                    col/n+1/(4*n),
                    textwrap.fill(features[(row) * n + (col)], 20),
                    ha="center",
                    va="center",
                    fontsize="x-small")
    fig.tight_layout()
    rules = "Rules: Maximum one person per row, column or diagonal"
    fs = "medium"
    ax.set_title(rules, fontsize=fs)
    fig.savefig(os.path.join("figs",str(np.random.randint(1000)).zfill(4)+".png"), format='png', dpi=200)
    plt.close()

def verify_featrues():
    for feat in load_features():
        if (long_string := textwrap.fill(feat, 20)).count("\n") > 4:
            raise OverflowError(f"{repr(long_string)} wraps to more than 5 lines, so it doesn't fit!")

def main(n=25, dim=5):
    verify_featrues()
    files = glob.glob("figs/*")
    for f in files:
        os.remove(f)  
    for i in range(n):
        draw_grid(dim)

if __name__ == "__main__":
    main(n=18, dim=5)
