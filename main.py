from src.utils.logger import get_logger, init_logging
from src.config.cli import parse_cli_args
from src.config.settings import Settings
from src.config.loader import load_config_file, merge_config


def main():
    cli_args = parse_cli_args()
    cfg_file = load_config_file(cli_args.config)

    settings = merge_config(cli_args, cfg_file)

    init_logging(
        level=settings.log_level,
        fmt=settings.log_format,
        datefmt=settings.log_datefmt,
    )

    logger = get_logger(__name__)

    logger.info("Hello from ri3a-proj-cyber!")

    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

if __name__ == "__main__":
    main()
