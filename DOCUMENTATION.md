# Patient Journey Analysis Documentation

## System Overview
This system analyzes patient journey data to extract insights about the completeness, sentiment, and topics discussed in each phase of the medical journey.

## Core Components

### 1. Data Structure
- Patient journeys are divided into chronological phases
- Each phase contains text descriptions of patient experiences
- Raw data phases:
  - early_symptoms_phase
  - referral_pathway
  - diagnosis
  - treatment
  - ongoing_care
  - documents
  - tips
  - confounding_factors

### 2. Phase Mapping
We map raw data phases to standardized phases for analysis:
```python
PHASE_MAPPING = {
    'early_symptoms_phase': 'symptom_onset',
    'referral_pathway': 'pre_diagnostic',
    'diagnosis': 'primary_diagnostic',
    'treatment': 'new_treatment',
    'ongoing_care': 'ongoing_care'
}
```

Additional phases are extracted through keyword analysis:
```python
ADDITIONAL_PHASE_MAPPING = {
    'diagnosis': ['decision'],
    'treatment': ['reevaluation']
}
```

### 3. Completeness Analysis
Completeness score (0.0-1.0) is calculated based on:
- Content length (70% of score)
  - Maximum score at 500 characters
  - Linear scaling below that
- Medical terminology presence (30% of score)
  - Each key medical term adds 0.06 to score
  - Terms: diagnosis, treatment, symptoms, doctor, medication

### 4. Sentiment Analysis
- Uses transformers sentiment analysis pipeline
- Three categories: POSITIVE, NEGATIVE, NEUTRAL
- Fallback to NEUTRAL (0.5) when analysis fails
- Sentiment scores are not normalized to preserve intensity

### 5. Topic Analysis
Uses zero-shot classification for topics:
- symptoms
- diagnosis
- treatment
- medication
- side effects
- doctor visits
- emotional state
- daily life impact

## Processing Flow

1. **Data Loading**
   - Load raw patient journey data
   - Clean and structure the data
   - Map to standardized phases

2. **Completeness Analysis**
   - Calculate base scores from content length
   - Add bonus for medical terminology
   - Weight scores by phase importance

3. **Text Analysis**
   - Analyze sentiment per phase
   - Classify topics in content
   - Extract additional phases

4. **Visualization**
   - Generate heatmaps for sentiment
   - Create topic distribution visualizations
   - Plot completeness scores

## Limitations and Considerations

1. **Data Quality**
   - Missing phases affect overall analysis
   - Text quality impacts sentiment accuracy
   - Language model limitations

2. **Phase Detection**
   - Keyword-based detection may miss context
   - Some phases may overlap
   - Additional phases may be less reliable

3. **Performance**
   - NLP operations are computationally intensive
   - Batch size affects memory usage
   - Caching helps but has memory implications 

## Possible Improvements

1. **Enhanced Phase Detection**
   - Implement contextual analysis instead of simple keyword matching
   - Train a custom classifier for phase detection
   - Fine-tune sentiment model on medical domain text

2. **Topic Analysis Enhancement**
   - Add medical-specific topics based on domain expertise
   - Implement hierarchical topic modeling
   - Consider temporal relationships between topics across phases

3. **Performance Optimization**
   - Implement distributed processing for large datasets
   - Optimize batch sizes based on available hardware
   - Add incremental processing capabilities
