import streamlit as st
import os
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# CareerPilot session memory
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "skill_gaps" not in st.session_state:
    st.session_state.skill_gaps = ""

if "learning_plan" not in st.session_state:
    st.session_state.learning_plan = ""

if "target_role" not in st.session_state:
    st.session_state.target_role = ""

if "portfolio_projects" not in st.session_state:
    st.session_state.portfolio_projects = ""


# Mock Interview memory
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = ""

if "interview_type" not in st.session_state:
    st.session_state.interview_type = ""

if "interview_evaluation" not in st.session_state:
    st.session_state.interview_evaluation = ""
# Progress Tracker memory
if "progress_tasks" not in st.session_state:
    st.session_state.progress_tasks = [
        {"task": "Learn Python fundamentals", "done": False},
        {"task": "Practice SQL queries", "done": False},
        {"task": "Learn Excel and Power BI", "done": False},
        {"task": "Complete one portfolio project", "done": False},
        {"task": "Practice interview questions", "done": False}
    ]

if "progress_feedback" not in st.session_state:
    st.session_state.progress_feedback = ""
# CareerPilot session memory
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "skill_gaps" not in st.session_state:
    st.session_state.skill_gaps = ""

if "learning_plan" not in st.session_state:
    st.session_state.learning_plan = ""

if "target_role" not in st.session_state:
    st.session_state.target_role = ""

# Page settings
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

# Main heading
st.title("🚀 CareerPilot AI")
st.subheader("Your Personal AI Career Navigator")

st.write(
    "Discover your skills, identify career opportunities "
    "and build your future with AI."
)

st.divider()

# Navigation
menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Resume Analyzer",
        "Skill Gap Analysis",
        "Learning Roadmap",
        "Portfolio Projects",
        "Mock Interview",
        "Progress Tracker",
        "Job Application Tracker",
        "AI Career Action Agent",
        "Voice Career Coach"
    ]
)

# Home page
if menu == "Home":

    st.header("Welcome to CareerPilot AI!")
    st.success("Your AI career journey starts here!")

    st.write("Start by uploading your resume.")

# Resume Analyzer
elif menu == "Resume Analyzer":

    st.header("📄 AI Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload your PDF resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        try:
            reader = PdfReader(uploaded_file)
            resume_text = ""

            for page in reader.pages:
                resume_text += page.extract_text() or ""

            if not resume_text.strip():
                st.warning(
                    "No readable text found. "
                    "Please upload a text-based PDF."
                )

            else:
                st.success("Resume uploaded successfully!")
                st.session_state.resume_text = resume_text

                with st.expander("View Resume Text"):
                    st.text(resume_text)

                if st.button("🤖 Analyze My Resume"):

                    if not api_key:
                        st.error(
                            "Gemini API key is missing. "
                            "Please check your .env file."
                        )

                    else:
                        try:
                            client = genai.Client(
                                api_key=api_key
                            )

                            prompt = f"""
                            You are CareerPilot AI,
                            an expert career coach.

                            Analyze the candidate's resume.

                            Provide these sections:

                            1. Candidate Profile
                            2. Education
                            3. Technical Skills
                            4. Projects and Experience
                            5. Strengths
                            6. Missing or Weak Skills
                            7. Recommended Job Roles
                            8. Resume Improvement Suggestions

                            Do not invent information.
                            Give practical advice for a fresher.

                            RESUME:
                            {resume_text[:15000]}
                            """

                            with st.spinner(
                                "Gemini is analyzing your resume..."
                            ):

                                response = client.models.generate_content(
                                    model="gemini-3.5-flash-lite",
                                    contents=prompt
                                )

                            st.subheader("🎯 AI Resume Analysis")
                            st.markdown(response.text)

                        except Exception as e:
                            st.error(
                                f"Gemini API Error: {e}"
                            )

        except Exception as e:
            st.error(f"Resume Reading Error: {e}")
# Skill Gap Analysis
elif menu == "Skill Gap Analysis":

    st.header("🔍 AI Skill Gap Analyzer")

    st.write(
        "Compare your resume with a real job description "
        "to discover the skills you need."
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload your resume first "
            "in the Resume Analyzer section."
        )

    else:

        st.success("Resume connected successfully!")

        target_role = st.text_input(
            "Target Job Role",
            placeholder="Example: Data Analyst"
        )

        job_description = st.text_area(
            "Paste a real job description",
            placeholder="Paste the complete job description here...",
            height=250
        )

        if st.button("🔍 Analyze My Skill Gaps"):

            if not target_role.strip():
                st.warning("Enter your target job role.")

            elif not job_description.strip():
                st.warning("Paste a real job description.")

            elif not api_key:
                st.error("Gemini API key is missing.")

            else:

                try:
                    client = genai.Client(api_key=api_key)

                    prompt = f"""
                    You are CareerPilot AI's Skill Gap Agent.

                    Compare the candidate's actual resume
                    against the supplied real job description.

                    CANDIDATE RESUME:
                    {st.session_state.resume_text[:12000]}

                    TARGET ROLE:
                    {target_role}

                    JOB DESCRIPTION:
                    {job_description[:12000]}

                    Perform a detailed skill gap analysis.

                    Include:

                    1. Overall job suitability.
                    2. Skills already present in the resume.
                    3. Required skills missing from the resume.
                    4. Skills that need improvement.
                    5. Technical tools and technologies required.
                    6. Priority level for every missing skill.
                    7. Recommended learning order.
                    8. Three practical actions to improve job readiness.

                    Classify missing skills as:
                    - High priority
                    - Medium priority
                    - Low priority

                    Rules:
                    - Only use evidence from the resume and JD.
                    - Never claim the candidate knows a skill
                      without resume evidence.
                    - Do not invent job requirements.
                    - Explain recommendations clearly.
                    """

                    with st.spinner(
                        "🤖 Comparing your resume with the job description..."
                    ):

                        response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt
                        )

                    st.session_state.skill_gaps = response.text or ""

                    st.session_state.target_role = target_role

                    st.success("Skill gap analysis completed!")

                    st.subheader("🎯 Your Skill Gap Report")

                    st.markdown(st.session_state.skill_gaps)

                except Exception as e:
                    st.error(f"Skill Gap Agent Error: {e}")


