from src.utils.logger import get_logger, init_logging
from src.config.cli import parse_cli_args
from src.config.loader import load_config_file, merge_config
from src.utils.data_loader import load_traces, load_textin
from src.context.shared import save_array_to_mmap
from src.guesser.dpa import dpa_guesser

KEY = [
    0x2B,
    0x7E,
    0x15,
    0x16,
    0x28,
    0xAE,
    0xD2,
    0xA6,
    0xAB,
    0xF7,
    0x15,
    0x88,
    0x09,
    0xCF,
    0x4F,
    0x3C,
]

NB_TRACES = 600


def main():
    cli_args = parse_cli_args()
    cfg_file = load_config_file(cli_args.config_file)

    settings = merge_config(cli_args, cfg_file)

    init_logging(
        level=settings.log_level,
        fmt=settings.log_format,
        datefmt=settings.log_datefmt,
    )

    logger = get_logger(__name__)

    traces = load_traces("data/traces.npy")
    textin = load_textin("data/textin.npy")

    traces_file, traces_shape, traces_dtype = save_array_to_mmap(
        traces, "data/traces.bin"
    )
    textin_file, textin_shape, textin_dtype = save_array_to_mmap(
        textin, "data/textin.bin"
    )

    logger.info("Starting guessing process")

    guesses = dpa_guesser(
        traces_file, traces_shape, traces_dtype, textin_file, textin_shape, textin_dtype
    )

    logger.info("Key guessed: %s", guesses)

    for i, guess in enumerate(guesses):
        formatted_guess = f"0x{int(guess, 16):02x}"
        correct = f"0x{KEY[i]:02x}"
        status = "OK" if formatted_guess == correct else "NOK"

        logger.raw(f"\tByte {i}: {formatted_guess}\t (Correct: {correct}) \t {status}")


if __name__ == "__main__":
    main()
