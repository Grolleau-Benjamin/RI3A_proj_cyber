from src.utils.logger import get_logger, init_logging
from src.config.cli import parse_cli_args
from src.config.loader import load_config_file, merge_config
from src.utils.data_loader import load_traces, load_textin
from src.guesser.guesser import guesser
from src.context.shared import save_array_to_mmap

KEY = [0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xa6,0xab,0xf7,0x15,0x88,0x09,0xcf,0x4f,0x3c]

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

    traces_file, traces_shape, traces_dtype = save_array_to_mmap(traces, "data/traces.bin")
    textin_file, textin_shape, textin_dtype = save_array_to_mmap(textin, "data/textin.bin")

    logger.info("Starting guessing process")

    guesses = guesser(
        traces_file, traces_shape, traces_dtype,
        textin_file, textin_shape, textin_dtype
    )

    logger.info("Key guessed: %s", guesses)

    for i, guess in enumerate(guesses):
        logger.raw(f"\tByte {i}: {guess}\t (Correct: {hex(KEY[i])}) \t {'OK' if guess == hex(KEY[i]) else 'NOK'}")


if __name__ == "__main__":
    main()