# Learning Roadmap
elif menu == "Learning Roadmap":

    st.header("📚 AI Learning Roadmap")

    st.write(
        "Generate a personalized week-by-week learning plan "
        "based on your skill gaps."
    )

    if not st.session_state.skill_gaps:

        st.warning(
            "Please complete Skill Gap Analysis first."
        )

    else:

        st.success(
            f"Skill gap analysis connected for: "
            f"{st.session_state.target_role}"
        )

        duration = st.selectbox(
            "Choose your learning duration",
            ["4 Weeks", "8 Weeks", "12 Weeks"]
        )

        hours = st.slider(
            "Available learning hours per day",
            min_value=1,
            max_value=8,
            value=2
        )

        if st.button("🚀 Generate My Learning Roadmap"):

            if not api_key:

                st.error("Gemini API key is missing.")

            else:

                try:

                    client = genai.Client(api_key=api_key)

                    prompt = f"""
                    You are CareerPilot AI's Learning Roadmap Agent.

                    Create a personalized learning roadmap.

                    TARGET ROLE:
                    {st.session_state.target_role}

                    SKILL GAP ANALYSIS:
                    {st.session_state.skill_gaps}

                    LEARNING DURATION:
                    {duration}

                    DAILY STUDY TIME:
                    {hours} hours

                    Create a practical week-by-week roadmap.

                    For every week include:

                    1. Learning topics.
                    2. Skills to develop.
                    3. Free learning resources.
                    4. Practical exercises.
                    5. A weekly mini-project or task.
                    6. A measurable completion goal.

                    Rules:
                    - Prioritize high-priority missing skills.
                    - Recommend free resources where possible.
                    - Keep the plan realistic for a beginner.
                    - Include revision and practice.
                    - Do not promise job placement.
                    - Clearly organize the roadmap by week.
                    """

                    with st.spinner(
                        "🤖 Creating your personalized learning roadmap..."
                    ):

                        response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt
                        )

                    st.session_state.learning_plan = (
                        response.text or ""
                    )

                    st.success(
                        "Your learning roadmap is ready!"
                    )

                    st.markdown(
                        st.session_state.learning_plan
                    )

                except Exception as e:

                    st.error(
                        f"Learning Roadmap Error: {e}"
                    )

        if st.session_state.learning_plan:

            st.divider()

            st.subheader("📋 Your Saved Learning Roadmap")

            st.markdown(
                st.session_state.learning_plan
            )

