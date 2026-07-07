# 🎯 Job Fit Analyzer

An AI-powered career tool that uses a **3-agent CrewAI pipeline** to analyze your resume against target companies and returns scored recommendations with strengths, skill gaps, and actionable next steps.

---

## 🚀 Features

- **Multi-agent AI pipeline** — 3 specialized CrewAI agents work sequentially to profile, research, and score
- **Resume input** — paste text directly or upload a `.txt` file with drag & drop support
- **Company selector** — toggle default companies on/off or add custom ones
- **Fit scoring** — each company gets a 0–100 match score with a recommendation (Apply / Upskill / Skip)
- **Strengths & gaps** — per-company breakdown of what matches and what's missing
- **Live agent log** — real-time progress tracking as each agent runs
- **Download report** — export the full analysis as a `.txt` file
- **Smart run button** — disabled until API key, resume, and companies are all set

---

## 🤖 How It Works

```
Your Resume + Target Companies
        ↓
┌─────────────────────────────┐
│  Agent 1: Profile Analyst   │  → Extracts skills, experience, projects
└─────────────────────────────┘
        ↓
┌─────────────────────────────┐
│  Agent 2: Job Researcher    │  → Researches entry-level roles per company
└─────────────────────────────┘
        ↓
┌─────────────────────────────┐
│  Agent 3: Fit Scorer        │  → Scores fit (0-100), flags strengths & gaps
└─────────────────────────────┘
        ↓
  Scored Recommendations
  Apply / Upskill / Skip
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Agents | CrewAI |
| LLM | Groq API — llama3-70b-8192 (free tier) |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML · CSS · Vanilla JavaScript |

---

## 📁 Project Structure

```
job-fit-analyzer-project/
│
├── backend.py          # FastAPI server + CrewAI crew setup
├── index.html          # Frontend — UI, resume upload, results display
├── .gitignore          # Ignores venv, cache, API keys
└── README.md           # You are here
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Free Groq API key → [console.groq.com](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/job-fit-analyzer-project.git
cd job-fit-analyzer-project
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install crewai fastapi groq uvicorn
```

### 4. Run the backend
```bash
uvicorn backend:app --reload
# running on http://127.0.0.1:8000
```

### 5. Open the frontend
```bash
# open a second terminal
python -m http.server 5500
# open http://localhost:5500 in browser
```

### 6. Use the app
- Enter your **Groq API key** in Step 0
- **Paste or upload** your resume in Step 1
- **Select target companies** in Step 2
- Click **Run Crew Analysis**

---

## 📦 Requirements

```
crewai
fastapi
uvicorn
groq
```


---

## 🔑 API Key

This project uses **Groq's free API** — no credit card required.

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up and generate an API key
3. Paste it into the UI — it is never stored or sent anywhere except directly to Groq

