import logging
import os
from datetime import datetime

class DynamicLogger:
    def __init__(self):
        self.current_logger = None
        self.current_log_file = None
    
    def _setup_new_logger(self):
        """Create a new logger with a fresh timestamp"""
        # Generate a new timestamp for this logging session
        LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
        os.makedirs(logs_path, exist_ok=True)
        LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
        
        # Create a unique logger name to avoid conflicts
        logger_name = f"training_logger_{LOG_FILE}"
        new_logger = logging.getLogger(logger_name)
        new_logger.setLevel(logging.INFO)
        
        # Remove any existing handlers
        for handler in new_logger.handlers[:]:
            new_logger.removeHandler(handler)
        
        # Create file handler
        file_handler = logging.FileHandler(LOG_FILE_PATH)
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        new_logger.addHandler(file_handler)
        
        self.current_logger = new_logger
        self.current_log_file = LOG_FILE_PATH
        return new_logger
    
    def info(self, message):
        if self.current_logger is None:
            self._setup_new_logger()
        self.current_logger.info(message)
    
    def error(self, message):
        if self.current_logger is None:
            self._setup_new_logger()
        self.current_logger.error(message)
    
    def warning(self, message):
        if self.current_logger is None:
            self._setup_new_logger()
        self.current_logger.warning(message)
    
    def debug(self, message):
        if self.current_logger is None:
            self._setup_new_logger()
        self.current_logger.debug(message)
    
    def get_new_logger(self):
        """Force create a new logger (useful for new training runs)"""
        # Reset current logger to force creation of a new one
        self.current_logger = None
        self.current_log_file = None
        return self._setup_new_logger()

# Create the logger instance that will be imported
logger = DynamicLogger()