# Portfolio Project Recommendations
elif menu == "Portfolio Projects":

    st.header("💡 AI Portfolio Project Agent")

    st.write(
        "Discover projects that help you demonstrate "
        "the skills required for your target job."
    )

    if not st.session_state.skill_gaps:

        st.warning(
            "Please complete Skill Gap Analysis first."
        )

    else:

        st.success(
            f"Target Role: {st.session_state.target_role}"
        )

        project_level = st.selectbox(
            "Choose your project difficulty",
            ["Beginner", "Intermediate", "Advanced"]
        )

        number_of_projects = st.slider(
            "Number of project recommendations",
            min_value=1,
            max_value=5,
            value=3
        )

        if st.button("🚀 Recommend My Projects"):

            if not api_key:

                st.error("Gemini API key is missing.")

            else:

                try:

                    client = genai.Client(api_key=api_key)

                    prompt = f"""
                    You are CareerPilot AI's Portfolio Project Agent.

                    Recommend practical portfolio projects
                    for this candidate.

                    TARGET JOB ROLE:
                    {st.session_state.target_role}

                    CANDIDATE SKILL GAPS:
                    {st.session_state.skill_gaps}

                    LEARNING ROADMAP:
                    {st.session_state.learning_plan}

                    PROJECT LEVEL:
                    {project_level}

                    NUMBER OF PROJECTS:
                    {number_of_projects}

                    For each project provide:

                    1. Project title.
                    2. Problem statement.
                    3. Real-world use case.
                    4. Technologies required.
                    5. Features to implement.
                    6. Step-by-step development plan.
                    7. Skills demonstrated.
                    8. Expected GitHub repository structure.
                    9. Resume bullet point after completion.

                    Rules:
                    - Match projects to the target job role.
                    - Address the candidate's missing skills.
                    - Prefer practical, real-world projects.
                    - Avoid generic projects such as a basic calculator.
                    - Keep recommendations achievable at the selected level.
                    - Never claim a project has already been completed.
                    """

                    with st.spinner(
                        "🤖 Finding the best portfolio projects..."
                    ):

                        response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt
                        )

                    st.session_state.portfolio_projects = (
                        response.text or ""
                    )

                    st.success(
                        "Portfolio recommendations generated!"
                    )

                    st.markdown(
                        st.session_state.portfolio_projects
                    )

                except Exception as e:

                    st.error(
                        f"Portfolio Agent Error: {e}"
                    )

        if (
            "portfolio_projects" in st.session_state
            and st.session_state.portfolio_projects
        ):

            st.divider()

            st.subheader("📁 Your Project Recommendations")

            st.markdown(
                st.session_state.portfolio_projects
            )

