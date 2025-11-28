# Disable import-error due to incoherent module from python 2.7 to 3.x transition
# pylint: disable=E0611
from concurrent.futures import (
    ProcessPoolExecutor,
    as_completed,
)

import numpy as np

from src.aes.functions import aes_internal
from src.context.shared import load_array_from_mmap
from src.utils.progress import progress_bar
from src.guesser.plots import save_diff_vector_plot, save_score_curve_plot


def dpa_compute_score(guess, traces, textin, byte_index=0):
    hyp = np.array([aes_internal(guess, t) for t in textin[:, byte_index]])
    mask = hyp & 1
    diff_vec = abs(traces[mask == 1].mean(0) - traces[mask == 0].mean(0))
    return np.max(diff_vec)


def dpa_diff_vector(guess, traces, textin, byte_index=0):
    hyp = np.array([aes_internal(guess, t) for t in textin[:, byte_index]])
    mask = hyp & 1
    one_avg = traces[mask == 1].mean(0)
    zero_avg = traces[mask == 0].mean(0)
    return abs(one_avg - zero_avg)


def dpa_worker(
    byte_index,
    traces_file,
    traces_shape,
    traces_dtype,
    textin_file,
    textin_shape,
    textin_dtype,
    plotting=False,
):

    traces = load_array_from_mmap(traces_file, traces_shape, traces_dtype)
    textin = load_array_from_mmap(textin_file, textin_shape, textin_dtype)

    scores = np.zeros(256)
    for g in range(256):
        scores[g] = dpa_compute_score(g, traces, textin, byte_index)

    if plotting:
        save_score_curve_plot(scores, byte_index)

    scores = np.array(scores)

    best_guess = int(np.argmax(scores))
    best_score = float(scores[best_guess])

    scores_copy = scores.copy()
    scores_copy[best_guess] = -np.inf
    second_guess = int(np.argmax(scores_copy))
    second_score = float(scores[second_guess])

    contrast = (best_score - second_score) / max(second_score, 1e-15)
    confidence = min(max(contrast, 0.0), 1.0)

    diff_vec = dpa_diff_vector(best_guess, traces, textin, byte_index)
    if plotting:
        save_diff_vector_plot(best_guess, diff_vec, byte_index)

    return {
        "guess": hex(best_guess),
        "confidence": confidence,
        "best": best_score,
        "second": second_score,
        "second_guess": second_guess,
    }


def dpa_guesser(
    traces_file,
    traces_shape,
    traces_dtype,
    textin_file,
    textin_shape,
    textin_dtype,
    plotting=False,
) -> list[dict]:

    guesses = [None] * 16

    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(
                dpa_worker,
                i,
                traces_file,
                traces_shape,
                traces_dtype,
                textin_file,
                textin_shape,
                textin_dtype,
                plotting=plotting,
            ): i
            for i in range(16)
        }

        for future in progress_bar(
            as_completed(futures), total=16, desc="Guessing bytes"
        ):
            guesses[futures[future]] = future.result()

    return guesses
