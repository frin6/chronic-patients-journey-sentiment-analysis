# Patient Journey Analysis Summary

## Overview
Analysis of patient journeys across 5 main phases: Symptom Onset, Pre-Diagnostic, Primary Diagnostic, New Treatment, and Ongoing Care.

## Completeness Analysis
Analysis of completeness scores across all phases:
- Main phases show consistently high completeness (0.75-0.82):
  - Highest completeness: Primary Diagnostic (0.82)
  - Strong performance: New Treatment (0.81) and Ongoing Care (0.79)
  - Consistent documentation: Symptom Onset (0.76) and Pre-Diagnostic (0.77)

- Additional phases show significantly lower completeness:
  - Decision phase: Very low completeness (0.10)
  - Reevaluation phase: Limited documentation (0.19)

- Overall trends:
  - Core treatment journey is well documented
  - Decision-making and follow-up reevaluation processes need more structured documentation
  - Clear gap between main phases (>0.75) and additional phases (<0.20)

## Sentiment Analysis
Clear sentiment patterns emerge across the main phases:
- Most positive phases: 
  - New Treatment (0.93 positive, 0.94 negative)
  - Ongoing Care (0.97 positive, 0.98 negative)
  - Primary Diagnostic (0.98 positive, 0.96 negative)
- Most negative phases:
  - Symptom Onset (1.00 negative)
  - Pre-Diagnostic (1.00 negative)
- Key observations: 
  - Clear progression from negative to positive sentiment as treatment progresses, which is expected
  - No neutral sentiments detected, indicating strong emotional experiences
  - Treatment phases show consistently positive sentiment
  - Sentiment aligns with typical patient journey: from initial concerns to successful treatment

## Topic Distribution
Dominant topics vary significantly by phase:
- Symptom Onset:
  - Highest: Symptoms (0.97), Diagnosis (0.80), Daily life impact (0.77)
  - Lowest: Medication (0.02), Emotional state (0.04)

- Pre-Diagnostic:
  - Highest: Doctor visits (0.93), Symptoms (0.96), Treatment (0.75)
  - Strong: Diagnosis (0.71), Medication (0.69)

- Primary Diagnostic:
  - Highest: Diagnosis (0.96), Symptoms (0.82)
  - Notable: Doctor visits (0.77), Daily life impact (0.73)

- New Treatment:
  - Highest: Side effects (0.95), Medication (0.94), Treatment (0.94)
  - Consistent: Symptoms (0.84), Daily life impact (0.84)

- Ongoing Care:
  - Highest: Treatment (0.93),  Daily life impact (0.88)
  - Strong: Symptoms (0.87), Emotional state (0.63)

## Key Insights
1. Documentation quality is consistently high across all main phases, indicating robust data collection
2. Patient sentiment shows clear progression from negative (early phases) to positive (treatment phases)
3. Topic focus evolves naturally: from symptoms/diagnosis to treatment/medication to ongoing management

## Recommendations
1. Consider enhancing emotional state and medication tracking in early phases
2. Maintain the strong documentation practices across all phases
3. Consider adding structured support for capturing treatment decisions and reevaluation data