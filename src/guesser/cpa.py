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
from src.guesser.plots import (
    save_corr_vector_plot,
    save_cpa_score_curve_plot,
    save_hw_plot,
)


HW = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint8)


def cpa_compute_score(guess, traces, textin, byte_index=0):
    hyp = np.array(
        [aes_internal(guess, t) for t in textin[:, byte_index]], dtype=np.uint8
    )
    hyp_hw = HW[hyp].astype(np.float64)

    hyp_c = hyp_hw - hyp_hw.mean()
    traces_c = traces - traces.mean(axis=0)

    num = np.dot(hyp_c, traces_c)
    denom = np.sqrt(np.sum(hyp_c**2) * np.sum(traces_c**2, axis=0))

    corr = np.divide(num, denom, out=np.zeros_like(num), where=denom != 0)

    return float(np.max(np.abs(corr)))


def cpa_corr_vector(guess, traces, textin, byte_index=0):
    hyp = np.array(
        [aes_internal(guess, t) for t in textin[:, byte_index]], dtype=np.uint8
    )
    hyp_hw = HW[hyp].astype(np.float64)

    hyp_c = hyp_hw - hyp_hw.mean()
    traces_c = traces - traces.mean(axis=0)

    num = np.dot(hyp_c, traces_c)
    denom = np.sqrt(np.sum(hyp_c**2) * np.sum(traces_c**2, axis=0))

    corr = np.divide(num, denom, out=np.zeros_like(num), where=denom != 0)
    return corr


def cpa_worker(
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
        scores[g] = cpa_compute_score(g, traces, textin, byte_index)

    if plotting:
        save_cpa_score_curve_plot(scores, byte_index)

    best_guess = int(np.argmax(scores))
    best_score = float(scores[best_guess])

    scores_copy = scores.copy()
    scores_copy[best_guess] = -np.inf
    second_guess = int(np.argmax(scores_copy))
    second_score = float(scores[second_guess])

    contrast = (best_score - second_score) / max(second_score, 1e-15)
    confidence = min(max(contrast, 0.0), 1.0)

    corr_vec = cpa_corr_vector(best_guess, traces, textin, byte_index)

    if plotting:
        save_corr_vector_plot(best_guess, corr_vec, byte_index)

    return {
        "guess": hex(best_guess),
        "confidence": confidence,
        "best": best_score,
        "second": second_score,
        "second_guess": second_guess,
    }


def cpa_guesser(
    traces_file,
    traces_shape,
    traces_dtype,
    textin_file,
    textin_shape,
    textin_dtype,
    plotting=False,
) -> list[dict]:

    if plotting:
        save_hw_plot(HW)

    guesses = [None] * 16

    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(
                cpa_worker,
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
            as_completed(futures), total=16, desc="Guessing bytes (CPA)"
        ):
            guesses[futures[future]] = future.result()

    return guesses
