import tomllib
import logging

from .settings import Settings


def load_config_file(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def merge_config(cli_args, cfg_file: dict) -> Settings:
    settings = Settings()

    if "logging" in cfg_file:
        log_cfg = cfg_file["logging"]
        settings.log_level = getattr(logging, log_cfg.get("level", settings.log_level).upper())
        settings.log_format = log_cfg.get("format", settings.log_format)
        settings.log_datefmt = log_cfg.get("datefmt", settings.log_datefmt)

    if cli_args.log_level:
        settings.log_level = getattr(logging, cli_args.log_level.upper())

    return settings
