from transformers import pipeline

class ResumeAnalyzer:
    def __init__(self, model_name="microsoft/phi-3-mini-4k-instruct"):
        self.llm = pipeline(
            "text-generation",
            model=model_name,
            max_new_tokens=256,
            temperature=0.2
        )

    def analyze(self, resume_chunks, job_role):
        context = "\n\n".join(resume_chunks)

        prompt = f"""
You are an AI resume reviewer.

JOB ROLE:
{job_role}

RESUME CONTENT (EXTRACTED SECTIONS):
{context}

INSTRUCTIONS:
- Do NOT repeat this prompt.
- Do NOT mention instructions.
- Focus on skills, experience, projects, tools, and technologies.
- Ignore contact details like name, email, phone number.
- If experience is limited, mention projects and education.
- Do NOT invent information not present in the resume.

TASK:
1. Write a 3–4 line professional summary of the candidate.
2. List key strengths (based only on resume content).
3. Identify missing skills or gaps for the job role.
4. Suggest concrete improvements or learning steps.

Use bullet points and clear headings.
"""

        raw_output = self.llm(prompt, return_full_text=False)[0]["generated_text"]

        cleaned_output = raw_output.replace(prompt, "").strip()

        return cleaned_output
