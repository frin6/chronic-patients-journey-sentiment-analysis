import pandas as pd
from pathlib import Path
import json

class DataLoader:
    def __init__(self, data_path: str = "data/"):
        self.data_path = Path(data_path)

    def load_data(self):
        """
        Load the dataset from the data directory.
        Returns:
            pd.DataFrame: The loaded dataset
        """
        # List all files in data directory
        data_files = list(self.data_path.glob('*.csv'))  # Assuming it's a CSV file
        if not data_files:
            data_files = list(self.data_path.glob('*.json'))  # Try JSON if no CSV
        
        if not data_files:
            raise FileNotFoundError(f"No data files found in {self.data_path}")
        
        # Load the first file found
        file_path = data_files[0]
        
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        else:  # JSON
            df = pd.read_json(file_path)
            
        # Display info about the dataset
        print("\nDataset Info:")
        print(df.info())
        
        print("\nFirst few rows:")
        print(df.head())
        
        print("\nColumns:")
        print(df.columns.tolist())
        
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and normalize the dataset
        Args:
            df: Raw dataframe
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        # Create a copy to avoid modifying the original dataframe
        cleaned_df = df.copy()
        
        # Drop columns with all null values or irrelevant to analysis
        columns_to_drop = [
            'medical_journey_mapper_text',    # 0 non-null
            'migration_background',           # 0 non-null
            'questionnaire_graph_id',         # 0 non-null
            'patient_expenses',               # 0 non-null
            'tips',                          # irrelevant
            'documents'                       # irrelevant
        ]
        cleaned_df = cleaned_df.drop(columns=[col for col in columns_to_drop if col in cleaned_df.columns])
        
        # Handle missing values for location data (291/297 non-null)
        location_columns = ['latitude', 'longitude']
        for col in location_columns:
            if col in cleaned_df.columns:
                # Fill with median instead of mean for geographical coordinates
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
        
        # Handle sparse categorical data
        # family_history (8/297 non-null) - mark as 'Not Provided' if missing
        if 'family_history' in cleaned_df.columns:
            cleaned_df['family_history'] = cleaned_df['family_history'].fillna('Not Provided')
        
        # occupational_status (263/297 non-null) - mark as 'Unknown' if missing
        if 'occupational_status' in cleaned_df.columns:
            cleaned_df['occupational_status'] = cleaned_df['occupational_status'].fillna('Unknown')
        
        # Handle other categorical columns
        categorical_columns = [
            'biological_sex',
            'age_range', 
            'profession',
            'country',
            'postal_code',
            'educational_level',
            'ethnicity',
            'insurance'
        ]
        for col in categorical_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = cleaned_df[col].fillna('Unknown')
        
        # Handle numeric columns
        numeric_columns = ['time_to_diagnosis']
        for col in numeric_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
        
        # Clean chat_summary_per_phase
        if 'chat_summary_per_phase' in cleaned_df.columns:
            cleaned_df['chat_summary_per_phase'] = cleaned_df['chat_summary_per_phase'].apply(
                self._clean_chat_summary
            )
        
        # Convert date columns to datetime
        date_columns = [
            'date_of_conversation',
            'date_of_birth',
            'created_at',
            'latest_question_visit_created_at'
        ]
        for col in date_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
        
        # Drop irrelevant columns
        columns_to_drop = ['tips', 'documents']
        cleaned_df = cleaned_df.drop(columns=[col for col in columns_to_drop if col in cleaned_df.columns])
        
        # Save cleaned dataset to outputs
        output_path = Path("outputs/cleaned_dataset.csv")
        cleaned_df.to_csv(output_path, index=False)
        print(f"\nCleaned dataset saved to {output_path}")
        
        return cleaned_df
    
    def _clean_chat_summary(self, summary_str: str) -> dict:
        """Clean chat summary by removing tips and documents"""
        if not isinstance(summary_str, str):
            return {}
        
        try:
            summary_dict = json.loads(summary_str)
            # Remove tips and documents from each phase
            for phase in summary_dict:
                if isinstance(summary_dict[phase], dict):
                    summary_dict[phase].pop('tips', None)
                    summary_dict[phase].pop('documents', None)
            return summary_dict
        except json.JSONDecodeError:
            return {} 