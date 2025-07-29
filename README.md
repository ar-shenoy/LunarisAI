# 🌙 LunarisAI

**LunarisAI** is a personalized period prediction assistant powered by Machine Learning.  
It estimates the next menstrual cycle start date using user health and cycle inputs with uncertainty awareness.  
Built with **Random Forest Regression**, and deployed via **Streamlit**, LunarisAI adapts predictions based on factors like PCOS, stress, and birth control usage.

---

## Features

-  **ML Model**: RandomForestRegressor with preprocessing pipeline
-  **Predicts**: Number of days until next period + predicted calendar date
-  **Uncertainty Window**: Adjusts based on cycle regularity, PCOS, stress, etc.
-  **Web App**: Streamlit interface with full prediction and feedback loop
-  **Explainability**: SHAP beeswarm plots for feature impact visualization
-  **Smart Alerts**: Flags post-menopausal inconsistencies, high-stress cases, abnormal outputs

---

##  Demo Preview

![App Screenshot](Lunaris%20UI.png)

---

##  How It Works

### Model Input Features:
- Average Cycle Length (days)
- Period Length (days)
- Age
- Stress Level (scale 1–10)
- BMI
- Cycle Regularity
- Symptoms
- Birth Control (Yes/No)
- PCOS (Yes/No)

### Model Output:
- Predicted days until next period
- Predicted next period date (calendar)
- Uncertainty range
- Optional error comparison if user inputs expected date

---

##  Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/ar-shenoy/LunarisAI.git
cd LunarisAI
```

### 2. Create environment & install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run app.py
```

---
##   Data & Ethics

 >  *LunarisAI is trained on synthetic data and does not store any user inputs.*


- The dataset is synthetically generated using ChatGPT, While building Lunaris I've added noise and variability to simulate real-world menstrual cycle patterns.
- This is not a clinical tool. For real concerns, consult a gynecologist.
- No personal data is logged or saved.
- Predictions are made locally per session.

---
##  Contact
For any questions or feedback, feel free to reach out:

Name: Adarsh R Shenoy

Email: adarshrshenoy1@gmail.com

LinkedIn: https://www.linkedin.com/in/ar-shenoy

GitHub: https://github.com/ar-shenoy?tab=repositories
