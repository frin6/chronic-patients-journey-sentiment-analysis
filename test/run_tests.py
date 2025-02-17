import unittest
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from test_metrics_calculator import TestMetricsCalculator
from test_nlp_analyzer import TestNLPAnalyzer
from test_results_visualizer import TestResultsVisualizer

def run_tests():
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMetricsCalculator))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestNLPAnalyzer))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestResultsVisualizer))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

if __name__ == '__main__':
    run_tests() 