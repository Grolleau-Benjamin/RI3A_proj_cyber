NB_TRACES = 600

RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
ORANGE = "\033[38;5;208m"
LIGHTGREEN = "\033[38;5;154m"


def conf_color(p):
    if p >= 80:
        return LIGHTGREEN
    if p >= 60:
        return GREEN
    if p >= 40:
        return YELLOW
    if p >= 20:
        return ORANGE
    return RED
