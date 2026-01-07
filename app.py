import streamlit as st
import tempfile

from resume_parser import extract_text_from_pdf
from chunker import chunk_text
from embedder import Embedder
from retriever import Retriever
from llm_analyzer import ResumeAnalyzer

IT_JOB_ROLES = {
    "Data Scientist": "Data Scientist with Python, Machine Learning, SQL, Statistics, and Deep Learning",
    "Data Analyst": "Data Analyst with SQL, Python, Excel, Power BI/Tableau, and Statistics",
    "Machine Learning Engineer": "Machine Learning Engineer with Python, ML algorithms, model deployment, and MLOps",
    "AI Engineer": "AI Engineer with Deep Learning, NLP, Computer Vision, and PyTorch/TensorFlow",
    "Software Engineer": "Software Engineer with Python/Java, DSA, OOPs, REST APIs, and system design",
    "Backend Developer": "Backend Developer with Python/Java, APIs, Databases, and cloud fundamentals",
    "Full Stack Developer": "Full Stack Developer with React, Node.js, Python, SQL, and REST APIs",
    "DevOps Engineer": "DevOps Engineer with Linux, Docker, Kubernetes, CI/CD, and cloud platforms",
    "Cloud Engineer": "Cloud Engineer with AWS/Azure/GCP, networking, security, and automation",
    "Cyber Security Analyst": "Cyber Security Analyst with networking, security tools, SOC, and incident response",
    "Business Analyst": "Business Analyst with SQL, Excel, data analysis, and stakeholder communication",
    "Custom (Write your own)": ""
}


@st.cache_resource
def load_embedder():
    return Embedder()

@st.cache_resource
def load_analyzer():
    return ResumeAnalyzer()

# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Reviewer & Skill Gap Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Reviewer & Skill Gap Analyzer")
st.write("Upload your resume and enter a target job role to get AI-powered feedback.")

# ---------------- INPUTS ----------------
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
st.subheader("🎯 Select Target Job Role")

selected_role = st.selectbox(
    "Choose a job role",
    list(IT_JOB_ROLES.keys())
)

if selected_role == "Custom (Write your own)":
    job_role = st.text_area(
        "Enter Custom Job Description",
        placeholder="Describe the target role and required skills"
    )
else:
    job_role = IT_JOB_ROLES[selected_role]
    st.info(f"📌 Job Role Description:\n\n{job_role}")

analyze_btn = st.button("🔍 Analyze Resume")


# ---------------- PROCESS ----------------
if analyze_btn:
    if uploaded_file is None or job_role.strip() == "":
        st.warning("Please upload a resume and enter a job role.")
    else:
        with st.spinner("Analyzing resume... This may take a minute on CPU ⏳"):
            progress = st.progress(0)

            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name

            # Step 1: Extract text
            resume_text = extract_text_from_pdf(pdf_path)
            progress.progress(15)

            # Step 2: Chunk text
            chunks = chunk_text(resume_text)
            progress.progress(30)

            # Step 3: Embed chunks
            embedder = load_embedder()
            chunk_embeddings = embedder.embed(chunks)
            progress.progress(55)

            # Step 4: Embed job role
            job_embedding = embedder.embed([job_role])

            # Step 5: Retrieve relevant chunks
            retriever = Retriever(chunk_embeddings, chunks)
            relevant_chunks = retriever.retrieve(job_embedding, top_k=8)
            progress.progress(70)

            # Step 6: LLM Analysis
            analyzer = load_analyzer()
            analysis = analyzer.analyze(relevant_chunks, job_role)
            progress.progress(100)

        # ---------------- OUTPUT ----------------
        st.success("Analysis Complete ✅")

        st.subheader("🧠 AI Resume Review & Skill Gap Analysis")
        st.markdown(analysis)
