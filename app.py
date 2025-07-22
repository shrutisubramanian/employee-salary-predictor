import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# --- Load Model and Data ---
model = joblib.load("model.pkl")
data = pd.read_csv("Salary_Data.csv")
job_titles = sorted(data['Job Title'].dropna().unique())

# --- Course & Advice Mapping ---
course_map = {
    'Data Analyst': [
        "Google Data Analytics Professional Certificate",
        "Excel to MySQL – Duke University (Coursera)",
        "Tableau for Beginners – Udemy"
    ],
    'Software Engineer': [
        "DSA Masterclass – Love Babbar",
        "System Design Primer – GitHub",
        "Clean Code – Robert C. Martin"
    ],
    'Machine Learning Engineer': [
        "Machine Learning Specialization – Andrew Ng",
        "Deep Learning A-Z – Udemy",
        "ML Ops – Coursera"
    ],
    'Web Developer': [
        "The Web Developer Bootcamp – Colt Steele",
        "Full Stack Open – University of Helsinki",
        "Frontend Masters – JavaScript Path"
    ],
    'Cybersecurity Analyst': [
        "Google Cybersecurity Certificate",
        "CompTIA Security+ Bootcamp – Udemy",
        "Network Security Essentials – Coursera"
    ]
}

def get_career_advice(salary):
    if salary < 500000:
        return [
            "Consider enhancing your skill set with online certifications.",
            "Build a strong LinkedIn and GitHub profile.",
            "Attend tech meetups, webinars, and job fairs."
        ]
    elif salary < 1000000:
        return [
            "Work towards leadership or specialization roles.",
            "Consider certifications in project management or domain-specific tools.",
            "Improve soft skills like communication and negotiation."
        ]
    else:
        return [
            "You're in a high-paying bracket! Consider mentoring juniors.",
            "Take executive or leadership courses for career growth.",
            "Explore options in tech consulting or product ownership."
        ]

# --- Streamlit UI ---
st.set_page_config(page_title="Employee Salary Predictor 💸")
st.title("💼 Employee Salary Predictor")

# --- Input Fields ---
age = st.number_input("Age", min_value=18, max_value=70, value=30)
experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=2)

gender = st.selectbox("Gender", ["Male", "Female", "Other"])
education = st.selectbox("Education Level", [
    "B.E in Artificial Intelligence and Data Science",
    "Bachelor's", "Master's", "Ph.D", "Other"
])

job_title = st.selectbox("Job Title", job_titles)

# --- Prediction Button ---
if st.button("Predict Salary 💰"):
    try:
        input_df = pd.DataFrame({
            'Age': [age],
            'Years of Experience': [experience],
            'Gender': [gender],
            'Education Level': [education],
            'Job Title': [job_title]
        })

        prediction = model.predict(input_df)[0]
        st.success(f"Estimated Salary: ₹{prediction:,.2f}")

        # --- Career Recommendation Based on Better Roles ---
        st.subheader("🎯 Career Recommendations")

        similar_profiles = data[
            (data['Education Level'] == education) &
            (data['Years of Experience'] >= experience - 2) &
            (data['Years of Experience'] <= experience + 2)
        ]

        recommendations = (similar_profiles.groupby('Job Title')['Salary']
                           .mean()
                           .reset_index()
                           .sort_values(by='Salary', ascending=False))

        better_jobs = recommendations[recommendations['Salary'] > prediction]

        if not better_jobs.empty:
            st.markdown("You might consider these high-paying roles:")
            for _, row in better_jobs.head(3).iterrows():
                st.markdown(f"- **{row['Job Title']}** — Avg Salary: ₹{row['Salary']:,.2f}")
        else:
            st.info("You're already in one of the top-paying roles for your background!")

        # --- Personalized Career Advice ---
        st.subheader("💡 Career Advice")
        for tip in get_career_advice(prediction):
            st.markdown(f"- {tip}")

        # --- Course Recommendations Based on Job Title ---
        st.subheader("📚 Suggested Courses to Upskill")
        courses = course_map.get(job_title, [
            "LinkedIn Learning: Top Skills for 2025",
            "Coursera: Career Success Specialization",
            "Udemy: Career Development Pathway"
        ])
        for course in courses:
            st.markdown(f"- {course}")

    except Exception as e:
        st.error(f"Prediction failed: {e}")

# --- Sidebar Info ---
with st.sidebar:
    st.markdown("📊 Adjust inputs to predict the salary")


    
