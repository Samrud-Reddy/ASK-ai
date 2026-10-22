# ASK AI

**Curriculum-Grounded Retrieval-Augmented Generation (RAG) Assistant for AS & A-Level Students**

## Overview

**ASK AI** is a full-stack Retrieval-Augmented Generation (RAG) Q&A tool designed to answer AS & A-Level students' questions strictly from official course materials and textbooks.

General-purpose LLMs often hallucinate or provide answers that fall outside exam board specifications and syllabus mark schemes. ASK AI solves this by **OCR-ing a 900-page textbook into structured paragraph chunks stored in Pinecone**, and grounding **Google Gemini** responses in the **top 3–5 retrieved paragraphs** to curb hallucination.

---

## Getting Started
### Prerequisites

1. **Python 3.9+** and **Node.js 18+**
2. **System Dependencies** (required by `pdf2image` and `pytesseract`):
   - **Ubuntu / Debian**:
     ```bash
     sudo apt-get update && sudo apt-get install -y tesseract-ocr poppler-utils
     ```
3. **API Keys**:
   - A **Google Gemini API Key** (from Google AI Studio)
   - A **Pinecone API Key** with an index named `textbooks` (dimension: `768`)

### 1. Backend Setup

1. Clone the repository and install Python dependencies:
   ```bash
   git clone <repository-url>
   cd ASK-ai
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

3. Start the Flask development server (runs on `http://127.0.0.1:5000`):
   ```bash
   flask --app server run --port 5000
   ```

### 2. Frontend Setup

1. Open a new terminal, navigate to the `website/` directory, and install dependencies:
   ```bash
   cd website
   npm install
   ```

2. Start the Vite development server:
   ```bash
   npm run dev
   ```

3. Open the local URL shown in your terminal (typically `http://localhost:5173`) to use the application.
