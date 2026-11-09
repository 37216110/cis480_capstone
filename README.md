# cis480_capstone
Predictive Maintenance & Machine Failure Analysis

# SIPJOLT – Predictive Maintenance Analytics

## Project Overview

SIPJOLT is a predictive maintenance analytics project developed as part of CIS480 Capstone. The goal is to explore how machine learning and data visualization can help identify potential equipment failures before they occur.

Our team developed and evaluated machine learning models using manufacturing equipment data. We compared different modeling approaches, analyzed their performance, and created visualizations to better understand relationships between operating conditions and equipment failures.

The project focuses on supporting data-driven maintenance decisions while recognizing the limitations of predictive models.

## Project Objectives

The primary objectives of this project are to:

- Analyze manufacturing equipment data to identify patterns associated with machine failures.
- Develop and compare Logistic Regression and Random Forest classification models.
- Evaluate model performance using recall, precision, accuracy, F1 score, and false-positive rate.
- Explore operating conditions through Tableau visualizations.
- Test model behavior under different operating conditions.
- Identify limitations, risks, and opportunities for future improvements.

## Dataset

This project uses the **AI4I 2020 Predictive Maintenance Dataset** from the UCI Machine Learning Repository.

The dataset contains 10,000 synthetic manufacturing observations and includes the following operating measurements:

- Air temperature (K)
- Process temperature (K)
- Rotational speed (RPM)
- Torque (Nm)
- Tool wear (minutes)
- Product type
- Machine failure indicators

### Data Preparation

During preprocessing, our team identified and removed 27 observations containing inconsistent failure labels.

This resulted in:

| Dataset | Records |
|---|---:|
| Original dataset | 10,000 |
| Removed inconsistent records | 27 |
| Cleaned dataset | 9,973 |
| Failure records in cleaned dataset | 330 |

The cleaned dataset was used to evaluate updated versions of our classification models.

## Methods and Tools

The project uses the following technologies:

- **Python:** Data preparation, modeling, evaluation, and boundary testing.
- **Scikit-learn:** Logistic Regression and Random Forest classification.
- **Jupyter Notebook:** Model development and reproducible analysis.
- **Tableau:** Exploratory data visualization.
- **GitHub:** Version control, documentation, and project evidence.

### Machine Learning Models

We evaluated two classification approaches:

**Logistic Regression:** A baseline classification model used to establish a comparison for predictive performance.

**Random Forest:** An ensemble classification model used to capture more complex relationships between operating measurements and equipment failures.

Random Forest was selected as the preferred candidate because it detected a substantially larger proportion of actual failures.

## Model Performance

The following results are based on the cleaned dataset.

| Metric | Random Forest | Logistic Regression |
|---|---:|---:|
| Accuracy | 97.89% | 97.04% |
| Recall | 78.79% | 16.67% |
| Precision | 65.00% | 73.33% |
| F1 Score | 71.23% | 27.16% |
| False-Positive Rate | 1.45% | 0.21% |

### Performance Evaluation

Because machine failures are relatively uncommon, accuracy alone is not sufficient to evaluate model performance.

Recall is particularly important because it measures the proportion of actual failures correctly identified.

Our team established provisional evaluation thresholds:

- Minimum recall: **75%**
- Maximum false-positive rate: **2%**

The cleaned Random Forest model met both thresholds.

These thresholds are intended for project evaluation and do not establish that the model is ready for operational deployment.

### Modeling Evidence