# Mock Interview
elif menu == "Mock Interview":

    st.header("🎤 AI Mock Interview")

    st.write(
        "Practice real-world interview questions "
        "and receive AI-powered feedback."
    )

    if not st.session_state.target_role:

        st.warning(
            "Please complete Skill Gap Analysis first."
        )

    else:

        st.success(
            f"Interview Role: {st.session_state.target_role}"
        )

        interview_type = st.selectbox(
            "Choose interview category",
            [
                "Technical Interview",
                "HR Interview",
                "Problem Solving",
                "Mixed Interview"
            ]
        )

        if st.button("🚀 Generate Interview Questions"):

            if not api_key:

                st.error("Gemini API key is missing.")

            else:

                try:

                    client = genai.Client(api_key=api_key)

                    prompt = f"""
                    You are CareerPilot AI's Interview Agent.

                    Create 5 realistic interview questions.

                    Target Role:
                    {st.session_state.target_role}

                    Candidate Skill Gaps:
                    {st.session_state.skill_gaps}

                    Interview Category:
                    {interview_type}

                    Rules:
                    - Match questions to the target role.
                    - Consider the candidate's skill gaps.
                    - Include beginner-friendly questions.
                    - Do not provide the answers.
                    - Number questions from 1 to 5.
                    """

                    with st.spinner(
                        "Generating interview questions..."
                    ):

                        response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt
                        )

                    st.session_state.interview_questions = (
                        response.text or ""
                    )

                    st.session_state.interview_type = interview_type
                    st.session_state.interview_answers = ""

                    st.success("Interview questions are ready!")

                except Exception as e:

                    st.error(
                        f"Interview Agent Error: {e}"
                    )

        if (
            "interview_questions" in st.session_state
            and st.session_state.interview_questions
        ):

            st.divider()

            st.subheader("📝 Your Interview Questions")

            st.markdown(
                st.session_state.interview_questions
            )

            st.write(
                "Answer the questions below. "
                "You can use Wispr Flow to dictate your answers."
            )

            answers = st.text_area(
                "Your answers",
                key="mock_interview_answers",
                height=300,
                placeholder=(
                    "Q1: Your answer...\n\n"
                    "Q2: Your answer...\n\n"
                    "Continue answering all 5 questions."
                )
            )

            if st.button("📊 Evaluate My Interview"):

                if not answers.strip():

                    st.warning("Please enter your answers.")

                else:

                    try:

                        client = genai.Client(api_key=api_key)

                        evaluation_prompt = f"""
                        You are an experienced technical interviewer.

                        Evaluate this candidate's interview.

                        Target Role:
                        {st.session_state.target_role}

                        Interview Category:
                        {st.session_state.interview_type}

                        Questions:
                        {st.session_state.interview_questions}

                        Candidate Answers:
                        {answers}

                        Evaluate fairly.

                        Provide:

                        1. Overall score out of 100.
                        2. Technical knowledge score out of 25.
                        3. Communication score out of 25.
                        4. Problem-solving score out of 25.
                        5. Answer relevance score out of 25.
                        6. Strengths.
                        7. Weak answers and why they need improvement.
                        8. Suggested improved answers.
                        9. Three actions to improve interview performance.

                        Do not give high scores for empty,
                        irrelevant or incorrect answers.

                        Explain that this is AI-generated
                        practice feedback, not an official assessment.
                        """

                        with st.spinner(
                            "🤖 Evaluating your interview..."
                        ):

                            evaluation = client.models.generate_content(
                                model="gemini-3.5-flash-lite",
                                contents=evaluation_prompt
                            )

                        st.session_state.interview_evaluation = (
                            evaluation.text or ""
                        )

                        st.success("Interview evaluation completed!")

                        st.subheader("📊 Interview Performance Report")

                        st.markdown(
                            st.session_state.interview_evaluation
                        )

                    except Exception as e:

                        st.error(
                            f"Evaluation Error: {e}"
                        )

# =====================================================
# PROGRESS TRACKER
# =====================================================

