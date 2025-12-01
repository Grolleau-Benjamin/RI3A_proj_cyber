import os
import numpy as np
import matplotlib.pyplot as plt


def save_diff_vector_plot(
    best_guess, diff_vec, byte_index, outdir="plots/dpa/diff_vectors"
):
    os.makedirs(outdir, exist_ok=True)

    x = np.arange(len(diff_vec))
    max_idx = int(np.argmax(diff_vec))
    max_val = float(diff_vec[max_idx])

    mean_val = float(np.mean(diff_vec))
    median_val = float(np.median(diff_vec))

    top10_threshold = np.sort(diff_vec)[-10]
    top10_idx = np.where(diff_vec >= top10_threshold)[0]

    plt.figure(figsize=(14, 3))

    plt.plot(
        x, diff_vec, color="blue", linewidth=0.7, label=f"Guess(0x{best_guess:02x})"
    )

    plt.scatter([max_idx], [max_val], color="red", s=40, label="Max")
    plt.text(max_idx, max_val, f"{max_val:.4f}", color="red", fontsize=9, ha="left")

    plt.scatter(top10_idx, diff_vec[top10_idx], color="purple", s=20, label="Top10")

    plt.axhline(
        mean_val,
        color="orange",
        linestyle="--",
        linewidth=0.8,
        label=f"Mean {mean_val:.4f}",
    )
    plt.axhline(
        median_val,
        color="cyan",
        linestyle="--",
        linewidth=0.8,
        label=f"Median {median_val:.4f}",
    )

    plt.title(f"DPA diff vector - byte {byte_index} - guess 0x{best_guess:02x}")
    plt.xlabel("Time")
    plt.ylabel("|mean1 - mean0|")

    plt.legend(loc="upper right")
    plt.tight_layout()

    filename = f"{outdir}/diff_vector_byte{byte_index:02d}.png"
    plt.savefig(filename, dpi=150)
    plt.close()


def save_score_curve_plot(scores, byte_index=0, outdir="plots/dpa/score_curves"):
    os.makedirs(outdir, exist_ok=True)

    best_guess = int(np.argmax(scores))
    best_score = scores[best_guess]

    scores_copy = scores.copy()
    scores_copy[best_guess] = -np.inf
    second_guess = int(np.argmax(scores_copy))
    second_score = scores[second_guess]

    plt.figure(figsize=(14, 4))
    plt.plot(range(256), scores, label="DPA score")

    plt.scatter([best_guess], [best_score], color="red", s=50)
    plt.annotate(
        f"{best_guess:#04x}\n{best_score:.4f}",
        xy=(best_guess, best_score),
        xytext=(best_guess + 8, best_score * 1.1),
        arrowprops=dict(arrowstyle="->", color="red"),
        fontsize=9,
        color="red",
    )

    plt.scatter([second_guess], [second_score], color="orange", s=50)
    plt.annotate(
        f"{second_guess:#04x}\n{second_score:.4f}",
        xy=(second_guess, second_score),
        xytext=(second_guess + 8, second_score * 1.1),
        arrowprops=dict(arrowstyle="->", color="orange"),
        fontsize=9,
        color="orange",
    )

    hex_labels = [f"{g:#04x}" for g in range(256)]
    plt.xticks(
        ticks=range(0, 256, 16),
        labels=hex_labels[0:256:16],
        rotation=45,
    )

    plt.title(f"DPA score curve (byte {byte_index})")
    plt.xlabel("Guess (hex)")
    plt.ylabel("Score")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    filename = f"{outdir}/score_curve_byte{byte_index:02d}.png"
    plt.savefig(filename, dpi=150)
    plt.close()


