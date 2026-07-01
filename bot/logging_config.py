"""
Logging configuration for the trading bot.
Configures file and console handlers, ensuring secrets are not logged.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_dir: str = "logs", log_file: str = "trading.log") -> None:
    """
    Sets up the logging configuration for the entire application.
    
    Creates the log directory if it does not exist and configures the formatting
    and handlers for log output.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, log_file)

    # Define log message format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Rotating File Handler (10 MB max size, keeps 5 backup files)
    file_handler = RotatingFileHandler(
        log_path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove any existing handlers to prevent duplicates
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(file_handler)
    
    # Set levels for third-party libraries (e.g. urllib3, binance) to prevent log clutter
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("binance").setLevel(logging.WARNING)
