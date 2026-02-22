import os
import streamlit as st

from backend.loader import load_documents
from backend.embeddings import create_vector_db
from backend.rag import get_answer
from backend.images import get_supporting_images
from backend.quiz import generate_quiz
from backend.tts import text_to_speech


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="DataSpark Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= MODERN VIBRANT CSS WITH NEW LAYOUT =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-attachment: fixed;
}

.main {
    padding: 2rem;
}

.main .block-container {
    max-width: 1400px;
    padding: 0 3rem;
}

/* Remove ALL empty divs */
.main div:empty {
    display: none !important;
}

/* Force removal of vertical block spacing */
.main > div > div > div:empty {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
}

/* ========== SIDEBAR ========== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    border-right: 5px solid #ffd700;
}

section[data-testid="stSidebar"] > div {
    padding: 2rem 1.5rem;
}

/* Sidebar Text - Headers and General Content */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {
    color: #ffd700 !important;
    font-weight: 800 !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

section[data-testid="stSidebar"] > div > div > p,
section[data-testid="stSidebar"] > div > div > ul > li,
section[data-testid="stSidebar"] .markdown-text-container p,
section[data-testid="stSidebar"] .markdown-text-container li,
section[data-testid="stSidebar"] .markdown-text-container span,
section[data-testid="stSidebar"] .markdown-text-container strong {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* File Uploader in Sidebar */
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 3px dashed #ffd700;
    border-radius: 20px;
    padding: 2rem 1rem;
}

section[data-testid="stSidebar"] div[data-testid="stFileUploader"]:hover {
    background: #fffef0 !important;
    border-color: #ff6b9d;
}

section[data-testid="stSidebar"] div[data-testid="stFileUploader"] label,
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] p,
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] span,
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] div,
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] small,
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] * {
    color: #1a1a2e !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
}

/* Force dark text in file uploader input area */
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] input {
    color: #1a1a2e !important;
}

/* File uploader drag and drop text */
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
    color: #1a1a2e !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] div[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%) !important;
    color: #ffffff !important;
    font-weight: 900 !important;
    font-size: 1.1rem !important;
    border: 3px solid #ffd700 !important;
    padding: 0.8rem 1.5rem !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4) !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
}

/* ========== HERO SECTION ========== */
.hero-container {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 25%, #c44569 50%, #a83279 75%, #8b008b 100%);
    border-radius: 30px;
    padding: 4rem 3rem;
    margin-bottom: 3rem;
    margin-top: 1rem;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    border: 5px solid #ffd700;
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 200%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { left: -100%; }
    100% { left: 100%; }
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    color: #ffffff;
    text-align: center;
    margin-bottom: 1rem;
    text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
    position: relative;
    z-index: 1;
}

.hero-subtitle {
    font-size: 1.3rem;
    color: #ffd700;
    text-align: center;
    font-weight: 600;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
}

.feature-badges {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
    position: relative;
    z-index: 1;
}

.badge {
    background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
    color: #1a1a2e;
    padding: 0.8rem 1.5rem;
    border-radius: 30px;
    font-weight: 800;
    font-size: 1.05rem;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    border: 3px solid #ffffff;
}

/* ========== MAIN CONTENT CARDS ========== */
.content-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 25px;
    /*padding: 2.5rem;*/
    margin-bottom: 2rem;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    border: 4px solid #667eea;
    transition: all 0.3s ease;
}

.content-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(102, 126, 234, 0.4);
    border-color: #ff6b9d;
}

/* Card Headers - Dark Text on Light Background */
.content-card h1,
.content-card h2,
.content-card h3 {
    color: #1e3c72 !important;
    font-weight: 800 !important;
    margin-bottom: 1.5rem !important;
    font-size: 2rem !important;
}

/* Card Text - Dark on Light */
.content-card p,
.content-card div,
.content-card span,
.content-card label {
    color: #2c3e50 !important;
    font-weight: 500 !important;
    line-height: 1.8 !important;
}

/* ========== ANSWER CARD (SPECIAL STYLING) ========== */
.answer-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 5px solid #ffd700;
    border-left: 15px solid #ff6b9d;
}

.answer-card h3 {
    color: #ffd700 !important;
    font-size: 2.2rem !important;
}

