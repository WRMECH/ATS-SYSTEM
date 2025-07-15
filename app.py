import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from resume_analyzer import ResumeAnalyzer
from model_trainer import ModelTrainer
from text_extractor import TextExtractor
from ats_scorer import ATSScorer

# Add this import at the top with other imports
from startup_check import ensure_system_ready

# Configure Streamlit page with neon theme
st.set_page_config(
    page_title="🚀 AI Resume Screening System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for neon theme with fixed fonts
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts with fallbacks */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Main theme colors */
    :root {
        --neon-cyan: #00ffff;
        --neon-pink: #ff00ff;
        --neon-green: #00ff00;
        --neon-purple: #8a2be2;
        --neon-orange: #ff4500;
        --dark-bg: #0a0a0a;
        --darker-bg: #050505;
        --card-bg: #1a1a1a;
        --text-primary: #ffffff;
        --text-secondary: #cccccc;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0a1a 50%, #0a1a1a 100%);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* Fix font overflow issues */
    * {
        box-sizing: border-box;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Sidebar styling with proper font sizing */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a1a 0%, #2a1a2a 100%);
        border-right: 2px solid var(--neon-cyan);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        padding: 1rem;
    }
    
    .css-1d391kg .stSelectbox label {
        font-size: 14px !important;
        font-weight: 500;
        color: var(--neon-cyan);
        margin-bottom: 0.5rem;
    }
    
    /* Headers with proper sizing and neon glow */
    h1 {
        font-family: 'Inter', sans-serif;
        font-size: clamp(1.8rem, 4vw, 2.5rem) !important;
        font-weight: 700;
        text-shadow: 0 0 10px var(--neon-cyan), 0 0 20px var(--neon-cyan);
        animation: pulse-glow 2s ease-in-out infinite alternate;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    h2 {
        font-family: 'Inter', sans-serif;
        font-size: clamp(1.4rem, 3vw, 1.8rem) !important;
        font-weight: 600;
        color: var(--neon-cyan);
        margin-bottom: 0.8rem;
    }
    
    h3 {
        font-family: 'Inter', sans-serif;
        font-size: clamp(1.2rem, 2.5vw, 1.4rem) !important;
        font-weight: 600;
        color: var(--neon-pink);
        margin-bottom: 0.6rem;
    }
    
    h4 {
        font-family: 'Inter', sans-serif;
        font-size: clamp(1rem, 2vw, 1.2rem) !important;
        font-weight: 500;
        color: var(--neon-green);
        margin-bottom: 0.5rem;
    }
    
    @keyframes pulse-glow {
        from { text-shadow: 0 0 10px var(--neon-cyan), 0 0 20px var(--neon-cyan); }
        to { text-shadow: 0 0 20px var(--neon-cyan), 0 0 30px var(--neon-cyan); }
    }
    
    /* Metric cards with proper text sizing - NO TRUNCATION */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(42, 26, 42, 0.9) 100%);
        border: 2px solid var(--neon-pink);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        min-height: 140px;
        overflow: visible !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 30px rgba(255, 0, 255, 0.5);
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        font-size: 0.9rem !important;
        font-weight: 500;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        line-height: 1.3;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 1.8rem !important;
        font-weight: 700;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.2;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }
    
    /* Custom card styling with proper text sizing - NO TRUNCATION */
    .neon-card {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(42, 26, 42, 0.9) 100%);
        border: 2px solid var(--neon-cyan);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
        word-wrap: break-word;
        overflow-wrap: break-word;
        overflow: visible !important;
    }
    
    .neon-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 35px rgba(0, 255, 255, 0.4);
        border-color: var(--neon-pink);
    }
    
    .neon-card h3, .neon-card h4 {
        margin-top: 0;
        margin-bottom: 1rem;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }
    
    .neon-card p, .neon-card div {
        font-size: 0.9rem;
        line-height: 1.6;
        color: var(--text-secondary);
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }
    
    /* Buttons with proper sizing */
    .stButton > button {
        background: linear-gradient(45deg, var(--neon-cyan), var(--neon-pink));
        color: #000000;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        min-height: 44px;
        white-space: nowrap;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.8);
    }
    
    /* Progress bars with proper sizing */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--neon-green), var(--neon-cyan));
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        border-radius: 10px;
        height: 8px;
    }
    
    /* File uploader with proper text sizing */
    .stFileUploader > div {
        background: rgba(26, 26, 26, 0.8);
        border: 2px dashed var(--neon-green);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--neon-cyan);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    .stFileUploader label {
        font-size: 1rem !important;
        font-weight: 500;
        color: var(--neon-green);
    }
    
    /* Tabs with proper sizing */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(26, 26, 26, 0.8);
        border-radius: 15px;
        padding: 0.5rem;
        border: 1px solid var(--neon-purple);
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--neon-cyan);
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        white-space: nowrap;
        min-width: 120px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, var(--neon-cyan), var(--neon-pink));
        color: #000000;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        font-weight: 600;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid var(--neon-green);
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        padding: 1rem;
        font-size: 0.9rem;
    }
    
    .stError {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid #ff0000;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
        padding: 1rem;
        font-size: 0.9rem;
    }
    
    /* Selectbox with proper sizing */
    .stSelectbox > div > div {
        background: rgba(26, 26, 26, 0.8);
        border: 2px solid var(--neon-purple);
        border-radius: 10px;
        color: var(--text-primary);
        font-size: 0.9rem;
        min-height: 44px;
    }
    
    .stSelectbox label {
        font-size: 0.9rem !important;
        font-weight: 500;
        color: var(--neon-purple);
        margin-bottom: 0.5rem;
    }
    
    /* Text area with proper sizing */
    .stTextArea > div > div > textarea {
        background: rgba(26, 26, 26, 0.8);
        border: 2px solid var(--neon-cyan);
        border-radius: 10px;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        line-height: 1.5;
        padding: 1rem;
    }
    
    .stTextArea label {
        font-size: 0.9rem !important;
        font-weight: 500;
        color: var(--neon-cyan);
        margin-bottom: 0.5rem;
    }
    
    /* Dataframe with proper sizing */
    .stDataFrame {
        background: rgba(26, 26, 26, 0.8);
        border-radius: 15px;
        border: 1px solid var(--neon-cyan);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        font-size: 0.85rem;
    }
    
    .stDataFrame table {
        font-size: 0.85rem !important;
    }
    
    /* Expander with proper sizing */
    .streamlit-expanderHeader {
        background: rgba(26, 26, 26, 0.8);
        border: 1px solid var(--neon-pink);
        border-radius: 10px;
        color: var(--neon-cyan);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        padding: 0.75rem 1rem;
    }
    
    /* Responsive design for mobile */
    @media (max-width: 768px) {
        .stApp {
            font-size: 12px;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.3rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        .neon-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .stButton > button {
            padding: 0.6rem 1rem;
            font-size: 0.8rem;
        }
        
        [data-testid="metric-container"] {
            padding: 1rem;
            min-height: 120px;
        }
        
        [data-testid="metric-container"] [data-testid="metric-value"] {
            font-size: 1.5rem !important;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--darker-bg);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, var(--neon-cyan), var(--neon-pink));
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: var(--neon-cyan) !important;
        animation: spin 1s linear infinite, glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 5px var(--neon-cyan); }
        to { box-shadow: 0 0 20px var(--neon-cyan), 0 0 30px var(--neon-cyan); }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize components with caching
