import streamlit as st
import pandas as pd
import joblib
from datetime import datetime, timedelta

# --- CONFIG ---
st.set_page_config(page_title="LunarisAI", layout="centered", page_icon="🌙")
st.markdown("<h1 style='text-align: center;'>🌙 LunarisAI</h1>", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <h3 style='text-align: center; color: #6B5B95;'>Personalized Period Prediction Assistant</h3>
    <hr style='border-top: 1px solid #bbb;'/>
""", unsafe_allow_html=True)

# --- LOAD MODEL ---
pipeline = joblib.load("model_pipeline/lunaris_pipeline.pkl, compress=3")

# --- UNCERTAINTY RANGE HELPER ---
def get_uncertainty_window(pred_days, *, PCOS, stress_level, cycle_regularity, birth_control, age):
    low, high = -2, 3  # default window

    if cycle_regularity == "Irregular":
        low, high = -4, 8

    if PCOS == "Yes":
        low, high = -5, 12
        if stress_level >= 7:
            low, high = -3, 15

    if birth_control == "Yes":
        low = min(low, -3)
        high = max(high, 8)

    if age >= 55 and cycle_regularity != 'Post-menopausal':
        st.warning("⚠️ User age suggests post-menopause. Please verify cycle status.")
    
    if pred_days < 18 or pred_days > 45:
        st.warning("Prediction outside normal range. Please consult a doctor.")
        st.stop()
    if PCOS == "Yes" or stress_level >= 8:
        st.info("Due to PCOS and/or high stress levels, your cycle is likely to vary more. "
            "Hence, the prediction range has been widened to reflect that uncertainty.")

    return low, high

# --- MODEL INFO (EXPANDER) ---
with st.expander("ℹ️ About This Model"):
    st.markdown("""
    - **Model Type**: Random Forest Regressor  
    - **Trained On**: Synthetic dataset with simulated real-world variability  
    - **Prediction Target**: Estimated number of days until next period  
    - **Uncertainty**: Adjusted based on user health and cycle-related inputs  
    - **Disclaimer**: This tool is not a substitute for clinical diagnosis  
    """)

# --- USER FORM ---
st.markdown("### Enter Your Cycle & Health Details")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        last_period_date = st.date_input("Last Period Date", help="Select the first day of your most recent period.")
        avg_cycle_length = st.number_input("Avg Cycle Length (days)", min_value=20, max_value=45, value=28,
                                        help="Average days between the start of two consecutive periods.")
        period_length = st.number_input("Period Length (days)", min_value=2, max_value=10, value=5,
                                        help="How many days your period usually lasts.")
        age = st.number_input("Age", min_value=10, max_value=60, value=25,
                            help="Your current age in years.")
        stress_level = st.slider("Stress Level (1-10)", min_value=1, max_value=10, value=5,
                                help="Your current stress level. 1 is low, 10 is very high.")

    with col2:
        BMI = st.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0,
                            help="Your Body Mass Index (BMI).")
        cycle_regularity = st.selectbox("Cycle Regularity", ["Regular", "Irregular", "Mostly Regular", "Post-menopausal"],
                                        help="How consistent your menstrual cycles are.")
        symptoms = st.selectbox("Symptoms", ["None", "Cramps", "Bloating", "Multiple"],
                                help="Select the symptoms you typically experience before/during your period.")
        birth_control = st.selectbox("On Birth Control?", ["Yes", "No"],
                                    help="Are you currently using any form of hormonal birth control?")
        PCOS = st.selectbox("PCOS Diagnosed?", ["Yes", "No"],
                            help="Have you been diagnosed with Polycystic Ovary Syndrome (PCOS)?")

    user_thought = st.text_input("Your Expected Next Period Date (optional)", placeholder="DD-MM-YYYY",
                                help="Optional: Enter the date you think your next period will start.")

    submitted = st.form_submit_button("Predict")

# --- VALIDATE DATE ---
if last_period_date > datetime.today().date():
    st.error("Last period date cannot be in the future.")
    st.stop()

# --- PREDICTION ---
if submitted:
    try:
        if cycle_regularity == "Post-menopausal":
            st.warning("Prediction skipped: cycle marked as post-menopausal.")
        else:
            input_df = pd.DataFrame([{
                'avg_cycle_length': avg_cycle_length,
                'period_length': period_length,
                'age': age,
                'stress_level': stress_level,
                'BMI': BMI,
                'cycle_regularity': cycle_regularity,
                'symptoms': symptoms,
                'birth_control': birth_control,
                'PCOS': PCOS
            }])

            pred_days = float(pipeline.predict(input_df)[0])
            predicted_next_period = last_period_date + timedelta(days=round(pred_days))

            # --- Uncertainty Window ---
            low_shift, high_shift = get_uncertainty_window(
                pred_days,
                PCOS=PCOS,
                stress_level=stress_level,
                cycle_regularity=cycle_regularity,
                birth_control=birth_control,
                age=age
            )

            low_date = predicted_next_period + timedelta(days=low_shift)
            high_date = predicted_next_period + timedelta(days=high_shift)

            # --- Display Prediction ---
            st.success(
                f"Your next period will likely fall between "
                f"**{low_date.strftime('%d-%m-%Y')} and {high_date.strftime('%d-%m-%Y')}**"
            )
            st.info(f"Model's Point Estimate: **{round(pred_days)} days**")

            if user_thought:
                try:
                    actual_date = datetime.strptime(user_thought, "%d-%m-%Y").date()
                    error = abs((predicted_next_period - actual_date).days)
                    st.write(f"Your Expected Date: **{actual_date.strftime('%d-%m-%Y')}**")
                    st.write(f"Point Estimate Error: **{error} day(s)**")
                    if error <= 4:
                        st.success("Your expected date closely aligns with our prediction! That's a great sign of a stable cycle.")
                except ValueError:
                    st.warning("Please enter expected date in DD-MM-YYYY format.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("🔒 Your data is never stored. Predictions are made locally in your browser session.")
st.caption("This tool is for informational purposes only and does not replace medical advice. If you have concerns about your cycle, consult a gynecologist.")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)
