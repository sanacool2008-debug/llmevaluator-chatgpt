import logging
import os
from src.path_setup import LOG_DIR, LOG_FPATH
from functools import wraps

def logger_setup(name, log_dir=LOG_DIR, log_file=LOG_FPATH, level=logging.DEBUG):
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s -%(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def get_logger(name=None):
    return logging.getLogger(name)

def log_call_with_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.info(f"Calling: {func.__name__} | args={args} | kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Finished: {func.__name__} | result={result}")
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__name__}")
            raise
    return wrapper