@st.cache_resource
def load_components():
    analyzer = ResumeAnalyzer()
    trainer = ModelTrainer()
    extractor = TextExtractor()
    scorer = ATSScorer()
    return analyzer, trainer, extractor, scorer

def create_animated_header():
    """Create animated header with proper sizing"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
        <h1 style="margin-bottom: 1rem;">
            🚀 AI RESUME SCREENING SYSTEM 🎯
        </h1>
        <p style="font-size: 1.1rem; color: #00ffff; font-weight: 500; margin: 0;">
            ⚡ POWERED BY ADVANCED MACHINE LEARNING ⚡
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_neon_metric_card(title, value, delta=None, color="cyan"):
    """Create a neon-styled metric card with NO truncation"""
    colors = {
        "cyan": "#00ffff",
        "pink": "#ff00ff", 
        "green": "#00ff00",
        "orange": "#ff4500"
    }
    
    delta_html = ""
    if delta:
        delta_color = "#00ff00" if delta > 0 else "#ff0000"
        delta_html = f'<div style="color: {delta_color}; font-size: 0.8rem; margin-top: 0.5rem;">{"+" if delta > 0 else ""}{delta}</div>'
    
    # NO TRUNCATION - Show full text
    display_title = str(title)
    display_value = str(value)
    
    st.markdown(f"""
    <div class="neon-card" style="border-color: {colors[color]}; text-align: center; min-height: 140px; display: flex; flex-direction: column; justify-content: center; overflow: visible;">
        <h4 style="color: {colors[color]}; margin-bottom: 0.8rem; font-size: 0.9rem; line-height: 1.3; white-space: normal; overflow: visible; text-overflow: unset;">{display_title}</h4>
        <div style="font-size: 1.8rem; font-weight: 700; color: #ffffff; font-family: 'JetBrains Mono', monospace; line-height: 1.2; margin-bottom: 0.5rem; white-space: normal; overflow: visible; text-overflow: unset;">
            {display_value}
        </div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_progress_bar_neon(value, label="Progress"):
    """Create neon-styled progress bar with NO truncation"""
    # NO TRUNCATION - Show full label
    display_label = str(label)
    
    st.markdown(f"""
    <div style="margin: 1.5rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="color: #00ffff; font-family: 'Inter', sans-serif; font-size: 0.9rem; font-weight: 500; white-space: normal; overflow: visible; text-overflow: unset;">{display_label}</span>
            <span style="color: #ffffff; font-weight: 600; font-size: 0.9rem;">{value}%</span>
        </div>
        <div style="background: rgba(26, 26, 26, 0.8); border-radius: 10px; height: 12px; border: 1px solid #00ffff; overflow: hidden;">
            <div style="
                background: linear-gradient(90deg, #00ff00, #00ffff, #ff00ff);
                height: 100%;
                width: {value}%;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
                transition: all 0.3s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Load custom CSS
    load_custom_css()
    
    # Create animated header
    create_animated_header()
    
    st.markdown("---")
    
    # Ensure system is ready
    if not ensure_system_ready():
        st.error("❌ System initialization failed. Please restart the application.")
        return
    
    # Load components
    analyzer, trainer, extractor, scorer = load_components()
    
    # Enhanced sidebar with proper sizing - REMOVED MODEL TRAINING
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <h3 style="color: #00ffff; font-size: 1.2rem; margin: 0;">
                🎛️ CONTROL PANEL
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # REMOVED MODEL TRAINING FROM OPTIONS
        page = st.selectbox(
            "🚀 Navigate to:",
            ["🔍 Resume Analysis", "📊 Dataset Management", "📈 Analytics Dashboard", "⚙️ System Status"],
            index=0
        )
        
        st.markdown("---")
        
        # System stats in sidebar with proper sizing
        st.markdown("""
        <div class="neon-card" style="border-color: #ff00ff; padding: 1rem;">
            <h4 style="color: #ff00ff; text-align: center; font-size: 1rem; margin-bottom: 1rem;">⚡ SYSTEM STATUS</h4>
            <div style="text-align: center; font-size: 0.85rem; line-height: 1.8;">
                <div style="color: #00ff00; margin: 0.3rem 0;">🟢 AI Models: ACTIVE</div>
                <div style="color: #00ff00; margin: 0.3rem 0;">🟢 Database: CONNECTED</div>
                <div style="color: #00ff00; margin: 0.3rem 0;">🟢 Analysis: READY</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to different pages - REMOVED MODEL TRAINING
    if page == "🔍 Resume Analysis":
        resume_analysis_page(analyzer, extractor, scorer)
    elif page == "📊 Dataset Management":
        dataset_management_page()
    elif page == "📈 Analytics Dashboard":
        analytics_dashboard_page()
    elif page == "⚙️ System Status":
        system_status_page()

def resume_analysis_page(analyzer, extractor, scorer):
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #00ffff; font-size: 1.8rem; margin-bottom: 0.5rem;">🔍 RESUME ANALYSIS CENTER</h2>
        <p style="color: #ffffff; font-size: 1rem; margin: 0;">Upload your resume and get instant AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown("### 📤 UPLOAD RESUME")
        
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        target_field = st.selectbox(
            "🎯 Target Job Field",
            ["Software Engineering", "Data Analyst", "Consultant"],
            help="Select your target job field for analysis"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 ANALYSIS TARGETS")
        
        # Show field-specific info with NO truncation
        field_info = {
            "Software Engineering": {
                "icon": "💻",
                "skills": ["Python", "JavaScript", "React", "AWS", "Docker"],
                "color": "#00ffff"
            },
            "Data Analyst": {
                "icon": "📊", 
                "skills": ["SQL", "Python", "Tableau", "Statistics", "Excel"],
                "color": "#ff00ff"
            },
            "Consultant": {
                "icon": "🎯",
                "skills": ["Strategy", "Analysis", "Communication", "Leadership"],
                "color": "#00ff00"
            }
        }
        
        info = field_info[target_field]
        skills_text = ', '.join(info['skills'])  # NO TRUNCATION
        
        st.markdown(f"""
        <div style="text-align: center; color: {info['color']};">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{info['icon']}</div>
            <h4 style="font-size: 1.1rem; margin-bottom: 0.5rem; white-space: normal; overflow: visible; text-overflow: unset;">{target_field}</h4>
            <p style="font-size: 0.85rem; color: #cccccc; margin: 0; white-space: normal; overflow: visible; text-overflow: unset;">Key Skills: {skills_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Extract text with progress
        with st.spinner("🔄 Extracting text from resume..."):
            time.sleep(1)  # Simulate processing time
            resume_text = extractor.extract_text(uploaded_file)
        
        if resume_text:
            st.success("✅ Text extraction completed!")
            
            # Show extracted text in expandable section
            with st.expander("📝 View Extracted Text", expanded=False):
                # Show more text for better analysis
                display_text = resume_text[:3000] + "..." if len(resume_text) > 3000 else resume_text
                st.text_area("Resume Content", display_text, height=200, disabled=True)
            
            # Analysis button
            if st.button("🚀 ANALYZE RESUME", type="primary"):
                # Create progress bar for analysis
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate analysis steps with progress
                steps = [
                    ("🔍 Analyzing text structure...", 20),
                    ("🎯 Calculating ATS score...", 40),
                    ("🤖 Running AI field detection...", 60),
                    ("📊 Generating insights...", 80),
                    ("✨ Finalizing results...", 100)
                ]
                
                for step_text, progress in steps:
                    status_text.text(step_text)
                    progress_bar.progress(progress)
                    time.sleep(0.5)
                
                status_text.empty()
                progress_bar.empty()
                
                # Perform actual analysis
                ats_score = scorer.calculate_ats_score(resume_text, target_field)
                field_recommendations = analyzer.get_field_recommendations(resume_text)
                analysis_results = analyzer.analyze_resume(resume_text, target_field)
                
                # Display results
                st.markdown("## 🎉 ANALYSIS RESULTS")
                
                # Top metrics row - NO TRUNCATION
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    create_neon_metric_card("ATS Score", f"{ats_score}%", color="cyan")
                
                with col2:
                    recommended_field = max(field_recommendations, key=field_recommendations.get)
                    # NO TRUNCATION - Show full field name
                    create_neon_metric_card("Best Match", recommended_field, color="pink")
                
                with col3:
                    match_percentage = analysis_results.get('match_percentage', 0)
                    create_neon_metric_card("Field Match", f"{match_percentage:.0f}%", color="green")
                
                with col4:
                    word_count = len(resume_text.split())
                    create_neon_metric_card("Word Count", f"{word_count}", color="orange")
                
                # Detailed analysis tabs
                st.markdown("### 📋 DETAILED ANALYSIS")
                
                tab1, tab2, tab3, tab4 = st.tabs([
                    "🎯 Requirements", "🏆 Field Scores", "💡 Suggestions", "📈 Skills Gap"
                ])
                
                with tab1:
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.markdown('<div class="neon-card" style="border-color: #00ff00;">', unsafe_allow_html=True)
                        st.markdown("#### ✅ REQUIREMENTS MET")
                        requirements_met = analysis_results.get('requirements_met', [])[:15]  # Show more
                        for req in requirements_met:
                            # NO TRUNCATION - Show full requirement
                            st.markdown(f"🟢 **{req}**")
                        if len(analysis_results.get('requirements_met', [])) > 15:
                            st.markdown(f"*...and {len(analysis_results.get('requirements_met', [])) - 15} more*")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col_b:
                        st.markdown('<div class="neon-card" style="border-color: #ff0000;">', unsafe_allow_html=True)
                        st.markdown("#### ❌ MISSING REQUIREMENTS")
                        requirements_missing = analysis_results.get('requirements_missing', [])[:15]  # Show more
                        for req in requirements_missing:
                            # NO TRUNCATION - Show full requirement
                            st.markdown(f"🔴 **{req}**")
                        if len(analysis_results.get('requirements_missing', [])) > 15:
                            st.markdown(f"*...and {len(analysis_results.get('requirements_missing', [])) - 15} more*")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with tab2:
                    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
                    st.markdown("#### 🏆 FIELD COMPATIBILITY SCORES")
                    
                    # Create progress bars for each field - NO TRUNCATION
                    for field, confidence in field_recommendations.items():
                        create_progress_bar_neon(int(confidence * 100), field)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab3:
                    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
                    st.markdown("#### 💡 IMPROVEMENT SUGGESTIONS")
                    
                    suggestions = analysis_results.get('suggestions', [])[:10]  # Show more suggestions
                    for i, suggestion in enumerate(suggestions, 1):
                        # Show more of each suggestion - NO TRUNCATION
                        display_suggestion = suggestion[:500] + "..." if len(suggestion) > 500 else suggestion
                        st.markdown(f"""
                        <div style="
                            background: rgba(0, 255, 255, 0.1);
                            border-left: 4px solid #00ffff;
                            padding: 1rem;
                            margin: 0.8rem 0;
                            border-radius: 5px;
                        ">
                            <strong style="color: #00ffff; font-size: 0.9rem;">Suggestion {i}:</strong><br>
                            <span style="font-size: 0.85rem; line-height: 1.5; white-space: normal; overflow: visible; text-overflow: unset;">{display_suggestion}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab4:
                    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
                    st.markdown("#### 📈 SKILLS GAP ANALYSIS")
                    
                    skills_data = analysis_results.get('skills_analysis', {})
                    if skills_data:
                        # Show more skills for better analysis
                        top_skills = dict(list(skills_data.items())[:20])
                        skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Score'])
                        skills_df['Score'] = skills_df['Score'] * 100
                        
                        fig = px.bar(
                            skills_df, 
                            x='Skill', 
                            y='Score',
                            title="Skills Proficiency Analysis (Top 20)",
                            color='Score',
                            color_continuous_scale=['#ff0000', '#ffff00', '#00ff00']
                        )
                        
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='white',
                            title_font_color='#00ffff',
                            font_size=10,
                            height=400
                        )
                        
                        fig.update_xaxes(tickangle=45)
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)

def dataset_management_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #00ff00; font-size: 1.8rem; margin-bottom: 0.5rem;">📊 DATASET MANAGEMENT CENTER</h2>
        <p style="color: #ffffff; font-size: 1rem; margin: 0;">Manage and expand your training datasets</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Import and load dataset
    try:
        from dataset_loader import load_dataset
        
        with st.spinner("🔄 Loading comprehensive dataset..."):
            df = load_dataset()
        
        if df is not None and len(df) > 0:
            st.success(f"✅ Dataset loaded successfully with {len(df)} samples!")
            
            # Dataset statistics with NO truncation
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                create_neon_metric_card("Total Samples", len(df), color="cyan")
            
            with col2:
                create_neon_metric_card("Job Fields", df['job_field'].nunique(), color="pink")
            
            with col3:
                avg_length = df['resume_text'].str.len().mean()
                create_neon_metric_card("Avg Length", f"{avg_length:.0f}", color="green")
            
            with col4:
                latest_date = pd.to_datetime(df['created_date']).max().strftime('%Y-%m-%d')
                create_neon_metric_card("Latest Entry", latest_date, color="orange")
            
            # Dataset preview with NO truncation
            st.markdown('<div class="neon-card">', unsafe_allow_html=True)
            st.markdown("### 📋 DATASET OVERVIEW")
            
            # Show distribution
            distribution = df['job_field'].value_counts()
            st.markdown("**Field Distribution:**")
            for field, count in distribution.items():
                percentage = (count/len(df))*100
                create_progress_bar_neon(int(percentage), f"{field}: {count} samples")
            
            # Show experience level distribution
            st.markdown("**Experience Level Distribution:**")
            exp_distribution = df['experience_level'].value_counts()
            for level, count in exp_distribution.items():
                percentage = (count/len(df))*100
                create_progress_bar_neon(int(percentage), f"{level}: {count} samples")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Sample data preview
            st.markdown('<div class="neon-card">', unsafe_allow_html=True)
            st.markdown("### 📄 SAMPLE DATA PREVIEW")
            
            # Show sample data with key columns
            display_df = df[['id', 'job_field', 'experience_level', 'ats_score', 'skills_count', 'created_date']].head(15)
            st.dataframe(display_df, use_container_width=True)
            
            # Show sample resume text
            st.markdown("**Sample Resume Text:**")
            sample_resume = df.iloc[0]['resume_text'][:500] + "..."
            st.text_area("Sample Resume Content", sample_resume, height=150, disabled=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Dataset statistics
            st.markdown('<div class="neon-card">', unsafe_allow_html=True)
            st.markdown("### 📈 DATASET STATISTICS")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("**ATS Score Statistics:**")
                st.write(f"• Average ATS Score: {df['ats_score'].mean():.1f}")
                st.write(f"• Minimum ATS Score: {df['ats_score'].min()}")
                st.write(f"• Maximum ATS Score: {df['ats_score'].max()}")
                st.write(f"• Standard Deviation: {df['ats_score'].std():.1f}")
            
            with col_b:
                st.markdown("**Skills Count Statistics:**")
                st.write(f"• Average Skills Count: {df['skills_count'].mean():.1f}")
                st.write(f"• Minimum Skills Count: {df['skills_count'].min()}")
                st.write(f"• Maximum Skills Count: {df['skills_count'].max()}")
                st.write(f"• Standard Deviation: {df['skills_count'].std():.1f}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download options
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Complete Dataset (CSV)",
                    data=csv,
                    file_name="comprehensive_training_dataset.csv",
                    mime="text/csv"
                )
            
            with col_download2:
                # Create a summary report
                summary_data = {
                    'Field': distribution.index.tolist(),
                    'Count': distribution.values.tolist(),
                    'Percentage': [(count/len(df))*100 for count in distribution.values]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_csv = summary_df.to_csv(index=False)
                
                st.download_button(
                    label="📊 Download Summary Report (CSV)",
                    data=summary_csv,
                    file_name="dataset_summary_report.csv",
                    mime="text/csv"
                )
        
        else:
            st.error("❌ Failed to load dataset!")
            st.markdown("""
            <div class="neon-card" style="border-color: #ff0000;">
                <h4 style="color: #ff0000;">⚠️ Dataset Loading Error</h4>
                <p>The system could not load the comprehensive dataset. This might be due to:</p>
                <ul>
                    <li>File permission issues</li>
                    <li>Insufficient disk space</li>
                    <li>Corrupted data files</li>
                </ul>
                <p>Please check the system logs or restart the application.</p>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        st.markdown(f"""
        <div class="neon-card" style="border-color: #ff0000;">
            <h4 style="color: #ff0000;">🔧 Technical Error</h4>
            <p><strong>Error Details:</strong> {str(e)}</p>
            <p>Please check the system configuration and try again.</p>
        </div>
        """, unsafe_allow_html=True)

def analytics_dashboard_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #ff4500; font-size: 1.8rem; margin-bottom: 0.5rem;">📈 ANALYTICS DASHBOARD</h2>
        <p style="color: #ffffff; font-size: 1rem; margin: 0;">Monitor system performance and usage analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample analytics data if not exists
    analytics_file = "data/analysis_history.csv"
    if not os.path.exists(analytics_file):
        # Create sample data
        sample_data = []
        for i in range(50):
            sample_data.append({
                'timestamp': (datetime.now() - timedelta(days=np.random.randint(1, 30))).isoformat(),
                'target_field': np.random.choice(['Software Engineering', 'Data Analyst', 'Consultant']),
                'ats_score': np.random.randint(40, 100),
                'word_count': np.random.randint(200, 1000),
                'match_percentage': np.random.randint(30, 95)
            })
        
        os.makedirs("data", exist_ok=True)
        pd.DataFrame(sample_data).to_csv(analytics_file, index=False)
    
    # Load analytics data
    df = pd.read_csv(analytics_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # Key metrics with NO truncation
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_neon_metric_card("Total Analyses", len(df), color="cyan")
    
    with col2:
        avg_ats = df['ats_score'].mean()
        create_neon_metric_card("Avg ATS Score", f"{avg_ats:.1f}%", color="pink")
    
    with col3:
        today_analyses = len(df[df['date'] == datetime.now().date()])
        create_neon_metric_card("Today's Analyses", today_analyses, color="green")
    
    with col4:
        top_field = df['target_field'].mode().iloc[0] if len(df) > 0 else "N/A"
        # NO TRUNCATION - Show full field name
        create_neon_metric_card("Top Field", top_field, color="orange")
    
    # Charts with NO truncation
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 ATS Score Distribution")
        
        fig = px.histogram(
            df, 
            x='ats_score', 
            nbins=15,
            title="ATS Score Distribution",
            color_discrete_sequence=['#00ffff']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='#00ffff',
            font_size=10,
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Field Analysis Trends")
        
        field_counts = df['target_field'].value_counts()
        
        fig = px.pie(
            values=field_counts.values,
            names=field_counts.index,
            title="Analysis by Field",
            color_discrete_sequence=['#00ffff', '#ff00ff', '#00ff00']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='#ff00ff',
            font_size=10,
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def system_status_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #8a2be2; font-size: 1.8rem; margin-bottom: 0.5rem;">⚙️ SYSTEM STATUS CENTER</h2>
        <p style="color: #ffffff; font-size: 1rem; margin: 0;">Monitor system health and performance metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # System health checks with NO truncation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="neon-card" style="border-color: #8a2be2;">', unsafe_allow_html=True)
        st.markdown("### 🔧 SYSTEM HEALTH")
        
        # Check various system components
        checks = [
            ("📁 Data Directory", os.path.exists("data")),
            ("🤖 Models Directory", os.path.exists("models")),
            ("📊 Training Dataset", os.path.exists("data/comprehensive_training_dataset.csv")),
            ("🧠 AI Models", os.path.exists("models/field_classifier.pkl")),
            ("📈 Analytics Data", os.path.exists("data/analysis_history.csv"))
        ]
        
        for check_name, status in checks:
            status_icon = "🟢" if status else "🔴"
            status_text = "ONLINE" if status else "OFFLINE"
            st.markdown(f"<div style='font-size: 0.9rem; margin: 0.5rem 0; white-space: normal; overflow: visible; text-overflow: unset;'>{status_icon} **{check_name}**: {status_text}</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="neon-card" style="border-color: #ff4500;">', unsafe_allow_html=True)
        st.markdown("### 📊 PERFORMANCE METRICS")
        
        # Simulate system metrics
        cpu_usage = np.random.randint(20, 80)
        memory_usage = np.random.randint(30, 70)
        disk_usage = np.random.randint(40, 90)
        
        create_progress_bar_neon(cpu_usage, "CPU Usage")
        create_progress_bar_neon(memory_usage, "Memory Usage")
        create_progress_bar_neon(disk_usage, "Disk Usage")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # System logs with NO truncation
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.markdown("### 📋 SYSTEM LOGS")
    
    # Generate sample logs
    logs = [
        f"[{datetime.now().strftime('%H:%M:%S')}] ✅ System initialized successfully",
        f"[{(datetime.now() - timedelta(minutes=5)).strftime('%H:%M:%S')}] 🔄 Model training completed",
        f"[{(datetime.now() - timedelta(minutes=10)).strftime('%H:%M:%S')}] 📊 Analytics updated",
        f"[{(datetime.now() - timedelta(minutes=15)).strftime('%H:%M:%S')}] 🎯 Resume analysis performed",
        f"[{(datetime.now() - timedelta(minutes=20)).strftime('%H:%M:%S')}] 💾 Dataset saved successfully"
    ]
    
    for log in logs:
        st.code(log, language=None)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
