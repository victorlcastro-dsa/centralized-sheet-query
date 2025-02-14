import logging


class LoggerConfig:
    """
    Logger configuration class to set up and obtain loggers.

    Methods:
        setup_logging(level): Sets up the logging configuration.
        get_logger(name): Returns a logger instance with the specified name.
    """

    @classmethod
    def setup_logging(cls, level=logging.INFO):
        """
        Sets up the logging configuration with the specified log level.

        Args:
            level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        """
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )

    @staticmethod
    def get_logger(name):
        """
        Returns a logger instance with the specified name.

        Args:
            name (str): Name of the logger.

        Returns:
            logging.Logger: Logger instance.
        """
        return logging.getLogger(name)
