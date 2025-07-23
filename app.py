from streamlit_lottie import st_lottie
import streamlit as st
import requests
import os
import fitz  # PyMuPDF
import random
import time
import speech_recognition as sr
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import json
import os
import numpy as np
import base64
import io

def load_lottie_url(url: str):
    try:
        res = requests.get(url)
        if res.status_code != 200:
            return None
        return res.json()
    except:
        return None

HISTORY_FILE = "chat_history.json"
BOOKMARK_FILE = "bookmarked_questions.json"

# Load Chat History
if "chat_history" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            st.session_state["chat_history"] = json.load(f)
    else:
        st.session_state["chat_history"] = []

# Load Bookmarked Questions
if "bookmarked_questions" not in st.session_state:
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
            st.session_state["bookmarked_questions"] = json.load(f)
    else:
        st.session_state["bookmarked_questions"] = []

# Save history back to file (optional)
with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(st.session_state["chat_history"], f, ensure_ascii=False, indent=2)

# Save bookmarks back to file (optional)
with open(BOOKMARK_FILE, "w", encoding="utf-8") as f:
    json.dump(st.session_state["bookmarked_questions"], f, ensure_ascii=False, indent=2)

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
st.set_page_config(page_title="AI STEM Tutor", page_icon="🧠", layout="wide")
def load_lottie_url(url: str):
    try:
        res = requests.get(url)
        if res.status_code != 200:
            return None
        return res.json()
    except:
        return None
robot_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json")
if robot_animation is None:
    st.warning("⚠️ Animation failed to load. Please check the URL or your internet connection.")
else:
    st_lottie(robot_animation, height=300, key="walking-robot-1")

# Streamlit App Config
st.set_page_config(page_title="AI STEM Tutor", page_icon="🧠", layout="wide")
st.markdown("""
    <div style='text-align: center; font-size: 90px;'>🤖</div>
    <h1 style='text-align: center;'>AI STEM Tutor</h1>
""", unsafe_allow_html=True)




# ======================= 🌙 Dark Mode  =======================
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)

if dark_mode:
    st.markdown("""
        <style>
        .stApp { background-color: #1e1e1e; color: #f0f0f0; }
        h1, h2, h3, label, .stMarkdown, .stTextInput label, .stRadio label {
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        .response-box {
            background-color: #333333;
            color: #f5f5f5;
            padding: 1rem;
            border-radius: 12px;
        }
        .stButton > button {
            background-color: #4a90e2 !important;
            color: white !important;
            border-radius: 10px !important;
            border: none;
        }
        .stButton > button:hover {
            background-color: #7fb3f5 !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background-color: #f9f9f6; }

        section[data-testid="stSidebar"] {
            background-color: #2c2c2c !important;
        }
        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        h1, h2, h3, label, .stMarkdown, .stTextInput label, .stRadio label {
            color: #1a1a1a !important;
        }

        .response-box {
            background-color: #dbeadf;
            color: #2a2a2a;
            padding: 1rem;
            border-radius: 12px;
        }

        .stButton > button {
            background-color: #ffcaa6;
            color: #2f2f2f;
            border-radius: 10px;
        }

        .stButton > button:hover {
            background-color: #f5ae84;
        }

        /* 👇 FIX st.info box visibility in light mode */
        div[data-testid="stAlert"] {
            background-color: #d0ebff !important;
            color: #003366 !important;
            font-weight: 600 !important;
            border-left: 5px solid #228be6 !important;
        }

        div[data-testid="stAlert"] p {
            color: #003366 !important;
            font-weight: 600 !important;
        }
        </style>
    """, unsafe_allow_html=True)



