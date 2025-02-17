import unittest
import pandas as pd
from src.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()
        self.sample_raw_data = pd.DataFrame({
            'patient_id': [1, 2],
            'chat_summary_per_phase': [
                {'early_symptoms_phase': 'test', 'invalid_phase': 'test'},
                {'early_symptoms_phase': None, 'diagnosis': ''}
            ]
        })

    def test_clean_chat_summaries(self):
        """Test chat summary cleaning"""
        cleaned_data = self.loader.clean_data(self.sample_raw_data)
        
        # Check structure
        self.assertIn('chat_summary_per_phase', cleaned_data.columns)
        
        # Check cleaning operations
        summary = cleaned_data.iloc[0]['chat_summary_per_phase']
        self.assertNotIn('invalid_phase', summary)  # Invalid phases removed
        
        # Check null handling
        summary = cleaned_data.iloc[1]['chat_summary_per_phase']
        self.assertNotIn('early_symptoms_phase', summary)  # Null values removed
        
    def test_validate_phase_names(self):
        """Test phase name validation"""
        valid_phases = {'early_symptoms_phase', 'diagnosis'}
        invalid_phases = {'unknown_phase', 'invalid_phase'}
        
        for phase in valid_phases:
            self.assertTrue(self.loader._validate_phase_name(phase))
        
        for phase in invalid_phases:
            self.assertFalse(self.loader._validate_phase_name(phase))

    def test_special_character_handling(self):
        """Test handling of special characters and formatting"""
        special_chars_data = pd.DataFrame({
            'patient_id': [1],
            'chat_summary_per_phase': [{
                'diagnosis': 'Patient\n\nhas\t\tspacing\r\nissues',
                'treatment': 'Contains <html> tags & special chars £$%'
            }]
        })
        
        cleaned = self.loader.clean_data(special_chars_data)
        summary = cleaned.iloc[0]['chat_summary_per_phase']
        
        # Check text cleaning
        self.assertNotIn('\t', summary['diagnosis'])
        self.assertNotIn('<html>', summary['treatment'])

    def test_duplicate_handling(self):
        """Test handling of duplicate patient records"""
        duplicate_data = pd.DataFrame({
            'patient_id': [1, 1],
            'chat_summary_per_phase': [
                {'diagnosis': 'first version'},
                {'diagnosis': 'second version'}
            ]
        })
        
        cleaned = self.loader.clean_data(duplicate_data)
        self.assertEqual(len(cleaned), 1)  # Should keep only one version 