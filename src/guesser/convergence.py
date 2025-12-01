# Disable import-error due to incoherent module from python 2.7 to 3.x transition
# pylint: disable=E0611
from concurrent.futures import (
    ProcessPoolExecutor,
    as_completed,
)

import os
import numpy as np
import matplotlib.pyplot as plt

from src.guesser.dpa import dpa_compute_score
from src.guesser.cpa import cpa_compute_score
from src.utils.logger import get_logger, init_logging

logger = get_logger(__name__)


def worker_init_logger(logging_settings):
    init_logging(
        level=logging_settings["level"],
        fmt=logging_settings["fmt"],
        datefmt=logging_settings["datefmt"],
    )


def plot_convergence_all_guesses_one_byte(
    traces, textin, byte_index, step=5, outdir="plots/dpa/convergence_all_guesses"
):
    os.makedirs(outdir, exist_ok=True)
    max_n = traces.shape[0]

    x = np.arange(10, max_n, step)
    n_points = len(x)

    plt.figure(figsize=(14, 6))

    dpa_score = dpa_compute_score
    traces_local = traces
    textin_local = textin

    all_scores = np.zeros((256, n_points), dtype=float)

    traces_cache = [traces_local[:n] for n in x]
    textin_cache = [textin_local[:n] for n in x]

    for g in range(256):
        scores_g = all_scores[g]
        for i, (t_n, ti_n) in enumerate(zip(traces_cache, textin_cache)):
            scores_g[i] = dpa_score(g, t_n, ti_n, byte_index=byte_index)

        plt.plot(x, scores_g, linewidth=0.6, alpha=0.6)
        logger.debug("[DPA Convergence][Byte %d][Guess 0x%02x] Done", byte_index, g)

    last_values = all_scores[:, -1]
    idx_sorted = np.argsort(last_values)[::-1]

    g1, g2 = idx_sorted[:2]
    score1, score2 = last_values[g1], last_values[g2]

    plt.plot(
        x,
        all_scores[g1],
        linewidth=2.0,
        label=f"Best guess: 0x{g1:02x} (score={score1:.4f})",
    )
    plt.plot(
        x,
        all_scores[g2],
        linewidth=2.0,
        label=f"Second best: 0x{g2:02x} (score={score2:.4f})",
    )

    plt.title(f"DPA Convergence — all guesses for byte {byte_index}")
    plt.xlabel("Number of measurements")
    plt.ylabel("DPA Score")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    out = f"{outdir}/convergence_byte{byte_index:02d}.png"
    plt.savefig(out, dpi=200)
    plt.close()
    return out


def plot_all_bytes_parallel(traces, textin, logging_settings):
    with ProcessPoolExecutor(
        initializer=worker_init_logger, initargs=(logging_settings,)
    ) as ex:
        futures = {
            ex.submit(plot_convergence_all_guesses_one_byte, traces, textin, i): i
            for i in range(16)
        }

        for f in as_completed(futures):
            i = futures[f]
            logger.info("[DPA Convergence] Done for byte %d", i)


def plot_convergence_all_guesses_one_byte_cpa(
    traces, textin, byte_index, step=5, outdir="plots/cpa/convergence_all_guesses"
):
    os.makedirs(outdir, exist_ok=True)
    max_n = traces.shape[0]

    x = np.arange(10, max_n, step)
    n_points = len(x)

    plt.figure(figsize=(14, 6))

    cpa_score = cpa_compute_score
    traces_local = traces
    textin_local = textin

    all_scores = np.zeros((256, n_points), dtype=float)

    traces_cache = [traces_local[:n] for n in x]
    textin_cache = [textin_local[:n] for n in x]

    for g in range(256):
        scores_g = all_scores[g]
        for i, (t_n, ti_n) in enumerate(zip(traces_cache, textin_cache)):
            scores_g[i] = cpa_score(g, t_n, ti_n, byte_index=byte_index)

        plt.plot(x, scores_g, linewidth=0.6, alpha=0.6)
        logger.debug("[CPA Convergence][Byte %d][Guess 0x%02x] Done", byte_index, g)

    last_values = all_scores[:, -1]
    idx_sorted = np.argsort(last_values)[::-1]

    g1, g2 = idx_sorted[:2]
    score1, score2 = last_values[g1], last_values[g2]

    plt.plot(
        x,
        all_scores[g1],
        linewidth=2.0,
        label=f"Best guess: 0x{g1:02x} (corr={score1:.4f})",
    )
    plt.plot(
        x,
        all_scores[g2],
        linewidth=2.0,
        label=f"Second best: 0x{g2:02x} (corr={score2:.4f})",
    )

    plt.title(f"CPA Convergence — all guesses for byte {byte_index}")
    plt.xlabel("Number of measurements")
    plt.ylabel("CPA Correlation")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    out = f"{outdir}/convergence_byte{byte_index:02d}.png"
    plt.savefig(out, dpi=200)
    plt.close()
    return out


def plot_all_bytes_parallel_cpa(traces, textin, logging_settings):
    with ProcessPoolExecutor(
        initializer=worker_init_logger, initargs=(logging_settings,)
    ) as ex:
        futures = {
            ex.submit(plot_convergence_all_guesses_one_byte_cpa, traces, textin, i): i
            for i in range(16)
        }

        for f in as_completed(futures):
            i = futures[f]
            logger.info("[CPA Convergence] Done for byte %d", i)