# ======================= SIDEBAR NAV =======================
section = st.sidebar.radio("📘 Navigation", ["🏠 Ask Tutor", "📄 PDF Reader", "📝 Quiz Section", "📷 Image Doubt","🔖 Bookmarked Questions"])
with st.sidebar.expander("🕓 Conversation History"):
    if "chat_history" in st.session_state and st.session_state["chat_history"]:
        for i, (q, a) in enumerate(reversed(st.session_state["chat_history"]), 1):
            st.markdown(f"*Q{i}:* {q}", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 12px; margin-bottom: 10px;'>{a[:100]}...</div>", unsafe_allow_html=True)
    else:
        st.write("No history yet.")
        
# 🔖 Bookmarked Questions Section
if section == "🔖 Bookmarked Questions":
    st.title("🔖 Your Bookmarked Questions")

    if not st.session_state["bookmarked_questions"]:
        st.info("You have no bookmarked questions yet.")
    else:
        for idx, b in enumerate(st.session_state["bookmarked_questions"]):
            q, a = b["question"], b["answer"]
            q_hash = abs(hash(q))  # or use something like uuid.uuid4() if needed
            with st.expander(f"🔖 Q{idx+1}: {q[:80]}"):
                st.markdown(f"*Question:* {q}")
                st.markdown("*Answer:*")
                st.markdown(f"<div class='response-box'>{a}</div>", unsafe_allow_html=True)
                if st.button(f"❌ Unbookmark Q{idx+1}", key=f"unbookmark_{q_hash}"):
                    st.session_state["bookmarked_questions"] = [
                         b for b in st.session_state["bookmarked_questions"] if b["question"] != q
            ]
            st.rerun()



# ======================= 📄 PDF READER =======================
elif section == "📄 PDF Reader":
    st.title("📄 Ask From Your Notes (PDF)")

    uploaded_file = st.file_uploader("Upload your PDF notes", type="pdf")
    pdf_text = ""

    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            pdf_text += page.get_text()

        with st.expander("🧾 Preview Extracted Text"):
            st.write(pdf_text[:2000] + "..." if len(pdf_text) > 2000 else pdf_text)

        pdf_question = st.text_area("💭 Ask something from your PDF notes:")

        if st.button("🔍 Get Answer from Notes"):
            if not pdf_question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Thinking..."):
                    prompt = f"""You are a tutor helping a student. They uploaded these notes:\n{pdf_text[:3000]}\nNow answer this question clearly:\n{pdf_question}"""
                    headers = {
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": "llama3-70b-8192",
                        "messages": [{"role": "user", "content": prompt}]
                    }

                    try:
                        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                            headers=headers, json=data, timeout=15)
                        res.raise_for_status()
                        pdf_answer = res.json()["choices"][0]["message"]["content"]

                        st.markdown("#### 🧾 Answer Based on Your Notes:")
                        st.markdown(f"<div class='response-box'>{pdf_answer}</div>", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"⚠ Error: {e}")

# ======================= VOICE TO TEXT =======================
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening... Speak clearly.")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        return r.recognize_google(audio)
    except:
        return "Sorry, I couldn't understand that."

# ======================= 📷 IMAGE DOUBT =======================
HUGGINGFACE_API_TOKEN = "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"  # Replace with your token

def extract_text_from_image(image_bytes):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/trocr-base-handwritten"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return "❌ Error: Unable to extract text."

def ask_tutor(question):
    prompt = f"You are a friendly STEM tutor. Explain this clearly:\n\n{question}"
    headers = {
        "Authorization": f"Bearer your_groq_api_key",  # Replace with your Groq key
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions",
                             headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "❌ Error: Tutor could not respond."

# Streamlit UI
st.title("📷 Image-Based Doubt Solver (No cv2, pytesseract)")

uploaded_image = st.file_uploader("Upload handwritten or printed image", type=["png", "jpg", "jpeg"])
if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    image_bytes = uploaded_image.read()
    with st.spinner("🔍 Extracting text..."):
        question = extract_text_from_image(image_bytes)
    st.markdown("#### ✨ Extracted Question:")
    st.code(question.strip())

    if st.button("Ask Tutor"):
        with st.spinner("🤔 Thinking..."):
            answer = ask_tutor(question)
        st.markdown("#### 🧾 Tutor's Answer:")
        st.markdown(answer)
# ======================= 🧠 ASK TUTOR =======================
if section == "🏠 Ask Tutor":
    st.title("🧠 Ask Your STEM Tutor")

    subject = st.selectbox("📚 Choose your subject", ["Physics", "Math", "Chemistry", "Biology", "Computer Science"])

    # Voice Input
    if st.button("🎤 Speak My Doubt"):
        spoken = recognize_speech()
        st.session_state["question"] = spoken
        st.success(f"🗣 You said: {spoken}")

    # Manual Input
    question = st.text_area("💭 Type or edit your doubt:", value=st.session_state.get("question", ""), height=120)

    if st.button("✨ Ask Tutor"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                prompt = f"You are a helpful and calm {subject} tutor. Explain this clearly:\n\n{question}"
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama3-70b-8192",
                    "messages": [{"role": "user", "content": prompt}]
                }

                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                        headers=headers, json=data, timeout=15)
                    res.raise_for_status()
                    answer = res.json()["choices"][0]["message"]["content"]

                    # Save to session
                    st.session_state["answer"] = answer
                    st.session_state["chat_history"].append((question, answer))

                    # Display
                    st.markdown("#### 🧾 Tutor’s Answer:")
                    st.markdown(f"<div class='response-box'>{answer}</div>", unsafe_allow_html=True)

                    # ✅ Bookmark Option
            
                    if st.button("🔖 Bookmark This Question", key=f"bookmark_{hash(question)}"):
                        already_bookmarked = any(
                            b["question"] == question and b["answer"] == answer
                            for b in st.session_state["bookmarked_questions"]
                            )
                        if not already_bookmarked:
                            st.session_state["bookmarked_questions"].append({"question": question, "answer": answer})
                            with open(BOOKMARK_FILE, "w", encoding="utf-8") as f:
                                json.dump(st.session_state["bookmarked_questions"], f, ensure_ascii=False, indent=2)
                                st.success("✅ Question bookmarked!")
                                st.rerun()
                        else:
                            st.info("This question is already bookmarked!")




                except Exception as e:
                    st.error(f"⚠ Error: {e}")

    # Show chat history
    with st.expander("🕓 View Conversation History"):
        if st.session_state["chat_history"]:
            for i, (q, a) in enumerate(reversed(st.session_state["chat_history"]), 1):
                st.markdown(f"*Q{i}:* {q}")
                st.markdown(f"<div class='response-box'>{a}</div>", unsafe_allow_html=True)
        else:
            st.info("No history yet. Start asking questions!")


