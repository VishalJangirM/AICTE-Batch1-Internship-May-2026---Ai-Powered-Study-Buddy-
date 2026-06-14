import streamlit as st
import os
from PIL import Image 

def update_rag_pipeline(new_text):
    from rag.chunker import chunk_text
    from rag.embeddings import get_embeddings
    from rag.vector_store import add_to_index

    if not new_text.strip():
        return

    
    new_chunks = chunk_text(new_text)
    if not new_chunks:
        return  
    new_embeddings = get_embeddings(new_chunks)
    if st.session_state.chunks is None:
        st.session_state.chunks = []
    
    st.session_state.chunks.extend(new_chunks)
    st.session_state.index = add_to_index(st.session_state.index, new_embeddings)

# def rebuild_rag():
#     if st.session_state.content_text.strip():
#         chunks, index = build_rag_pipeline(st.session_state.content_text)

#         print("DEBUG CHUNKS:", len(chunks))

#         st.session_state.chunks = chunks
#         st.session_state.index = index

def retrieve_chunks(query):
    from rag.vector_store import search_index
    from rag.embeddings import model
    return search_index(st.session_state.index, st.session_state.chunks, query, model)

from pdf_reader import extract_text
from image_reader import extract_text_from_image
from study_analytics import init_db, log_activity
init_db()

from yt_transcript import get_transcript
# import youtube_reader

from summarizer import summarize_notes
from qa import answer_question_rag
from quiz_generator import generate_quiz    
from flashcards import generate_flashcards
from rag.chunker import chunk_text
from rag.embeddings import model, get_embeddings
from rag.vector_store import build_index



@st.cache_data
def get_summary(text):
    return summarize_notes(text)

@st.cache_data
def get_quiz(text):
    return generate_quiz(text)

