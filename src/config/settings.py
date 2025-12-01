import logging


class Settings:
    def __init__(self):
        self.log_level = logging.INFO
        self.log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        self.log_datefmt = "%Y-%m-%d %H:%M:%S"
        self.plot = False
        self.plot_correlations = False
        self.nb_cpa_traces = 100
