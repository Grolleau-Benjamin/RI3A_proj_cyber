# RI3A Cyber Project

## Usage
Run the program:
```bash
uv run main.py
```

## Command-line arguments
Set the log level:
```bash
uv run main.py --log-level DEBUG
```
Default log level is `DEBUG` and is defined in the configuration file (see below).

Use a custom config file:
```bash
uv run main.py --config-file path/to/config.toml
```
Default config file is `app_config.toml` in the project root.

## Configuration file (`app_config.toml`)
```toml
[logging]
level = "DEBUG"
format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
```