def save_corr_vector_plot(
    best_guess, corr_vec, byte_index, outdir="plots/cpa/corr_vectors"
):
    os.makedirs(outdir, exist_ok=True)

    x = np.arange(len(corr_vec))
    max_idx = int(np.argmax(np.abs(corr_vec)))
    max_val = float(corr_vec[max_idx])

    mean_val = float(np.mean(corr_vec))
    median_val = float(np.median(corr_vec))

    idx_sorted_abs = np.argsort(np.abs(corr_vec))
    top10_idx = idx_sorted_abs[-10:]

    plt.figure(figsize=(14, 3))

    plt.plot(
        x,
        corr_vec,
        color="blue",
        linewidth=0.7,
        label=f"Guess(0x{best_guess:02x})",
    )

    plt.scatter([max_idx], [max_val], color="red", s=40, label="Max")
    plt.text(max_idx, max_val, f"{max_val:.4f}", color="red", fontsize=9, ha="left")

    plt.scatter(top10_idx, corr_vec[top10_idx], color="purple", s=20, label="Top10")

    plt.axhline(
        mean_val,
        color="orange",
        linestyle="--",
        linewidth=0.8,
        label=f"Mean {mean_val:.4f}",
    )
    plt.axhline(
        median_val,
        color="cyan",
        linestyle="--",
        linewidth=0.8,
        label=f"Median {median_val:.4f}",
    )

    plt.title(f"CPA correlation vector - byte {byte_index} - guess 0x{best_guess:02x}")
    plt.xlabel("Time")
    plt.ylabel("Correlation")

    plt.legend(loc="upper right")
    plt.tight_layout()

    filename = f"{outdir}/corr_vector_byte{byte_index:02d}.png"
    plt.savefig(filename, dpi=150)
    plt.close()


def save_cpa_score_curve_plot(scores, byte_index=0, outdir="plots/cpa/score_curves"):
    os.makedirs(outdir, exist_ok=True)

    best_guess = int(np.argmax(np.abs(scores)))
    best_score = float(scores[best_guess])

    scores_copy = scores.copy()
    scores_copy[best_guess] = 0.0
    second_guess = int(np.argmax(np.abs(scores_copy)))
    second_score = float(scores[second_guess])

    plt.figure(figsize=(14, 4))
    plt.plot(range(256), scores, label="CPA correlation")

    plt.scatter([best_guess], [best_score], color="red", s=50)
    plt.annotate(
        f"{best_guess:#04x}\n{best_score:.4f}",
        xy=(best_guess, best_score),
        xytext=(best_guess + 8, best_score * 1.1),
        arrowprops=dict(arrowstyle="->", color="red"),
        fontsize=9,
        color="red",
    )

    plt.scatter([second_guess], [second_score], color="orange", s=50)
    plt.annotate(
        f"{second_guess:#04x}\n{second_score:.4f}",
        xy=(second_guess, second_score),
        xytext=(second_guess + 8, second_score * 1.1),
        arrowprops=dict(arrowstyle="->", color="orange"),
        fontsize=9,
        color="orange",
    )

    hex_labels = [f"{g:#04x}" for g in range(256)]
    plt.xticks(
        ticks=range(0, 256, 16),
        labels=hex_labels[0:256:16],
        rotation=45,
    )

    plt.title(f"CPA score curve (byte {byte_index})")
    plt.xlabel("Guess (hex)")
    plt.ylabel("Correlation")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    filename = f"{outdir}/score_curve_byte{byte_index:02d}.png"
    plt.savefig(filename, dpi=150)
    plt.close()


def save_hw_plot(hw, outdir="plots/cpa/hamming_weight"):
    os.makedirs(outdir, exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.bar(range(256), hw, color="blue", alpha=0.7)

    plt.title("Hamming Weight of Byte Values")
    plt.xlabel("Byte Value (0x00 to 0xFF)")
    plt.ylabel("Hamming Weight")
    plt.xticks(
        ticks=range(0, 256, 16),
        labels=[f"{i:#04x}" for i in range(0, 256, 16)],
        rotation=45,
    )
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    filename = f"{outdir}/hamming_weight_plot.png"
    plt.savefig(filename, dpi=150)
    plt.close()
