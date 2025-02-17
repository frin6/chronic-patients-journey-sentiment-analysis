from transformers import pipeline
from typing import Dict, List
import pandas as pd
from tqdm import tqdm
try:
    # Try relative import first (for when used as a package)
    from .metrics_calculator import PHASE_MAPPING, EXPECTED_PHASES, PHASE_KEYWORDS
except ImportError:
    # Fallback to absolute import (for when run directly)
    from metrics_calculator import PHASE_MAPPING, EXPECTED_PHASES, PHASE_KEYWORDS
from multiprocessing import Pool
import multiprocessing
from functools import lru_cache

class NLPAnalyzer:
    def __init__(self):
        # Initialize sentiment analysis model with explicit model name
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
            revision="714eb0f"
        )
        
        # Initialize zero-shot classifier with explicit model name
        self.zero_shot_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            revision="d7645e1"
        )
        
        # Define topics for classification
        self.topics = [
            "symptoms",
            "diagnosis",
            "treatment",
            "medication",
            "side effects",
            "doctor visits",
            "emotional state",
            "daily life impact"
        ]
        
        # Define phase mapping (same as in MetricsCalculator)
        self.phase_mapping = PHASE_MAPPING
        
        # Define fallback values
        self.fallback_sentiment = {
            'label': 'NEUTRAL',
            'score': 0.5
        }
        self.fallback_topics = {
            'labels': self.topics,
            'scores': [0.0] * len(self.topics)
        }
    
    def analyze_chat_summaries(self, chat_summaries: pd.Series) -> Dict:
        """
        Analyze chat summaries using NLP techniques
        Args:
            chat_summaries: Series of chat summary dictionaries
        Returns:
            dict: Analysis results containing sentiment and topics per phase
        """
        results = {
            'sentiment_per_phase': {},
            'topics_per_phase': {}
        }
        
        print(f"\nAnalyzing {len(chat_summaries)} patient summaries...")
        
        # Process summaries in batches for better performance
        batch_size = 8
        for i in tqdm(range(0, len(chat_summaries), batch_size), desc="Processing patients"):
            batch = chat_summaries.iloc[i:i+batch_size]
            
            # Process each summary in the batch
            for summary in batch:
                phase_results = self._analyze_single_summary(summary)
                
                # Aggregate results
                for phase, phase_data in phase_results['sentiment'].items():
                    if phase not in results['sentiment_per_phase']:
                        results['sentiment_per_phase'][phase] = []
                    results['sentiment_per_phase'][phase].append(phase_data)
                
                for phase, phase_data in phase_results['topics'].items():
                    if phase not in results['topics_per_phase']:
                        results['topics_per_phase'][phase] = []
                    results['topics_per_phase'][phase].append(phase_data)
        
        return results
    
    def _analyze_single_summary(self, summary: Dict) -> Dict:
        """
        Analyze a single patient's chat summaries
        Args:
            summary: Dictionary containing chat summaries per phase
        Returns:
            dict: Analysis results for this summary with fallback values for missing data
        """
        results = {
            'sentiment': {},
            'topics': {}
        }
        
        # Initialize all expected phases with fallback values
        for phase in EXPECTED_PHASES:
            results['sentiment'][phase] = self.fallback_sentiment
            results['topics'][phase] = self.fallback_topics
        
        # Analyze mapped phases
        for dataset_phase, expected_phases in PHASE_MAPPING.items():
            content = summary.get(dataset_phase, '')
            if not content or not isinstance(content, str):
                continue
            
            # Convert to list if single string
            if isinstance(expected_phases, str):
                expected_phases = [expected_phases]
            
            for expected_phase in expected_phases:
                # Skip if phase requires specific keywords and none are found
                if expected_phase in PHASE_KEYWORDS and not self._extract_phase_content(content, expected_phase):
                    continue
                
                try:
                    # Get raw sentiment scores
                    sentiment = self.sentiment_analyzer(content)[0]
                    
                    # Amplify the dominant sentiment
                    if sentiment['score'] > 0.6:  # Solo se il modello è abbastanza sicuro
                        sentiment['score'] = max(sentiment['score'], 0.9)  # Aumenta il punteggio
                    
                    results['sentiment'][expected_phase] = sentiment
                except Exception:
                    results['sentiment'][expected_phase] = self.fallback_sentiment
                
                try:
                    # Topic classification
                    topic_result = self.zero_shot_classifier(
                        content,
                        candidate_labels=self.topics,
                        multi_label=True
                    )
                    results['topics'][expected_phase] = topic_result
                except Exception:
                    results['topics'][expected_phase] = self.fallback_topics
        
        return results 

    def _extract_phase_content(self, content: str, phase: str) -> bool:
        """
        Check if content contains keywords related to a specific phase
        Args:
            content: Text content to analyze
            phase: Phase to check for
        Returns:
            bool: True if content contains keywords for the phase
        """
        if not content:
            return False
        
        keywords = PHASE_KEYWORDS.get(phase, [])
        return any(keyword.lower() in content.lower() for keyword in keywords) 

    @lru_cache(maxsize=1000)
    def _analyze_content(self, content: str) -> tuple:
        """Analyze content and cache results"""
        sentiment = self.sentiment_analyzer(content)[0]
        topics = self.zero_shot_classifier(content, candidate_labels=self.topics, multi_label=True)
        return sentiment, topics 