import argparse


def parse_cli_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config-file", help="Path to config file", default="app_config.toml"
    )

    parser.add_argument(
        "--log-level",
        default=None,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Override log level",
    )

    return parser.parse_args()
