import streamlit as st
import os
from groq import Groq
from fpdf import FPDF

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.title("🚀 AI Learning Path Generator")
st.write("Generate a personalized roadmap to master any skill.")

st.divider()

# User Inputs
topic = st.text_input("Enter the skill you want to learn")

level = st.selectbox(
    "Select your current level",
    ["Beginner", "Intermediate", "Advanced"]
)

hours = st.slider(
    "How many hours can you study per week?",
    1, 40, 10
)

goal = st.text_input(
    "What is your goal? (job, project, interview, etc)"
)

st.divider()

# Generate Learning Path
if st.button("Generate Learning Path"):

    if topic == "":
        st.warning("⚠️ Please enter a skill first.")
    else:

        prompt = f"""
        Create a structured learning roadmap for learning {topic}.

        User Details:
        Skill Level: {level}
        Weekly Study Time: {hours} hours
        Goal: {goal}

        IMPORTANT:
        The user is currently at {level} level.
        Start the roadmap from this level and do NOT include earlier levels.

        Provide the roadmap in this format:

        1. Learning Stages (starting from {level})

        2. Weekly Learning Plan based on {hours} hours per week

        3. Important Concepts to Learn

        4. Practice Projects

        5. Reference Resources
        Include YouTube, documentation, and free courses.

        6. Estimated Time to Complete
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
        )

        result = chat_completion.choices[0].message.content

        st.success(f"Learning roadmap generated for {level} level in {topic}")

        st.subheader("📚 Your Learning Roadmap")
        st.write(result)

        # Create PDF
        def create_pdf(text):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for line in text.split("\n"):
                pdf.multi_cell(0, 8, txt=line)

            pdf.output("learning_path.pdf")

        create_pdf(result)

        with open("learning_path.pdf", "rb") as file:
            st.download_button(
                label="📄 Download Learning Plan",
                data=file,
                file_name="learning_path.pdf"
            )

st.divider()

# Progress Tracker
st.subheader("📊 Track Your Learning Progress")

tasks = [
    "Complete Basics",
    "Practice Exercises",
    "Build First Project",
    "Build Advanced Project"
]

for task in tasks:
    st.checkbox(task)

st.divider()

# Resource Section
st.subheader("📚 Recommended Learning Resources")

st.markdown("[Python Full Course - FreeCodeCamp](https://www.youtube.com/watch?v=rfscVS0vtbw)")
st.markdown("[Machine Learning Course - Coursera](https://www.coursera.org/learn/machine-learning)")
st.markdown("[Python Documentation](https://docs.python.org/3/)")

st.divider()

# AI Mentor
st.subheader("🤖 Ask AI Mentor")

question = st.text_input("Ask any doubt about the topic")

if st.button("Ask AI Mentor"):

    if question == "":
        st.warning("⚠️ Please enter a question.")
    else:

        mentor_prompt = f"""
        Topic: {topic}
        User Level: {level}

        Question: {question}

        Explain in a beginner friendly way suitable for a {level} learner.
        """

        mentor_chat = client.chat.completions.create(
            messages=[
                {"role": "user", "content": mentor_prompt}
            ],
            model="llama-3.1-8b-instant",
        )

        mentor_answer = mentor_chat.choices[0].message.content

        st.write(mentor_answer)