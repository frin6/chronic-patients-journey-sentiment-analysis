import unittest
import logging
from src.utils.logging_config import setup_logging

class TestLogging(unittest.TestCase):
    def setUp(self):
        self.logger = setup_logging()

    def test_log_levels(self):
        """Test different logging levels"""
        with self.assertLogs(level='DEBUG') as log:
            self.logger.debug("Debug message")
            self.logger.info("Info message")
            self.logger.warning("Warning message")
            self.assertEqual(len(log.output), 3)

    def test_log_formatting(self):
        """Test log message formatting"""
        with self.assertLogs(level='INFO') as log:
            self.logger.info("Test message")
            self.assertRegex(log.output[0], r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')