elif menu == "Progress Tracker":

    st.header("📊 AI Career Progress Tracker")

    st.write(
        "Track your learning activities and improve "
        "your career readiness."
    )

    # Initialize progress tasks
    if "progress_tasks" not in st.session_state:
        st.session_state.progress_tasks = [
            {"task": "Learn Python fundamentals", "done": False},
            {"task": "Practice SQL queries", "done": False},
            {"task": "Learn Excel and Power BI", "done": False},
            {"task": "Complete one portfolio project", "done": False},
            {"task": "Practice interview questions", "done": False}
        ]

    if "progress_feedback" not in st.session_state:
        st.session_state.progress_feedback = ""

    st.subheader("🎯 Your Learning Tasks")

    completed = 0

    for i, task in enumerate(st.session_state.progress_tasks):

        task["done"] = st.checkbox(
            task["task"],
            value=task["done"],
            key=f"progress_task_{i}"
        )

        if task["done"]:
            completed += 1

    total = len(st.session_state.progress_tasks)

    # Progress calculation
    if total > 0:

        progress = completed / total

        st.divider()

        st.subheader("📈 Your Progress")

        st.progress(progress)

        col1, col2 = st.columns(2)

        col1.metric(
            "Tasks Completed",
            f"{completed}/{total}"
        )

        col2.metric(
            "Completion Percentage",
            f"{progress * 100:.0f}%"
        )

    st.divider()

    # Add new task
    st.subheader("➕ Add a New Learning Task")

    new_task = st.text_input(
        "Enter a learning task",
        placeholder="Example: Complete a SQL project"
    )

    if st.button("Add Task"):

        if new_task.strip():

            st.session_state.progress_tasks.append({
                "task": new_task.strip(),
                "done": False
            })

            st.rerun()

        else:
            st.warning("Please enter a task.")

    st.divider()

    # AI progress analysis
    st.subheader("🤖 AI Progress Analysis")

    if st.button("Analyze My Progress"):

        if not api_key:

            st.error("Gemini API key is missing.")

        else:

            task_summary = "\n".join([
                f"{task['task']}: "
                f"{'Completed' if task['done'] else 'Pending'}"
                for task in st.session_state.progress_tasks
            ])

            prompt = f"""
            You are CareerPilot AI's Progress Tracking Agent.

            Target Role:
            {st.session_state.target_role}

            Skill Gaps:
            {st.session_state.skill_gaps}

            Learning Roadmap:
            {st.session_state.learning_plan}

            Task Status:
            {task_summary}

            Analyze the candidate's progress.

            Provide:
            1. Progress summary.
            2. Completed achievements.
            3. Important pending tasks.
            4. Skills needing attention.
            5. Three recommended next actions.
            6. Suggested roadmap adjustments.

            Never claim incomplete tasks are completed.
            """

            try:

                with st.spinner("Analyzing your progress..."):

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )

                st.session_state.progress_feedback = (
                    response.text or ""
                )

                st.markdown(
                    st.session_state.progress_feedback
                )

            except Exception as e:

                st.error(f"Progress Tracker Error: {e}")

    # Previous recommendations
    if st.session_state.progress_feedback:

        st.divider()

        st.subheader("📋 Previous Recommendations")

        st.markdown(
            st.session_state.progress_feedback
        )
elif menu == "AI Career Action Agent":

    st.header("🤖 AI Career Action Agent")

    st.write(
        "Your personal AI agent that decides what you should "
        "focus on next to become job-ready."
    )

    st.subheader("🎯 Your Career Profile")

    target_role = st.session_state.target_role

    st.write("**Target Role:**", target_role)

    if st.button("Generate My Next Career Actions"):

        if not api_key:
            st.error("Gemini API key is missing.")

        else:
            try:
                client = genai.Client(api_key=api_key)

                completed_tasks = [
                    task["task"]
                    for task in st.session_state.progress_tasks
                    if task["done"]
                ]

                pending_tasks = [
                    task["task"]
                    for task in st.session_state.progress_tasks
                    if not task["done"]
                ]

                prompt = f"""
                You are CareerPilot AI, an intelligent career action agent.

                Candidate target role:
                {target_role}

                Candidate skill gaps:
                {st.session_state.skill_gaps}

                Learning roadmap:
                {st.session_state.learning_plan}

                Completed tasks:
                {completed_tasks}

                Pending tasks:
                {pending_tasks}

                Analyze the candidate's current situation.

                Generate:
                1. Current career readiness assessment.
                2. The three most important skill gaps.
                3. The single best task to complete today.
                4. A practical 7-day action plan.
                5. One portfolio project recommendation.
                6. One interview preparation recommendation.

                Prioritize realistic beginner-friendly actions.
                Do not assume skills or achievements that are not provided.
                """

                with st.spinner("AI Agent is planning your next steps..."):

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )

                st.markdown("### 📌 Your Personalized Career Action Plan")
                st.markdown(response.text or "No response generated.")

            except Exception as e:
                st.error(f"Career Action Agent Error: {e}")        
