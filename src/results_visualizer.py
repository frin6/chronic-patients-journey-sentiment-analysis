import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
import json
from pathlib import Path
try:
    from .metrics_calculator import EXPECTED_PHASES
except ImportError:
    from metrics_calculator import EXPECTED_PHASES

class ResultsVisualizer:
    def __init__(self, output_dir: str = "outputs/"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def visualize_and_save_results(self, 
                                 sentiment_analysis: Dict, 
                                 topic_analysis: Dict, 
                                 completeness_metrics: Dict):
        """
        Visualize and save analysis results
        """
        
        # Saving raw results to JSON
        self._save_results_to_json({
            'sentiment': sentiment_analysis,
            'topics': topic_analysis,
            'completeness': completeness_metrics
        })
        
        self._plot_sentiment_analysis(sentiment_analysis)
        
        self._plot_topic_distribution(topic_analysis)
        
        self._plot_completeness_scores(completeness_metrics)
        
        print("All visualizations saved successfully!")
    
    def _save_results_to_json(self, results: Dict):
        """Save raw results to JSON file"""
        with open(self.output_dir / 'analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2)
    
    def _plot_sentiment_analysis(self, sentiment_results: Dict):
        """Create sentiment analysis visualization"""
        sentiment_data = []
        all_sentiments = {'POSITIVE', 'NEGATIVE', 'NEUTRAL'}
        
        # Define main phases only
        main_phases = ['symptom_onset', 'pre_diagnostic', 'primary_diagnostic', 'new_treatment', 'ongoing_care']
        
        # Create complete data, filtering out phases with only fallback values
        for phase in main_phases:  # Usa solo le fasi principali invece di EXPECTED_PHASES
            phase_sentiments = sentiment_results.get(phase, [])
            
            # Create a dict to store scores for each sentiment
            sentiment_scores = {s: 0.0 for s in all_sentiments}
            
            # Update with actual values
            has_real_values = False
            for s in phase_sentiments:
                # Check if this is not a fallback value (0.5)
                if s['score'] != 0.5:
                    has_real_values = True
                sentiment_scores[s['label']] = s['score']
            
            # Only include phases with real sentiment values
            if has_real_values:
                for sentiment, score in sentiment_scores.items():
                    sentiment_data.append({
                        'phase': phase,
                        'sentiment': sentiment,
                        'score': score
                    })
        
        df = pd.DataFrame(sentiment_data)
        
        # Create sentiment heatmap
        plt.figure(figsize=(12, 6))
        sentiment_pivot = df.pivot_table(
            values='score', 
            index='phase',
            columns='sentiment',
            aggfunc='mean',
            fill_value=0.0
        )
        
        # Reorder by main phases order
        sentiment_pivot = sentiment_pivot.reindex(main_phases)
        
        # Use a colormap that shows better shades
        sns.heatmap(
            sentiment_pivot, 
            annot=True, 
            cmap='RdYlGn',
            vmin=0, 
            vmax=1,
            fmt='.2f'
        )
        plt.title('Sentiment Analysis by Phase')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'sentiment_analysis.png')
        plt.close()
    
    def _plot_topic_distribution(self, topic_results: Dict):
        """Create topic distribution visualization"""
        topic_data = []
        
        # Filter phases with only zero scores and exclude additional phases
        main_phases = ['symptom_onset', 'pre_diagnostic', 'primary_diagnostic', 'new_treatment', 'ongoing_care']
        for phase, topics in topic_results.items():
            if phase not in main_phases:  # Skip additional phases
                continue
            for topic_list in topics:
                if any(score > 0.0 for score in topic_list['scores']):
                    for label, score in zip(topic_list['labels'], topic_list['scores']):
                        topic_data.append({
                            'phase': phase,
                            'topic': label,
                            'score': score
                        })
        
        df = pd.DataFrame(topic_data)
        
        # Create topic heatmap
        plt.figure(figsize=(15, 10))
        topic_pivot = df.pivot_table(
            values='score',
            index='phase',
            columns='topic',
            aggfunc='mean'
        )
        
        # Reorder by main phases
        topic_pivot = topic_pivot.reindex(main_phases)
        
        # Improve readability of labels
        sns.heatmap(
            topic_pivot, 
            annot=True, 
            cmap='YlOrRd',
            fmt='.2f',
            yticklabels=[label.replace('_', ' ').title() for label in topic_pivot.index]
        )
        
        plt.title('Topic Distribution by Phase', pad=20)
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'topic_distribution.png', bbox_inches='tight', dpi=300)
        plt.close()
    
    def _plot_completeness_scores(self, completeness_results: Dict):
        """Create completeness scores visualization"""
        plt.figure(figsize=(10, 6))
        
        # Reorder by EXPECTED_PHASES
        ordered_phases = [p for p in EXPECTED_PHASES if p in completeness_results['phase_completeness']]
        scores = [completeness_results['phase_completeness'][p] for p in ordered_phases]
        
        plt.bar(ordered_phases, scores)
        plt.title('Completeness Score by Phase')
        plt.xticks(rotation=45)
        plt.ylabel('Completeness Score')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'completeness_scores.png')
        plt.close() 