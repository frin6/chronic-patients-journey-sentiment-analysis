import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.nlp_analyzer import NLPAnalyzer
from src.metrics_calculator import EXPECTED_PHASES
import pandas as pd

class TestNLPAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = NLPAnalyzer()
        self.sample_summary = {
            'early_symptoms_phase': 'Patient felt very worried about symptoms',
            'diagnosis': 'Doctor confirmed diagnosis, patient considered options',
            'treatment': 'Treatment going well, regular monitoring shows progress'
        }

    def test_extract_phase_content(self):
        """Test phase content extraction with keywords"""
        content = "Patient decided to proceed with treatment"
        self.assertTrue(self.analyzer._extract_phase_content(content, 'decision'))
        self.assertFalse(self.analyzer._extract_phase_content('', 'decision'))

    def test_analyze_single_summary(self):
        """Test analysis of a single patient summary"""
        results = self.analyzer._analyze_single_summary(self.sample_summary)
        
        # Check structure
        self.assertIn('sentiment', results)
        self.assertIn('topics', results)
        
        # Check sentiment results
        for phase, sentiment in results['sentiment'].items():
            self.assertIn('label', sentiment)
            self.assertIn('score', sentiment)
            self.assertGreaterEqual(sentiment['score'], 0.0)
            self.assertLessEqual(sentiment['score'], 1.0)
        
        # Check topic results
        for phase, topics in results['topics'].items():
            self.assertIn('labels', topics)
            self.assertIn('scores', topics)
            self.assertEqual(len(topics['labels']), len(topics['scores']))

    def test_batch_processing(self):
        """Test batch processing of summaries"""
        batch_size = 2
        sample_series = pd.Series([
            self.sample_summary,
            self.sample_summary,
            self.sample_summary
        ])
        
        results = self.analyzer.analyze_chat_summaries(sample_series)
        
        # Check all summaries were processed
        self.assertEqual(
            len(results['sentiment_per_phase']['symptom_onset']), 
            len(sample_series)
        )

    def test_error_handling(self):
        """Test error handling in analysis"""
        # Test with invalid input
        invalid_summary = {'invalid_phase': 'content'}
        results = self.analyzer._analyze_single_summary(invalid_summary)
        
        # Should return valid structure with fallback values
        self.assertIn('sentiment', results)
        self.assertIn('topics', results)
        
        # Verify that invalid phases have fallback values
        for phase in EXPECTED_PHASES:
            self.assertIn(phase, results['sentiment'])
            self.assertIn(phase, results['topics'])

    def test_keyword_extraction(self):
        """Test keyword-based phase extraction"""
        test_cases = [
            ("Patient decided to start treatment", "decision", True),
            ("Regular follow-up and monitoring", "reevaluation", True),
            ("Normal symptoms description", "decision", False)
        ]
        
        for content, phase, expected in test_cases:
            result = self.analyzer._extract_phase_content(content, phase)
            self.assertEqual(result, expected)

    def test_sentiment_consistency(self):
        """Test that sentiment analysis is consistent across similar texts"""
        similar_texts = [
            "Patient was very happy with the treatment",
            "Patient felt satisfied with the treatment outcome",
            "Treatment results were excellent"
        ]
        
        sentiments = []
        for text in similar_texts:
            result = self.analyzer.sentiment_analyzer(text)[0]
            sentiments.append(result['label'])
        
        # All positive texts should get consistent sentiment
        self.assertEqual(len(set(sentiments)), 1)
        self.assertEqual(sentiments[0], 'POSITIVE')

    def test_topic_relevance(self):
        """Test that topic scores are higher for relevant content"""
        test_cases = [
            ("Patient had severe headaches", "symptoms", 0.7),
            ("Doctor prescribed new medication", "medication", 0.7),
            ("Regular visits to the clinic", "doctor visits", 0.7)
        ]
        
        for text, expected_topic, min_score in test_cases:
            result = self.analyzer.zero_shot_classifier(text, 
                                                      candidate_labels=[expected_topic],
                                                      multi_label=True)
            self.assertGreater(result['scores'][0], min_score)