# 🌙 LunarisAI

**LunarisAI** is a personalized period prediction assistant powered by Machine Learning.  
It estimates the next menstrual cycle start date using user health and cycle inputs with uncertainty awareness.  
Built with **Random Forest Regression**, and deployed via **Streamlit**, LunarisAI adapts predictions based on factors like PCOS, stress, and birth control usage.

---

## 🚀 Features

- 🧠 **ML Model**: RandomForestRegressor with preprocessing pipeline
- 📅 **Predicts**: Number of days until next period + predicted calendar date
- 📈 **Uncertainty Window**: Adjusts based on cycle regularity, PCOS, stress, etc.
- 🌐 **Web App**: Streamlit interface with full prediction and feedback loop
- 🔍 **Explainability**: SHAP beeswarm plots for feature impact visualization
- ⚠️ **Smart Alerts**: Flags post-menopausal inconsistencies, high-stress cases, abnormal outputs

---

## 📷 Demo Preview

![App Screenshot]()

---

## 🧪 How It Works

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

## 💻 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/ar-shenoy/LunarisAI.git
cd LunarisAI
```