elif menu == "Job Application Tracker":

    st.header("💼 AI Job Application Tracker")

    st.write(
        "Track your job applications and understand "
        "which roles are getting responses."
    )

    # Initialize application storage
    if "job_applications" not in st.session_state:
        st.session_state.job_applications = []

    # Add new application
    st.subheader("➕ Add Job Application")

    company = st.text_input(
        "Company Name",
        placeholder="Example: Google"
    )

    role = st.text_input(
        "Job Role",
        placeholder="Example: Software Engineer"
    )

    job_link = st.text_input(
        "Application Link (Optional)",
        placeholder="Paste job URL"
    )

    status = st.selectbox(
        "Application Status",
        [
            "Applied",
            "Assessment",
            "Interview",
            "Selected",
            "Rejected"
        ]
    )

    if st.button("Add Application"):

        if company.strip() and role.strip():

            st.session_state.job_applications.append({
                "company": company.strip(),
                "role": role.strip(),
                "link": job_link.strip(),
                "status": status
            })

            st.success("Application added successfully!")
            st.rerun()

        else:
            st.warning("Please enter company name and job role.")

    st.divider()

    # Display applications
    st.subheader("📋 Your Applications")

    applications = st.session_state.job_applications

    if applications:

        for i, app in enumerate(applications):

            with st.expander(
                f"{app['company']} - {app['role']}"
            ):

                st.write("**Company:**", app["company"])
                st.write("**Role:**", app["role"])
                st.write("**Status:**", app["status"])

                if app["link"]:
                    st.markdown(
                        f"[Open Job Application]({app['link']})"
                    )

                updated_status = st.selectbox(
                    "Update Status",
                    [
                        "Applied",
                        "Assessment",
                        "Interview",
                        "Selected",
                        "Rejected"
                    ],
                    index=[
                        "Applied",
                        "Assessment",
                        "Interview",
                        "Selected",
                        "Rejected"
                    ].index(app["status"]),
                    key=f"status_{i}"
                )

                if updated_status != app["status"]:
                    app["status"] = updated_status
                    st.rerun()

                if st.button("Delete Application", key=f"delete_{i}"):
                    st.session_state.job_applications.pop(i)
                    st.rerun()

    else:
        st.info("No applications added yet.")

    st.divider()

    # Application statistics
    st.subheader("📊 Application Statistics")

    total = len(applications)

    applied_count = sum(
        1 for app in applications
        if app["status"] == "Applied"
    )

    interview_count = sum(
        1 for app in applications
        if app["status"] == "Interview"
    )

    selected_count = sum(
        1 for app in applications
        if app["status"] == "Selected"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", total)
    col2.metric("Applied", applied_count)
    col3.metric("Interviews", interview_count)
    col4.metric("Selected", selected_count)

    # AI application analysis
    st.divider()

    st.subheader("🤖 AI Application Insights")

    if st.button("Analyze My Applications"):

        if not applications:
            st.warning("Add applications before analyzing.")

        elif not api_key:
            st.error("Gemini API key is missing.")

        else:
            try:

                client = genai.Client(api_key=api_key)

                application_summary = "\n".join([
                    f"Company: {app['company']}, "
                    f"Role: {app['role']}, "
                    f"Status: {app['status']}"
                    for app in applications
                ])

                prompt = f"""
                You are CareerPilot AI's Job Search Analyst.

                Analyze these job applications:

                {application_summary}

                Provide:
                1. Application summary.
                2. Interview conversion observations.
                3. Which roles appear to be getting responses.
                4. Possible reasons for rejections.
                5. Three improvements to the job search strategy.
                6. Recommended next actions.

                Important:
                Do not invent response rates or claim trends
                from insufficient data.
                Clearly mention when there is not enough data.
                """

                with st.spinner("Analyzing applications..."):

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )

                st.markdown(response.text or "No analysis generated.")

            except Exception as e:
                st.error(f"Application Analysis Error: {e}")        
elif menu == "Voice Career Coach":

    st.header("🎙️ Voice Career Coach")

    st.write(
        "Speak your career goals using Wispr Flow "
        "or type them below."
    )

    career_goal = st.text_area(
        "Tell CareerPilot about your career goals:",
        placeholder="Example: I am a final-year CSE student. "
                    "I know Python and SQL. I want to become "
                    "a Data Analyst in six months."
    )

    if st.button("🚀 Generate My Career Plan"):

        if not api_key:
            st.error("Gemini API key is missing.")

        elif not career_goal.strip():
            st.warning("Please enter your career goal first.")

        else:
            try:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                You are CareerPilot AI, an intelligent career coach.

                Understand the user's career instructions.

                Extract:
                1. Current education
                2. Current skills
                3. Target job role
                4. Career timeline
                5. Missing skills
                6. Learning priorities
                7. First practical action

                Give a personalized and realistic response.
                Never invent information.

                USER INSTRUCTION:
                {career_goal}
                """

                with st.spinner("CareerPilot is thinking..."):

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )

                st.subheader("🎯 Your Career Plan")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Career Coach Error: {e}")