import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.results_visualizer import ResultsVisualizer
from src.metrics_calculator import EXPECTED_PHASES
import pandas as pd
import os
from pathlib import Path

class TestResultsVisualizer(unittest.TestCase):
    def setUp(self):
        self.test_output_dir = "test_outputs"
        self.visualizer = ResultsVisualizer(output_dir=self.test_output_dir)
        
        # Sample results
        self.sample_sentiment = {
            'symptom_onset': [{'label': 'NEGATIVE', 'score': 0.8}],
            'primary_diagnostic': [{'label': 'NEUTRAL', 'score': 0.6}]
        }
        
        self.sample_topics = {
            'symptom_onset': [{'labels': ['symptoms'], 'scores': [0.9]}],
            'primary_diagnostic': [{'labels': ['diagnosis'], 'scores': [0.8]}]
        }
        
        self.sample_completeness = {
            'phase_completeness': {
                'symptom_onset': 0.8,
                'primary_diagnostic': 0.9
            }
        }

    def tearDown(self):
        # Clean up test output directory
        if os.path.exists(self.test_output_dir):
            for file in os.listdir(self.test_output_dir):
                os.remove(os.path.join(self.test_output_dir, file))
            os.rmdir(self.test_output_dir)

    def test_save_results_json(self):
        """Test JSON results saving"""
        self.visualizer._save_results_to_json({
            'sentiment': self.sample_sentiment,
            'topics': self.sample_topics,
            'completeness': self.sample_completeness
        })
        
        json_path = Path(self.test_output_dir) / 'analysis_results.json'
        self.assertTrue(json_path.exists())

    def test_plot_sentiment_analysis(self):
        """Test sentiment visualization"""
        self.visualizer._plot_sentiment_analysis(self.sample_sentiment)
        sentiment_plot_path = Path(self.test_output_dir) / 'sentiment_analysis.png'
        self.assertTrue(sentiment_plot_path.exists())

    def test_plot_topic_distribution(self):
        """Test topic visualization"""
        self.visualizer._plot_topic_distribution(self.sample_topics)
        topic_plot_path = Path(self.test_output_dir) / 'topic_distribution.png'
        self.assertTrue(topic_plot_path.exists())

    def test_filter_fallback_values(self):
        """Test filtering of fallback values in visualizations"""
        # Add a phase with fallback values
        sentiment_with_fallback = self.sample_sentiment.copy()
        sentiment_with_fallback['fallback_phase'] = [{'label': 'NEUTRAL', 'score': 0.5}]
        
        self.visualizer._plot_sentiment_analysis(sentiment_with_fallback)
        # Verify fallback phase is not included in visualization
        # This would require checking the actual plot data 

    def test_visualization_consistency(self):
        """Test that visualizations are consistent with input data"""
        # Add phase with all sentiment types
        self.sample_sentiment['test_phase'] = [
            {'label': 'POSITIVE', 'score': 0.8},
            {'label': 'NEGATIVE', 'score': 0.7},
            {'label': 'NEUTRAL', 'score': 0.6}
        ]
        
        # Generate visualization
        self.visualizer._plot_sentiment_analysis(self.sample_sentiment)
        
        # Could add checks for image properties, size, format
        sentiment_plot_path = Path(self.test_output_dir) / 'sentiment_analysis.png'
        self.assertTrue(sentiment_plot_path.exists())
        self.assertGreater(sentiment_plot_path.stat().st_size, 0) 