.answer-card p,
.answer-card div {
    color: #ffffff !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    line-height: 2 !important;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

/* ========== QUIZ CARDS ========== */
.quiz-question-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    border-radius: 20px;
   /* padding: 2rem;*/
    margin-bottom: 1.5rem;
    border: 4px solid #ffd700;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.quiz-question-card strong {
    color: #1a1a2e !important;
    font-size: 1.3rem !important;
    font-weight: 800 !important;
    display: block;
    margin-bottom: 1rem;
}

/* ========== BUTTONS ========== */
.stButton > button {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%) !important;
    color: #ffffff !important;
    font-weight: 900 !important;
    font-size: 1.2rem !important;
    padding: 1.2rem 2rem !important;
    border-radius: 20px !important;
    border: 4px solid #ffd700 !important;
    box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
    transition: all 0.3s ease !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
    letter-spacing: 1px !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ee5a6f 0%, #c44569 100%) !important;
    transform: translateY(-5px) scale(1.02) !important;
    box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6) !important;
    border-color: #ff6b9d !important;
}

/* Secondary Button Style */
.secondary-button button {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
    border-color: #ffd700 !important;
}

.secondary-button button:hover {
    background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%) !important;
}

/* ========== TEXT INPUT ========== */
input[type="text"] {
    background: #ffffff !important;
    color: #1a1a2e !important;
    border: 4px solid #667eea !important;
    border-radius: 15px !important;
    padding: 1.2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

input[type="text"]:focus {
    border-color: #ff6b9d !important;
    box-shadow: 0 0 0 4px rgba(255, 107, 157, 0.2) !important;
    outline: none !important;
}

input[type="text"]::placeholder {
    color: #7f8c8d !important;
    font-weight: 500 !important;
}

/* ========== RADIO BUTTONS ========== */
.stRadio > div {
    background: rgba(255, 255, 255, 0.5);
    padding: 1.5rem;
    border-radius: 15px;
    border: 3px solid rgba(102, 126, 234, 0.3);
}

.stRadio label {
    color: #1a1a2e !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 0.8rem !important;
}

.stRadio label:hover {
    background: rgba(255, 215, 0, 0.3);
    border-radius: 10px;
}

/* ========== ALERTS ========== */
div[data-testid="stAlert"] {
    border-radius: 15px;
    padding: 1.5rem;
    font-weight: 800;
    font-size: 1.3rem;
    border: 4px solid;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

/* Success Alert */
div[data-testid="stAlert"][data-baseweb="notification"] {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
    border-color: #ffd700 !important;
    color: #ffffff !important;
}

/* Info Alert */
div[data-testid="stAlert"][kind="info"] {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
    border-color: #667eea !important;
    color: #1a1a2e !important;
    font-weight: 900 !important;
}

/* Warning Alert */
div[data-testid="stAlert"][kind="warning"] {
    background: linear-gradient(135deg, #ff6b6b 0%, #f5576c 100%) !important;
    border-color: #ffd700 !important;
    color: #ffffff !important;
}

/* Success/Warning/Info message text */
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] div,
div[data-testid="stAlert"] span {
    color: inherit !important;
    font-weight: 800 !important;
    font-size: 1.3rem !important;
}

/* ========== HIDE EMPTY BLOCKS ========== */
/* Hide empty expanders and containers */
div[data-testid="stExpander"]:empty,
div[data-testid="stVerticalBlock"]:empty,
.element-container:empty {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Hide streamlit default spacing blocks */
.row-widget.stButton + div:empty,
div[data-testid="column"] > div:empty {
    display: none !important;
}

/* Remove extra spacing */
.main .block-container > div:empty {
    display: none !important;
}

/* Remove unnecessary margins between elements */
.element-container {
    margin-bottom: 0 !important;
}

/* Fix spacing for cards */
.content-card + .element-container:empty + .content-card {
    margin-top: 2rem;
}

/* Remove empty vertical blocks */
div[data-testid="stVerticalBlock"] > div:empty,
div[data-testid="stHorizontalBlock"] > div:empty {
    display: none !important;
}

/* Control spacing in columns */
div[data-testid="column"] {
    padding-top: 0 !important;
}

/* Remove default streamlit gaps */
.block-container > div:not(.content-card):empty {
    display: none !important;
}

/* Ensure no extra space above sections */
section[data-testid="stSidebar"] + section > div > div > div:empty:first-child {
    display: none !important;
}

/* ========== IMAGES ========== */
.stImage {
    border-radius: 20px;
    border: 5px solid #667eea;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    transition: all 0.3s ease;
}

.stImage:hover {
    transform: scale(1.05);
    border-color: #ff6b9d;
    box-shadow: 0 20px 45px rgba(255, 107, 157, 0.4);
}

/* ========== DIVIDER ========== */
.fancy-divider {
    height: 4px;
    background: linear-gradient(90deg, #ff6b6b, #ffd700, #4facfe, #38ef7d, #ff6b6b);
    border-radius: 10px;
    margin: 3rem 0;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {
    width: 14px;
}

::-webkit-scrollbar-track {
    background: #1e3c72;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #ff6b6b, #ffd700, #4facfe);
    border-radius: 10px;
    border: 2px solid #1e3c72;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #4facfe, #ffd700, #ff6b6b);
}

/* ========== WELCOME CARD ========== */
.welcome-content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 5px solid #ffd700;
}

.welcome-content h3 {
    color: #ffd700 !important;
    font-size: 2.5rem !important;
}

.welcome-content p,
.welcome-content li {
    color: #ffffff !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
}

.welcome-content strong {
    color: #ffd700 !important;
    font-weight: 800 !important;
}

/* ========== SPINNER ========== */
.stSpinner > div {
    border-top-color: #ffd700 !important;
    border-right-color: #ff6b9d !important;
}

/* ========== FOOTER ========== */
.footer-text {
    text-align: center;
    color: #ffffff;
    font-size: 1.2rem;
    font-weight: 700;
    padding: 2rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .content-card {
        padding: 1.5rem;
    }
    
    .main .block-container {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ================= HERO SECTION =================
st.markdown("""
<div class="hero-container">
    <div class="hero-title"> DataSpark Assistant</div>
    <div class="hero-subtitle">Transform Your Documents into Interactive Learning Experiences</div>
    <div class="feature-badges">
        <div class="badge"> Upload Documents</div>
        <div class="badge"> Ask Questions</div>
        <div class="badge"> Visual Learning</div>
        <div class="badge"> Audio Support</div>
        <div class="badge"> Practice Quizzes</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
for key, default in {
    "db": None,
    "documents": None,
    "answer": None,
    "question": "",
    "quiz": None,
    "quiz_answers": {},
    "file_processed": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 📂 Document Upload")
    st.markdown("---")
    
    uploaded_files = st.file_uploader(
    "Choose your documents",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True
)

    
    st.markdown("---")
    
    if st.session_state.file_processed:
        st.success("✅ Document Loaded Successfully!")
        st.markdown("---")
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        ** Ask Better Questions:**
        - Be specific and clear
        - Use keywords from document
        - Ask conceptual questions
        
        **🎓 Learn Effectively:**
        - Read the AI answers
        - View supporting visuals
        - Listen to audio version
        - Test with quiz questions
        """)
    else:
        st.info(" Upload a document to get started!")
        st.markdown("---")
        st.markdown("###  Supported Formats")
        st.markdown("""
        - **PDF** documents
        - **TXT** text files
        - **DOCX** Word documents
        """)

# ================= FILE PROCESSING =================
if uploaded_files and not st.session_state.file_processed:
    with st.spinner("🔄 Processing your documents... Please wait"):
        os.makedirs("data/uploads", exist_ok=True)

        all_documents = []

        for uploaded_file in uploaded_files:
            file_path = os.path.join("data", "uploads", uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            docs = load_documents(file_path)
            all_documents.extend(docs)

        st.session_state.documents = all_documents
        st.session_state.db = create_vector_db(all_documents)
        st.session_state.file_processed = True
        st.rerun()


# Reset if new file uploaded
if uploaded_files and st.session_state.file_processed:
    current_files = sorted([f.name for f in uploaded_files])
    if "last_files" not in st.session_state or st.session_state.last_files != current_files:
        st.session_state.file_processed = False
        st.session_state.answer = None
        st.session_state.quiz = None
        st.session_state.last_files = current_files
        st.rerun()



# ================= MAIN CONTENT =================
if st.session_state.db:

    # -------- QUESTION SECTION --------
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("###  Ask Your Question")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.session_state.question = st.text_input(
            "Type your question here",
            placeholder="What are the main points discussed in this document?",
            label_visibility="collapsed"
        )
    
    with col2:
        ask_button = st.button("🔍 Search", use_container_width=True)

    if ask_button and st.session_state.question:
        with st.spinner("🤔 AI is thinking..."):
            st.session_state.answer = get_answer(
                st.session_state.db,
                st.session_state.question
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- ANSWER SECTION --------
    if st.session_state.answer:
        st.markdown('<div class="content-card answer-card">', unsafe_allow_html=True)
        st.markdown("###  AI Answer")
        st.write(st.session_state.answer)
        st.markdown('</div>', unsafe_allow_html=True)

        # -------- TWO COLUMN LAYOUT --------
        col_left, col_right = st.columns([2, 1])

        # LEFT COLUMN - VISUALS
        with col_left:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("###  Visual Resources")
            
            with st.spinner("🎨 Finding relevant images..."):
                images = get_supporting_images(st.session_state.answer)

            if images:
                for idx, img in enumerate(images):
                    if os.path.exists(img):
                        st.image(
                            img,
                            caption=f" Image {idx + 1}",
                            use_container_width=True
                        )
                    else:
                        st.warning(f" Image not found: {img}")
            else:
                st.info("No images available for this answer")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # RIGHT COLUMN - AUDIO
        with col_right:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### Listen")
            st.write("Convert answer to audio")
            
            st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
            if st.button(" Generate Audio", use_container_width=True, key="tts_btn"):
                with st.spinner("Creating audio..."):
                    audio = text_to_speech(st.session_state.answer)
                    st.audio(audio, format="audio/mp3")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    # -------- QUIZ SECTION --------
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Knowledge Quiz")
    st.write("Test your understanding with auto-generated questions")

    if st.button(" Create Quiz", use_container_width=True):
        with st.spinner(" Generating quiz questions..."):
            st.session_state.quiz = generate_quiz(
                st.session_state.documents[0].page_content
            )
            st.session_state.quiz_answers = {}
        st.rerun()

    if st.session_state.quiz:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f'<div class="quiz-question-card">', unsafe_allow_html=True)
            st.markdown(f"<strong>Question {i+1}:</strong>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #1a1a2e; font-size: 1.15rem; font-weight: 600;'>{q['question']}</p>", unsafe_allow_html=True)

            st.session_state.quiz_answers[i] = st.radio(
                f"Choose your answer:",
                list(q["options"].keys()),
                format_func=lambda x: f"{x}. {q['options'][x]}",
                key=f"quiz_{i}",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
        if st.button(" Submit Quiz", use_container_width=True):
            score = sum(
                1 for i, q in enumerate(st.session_state.quiz)
                if st.session_state.quiz_answers.get(i) == q["answer"]
            )
            total = len(st.session_state.quiz)
            percentage = (score / total) * 100
            
            if percentage >= 80:
                st.success(f"🏆 Outstanding! Score: {score}/{total} ({percentage:.0f}%)")
            elif percentage >= 60:
                st.info(f" Good Work! Score: {score}/{total} ({percentage:.0f}%)")
            else:
                st.warning(f" Keep Practicing! Score: {score}/{total} ({percentage:.0f}%)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # -------- WELCOME SCREEN --------
    st.markdown('<div class="content-card welcome-content">', unsafe_allow_html=True)
    st.markdown("###  Welcome to Your AI Learning Assistant")
    
    st.markdown("""
    <p style='font-size: 1.2rem; margin-bottom: 2rem;'>
    Transform any document into an interactive learning experience in 3 simple steps:
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem;'>
            <div style='font-size: 3rem;'></div>
            <h4 style='color: #ffd700;'>Step 1: Upload</h4>
            <p>Upload your PDF, TXT, or DOCX document</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem;'>
            <div style='font-size: 3rem;'></div>
            <h4 style='color: #ffd700;'>Step 2: Ask</h4>
            <p>Type any question about your document</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem;'>
            <div style='font-size: 3rem;'></div>
            <h4 style='color: #ffd700;'>Step 3: Learn</h4>
            <p>Get answers, visuals, audio, and quizzes</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <h4 style='color: #ffd700; text-align: center; margin-bottom: 1.5rem;'>✨ Powerful Features</h4>
    
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;'>
        <div>
            <p><strong> AI-Powered Answers:</strong> Get instant, accurate responses using advanced RAG technology</p>
            <p><strong> Visual Learning:</strong> Automatically discover relevant images and diagrams</p>
        </div>
        <div>
            <p><strong> Audio Support:</strong> Listen to answers with text-to-speech conversion</p>
            <p><strong> Smart Quizzes:</strong> Test your knowledge with AI-generated questions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<div class="footer-text">
    Made with ❤️ using Streamlit • Powered by RAG Technology 
</div>
""", unsafe_allow_html=True)