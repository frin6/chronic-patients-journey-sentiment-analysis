from data_loader import DataLoader
from nlp_analyzer import NLPAnalyzer
from metrics_calculator import MetricsCalculator
from results_visualizer import ResultsVisualizer
from pathlib import Path

def main():
    # Initialize components
    data_loader = DataLoader()
    nlp_analyzer = NLPAnalyzer()
    metrics_calc = MetricsCalculator()
    visualizer = ResultsVisualizer()
    
    # Load and clean data
    raw_data = data_loader.load_data()
    clean_data = data_loader.clean_data(raw_data)
    
    # Save cleaned dataset
    output_path = Path("outputs/cleaned_dataset.csv")
    clean_data.to_csv(output_path, index=False)
    print(f"\nCleaned dataset saved to {output_path}")

    # Analyze text data
    print("Performing NLP analysis...")
    text_analysis = nlp_analyzer.analyze_chat_summaries(clean_data['chat_summary_per_phase'])

    # Calculate metrics
    completeness_scores = metrics_calc.calculate_phase_completeness(clean_data)

    # Visualize and save results
    visualizer.visualize_and_save_results(
        text_analysis['sentiment_per_phase'],
        text_analysis['topics_per_phase'],
        completeness_scores
    )
    
    print("Analysis complete! Results saved in outputs/")

if __name__ == "__main__":
    main() 