Modeling notebooks and evaluation results are available in the [modeling directory](https://github.com/37216110/cis480_capstone/tree/main/notebooks/modeling).

## Boundary Testing

During Week 11, the team expanded its evaluation by examining how model predictions respond to different operating conditions.

The boundary testing focused on combinations of:

- Torque (Nm)
- Tool wear (minutes)

Heatmaps were created to visualize predicted machine-failure probabilities across different combinations of these measurements.

### Key Observations

The boundary-testing visualizations demonstrate that predicted failure probabilities can change significantly as operating conditions vary.

Some combinations of high torque and tool wear produce substantially higher predicted failure probabilities.

The tests also highlight the importance of examining model behavior near the boundaries of the available data.

**Important:** The heatmaps display model-generated probabilities, not actual observed failure rates. These predictions have not been validated using real manufacturing equipment.

The boundary tests provide evidence about model behavior under the tested conditions, but they do not establish that the predictions are accurate outside the training data distribution.

## Data Visualizations

Tableau was used to explore relationships between manufacturing operating conditions.

The visualization workbook includes:

- Air temperature versus process temperature.
- Torque versus rotational speed for product type H.
- Torque versus rotational speed for product type L.
- Torque versus rotational speed for product type M.

These visualizations support exploratory analysis and help identify differences in operating conditions across product types.

However, descriptive visualizations do not independently establish the causes of equipment failures or validate model predictions.

## Project Limitations

The project has several important limitations that should be considered when interpreting its findings.

### 1. Synthetic Data

The dataset contains simulated manufacturing observations rather than measurements collected from actual equipment.

Although synthetic data is useful for developing and testing models, it may not represent all real-world operating conditions, equipment behaviors, or failure mechanisms.

Model performance on synthetic data cannot guarantee similar performance in an actual manufacturing environment.

### 2. Class Imbalance

Machine failures represent a small percentage of the dataset.

This imbalance means that a model can achieve high overall accuracy while failing to identify many actual equipment failures.

For this reason, recall, precision, and false-positive rate are emphasized alongside accuracy.

### 3. Missed Failures and False Alarms

The Random Forest model does not identify every actual failure.

Based on the cleaned test dataset:

- Actual failures: 66
- Correctly identified failures: 52
- Missed failures: 14
- False alarms: 28

Missed failures could result in unexpected equipment downtime, while false alarms could lead to unnecessary inspections and increased maintenance costs.

### 4. Boundary Behavior

Model predictions may become unreliable when operating conditions approach or exceed the ranges represented in the training dataset.

Boundary testing helps identify potentially sensitive regions, but additional validation is required to determine whether the predictions are reliable.

### 5. Generalizability

The models were evaluated using a single synthetic dataset.

Performance may differ across manufacturing environments, equipment types, operating conditions, and failure patterns.

### 6. Data Cleaning Comparisons

The original and cleaned datasets were evaluated using different train/test splits.

Although performance improved after removing inconsistent observations, the results do not establish that data cleaning alone caused the improvement.

A controlled comparison using matched splits would provide stronger evidence.

## Future Work

The team identified three prioritized improvements based on expected value, feasibility, and risk.

| Priority | Improvement | Value | Feasibility | Risk |
|---|---|---|---|---|
| 1 | Expand boundary testing | High | High | Low |
| 2 | Cross-validation and model tuning | High | Medium | Medium |
| 3 | Additional feature testing and model comparisons | Medium | High | Low |

### Priority 1: Expand Boundary Testing

Additional boundary testing should evaluate how predictions respond to changes in rotational speed, temperature, torque, and tool wear.

This would help identify unexpected predictions and potentially unstable behavior under extreme operating conditions.

### Priority 2: Cross-Validation and Model Tuning

Future work should evaluate model performance across multiple training and validation splits.

This would provide stronger evidence about the consistency of recall, precision, and false-positive rates.

Additional hyperparameter tuning could also be used to evaluate whether model performance can be improved.

### Priority 3: Additional Feature Testing and Model Comparisons

Future improvements could include evaluating additional derived features and comparing how different models respond to extreme operating conditions.

This would help determine whether alternative feature combinations improve predictive performance or model interpretability.

## Responsible Technology and Intended Use

This project is intended for:

- Educational research and model evaluation.
- Exploratory predictive maintenance analysis.
- Comparing machine learning classification methods.
- Understanding relationships between operating conditions and predicted equipment failures.

### Prohibited Uses

The model should not be used for:

- Automatically shutting down manufacturing equipment.
- Making safety-critical decisions without human review.
- Replacing qualified maintenance personnel.
- Making operational decisions based solely on model predictions.
- Production deployment without additional real-world validation.

### Human Oversight

Any future operational implementation should require qualified personnel to review model predictions before taking action.

The model should support human decision-making rather than replace it.

If the model cannot produce a reliable prediction, the system should not treat that uncertainty as confirmation that equipment is safe.

## Team Contributions

| Team Member | Primary Contributions |
|---|---|
| Keeshaun | Project coordination, report development, documentation, validation records, and submission management |
| Brett | Machine learning models, evaluation metrics, performance checks, and boundary testing |
| Wynn | Model interpretation, impact evaluation, risk assessment, limitations, and future work |
| Zach | Tableau visualizations and exploratory analysis |

## Repository and Supporting Evidence

The repository contains the project's modeling notebooks, documentation, and supporting analysis.

Key resources:

- [Modeling notebooks](https://github.com/37216110/cis480_capstone/tree/main/notebooks/modeling)
- [Week 10 performance-check implementation](https://github.com/37216110/cis480_capstone/commit/0b41dca295ce334ce91a7c78fcc448a9770dedee)
- [Project repository](https://github.com/37216110/cis480_capstone)

Additional boundary-testing evidence and issue documentation will be linked once committed.

## Data Source

UCI Machine Learning Repository — AI4I 2020 Predictive Maintenance Dataset.

The dataset is publicly available and contains synthetic manufacturing equipment measurements.

AI assistance does not replace the team's responsibility for validating results and documenting contributions.

