import numpy as np
import mmap
import os

def save_array_to_mmap(arr: np.ndarray, filename: str):
    with open(filename, "wb") as f:
        f.write(arr.tobytes())

    return filename, arr.shape, arr.dtype


def load_array_from_mmap(filename: str, shape, dtype):
    size = np.prod(shape) * np.dtype(dtype).itemsize

    fd = os.open(filename, os.O_RDONLY)
    mm = mmap.mmap(fd, size, access=mmap.ACCESS_READ)

    arr = np.ndarray(shape, dtype=dtype, buffer=mm)

    return arr