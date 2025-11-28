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
):

    traces = load_array_from_mmap(traces_file, traces_shape, traces_dtype)
    textin = load_array_from_mmap(textin_file, textin_shape, textin_dtype)

    best_guess = max(
        range(256), key=lambda g: dpa_compute_score(g, traces, textin, byte_index)
    )

    return hex(best_guess)


def dpa_guesser(
    traces_file, traces_shape, traces_dtype, textin_file, textin_shape, textin_dtype
):

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
            ): i
            for i in range(16)
        }

        for future in progress_bar(
            as_completed(futures), total=16, desc="Guessing bytes"
        ):
            guesses[futures[future]] = future.result()

    return guesses