@st.cache_data
def get_flashcards(text):
    return generate_flashcards(text)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Study Buddy | Your Personal Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- MODERN CSS ---------------- #
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .hero-subtext {
    text-align: justify;
    line-height: 1.8;
    max-width: 700px;
    }
    .hero-description {
    color: #64748b;
    font-size: 1rem;
    line-height: 1.8;
    text-align: justify;
    padding: 15px 20px;
    background: #eef7ff;
    border-radius: 20px;
    }
            
    /* Global Styles */
    .main {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom Sidebar (Glassmorphism Light) */
    [data-testid="stSidebar"] {
        background: rgba(248, 250, 252, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: #475569;
    }
    
    [data-testid="stSidebar"] img {
        border-radius: 1rem;
        margin-bottom: 1rem;
    }

    /* Custom Card Style */
    .stCard {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        color: #334155;
        line-height: 1.6;
        margin-top: 1rem;
    }

    /* Hero Section */
    .hero-container {
        background: linear-gradient(
            135deg,
            #eff6ff 0%,
            #dbeafe 100%
        );

        padding: 3rem;
        border-radius: 30px;
        border: 1px solid #bfdbfe;
        margin-top: 1rem;
    }

    .hero-text-h1 {
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        line-height: 1;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
    }

    .hero-subtext {
        font-size: 1.25rem;
        color: #64748b;
        max-width: 600px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        background: #2563eb;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: unset;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0.5rem;
        color: #64748b;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border: 1px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #2563eb !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1) !important;
    }

    /* File Uploader styling */
    section[data-testid="stFileUploader"] {
        background-color: rgba(37, 99, 235, 0.02);
        border: 1px dashed rgba(37, 99, 235, 0.1);
        border-radius: 0.5rem;
        padding: 1rem;
    }

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #
if "content_text" not in st.session_state:
    st.session_state.content_text = ""

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "index" not in st.session_state:
    st.session_state.index = None

if "last_rag_text" not in st.session_state:
    st.session_state.last_rag_text = ""

if "processed_sources" not in st.session_state:
    st.session_state.processed_sources = set()

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)

    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.markdown("# 🎓 AI Study Buddy")

    st.markdown("### 🛠️ Lab Tools")
    st.write("Construct your knowledge base here.")
    

    # ---------------- PDF ---------------- #
    with st.expander("📄 PDF Analyzer", expanded=True):
        uploaded_file = st.file_uploader("Upload Document", type=["pdf"], key="pdf_up")

        if uploaded_file:
            source_id = f"pdf_{uploaded_file.name}_{uploaded_file.size}"
            if source_id not in st.session_state.processed_sources:
                with st.spinner("Processing PDF..."):
                    try:
                        text = extract_text(uploaded_file)
                        if text and text.strip():
                            st.session_state.content_text = (st.session_state.content_text + " " + text).strip()
                            update_rag_pipeline(text)
                            st.session_state.processed_sources.add(source_id)
                            log_activity("PDF Uploaded", uploaded_file.name)
                            st.toast("PDF successfully added!", icon="✅")
                        else:
                            st.warning("No text extracted from PDF")
                    except Exception as e:
                        st.error(f"Error reading PDF: {e}")
    # ---------------- IMAGE ---------------- #
    with st.expander("🖼️ Visual Notes", expanded=False):
        uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="img_up")
        if uploaded_image:
            source_id = f"img_{uploaded_image.name}_{uploaded_image.size}"
            if source_id not in st.session_state.processed_sources:
                with st.spinner("OCR in progress..."):
                    try:
                        text = extract_text_from_image(uploaded_image)
                        if text:
                            st.session_state.content_text = (st.session_state.content_text + " " + text).strip()
                            update_rag_pipeline(text)
                            st.session_state.processed_sources.add(source_id)
                            log_activity("Image Uploaded", uploaded_image.name)
                            st.toast("Image text captured!", icon="✅")
                    except Exception as e:
                        st.error(f"Error reading image: {e}")

    # ---------------- YOUTUBE ---------------- #
    with st.expander("📺 Video Lecture", expanded=False):
        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="https://youtube.com/watch?v=...",
            key="yt_up"
        )

    if youtube_url:
        source_id = f"yt_{youtube_url}"
        if source_id not in st.session_state.processed_sources:
            try:
                text = get_transcript(youtube_url)
                if text:
                    st.session_state.content_text = (st.session_state.content_text + " " + text).strip()
                    update_rag_pipeline(text)
                    st.session_state.processed_sources.add(source_id)
                    log_activity("YouTube Transcript", youtube_url)
                    st.success("✅ Transcript added!")
            except Exception as e:
                st.error(f"❌ YouTube Error: {str(e)}")

    # ---------------- CLEAR WORKSPACE ---------------- #
    st.markdown("---")

    if st.button("🗑️ Clear Workspace", use_container_width=True):
        st.session_state.content_text = ""
        st.session_state.chunks = []
        st.session_state.index = None
        st.session_state.processed_sources = set()
        st.rerun()

    # ---------------- KNOWLEDGE BANK STATUS ---------------- #
    if st.session_state.content_text:
        char_count = len(st.session_state.content_text)

        st.markdown(f"""
        <div style='
            background: rgba(37, 99, 235, 0.05);
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid rgba(37, 99, 235, 0.1);
            margin-top: 0.5rem;
        '>
            <span style='color: #2563eb; font-weight: bold;'>
                Knowledge Bank Ready
            </span><br>
            <span style='color: #64748b; font-size: 0.8rem;'>
                {char_count:,} characters indexed
            </span>
        </div>
        """, unsafe_allow_html=True)
        

# ---------------- MAIN CONTENT ---------------- #

# Hero / Dashboard Header
st.container()
col_head1, col_head2 = st.columns([2, 1], gap="large")

with col_head1:
    st.markdown("""
    <h1 class="hero-text-h1">
        Elevate Your<br>Learning.
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-description">
    AI Study Buddy combines document analysis, OCR, transcript extraction, and generative AI to transform learning materials into actionable study resources. Users can upload notes, images, or video lectures to generate concise summaries, practice quizzes, flashcards, and AI-assisted explanations. The platform also includes an analytics dashboard that helps users monitor study activity, track progress, and gain valuable insights into their learning journey.
    </div>
    """, unsafe_allow_html=True)
  
    