# ======================= 📝 QUIZ FROM THEORY =======================
elif section == "📝 Quiz Section":
    st.title("📝 Auto-Generated Quiz From Your Theory Notes")

    uploaded_quiz_pdf = st.file_uploader("Upload a theory-based PDF", type="pdf")
    num_questions = st.number_input("How many questions to generate?", min_value=1, max_value=10, value=3)
    time_per_question = st.number_input("Time per question (in seconds)", min_value=10, max_value=120, value=20)

    if uploaded_quiz_pdf:
        doc = fitz.open(stream=uploaded_quiz_pdf.read(), filetype="pdf")
        content = ""
        for page in doc:
            content += page.get_text()

        with st.expander("📄 Preview Extracted Text"):
            st.write(content[:2000] + "..." if len(content) > 2000 else content)

        if st.button("🧠 Generate Quiz"):
            with st.spinner("Generating MCQs from your content..."):
                prompt = f"""
You are an expert education quiz assistant. Based on this study material, generate exactly {num_questions} MCQs. Each question should follow this format:

Q: What is ...
A) Option A
B) Option B
C) Option C
D) Option D
Answer: B

Here is the theory material:
{content[:3000]}
"""
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama3-70b-8192",
                    "messages": [{"role": "user", "content": prompt}]
                }

                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                        headers=headers, json=data, timeout=30)
                    res.raise_for_status()
                    raw_quiz_text = res.json()["choices"][0]["message"]["content"]
                    st.session_state["quiz_data"] = raw_quiz_text.strip().split("Q:")[1:]
                    st.session_state["quiz_index"] = 0
                    st.session_state["quiz_score"] = 0
                    st.session_state["quiz_answers"] = []
                    st.success("✅ Quiz Generated!")
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")

    if "quiz_data" in st.session_state and st.session_state["quiz_index"] < len(st.session_state["quiz_data"]):
        quiz = st.session_state["quiz_data"][st.session_state["quiz_index"]]
        lines = quiz.strip().split("\n")
        question = lines[0]
        options = lines[1:5]
        correct = next((line for line in lines if "Answer:" in line), "Answer: A").split(":")[-1].strip()

        st.markdown(f"### Q{st.session_state['quiz_index'] + 1}: {question}")
        selected = st.radio("Choose an option:", options, key=f"q_{st.session_state['quiz_index']}")

        if "start_time" not in st.session_state:
            st.session_state["start_time"] = time.time()

        time_elapsed = int(time.time() - st.session_state["start_time"])
        remaining = time_per_question - time_elapsed
        if remaining > 0:
            st.info(f"⏰ Time remaining: {remaining} seconds")
        else:
            st.warning("⏰ Time's up! Moving to next question...")
            st.session_state["quiz_answers"].append((question, correct, "(No Answer)"))
            st.session_state["quiz_index"] += 1
            st.session_state.pop("start_time", None)
            st.rerun()

        if st.button("✅ Submit Answer"):
            selected_letter = selected.split(")")[0]
            st.session_state["quiz_answers"].append((question, correct, selected_letter.strip()))
            if selected_letter.strip() == correct:
                st.success("✅ Correct!")
                st.session_state["quiz_score"] += 1
            else:
                st.error(f"❌ Incorrect. Correct answer: {correct}")
            st.session_state["quiz_index"] += 1
            st.session_state.pop("start_time", None)
            st.rerun()

    elif "quiz_data" in st.session_state:
        total = len(st.session_state["quiz_data"])
        score = st.session_state.get("quiz_score", 0)
        st.markdown(f"### 🧠 Your Final Score: {score}/{total}")

        with st.expander("📘 View Solutions"):
            for i, (q, correct, user_ans) in enumerate(st.session_state["quiz_answers"], 1):
                st.markdown(f"*Q{i}:* {q}")
                st.markdown(f"- ✅ Correct Answer: {correct}")
                st.markdown(f"- 📝 Your Answer: {user_ans}")
