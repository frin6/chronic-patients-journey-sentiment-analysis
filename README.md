# **Data Science Challenge Repository**

Welcome to the **Data Science Challenge Repository**! This repository is designed to assess candidates’ skills in handling messy, real-world healthcare data, building robust data pipelines, and deriving actionable insights. Below, you’ll find all the resources and instructions needed to complete the challenge.

---

## **Repository Structure**
```plaintext
repository_root/
├── src/        # Python source code
├── test/       # Unit tests
├── data/       # Provided dataset (challenge-specific)
├── outputs/    # Optional: Processed data or generated outputs
└── README.md   # Documentation (this file)
```

- **`src/`**: Place your Python scripts here. Ensure your code is modular, well-documented, and production-ready.
- **`test/`**: Include unit tests covering data cleaning, NLP models, and metrics calculations.
- **`data/`**: Contains the provided dataset. Delete this folder after the challenge as it contains synthetic data modeled after real healthcare scenarios.
- **`outputs/`**: *(Optional)* Store processed data or metrics outputs in this directory.

---

## **Dataset Overview**
The dataset, located in the `data/` directory, is synthetically generated to mimic real-world patient journey scenarios. It includes both structured and unstructured data and is designed to reflect common challenges in healthcare analytics.

### **Key Features**
- **Structured Data**: Includes fields such as `biological_sex`, `age_range`, `profession`, `country`, as well as numerical fields like `time_to_diagnosis`, `time_to_first_visit`, and `patient_expenses`.
- **Unstructured Text Data**: The `chat_summary_per_phase` field contains JSON-like objects summarizing patient conversations across different journey phases. Note that the `tips` and `documents` keys should be discarded, as they are irrelevant to the challenge.

### **Challenges**
- **Missing Values**: Fields like `location` and `gender` may be incomplete.
- **Inconsistent Formats**: Fields (e.g., dates, numerical ranges) may appear in varied formats or contain errors.
- **Partial Data**: The `chat_summary_per_phase` field may have incomplete or missing summaries for certain phases.
- **Heterogeneous Values**: Demographic fields (e.g., `biological_sex`, `occupation`) may have inconsistent representations for the same values.

---

## **Patient Journey Overview**
The patient journey captures the stages of care from symptom onset to recovery or long-term management. This challenge uses automated interview data, structured into the following key phases:

1. **Symptom Onset**: Initial symptoms appear.
2. **Pre-Diagnostic Phase**: Consultations and preliminary tests occur.
3. **Primary Diagnostic Phase**: Tests confirm a diagnosis.
4. **Decision Phase**: Treatment plans are established.
5. **New Treatment Phase**: Treatment begins, and progress is monitored.
6. **Ongoing Care Phase**: Long-term management of chronic conditions.
7. **Reevaluation Phase**: Periodic reassessment of treatments.

Each phase may have a corresponding summary in the `chat_summary_per_phase` field. Analyzing interrelationships across phases adds complexity to the challenge.

---

## **Objectives of the Challenge**

### 1. **Data Cleaning and Normalization**
- Normalize date formats.
- Handle missing demographic fields (e.g., `biological_sex`, `age_range`).
- Extract and process the `chat_summary_per_phase` field for patient journey analysis.

### 2. **NLP Analysis**
- **Topic Extraction**: Use a zero-shot classification model for text classification. Perform statistical analyses where relevant.
- **Sentiment Analysis**: Apply a pre-trained sentiment model to assess sentiment across phases. Conduct statistical analyses where applicable.
- **Patient Journey Overview**: 
  •	Objective: Represent the patient journey as a comprehensive, aggregated pathway that captures key milestones, challenges, and overall progress. The representation should balance a high-level overview with detailed insights into each phase. Here a few examples, but not limited to:
	-	**Phase-Based Aggregated Metrics**:
		-	Use visualizations like heatmaps or stacked bar charts to present aggregated metrics for each phase.
		-	Example Metrics:
			-	Average sentiment.
			-	Commonly discussed topics.
		-	Example:
			-	A heatmap showing sentiment intensity across phases to identify where patients encounter the most significant challenges.
	-	**Text Summary**:
		-	Generate a concise textual overview of the aggregated journey to highlight critical patterns and insights.
			-	Example 1: “Most patients experience a delay of X days between symptom onset and diagnosis.”
			-	Example 2: “The decision phase frequently correlates with negative sentiment due to treatment uncertainties.”
- **Partial Conversations** *(Optional)*: Handle incomplete summaries by assigning fallback labels or calculating a “Completeness Score.”

### 3. **Metrics Development**
- **Phase Completeness Score** *(Optional)*: Quantify the completeness of patient journey phases.

### 4. **Unit Testing and Production-Ready Code**
- Include robust tests for data cleaning, NLP inference, and metrics.
- Implement error handling, logging, and scalability best practices.

---

## **Evaluation Criteria**
Your submission will be assessed based on the following:

- **Data Handling**: Effectiveness in cleaning, normalizing, and handling missing data.
- **NLP and Statistical Analysis**: Accurate and meaningful insights from text and statistical analyses.
- **Metrics Actionability**: Insights must provide real-world value.
- **Code Quality**: Ensure modularity, maintainability, and comprehensive documentation.
- **Testing**: Thorough unit tests with coverage of edge cases.

---

## **How to Use This Repository**

### 1. **Clone the Repository**
```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. **Install Required Libraries**
Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. **Run Your Code**
Place your scripts in the `src/` directory and execute them from the repository root:
```bash
python src/your_script.py
```

### 4. **Run Unit Tests**
Include your tests in the `test/` directory and run them with:
```bash
pytest test/
```

### 5. **Save Output Results**
Store any outputs (e.g., metrics CSV, processed datasets) in the `outputs/` folder.

---

## **Deliverables**
1. **Code**: All Python scripts should be in the `src/` directory, structured for modularity and readability.
2. **Tests**: Include detailed unit tests in the `test/` directory.
3. **Documentation**: Add comments/docstrings explaining assumptions and logic. Update this README as needed.
4. **Metrics**: Save results in a structured format (e.g., CSV, JSON).

---

## **Important Notes**
- **Data Deletion Policy**: The dataset in `data/` must be deleted after the challenge.
- **Licensing and Usage**: This repository and its contents are for challenge use only. Redistribution or reuse is prohibited.

---

## **Contact**
For questions or technical issues, reach out to:

- **Name**: Lorenzo Famiglini  
- **Email**: lorenzo.famiglini@mamahealth.com