with col_head2:
    if os.path.exists("hero.png"):
        st.image("hero.png", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

if not st.session_state.content_text:
    st.info("👋 **Welcome!** Start by uploading your study materials in the sidebar to unlock the AI Lab.")
    
    # Feature Preview Cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid #e2e8f0;'>
            <h3 style='margin-top:0;'>📝 Smart Summary</h3>
            <p style='color: #64748b;'>Condense hours of reading into minutes of understanding.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid #e2e8f0;'>
            <h3 style='margin-top:0;'>❓ Exam Simulator</h3>
            <p style='color: #64748b;'>Test your knowledge with AI-generated quizzes from your own material.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid #e2e8f0;'>
            <h3 style='margin-top:0;'>🤖 24/7 AI Tutor</h3>
            <p style='color: #64748b;'>Ask any question and get instant, context-aware answers.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # Modern Tabbed Interface
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "✨ Intelligence Summary", 
        "📝 Knowledge Quiz", 
        "🗂️ Active Recall Cards", 
        "💬 Ask AI Tutor",
        "📊 Dashboard"
    ])

    with tab1:
        st.markdown("### 📝 Intelligence Summary")
        st.write("Deep insights extracted from your provided resources.")
        if st.button("Generate Intelligence Report", key="sum_btn"):
            with st.spinner("Analyzing content..."):
                result = get_summary(st.session_state.content_text)
                log_activity("Summary Generated")
                st.markdown(f'<div class="stCard">{result}</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown("### ❓ Knowledge Quiz")
        st.write("Test your retention with custom questions.")
        if st.button("Construct Quiz Deck", key="quiz_btn"):
            with st.spinner("Drafting questions..."):
                result = generate_quiz(st.session_state.content_text)
                log_activity("Quiz Generated")
                st.markdown(f'<div class="stCard">{result}</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🗂️ Active Recall Cards")
        st.write("Master the concepts with flashcards.")
        if st.button("Generate Study Cards", key="flash_btn"):
            with st.spinner("Creating flashcards..."):
                result = generate_flashcards(st.session_state.content_text)
                log_activity("Flashcards Generated")
                st.markdown(f'<div class="stCard">{result}</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("### 🤖 Interactive AI Tutor")
        st.write("Ask specifics about your uploaded material.")

        query = st.text_input(
            "Your question:",
            placeholder="e.g. Explain the second law of thermodynamics from my notes..."
        )

        if query:
            with st.spinner("Consulting knowledge base..."):
                log_activity("Question Asked", query)

                retrieved_chunks = retrieve_chunks(query)

                answer = answer_question_rag(
                    retrieved_chunks,
                    query
                )  

            st.markdown(f"""
            <div class="stCard">
                <b style='color: #2563eb;'>Question:</b> {query}<br><br>
                <b style='color: #2563eb;'>Tutor Response:</b><br>{answer}
            </div>
            """, unsafe_allow_html=True)
    with tab5:
        import sqlite3
        import pandas as pd

        conn = sqlite3.connect("studybuddy.db")

        df = pd.read_sql_query(
            "SELECT * FROM activity",
            conn
        )
        conn.close()

        st.title("📊 Learning Analytics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Activities", len(df))

        with col2:
            st.metric(
                "PDFs",
                len(df[df["event_type"] == "PDF Uploaded"])
            )

        with col3:
            st.metric(
                "Questions",
                len(df[df["event_type"] == "Question Asked"])
            )

        with col4:
            st.metric(
                "Videos",
                len(df[df["event_type"] == "YouTube Transcript"])
            )

        st.subheader("Activity Distribution")
        st.bar_chart(df["event_type"].value_counts())

        st.subheader("Recent Activity")
        st.dataframe(
            df.sort_values("timestamp", ascending=False),
            use_container_width=True
        )
# ---------------- FOOTER ---------------- #
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #94a3b8; font-size: 0.8rem; border-top: 1px solid #e2e8f0; " \
"padding-top: 2rem;'>AI Study Buddy •   By Vishal Jangir M </div>", unsafe_allow_html=True) 