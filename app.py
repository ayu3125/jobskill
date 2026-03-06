import streamlit as st
import pandas as pd

# Load job data
data = pd.read_csv("jobs.csv")

st.title("Job Skill Gap Analyzer")

# Dropdown for job roles
job_role = st.selectbox("Select Target Job Role", data["job_role"])

# User input for skills
all_skills = list(set(",".join(data["skills"]).split(",")))

user_skills = st.multiselect(
    "Select Your Skills",
    options=sorted([s.strip() for s in all_skills])
)

if st.button("Analyze Skill Gap"):

    # Get job skills
    job_skills = data[data["job_role"] == job_role]["skills"].values[0]
    job_skills = [skill.strip().lower() for skill in job_skills.split(",")]

    # Convert user skills
    user_skills_list = [skill.strip().lower() for skill in user_skills.split(",")]

    # Find missing skills
    missing_skills = [skill for skill in job_skills if skill not in user_skills_list]

    st.subheader("Required Skills")
    st.write(job_skills)

    st.subheader("Your Skills")
    st.write(user_skills_list)

    st.subheader("Missing Skills")

    if missing_skills:
        st.write(missing_skills)
    else:
        st.success("You already have all required skills!")

match_percentage = (len(set(user_skills_list) & set(job_skills)) / len(job_skills)) * 100

st.subheader("Skill Match Score")
st.write(f"{match_percentage:.2f}% match")

matched_skills = list(set(user_skills_list) & set(job_skills))

st.subheader("Useful Skills You Already Have")
st.write(matched_skills)

from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def get_learning_advice(missing_skills):

    prompt = f"""
    A student is missing the following skills for a job: {missing_skills}.
    Recommend how they can learn these skills and useful resources.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content

if missing_skills:
    advice = get_learning_advice(missing_skills)
    st.subheader("AI Learning Recommendations")
    st.write(advice)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Skills")
    st.write(user_skills)

with col2:
    st.subheader("Missing Skills")
    st.write(missing_skills)