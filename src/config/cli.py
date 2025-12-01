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

    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate plots after processing",
    )

    parser.add_argument(
        "--plot-correlations",
        action="store_true",
        help="Generate correlation plots after processing",
    )

    parser.add_argument(
        "--nb-cpa-traces",
        type=int,
        default=None,
        help="Number of traces to use for CPA analysis",
    )

    return parser.parse_args()
