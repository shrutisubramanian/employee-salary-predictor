import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load trained model
model = joblib.load("model.pkl")

# UI
st.set_page_config(page_title="Employee Salary Predictor 💸")
st.title("💼 Employee Salary Predictor")

# Input fields
age = st.number_input("Age", min_value=18, max_value=70, value=30)
experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=2)

gender = st.selectbox("Gender", ["Male", "Female", "Other"])
education = st.selectbox("Education Level", [
    "B.E in Artificial Intelligence and Data Science", 
    "Bachelor's", "Master's", "Ph.D", "Other"
])
job_title = st.text_input("Job Title", "Software Engineer")

if st.button("Predict Salary 💰"):
    # Build DataFrame from input
    input_df = pd.DataFrame({
        'Age': [age],
        'Years of Experience': [experience],
        'Gender': [gender],
        'Education Level': [education],
        'Job Title': [job_title]
    })

    # Predict
    prediction = model.predict(input_df)[0]
    st.success(f"Estimated Salary: ₹{prediction:,.2f}")
