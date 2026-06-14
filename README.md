# 🎓 AI Study Buddy

An AI-powered learning assistant developed as part of the **EDUNET FOUNDATION | IBM SkillsBuild | Artificial Intelligence | 6-Week Internship (May 2026 Batch)**.

AI Study Buddy transforms study materials such as PDFs, images, and YouTube lectures into structured learning resources including summaries, quizzes, flashcards, and AI-generated answers.

---

## 🚀 Live Demo

🔗 https://aicte-batch1-internship-may-2026---ai-powered-study-buddy-git.streamlit.app/

## 📂 GitHub Repository

🔗 https://github.com/VishalJangirM/AICTE-Batch1-Internship-May-2026---Ai-Powered-Study-Buddy-

---

## 📖 Project Overview

Students often spend significant time reading lengthy documents, watching educational videos, and creating revision notes. AI Study Buddy simplifies this process by automatically extracting information from multiple sources and converting it into concise, interactive learning content.

The application leverages Artificial Intelligence, OCR, Natural Language Processing, and Retrieval-Augmented Generation (RAG) techniques to enhance learning efficiency and knowledge retention.

---

## 🎯 Objectives

* Simplify the learning process using AI.
* Convert unstructured content into organized study material.
* Improve revision efficiency through quizzes and flashcards.
* Provide instant AI-powered academic assistance.
* Enhance student productivity and understanding.

---

## ✨ Key Features

### 📄 PDF Analyzer

* Extract text from PDF documents
* Generate summaries
* Create question-answer pairs
* Build quizzes and flashcards

### 🖼️ Visual Notes (OCR)

* Extract text from images
* Analyze handwritten or printed notes
* Generate structured study material

### 🎥 Video Lecture Analysis

* Extract YouTube transcripts
* Generate concise summaries
* Create revision resources from video content

### 🤖 AI Tutor

* Context-aware question answering
* Personalized learning assistance
* Instant concept clarification

### 📝 Smart Summary

* Condense lengthy content into concise notes
* Highlight key concepts and important points

### ❓ Exam Simulator

* Generate AI-powered quizzes
* Self-assessment and knowledge evaluation

### 🗂️ Flashcards

* Quick revision cards
* Improve memory retention and recall

### 📊 Study Analytics

* Track study activity
* Monitor learning progress
* Gain actionable insights

---

## 🏗️ System Workflow

```text
Input (PDF / Image / YouTube)
            │
            ▼
      Text Extraction
            │
            ▼
      Content Chunking
            │
            ▼
   Embedding Generation
            │
            ▼
      FAISS Vector Store
            │
            ▼
      User Question
            │
            ▼
   Relevant Chunk Retrieval
            │
            ▼
       Gemini AI Model
            │
            ▼
     Generated Response
```

---

## 🛠️ Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### Artificial Intelligence

* Google Gemini API
* Retrieval-Augmented Generation (RAG)

### Machine Learning & NLP

* Sentence Transformers
* FAISS Vector Database

### Document Processing

* PyPDF
* OCR Processing

### Video Processing

* YouTube Transcript API

---

## 📁 Project Structure

```text
study_buddy/
│
├── app.py
├── core/
│   └── gemini_client.py
│
├── rag/
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── vector_store.py
│
├── flashcards.py
├── quiz_generator.py
├── summarizer.py
├── qa.py
├── image_reader.py
├── pdf_reader.py
├── yt_transcript.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/VishalJangirM/AICTE-Batch1-Internship-May-2026---Ai-Powered-Study-Buddy-.git
cd AICTE-Batch1-Internship-May-2026---Ai-Powered-Study-Buddy-
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### Run Application

```bash
streamlit run app.py
```

---

## 📸 Application Preview

Add screenshots of:

* Landing Page
* PDF Analyzer
* Quiz Generator
* AI Tutor
* Study Analytics Dashboard

---

## 🎓 Internship Details

**EDUNET FOUNDATION | IBM SkillsBuild**

**Domain:** Artificial Intelligence

**Duration:** 6 Weeks

**Batch:** May 2026

This project was developed as part of the internship program to apply AI concepts in solving real-world educational challenges.

---

## 🔮 Future Enhancements

* Multi-language support
* Voice-based learning assistant
* Personalized study plans
* Cloud database integration
* Mobile application support
* Advanced analytics dashboard

---

## 👨‍💻 Author

**Vishal Jangir M**

Artificial Intelligence & Data Science Enthusiast

---

## 📜 License

This project is developed for educational and learning purposes as part of the IBM SkillsBuild Internship Program.
