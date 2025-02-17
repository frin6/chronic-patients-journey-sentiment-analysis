import pandas as pd
from typing import Dict, List
from tqdm import tqdm

# Phase mapping from dataset to README phases
PHASE_MAPPING = {
    'early_symptoms_phase': 'symptom_onset',
    'referral_pathway': 'pre_diagnostic',
    'diagnosis': 'primary_diagnostic',      # torniamo al mapping diretto
    'treatment': 'new_treatment',           # torniamo al mapping diretto
    'ongoing_care': 'ongoing_care'
}

# Additional phase mappings for keyword search
ADDITIONAL_PHASE_MAPPING = {
    'diagnosis': ['decision'],              # cerca solo decision come extra
    'treatment': ['reevaluation']           # cerca solo reevaluation come extra
}

# Keywords per identificare le fasi
PHASE_KEYWORDS = {
    'decision': ['decide', 'decision', 'chose', 'choice', 'opt', 'option', 'consider'],
    'reevaluation': ['reevaluation', 'reassess', 'follow-up', 'follow up', 'monitoring', 'review']
}

# Expected phases from README (for consistent visualization)
EXPECTED_PHASES = [
    'symptom_onset',
    'pre_diagnostic', 
    'primary_diagnostic',
    'decision',
    'new_treatment',
    'ongoing_care',
    'reevaluation'
]

class MetricsCalculator:
    def __init__(self):
        # Weights for different phases (as per README importance)
        self.phase_weights = {
            'symptom_onset': 1.0,
            'pre_diagnostic': 1.0,
            'primary_diagnostic': 1.5,  # More important phase
            'decision': 1.2,
            'new_treatment': 1.3,
            'ongoing_care': 1.0,
            'reevaluation': 1.0
        }
    
    def calculate_phase_completeness(self, patient_data: pd.DataFrame) -> Dict:
        """
        Calculate completeness scores for patient journey phases
        Args:
            patient_data: Cleaned patient data
        Returns:
            dict: Completeness metrics
        """
        # Debug: analyze first patient's data structure
        first_summary = patient_data.iloc[0]['chat_summary_per_phase']
        print("\nDEBUG - First Patient Chat Summary Structure:")
        print(f"Type: {type(first_summary)}")
        print("Content sample:")
        for phase, content in first_summary.items():
            print(f"\n{phase}:")
            print(f"- Type: {type(content)}")
            print(f"- Value: {str(content)[:100]}...")  # First 100 chars
        
        # Continue with normal processing...
        results = {
            'overall_completeness': [],
            'phase_completeness': {},
            'demographic_analysis': {}
        }
        
        print(f"\nCalculating completeness for {len(patient_data)} patients...")
        for _, row in tqdm(patient_data.iterrows(), desc="Processing completeness"):
            chat_summary = row['chat_summary_per_phase']
            completeness = self._calculate_single_patient_completeness(chat_summary)
            results['overall_completeness'].append(completeness['overall'])
            
            # Aggregate phase-specific completeness
            for phase, score in completeness['phases'].items():
                if phase not in results['phase_completeness']:
                    results['phase_completeness'][phase] = []
                results['phase_completeness'][phase].append(score)
        
        # Calculate averages
        results['overall_completeness'] = sum(results['overall_completeness']) / len(results['overall_completeness'])
        for phase in results['phase_completeness']:
            scores = results['phase_completeness'][phase]
            results['phase_completeness'][phase] = sum(scores) / len(scores)
        
        # Debug: print final phase completeness
        print("\nDEBUG - Final Phase Completeness:")
        for phase, score in results['phase_completeness'].items():
            print(f"{phase}: {score:.2f}")
        
        return results
    
    def _extract_phase_content(self, content: str, phase: str) -> bool:
        """Check if content contains keywords related to a specific phase"""
        if not content:
            return False
        
        keywords = PHASE_KEYWORDS.get(phase, [])
        return any(keyword.lower() in content.lower() for keyword in keywords)

    def _calculate_single_patient_completeness(self, chat_summary: Dict) -> Dict:
        results = {
            'overall': 0.0,
            'phases': {}
        }
        
        total_weight = sum(self.phase_weights.values())
        weighted_sum = 0
        
        # Process main phases
        for dataset_phase, expected_phase in PHASE_MAPPING.items():
            content = chat_summary.get(dataset_phase, '')
            if content and isinstance(content, str):
                # Calculate score for main phase
                phase_score = self._calculate_content_score(content)
                results['phases'][expected_phase] = phase_score
                weighted_sum += phase_score * self.phase_weights[expected_phase]
                
                # Check for additional phases in this content
                additional_phases = ADDITIONAL_PHASE_MAPPING.get(dataset_phase, [])
                for add_phase in additional_phases:
                    if self._extract_phase_content(content, add_phase):
                        phase_score = self._calculate_content_score(content)
                        results['phases'][add_phase] = phase_score
                        weighted_sum += phase_score * self.phase_weights[add_phase]
                    else:
                        results['phases'][add_phase] = 0.0
        
        results['overall'] = weighted_sum / total_weight
        return results

    def _calculate_content_score(self, content: str) -> float:
        """Calculate score for a piece of content"""
        content = content.strip()
        if not content:
            return 0.0
        
        # Base score from content length (0.0 - 0.7)
        length_score = min(len(content) / 500, 0.7)
        
        # Additional score for key medical terms (0.0 - 0.3)
        medical_terms = ['diagnosis', 'treatment', 'symptoms', 'doctor', 'medication']
        term_score = sum(0.06 for term in medical_terms if term.lower() in content.lower())
        
        return length_score + term_score 