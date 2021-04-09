import logging

class Logger:
    @staticmethod
    def get_logger(logger_name="logging", level=logging.INFO):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
