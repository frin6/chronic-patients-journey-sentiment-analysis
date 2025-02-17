import logging
import sys
from pathlib import Path

def setup_logging(log_level=logging.INFO):
    """
    Setup logging configuration
    Args:
        log_level: Logging level (default: INFO)
    Returns:
        logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('patient_journey_analysis')
    logger.setLevel(log_level)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_dir / 'analysis.log')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 