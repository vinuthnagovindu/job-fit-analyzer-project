from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process, LLM
import os, re

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class AnalyzeRequest(BaseModel):
    api_key: str
    resume: str
    companies: list[str]

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    os.environ["GROQ_API_KEY"] = req.api_key

    llm = LLM(model="groq/llama3-70b-8192", api_key=req.api_key, temperature=0.3)
    companies_str = ", ".join(req.companies)

    profile_analyst = Agent(
        role="Student Profile Analyst",
        goal="Analyze the student's resume to identify technical skills, experience level, key projects, suitable roles, top strengths, and areas for improvement.",
        backstory="Senior technical recruiter with 10+ years of experience.",
        llm=llm, verbose=False,
    )
    jd_researcher = Agent(
        role="Job Market Researcher",
        goal="For each target company, describe entry-level roles, required skills, and hiring traits.",
        backstory="Career intelligence analyst tracking tech hiring trends.",
        llm=llm, verbose=False,
    )
    fit_scorer = Agent(
        role="Candidate Fit Evaluator",
        goal="Score candidate fit (0-100) per company, list strengths and gaps, recommend Apply/Skip/Upskill.",
        backstory="Objective hiring consultant.",
        llm=llm, verbose=False,
    )

    task_profile = Task(
        description=f"Analyze this resume:\n{req.resume}\n\nExtract: skills, experience level, projects, suitable roles, top 2 strengths and gaps.",
        expected_output="Structured profile: Skills, Experience, Projects, Roles, Strengths, Gaps.",
        agent=profile_analyst,
    )
    task_research = Task(
        description=f"Research entry-level hiring for: {companies_str}\nFor each: domain, roles, must-have skills, one unique hiring trait.",
        expected_output="Per-company breakdown.",
        agent=jd_researcher,
    )
    task_score = Task(
        description="""For each company give:
1. Match score: 0-100
2. 2-3 matching strengths
3. 1-2 skill gaps
4. Recommendation: Apply / Skip / Upskill-then-Apply

Format exactly like:
## CompanyName
Score: XX/100
Strengths: point1, point2
Gaps: gap1, gap2
Recommendation: Apply""",
        expected_output="Scored list per company.",
        agent=fit_scorer,
        context=[task_profile, task_research],
    )

    crew = Crew(
        agents=[profile_analyst, jd_researcher, fit_scorer],
        tasks=[task_profile, task_research, task_score],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    result_str = str(result)

    # Parse scores per company
    scores = []
    for co in req.companies:
        score_match = re.search(
            rf"{re.escape(co)}.*?(\d{{2,3}})\s*/?\s*100",
            result_str, re.IGNORECASE | re.DOTALL
        )
        strengths_match = re.search(
            rf"Strengths?:\s*(.+?)(?:\n|Gaps?:)",
            result_str, re.IGNORECASE
        )
        gaps_match = re.search(
            rf"Gaps?:\s*(.+?)(?:\n|Recommendation:)",
            result_str, re.IGNORECASE
        )
        rec_match = re.search(
            rf"Recommendation:\s*(.+?)(?:\n|$)",
            result_str, re.IGNORECASE
        )
        scores.append({
            "company": co,
            "score": int(score_match.group(1)) if score_match else 60,
            "strengths": strengths_match.group(1).split(",") if strengths_match else ["See full report"],
            "gaps": gaps_match.group(1).split(",") if gaps_match else ["See full report"],
            "recommendation": rec_match.group(1).strip() if rec_match else "Upskill-then-Apply",
        })

    return { "scores": scores, "full_report": result_str }

@app.get("/")
def root():
    return {"status": "Job Fit Analyzer backend is running ✅"}