# RI3A Cyber Project

## Related notes
- [CPA Explanation (fr)](./papers/CPA_Explication)
- [DPA Explanation (fr)](./papers/DPA_Explication.pdf)

## Usage
Run the program:
```bash
uv run main.py
```

> [!TIP]
> The project takes around 1-2 minutes with a MACBook Pro M4 on 5000 traces when correlation plotting is enabled.

## Command-line arguments

Set the log level:
```bash
uv run main.py --log-level DEBUG
```
The default log level is defined in `app_config.toml` (current value: INFO).

Use a custom configuration file:
```bash
uv run main.py --config-file path/to/config.toml
```
The default configuration file is `app_config.toml` at the project root.

Enable plotting:
```bash
uv run main.py --plot
```

Plot the correlation of curves can be enabled with the flag `--plot-correlations`.
```bash
uv run main.py --plot-correlations
```

Set the number of traces to use for CPA analysis, (default: 100):
```bash
uv run main.py --nb-cpa-traces 200
```

## Logging
The project uses a colored logging system (colorama).  
Default values (from `src/utils/logger.py`):
- Default format: `[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s`
- Default date format: `%Y-%m-%dT%H:%M:%SZ`
- Color mapping:
  - DEBUG: blue
  - INFO: green
  - WARNING: yellow
  - ERROR: red
  - CRITICAL: magenta

These can be overridden by command-line arguments or by the configuration file.

## Configuration file (app_config.toml)
Example:
```toml
[logging]
level = "INFO"
format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

[output]
plot = false
```

## Notes
- DPA uses all available traces.
- CPA can be restricted to a smaller number of traces passed as a command-line argument (`--nb-cpa-traces`).
- Traces and inputs are loaded from NumPy files and written to mmap-backed binary files for fast processing.
