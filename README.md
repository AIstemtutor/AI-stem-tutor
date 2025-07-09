# 🤖 AI STEM Tutor

AI STEM Tutor is an interactive, AI-powered educational assistant that helps students learn STEM subjects through text, voice, image, and PDF-based inputs. Built with Streamlit and powered by Generative AI, this app allows students to ask questions, extract content from notes, solve handwritten queries, take quizzes, and bookmark useful answers.



---

## 🔍 Features

- 🧠 **Ask Doubts in Any STEM Subject**
  - Ask questions by typing or speaking
  - Select subject (Physics, Chemistry, Math, Bio, CS)
  - AI gives clear, student-friendly answers

- 📄 **PDF Notes Support**
  - Upload class notes or books
  - Ask questions based on the content
  - Preview extracted text

- 📷 **Image-Based Doubt Solving**
  - Upload images of handwritten or printed questions
  - OCR extracts text and AI explains the question

- 📝 **Auto-Generated Quizzes**
  - Upload theory-based PDFs
  - AI generates multiple-choice questions (MCQs)
  - Timer-based quiz with score tracking

- 🔖 **Bookmark Questions**
  - Save important Q&As for future revision

- 🌙 **Dark Mode Toggle**
  - Switch between light and dark themes

- 🕓 **Conversation History**
  - Track previous questions and answers in a collapsible view

---

## 🛠️ Tech Stack

| Tool            | Purpose                            |
|-----------------|------------------------------------|
| `Streamlit`     | UI framework                       |
| `OpenAI/Groq`   | Generative AI for answers & quizzes|
| `Tesseract OCR` | Extract text from images           |
| `PyMuPDF`       | Read and parse PDF documents       |
| `SpeechRecognition` | Convert speech to text        |
| `Python`        | Core programming language          |
| `Lottie`        | Add animated robot for engagement  |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-stem-tutor.git
cd ai-stem-tutor
