# Logging configuration
import logging
import os
from datetime import datetime

def get_logger(name):
    # Create logs directory if not exists
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Generate a unique filename for this session
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f'logs/session_{timestamp}.log'

    # Create a new logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Remove any existing handlers to avoid duplicate logging
    logger.handlers = []

    # Create a file handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatting configuration
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
