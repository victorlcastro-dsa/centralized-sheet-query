import logging


class LoggerConfig:
    @staticmethod
    def setup_logging(level=logging.INFO):
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
