import os
import numpy as np

from src.utils.logger import get_logger

logger = get_logger(__name__)


def _load_numpy(file_path: str) -> np.ndarray:
    if not os.path.exists(file_path):
        logger.critical("File not found: %s", file_path)
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        return np.load(file_path)
    except Exception:
        logger.exception("Failed to load numpy file: %s", file_path)
        raise


def load_traces(file_path: str) -> np.ndarray:
    return _load_numpy(file_path)


def load_textin(file_path: str) -> np.ndarray:
    return _load_numpy(file_path)
