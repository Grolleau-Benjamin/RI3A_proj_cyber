import logging
from src.guesser.plots import save_trace_plot
from src.utils.logger import get_logger, init_logging
from src.config.cli import parse_cli_args
from src.config.loader import load_config_file, merge_config
from src.utils.data_loader import load_traces, load_textin
from src.context.shared import save_array_to_mmap
from src.guesser.dpa import (
    dpa_guesser,
)
from src.guesser.cpa import (
    cpa_guesser,
)
from src.guesser.convergence import (
    plot_all_bytes_parallel,
    plot_all_bytes_parallel_cpa,
)
from src.utils.colors import RED, GREEN, BOLD, RESET, conf_color

KEY = [
    0x2B,  # Byte 0
    0x7E,  # Byte 1
    0x15,  # ...
    0x16,
    0x28,
    0xAE,
    0xD2,
    0xA6,
    0xAB,
    0xF7,  # Byte 9
    0x15,
    0x88,
    0x09,
    0xCF,
    0x4F,
    0x3C,
]


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
    logger.info(
        "Program started, log level: %s", logging.getLevelName(settings.log_level)
    )

    traces = load_traces("data/traces.npy")
    textin = load_textin("data/textin.npy")

    logger.info("Traces shape: %s", traces.shape)
    logger.info("Textin shape: %s", textin.shape)

    logger.debug("Trace[0]: %s", traces[0])
    logger.debug("Textin[0]: %s", textin[0])

    traces_file, traces_shape, traces_dtype = save_array_to_mmap(
        traces, "data/traces.bin"
    )
    textin_file, textin_shape, textin_dtype = save_array_to_mmap(
        textin, "data/textin.bin"
    )

    logger.info("Starting guessing process")
    if settings.plot:
        logger.info("[+] Plotting enabled")

    if settings.plot:
        save_trace_plot(traces[:5])

    guesses: list[dict] = dpa_guesser(
        traces_file,
        traces_shape,
        traces_dtype,
        textin_file,
        textin_shape,
        textin_dtype,
        {
            "level": settings.log_level,
            "fmt": settings.log_format,
            "datefmt": settings.log_datefmt,
        },
        plotting=settings.plot,
    )

    #  pylint: disable=E1136
    logger.info("Key guessed: %s", [r["guess"] for r in guesses])

    logger.raw("")
    logger.raw("=== DPA BYTE SUMMARY ===")
    logger.raw("Byte | Guess  | Correct | Status | Confidence | Second Best")
    logger.raw(
        "-----+--------+---------+--------+------------+------------------------"
    )

    for i, result in enumerate(guesses):
        guess_hex = f"0x{int(result['guess'], 16):02x}"
        correct_hex = f"0x{KEY[i]:02x}"

        ok = guess_hex == correct_hex
        status = f"{GREEN}OK {RESET}" if ok else f"{BOLD}{RED}NOK{RESET}"

        pct = result["confidence"] * 100
        color = conf_color(pct)
        conf_str = f"{color}{pct:6.2f}%{RESET}"

        if not ok:
            second_hex = f"0x{result['second_guess']:02x}"
            logger.raw(
                f"{i:>4} | {guess_hex:>6} | {correct_hex:>7} |    {status:>6} |    "
                f"{conf_str:>10} | {second_hex} ({round(result['second'], 5)} vs {round(result['best'], 5)})"
            )
        else:
            logger.raw(
                f"{i:>4} | {guess_hex:>6} | {correct_hex:>7} |    {status:>6} |    "
                f"{conf_str:>10} |"
            )

    traces_cpa = traces[: settings.nb_cpa_traces]
    textin_cpa = textin[: settings.nb_cpa_traces]

    traces_cpa_file, traces_cpa_shape, traces_cpa_dtype = save_array_to_mmap(
        traces_cpa, "data/traces_cpa.bin"
    )
    textin_cpa_file, textin_cpa_shape, textin_cpa_dtype = save_array_to_mmap(
        textin_cpa, "data/textin_cpa.bin"
    )

    guesses: list[dict] = cpa_guesser(
        traces_cpa_file,
        traces_cpa_shape,
        traces_cpa_dtype,
        textin_cpa_file,
        textin_cpa_shape,
        textin_cpa_dtype,
        plotting=settings.plot,
    )
    logger.info("Key guessed: %s", [r["guess"] for r in guesses])
    logger.raw("")
    logger.raw("=== CPA BYTE SUMMARY ===")
    logger.raw("Byte | Guess  | Correct | Status | Confidence | Second Best")
    logger.raw(
        "-----+--------+---------+--------+------------+------------------------"
    )
    for i, result in enumerate(guesses):
        guess_hex = f"0x{int(result['guess'], 16):02x}"
        correct_hex = f"0x{KEY[i]:02x}"

        ok = guess_hex == correct_hex
        status = f"{GREEN}OK {RESET}" if ok else f"{BOLD}{RED}NOK{RESET}"

        pct = result["confidence"] * 100
        color = conf_color(pct)
        conf_str = f"{color}{pct:6.2f}%{RESET}"

        if not ok:
            second_hex = f"0x{result['second_guess']:02x}"
            logger.raw(
                f"{i:>4} | {guess_hex:>6} | {correct_hex:>7} |    {status:>6} |    "
                f"{conf_str:>10} | {second_hex} ({round(result['second'], 5)} vs {round(result['best'], 5)})"
            )
        else:
            logger.raw(
                f"{i:>4} | {guess_hex:>6} | {correct_hex:>7} |    {status:>6} |    "
                f"{conf_str:>10} |"
            )

    if settings.plot_correlations:
        logger.raw("=========================")
        logger.raw("Plotting all guesses convergence for each byte...")
        plot_all_bytes_parallel(
            traces,
            textin,
            {
                "level": settings.log_level,
                "fmt": settings.log_format,
                "datefmt": settings.log_datefmt,
            },
        )

        logger.raw("Done.")
        logger.raw("=========================")
        logger.raw("Plotting all guesses convergence for each byte... (CPA)")
        plot_all_bytes_parallel_cpa(
            traces_cpa,
            textin_cpa,
            {
                "level": settings.log_level,
                "fmt": settings.log_format,
                "datefmt": settings.log_datefmt,
            },
        )

        logger.raw("Done.")
        logger.raw("=========================")


if __name__ == "__main__":
    main()
