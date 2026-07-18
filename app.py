import os
import streamlit as st
import pandas as pd

from parser import get_all_resume_texts
from scorer import score_resume

# -----------------------
# Page Config
# -----------------------

st.set_page_config(
    page_title="InternLoom ATS",
    page_icon="🧠",
    layout="wide"
)

# -----------------------
# Styling
# -----------------------

st.markdown("""
<style>

.main{
    background:#f8fafc;
}

.big{
    font-size:48px;
    font-weight:700;
    color:#2563eb;
}

.small{
    font-size:18px;
    color:#666666;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    padding:18px;
    border:1px solid #dddddd;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# Header
# -----------------------

st.markdown(
    "<div class='big'>🧠 InternLoom ATS</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='small'>AI Resume Screening Engine for Recruiters</div>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------
# Sidebar
# -----------------------
JOB_DETAILS = {

    "Frontend Developer": {
        "Required": [
            "HTML", "CSS", "JavaScript", "React", "Git", "REST API"
        ],
        "Preferred": [
            "Next.js", "TypeScript", "Redux", "Jest"
        ],
        "CGPA": "6.5+",
        "Slots": 8
    },

    "Backend Developer": {
        "Required": [
            "Python", "Java", "Node.js",
            "SQL", "MySQL", "PostgreSQL",
            "MongoDB", "Git", "REST API"
        ],
        "Preferred": [
            "Docker", "JWT", "OAuth",
            "AWS", "Cloud"
        ],
        "CGPA": "6.5+",
        "Slots": 10
    },

    "Full Stack Developer": {
        "Required": [
            "React", "Node.js", "SQL",
            "MongoDB", "Firebase", "Git"
        ],
        "Preferred": [
            "GraphQL", "Docker", "AWS"
        ],
        "CGPA": "7.0+",
        "Slots": 7
    },

    "Database Developer": {
        "Required": [
            "MySQL", "PostgreSQL", "SQL", "MongoDB"
        ],
        "Preferred": [
            "Redis", "Indexing", "ERD"
        ],
        "CGPA": "6.0+",
        "Slots": 3
    },

    "API Integration Developer": {
        "Required": [
            "REST API", "JSON", "Postman"
        ],
        "Preferred": [
            "Swagger", "OAuth", "JWT"
        ],
        "CGPA": "6.0+",
        "Slots": 2
    }

}
with st.sidebar:

    st.title("Recruiter Dashboard")

    st.markdown("---")

    role = st.selectbox(
        "Job Role",
        [
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "Database Developer",
            "API Integration Developer"
        ]
    )
    slots = st.number_input(
    "👥 Number of Open Positions",
    min_value=1,
    value=5,
    step=1
)
    min_cgpa = st.number_input(
    "🎓 Minimum CGPA Required",
    min_value=0.0,
    max_value=10.0,
    value=6.5,
    step=0.1
)


    uploaded_files = st.file_uploader(
        "📂 Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    analyze = st.button(
        "🚀 Analyze Resumes",
        use_container_width=True,
        type="primary"
    )
    

     
st.markdown("---")

jd = JOB_DETAILS[role]

st.markdown("## 📋 Job Description")

st.write("### ✅ Required Skills")

for skill in jd["Required"]:
    st.write(f"✔ {skill}")

st.write("### ⭐ Preferred Skills")

for skill in jd["Preferred"]:
    st.write(f"• {skill}")

st.write(f"### 🎓 Minimum CGPA : {jd['CGPA']}")

st.write(f"### 👥 Open Positions : {slots}")

st.markdown("---")

# -----------------------
# Session State
# -----------------------

if "df_results" not in st.session_state:

    st.session_state.df_results = None
# -----------------------
# Analyze Button
# -----------------------

if analyze:

    if len(uploaded_files) == 0:

        st.error("Please upload at least one resume PDF.")

        st.stop()

    temp_folder = "temp_resumes"

    os.makedirs(temp_folder, exist_ok=True)

    # Delete old resumes
    for file in os.listdir(temp_folder):

        try:
            os.remove(os.path.join(temp_folder, file))
        except:
            pass

    # Save uploaded resumes
    for file in uploaded_files:

        with open(
            os.path.join(temp_folder, file.name),
            "wb"
        ) as out:

            out.write(file.getbuffer())

    resumes = get_all_resume_texts(temp_folder)
    st.session_state.resumes = resumes

    progress = st.progress(0)

    status = st.empty()

    results = []

    total = len(resumes)

    for i, resume in enumerate(resumes):

        status.info(
            f"Analyzing Resume {i+1}/{total}"
        )

        result = score_resume(
            resume["text"],
            role
        )

        result["Resume File"] = resume["filename"]

        results.append(result)

        progress.progress(
            (i + 1) / total
        )

    status.success("✅ Analysis Completed")

    df = pd.DataFrame(results)

    df["Score"] = pd.to_numeric(
        df["Score"],
        errors="coerce"
    ).fillna(0).astype(int)

    df = df.sort_values(
        by="Score",
        ascending=False
    )

    st.session_state.df_results = df
# -----------------------
# Show Results
# -----------------------

if st.session_state.df_results is not None:

    df = st.session_state.df_results.copy()
col1, col2 = st.columns([1, 5])

with col1:
    if st.button("🔄 Analyze New Batch"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
   

df["Status"] = "Reserve"

df.loc[df.index[:slots-1], "Status"] = "✅ Shortlisted"

highest = int(df["Score"].max())
average = round(df["Score"].mean(), 1)
shortlisted = len(df[df["Status"] == "✅ Shortlisted"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("📄 Resumes", len(df))
col2.metric("🏆 Highest", highest)
col3.metric("📊 Average", average)
col4.metric("✅ Shortlisted", shortlisted)

st.divider()

st.subheader("🔍 Search Candidate")

search = st.text_input("Search by Name")

df_filtered = df.copy()

if search:

    df_filtered = df_filtered[
        df_filtered["Name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

display_columns = [

    "Status",

    "Name",

    "Score",

    "Confidence",

    "Parse Quality",

    "CGPA",

    "Required Skills",

    "Preferred Skills",

    "Projects",

    "Reason"

]

st.subheader("📋 Candidate Ranking")
st.dataframe(
    df_filtered[display_columns],
    use_container_width=True,
    hide_index=True
)



csv = df_filtered.to_csv(index=False)

st.download_button(

    "⬇ Download CSV",

    csv,

    "Shortlisted_Candidates.csv",

    "text/csv"

)

st.divider()

st.subheader("👤 Candidate Details")

candidate = st.selectbox(

    "Choose Candidate",

    df["Name"]

)

selected = df[
    df["Name"] == candidate
].iloc[0]

left, right = st.columns(2)

with left:

    st.markdown("### 👤 Personal")

    st.write(f"**Name:** {selected['Name']}")
    st.write(f"**Email:** {selected['Email']}")
    st.write(f"**Phone:** {selected['Phone']}")
    st.write(f"**CGPA:** {selected['CGPA']}")

with right:

    st.markdown("### 📊 Evaluation")

    st.success(f"⭐ Score : {selected['Score']}")

    st.write(f"**Confidence:** {selected['Confidence']}")
    st.write(f"**Parse Quality:** {selected['Parse Quality']}")
    st.write(f"**Status:** {selected['Status']}")

    st.write("**Required Skills**")
    st.code(selected["Required Skills"])

    st.write("**Preferred Skills**")
    st.code(selected["Preferred Skills"])

    st.write("**Reason**")
    st.info(selected["Reason"])

st.divider()

st.subheader("🏆 Top 10 Candidates")

top10 = df.head(10).copy()

medals = [
    "🥇","🥈","🥉","4️⃣","5️⃣",
    "6️⃣","7️⃣","8️⃣","9️⃣","🔟"
]

top10.insert(
    0,
    "Rank",
    medals[:len(top10)]
)

st.dataframe(
    top10,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    top10.set_index("Name")["Score"]
)

st.divider()

st.caption(
    "InternLoom ATS • AI Resume Screening Engine • Hackathon 2026"
)