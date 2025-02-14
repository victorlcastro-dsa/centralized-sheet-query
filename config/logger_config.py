import logging


class LoggerConfig:
    @classmethod
    def setup_logging(cls, level=logging.INFO):
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
