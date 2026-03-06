import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Job Skill Gap Analyzer", layout="wide")

st.title("💼 Job Skill Gap Analyzer")
st.write("Analyze your skills and find gaps for your target job role.")

# -----------------------------
# LOAD JOB DATABASE
# -----------------------------
data = pd.read_csv("jobs.csv")

# -----------------------------
# JOB ROLE SELECTION
# -----------------------------
job_role = st.selectbox(
    "Select Your Target Job Role",
    data["job_role"]
)

# Get skills for selected job
job_skills_raw = data[data["job_role"] == job_role]["skills"].values[0]
job_skills = [skill.strip().lower() for skill in job_skills_raw.split(",")]

# -----------------------------
# CREATE GLOBAL SKILL LIST
# -----------------------------
all_skills = list(set(",".join(data["skills"]).split(",")))
all_skills = [s.strip() for s in all_skills]
all_skills = sorted(all_skills)

# -----------------------------
# USER SKILL INPUT
# -----------------------------
user_skills = st.multiselect(
    "Select Your Skills",
    options=all_skills
)
user_skills_list = [skill.strip().lower() for skill in user_skills]
# -----------------------------
# ANALYZE BUTTON
# -----------------------------
if st.button("Analyze Skill Gap"):

    # Calculate matches
    matched_skills = list(set(user_skills_list) & set(job_skills))
    missing_skills = [skill for skill in job_skills if skill not in user_skills_list]

    # Skill match percentage
    match_percentage = (len(matched_skills) / len(job_skills)) * 100

    st.divider()

    col1, col2 = st.columns(2)

    # -----------------------------
    # LEFT COLUMN
    # -----------------------------
    with col1:

        st.subheader("📊 Skill Match Score")
        st.metric(label="Match Percentage", value=f"{match_percentage:.1f}%")

        st.subheader("✅ Useful Skills You Already Have")

        if matched_skills:
            for skill in matched_skills:
                st.success(skill.capitalize())
        else:
            st.warning("No matching skills found")

    # -----------------------------
    # RIGHT COLUMN
    # -----------------------------
    with col2:

        st.subheader("⚠️ Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.error(skill.capitalize())
        else:
            st.success("You already have all required skills!")

    # -----------------------------
    # REQUIRED SKILLS DISPLAY
    # -----------------------------
    st.divider()

    st.subheader("🎯 Skills Required for This Job")

    for skill in job_skills:
        st.write("•", skill.capitalize())

    # -----------------------------
    # LEARNING RECOMMENDATIONS
    # -----------------------------
    st.divider()

    st.subheader("📚 Recommended Learning Resources")

    resource_links = {
        "python": "https://www.learnpython.org",
        "sql": "https://sqlbolt.com",
        "excel": "https://excel-practice-online.com",
        "power bi": "https://learn.microsoft.com/en-us/power-bi/",
        "statistics": "https://www.khanacademy.org/math/statistics-probability",
        "linux": "https://linuxjourney.com",
        "networking": "https://www.netacad.com",
        "docker": "https://docker-curriculum.com",
        "react": "https://react.dev",
        "javascript": "https://javascript.info",
        "git": "https://git-scm.com/docs/gittutorial"
    }

    if missing_skills:
        for skill in missing_skills:
            link = resource_links.get(skill, "https://www.google.com/search?q=learn+" + skill)
            st.write(f"🔗 Learn {skill.capitalize()}: {link}")

    else:
        st.write("You already have all the required skills for this role!")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("Built with Python + Streamlit")
