import streamlit as st
import json
import os
import toml
from utils.qloo_api import QlooAPI
from utils.perplexity_api import PerplexityAPI
from utils.openai_api import OpenAIAPI
from utils.music_trends_api import MusicTrendsAPI
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="🚀 AI Influencer Research Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load API keys
@st.cache_data
def load_api_keys():
    """Load API keys from Streamlit secrets or secrets.toml file"""
    try:
        return {
            'qloo': st.secrets.get('QLOO_API_KEY') or st.secrets.get('qloo'),
            'perplexity': st.secrets.get('PERPLEXITY_API_KEY') or st.secrets.get('perplexity'), 
            'openai': st.secrets.get('OPENAI_API_KEY') or st.secrets.get('openai')
        }
    except:
        try:
            secrets = toml.load("secrets.toml")
            return {
                'qloo': secrets.get('default', {}).get('QLOO_API_KEY') or secrets.get('secrets', {}).get('qloo'),
                'perplexity': secrets.get('default', {}).get('PERPLEXITY_API_KEY') or secrets.get('secrets', {}).get('perplexity'), 
                'openai': secrets.get('default', {}).get('OPENAI_API_KEY') or secrets.get('secrets', {}).get('openai')
            }
        except:
            return {'qloo': None, 'perplexity': None, 'openai': None}

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'api_keys': load_api_keys(),
        'messages': [],
        'user_profile': {},
        'onboarding_complete': False,
        'world_data': None,
        'content_analysis': None,
        'growth_insights': None
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Enhanced CSS with Dark Mode, Animations, and Professional Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #10b981;
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --text-primary: #1a202c;
    --text-secondary: #718096;
    --border-color: #e2e8f0;
    --shadow-light: 0 4px 12px rgba(0,0,0,0.08);
    --shadow-medium: 0 10px 25px rgba(0,0,0,0.15);
    --shadow-heavy: 0 20px 40px rgba(0,0,0,0.2);
}

[data-theme="dark"] {
    --bg-primary: #1a202c;
    --bg-secondary: #2d3748;
    --text-primary: #f7fafc;
    --text-secondary: #a0aec0;
    --border-color: #4a5568;
    --shadow-light: 0 4px 12px rgba(0,0,0,0.3);
    --shadow-medium: 0 10px 25px rgba(0,0,0,0.4);
    --shadow-heavy: 0 20px 40px rgba(0,0,0,0.6);
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

body {
    background: var(--bg-secondary);
    color: var(--text-primary);
}

/* Theme Toggle */
.theme-toggle {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1001;
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: var(--shadow-light);
    transition: all 0.3s ease;
}

.theme-toggle:hover {
    transform: scale(1.1) rotate(180deg);
    box-shadow: var(--shadow-medium);
}

/* Enhanced Hero Section */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 25px;
    margin-bottom: 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-heavy);
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: rotate(45deg);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.hero h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #fff, #f0f8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(255,255,255,0.5);
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 20px rgba(255,255,255,0.5), 0 0 30px rgba(255,255,255,0.3); }
    to { text-shadow: 0 0 30px rgba(255,255,255,0.8), 0 0 40px rgba(255,255,255,0.4); }
}

.hero p {
    font-size: 1.4rem;
    opacity: 0.95;
    font-weight: 400;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

/* Enhanced Chat Messages */
.chat-msg {
    padding: 1.5rem;
    margin: 1.5rem 0;
    border-radius: 20px;
    border: 1px solid var(--border-color);
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.chat-msg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
    pointer-events: none;
}

.msg-ai {
    background: linear-gradient(135deg, var(--bg-primary), rgba(102, 126, 234, 0.05));
    border-left: 4px solid var(--primary-color);
    transform: translateX(0);
    animation: slideInLeft 0.5s ease-out;
}

.msg-user {
    background: linear-gradient(135deg, var(--bg-primary), rgba(16, 185, 129, 0.05));
    border-left: 4px solid var(--accent-color);
    transform: translateX(0);
    animation: slideInRight 0.5s ease-out;
}

@keyframes slideInLeft {
    from { transform: translateX(-100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInRight {
    from { transform: translateX(100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.chat-msg:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: var(--shadow-medium);
}

/* Enhanced Insight Boxes */
.insight-box {
    background: var(--bg-primary);
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: var(--shadow-light);
    margin: 1.5rem 0;
    border: 1px solid var(--border-color);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.insight-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
}

.insight-box:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: var(--shadow-heavy);
    border-color: var(--primary-color);
}

.insight-box h4 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    font-weight: 600;
    font-size: 1.3rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Enhanced Metrics */
.metric {
    text-align: center;
    padding: 2rem 1rem;
    background: linear-gradient(135deg, var(--bg-primary), var(--bg-secondary));
    border-radius: 20px;
    margin: 0.5rem 0;
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.metric::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s;
}

.metric:hover::before {
    left: 100%;
}

.metric:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: var(--shadow-medium);
    border-color: var(--primary-color);
}

.metric h3 {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.metric p {
    color: var(--text-secondary);
    font-weight: 500;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Enhanced API Status */
.api-status {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--bg-primary);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: var(--shadow-medium);
    z-index: 1000;
    border: 1px solid var(--border-color);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.api-status:hover {
    transform: scale(1.05);
    box-shadow: var(--shadow-heavy);
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0.3rem 0;
    font-weight: 500;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    animation: blink 2s infinite;
}

.status-dot.connected { background: var(--accent-color); }
.status-dot.disconnected { background: #ef4444; }

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.3; }
}

/* Enhanced Trend Tags */
.trend-tag {
    display: inline-block;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 0.7rem 1.2rem;
    border-radius: 25px;
    margin: 0.4rem;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
}

.trend-tag::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.3s;
}

.trend-tag:hover::before {
    left: 100%;
}

.trend-tag:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    border-color: rgba(255,255,255,0.3);
}

/* Loading Animation */
.loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 3rem;
}

.loading-spinner {
    width: 50px;
    height: 50px;
    border: 4px solid var(--border-color);
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Smooth Transitions */
.stApp {
    transition: all 0.3s ease;
}

/* Button Enhancements */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: var(--shadow-light) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.3s;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: var(--shadow-medium) !important;
}

/* Input Field Enhancements */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 15px !important;
    border: 2px solid var(--border-color) !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    padding: 1rem !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    transform: scale(1.02) !important;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Responsive Design */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2.5rem;
    }
    
    .hero p {
        font-size: 1.1rem;
    }
    
    .insight-box {
        padding: 1.5rem;
    }
    
    .metric {
        padding: 1.5rem 1rem;
    }
}

/* Scroll Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out forwards;
}

/* Print Styles */
@media print {
    .api-status, .theme-toggle {
        display: none !important;
    }
}
</style>

<script>
// Theme Toggle Functionality
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Apply saved theme on load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
});

// Add intersection observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
        }
    });
}, observerOptions);

// Observe elements when they're added to the DOM
setTimeout(() => {
    document.querySelectorAll('.insight-box, .metric, .chat-msg').forEach(el => {
        observer.observe(el);
    });
}, 1000);
</script>
""", unsafe_allow_html=True)

def initialize_apis():
    """Initialize API clients"""
    apis = {}
    
    if st.session_state.api_keys['qloo'] and st.session_state.api_keys['qloo'] != 'your_qloo_api_key_here':
        try:
            apis['qloo'] = QlooAPI(st.session_state.api_keys['qloo'])
        except:
            pass
    
    if st.session_state.api_keys['perplexity'] and st.session_state.api_keys['perplexity'] != 'your_perplexity_api_key_here':
        try:
            apis['perplexity'] = PerplexityAPI(st.session_state.api_keys['perplexity'])
        except:
            pass
    
    if st.session_state.api_keys['openai'] and st.session_state.api_keys['openai'] != 'your_openai_api_key_here':
        try:
            apis['openai'] = OpenAIAPI(st.session_state.api_keys['openai'])
        except:
            pass
    
    return apis

def generate_ai_question(apis, conversation_history):
    """Generate next AI question"""
    # Simple predefined questions to avoid complexity
    simple_questions = [
        "What content niche do you primarily focus on?",
        "Who is your target audience?",
        "What platforms do you mainly use?",
        "What's your main goal with your content?"
    ]
    
    # Count user messages to determine which question to ask
    user_msg_count = len([msg for msg in conversation_history if msg.startswith("You:")])
    
    if user_msg_count < len(simple_questions):
        return simple_questions[user_msg_count]
    else:
        return "Great! Let me analyze your profile now."

def get_comprehensive_insights(apis, user_niche, user_audience):
    """Get comprehensive insights using Perplexity AI - NO HARDCODING"""
    if 'perplexity' not in apis:
        st.error("Perplexity API required for insights generation")
        return None
    
    try:
        # Get global engagement analysis with country scores
        engagement_query = f"""Rate the engagement potential for {user_niche} content targeting {user_audience} across different countries on a scale of 0.0 to 1.0. Consider cultural relevance, internet penetration, and audience interest. Provide scores for: USA, Canada, UK, Germany, France, Japan, Australia, Brazil, India, South Africa. Format as: Country: 0.XX"""
        
        engagement_response = apis['perplexity'].ask_question(engagement_query, model="sonar-pro")
        
        # Get regional trends for the specific niche
        regional_query = f"What are the specific viral trends and content formats for {user_niche} content in different regions: USA, Europe, India, Southeast Asia, Middle East, and Latin America in 2024? Be specific about what works in each region."
        
        regional_response = apis['perplexity'].ask_question(regional_query, model="sonar-pro")
        
        # Get competition analysis using structured response
        from utils.perplexity_api import CompetitorAnalysis
        competition_query = f"""Find the top 5 successful {user_niche} content creators targeting {user_audience} globally in 2024. 
        
        For each creator, provide exact details:
        - name: exact creator name or handle
        - platform: primary platform (TikTok, Instagram, YouTube, etc.)
        - followers: follower count (e.g., "2.5M", "500K")  
        - content_style: brief description of their content style
        - success_factor: what makes them successful (1-2 sentences)
        
        Focus on diverse creators from different regions, not just the same influencer repeatedly."""
        
        competition_response = apis['perplexity'].ask_structured_question(competition_query, CompetitorAnalysis, model="sonar-pro")
        
        # Get global trends using structured response
        from utils.perplexity_api import TrendsAnalysis
        trends_query = f"""Find the top 5 most viral and trending content topics for {user_niche} creators targeting {user_audience} in 2024.
        
        For each trend, provide exact details:
        - trend: concise trend name/topic
        - description: brief description of the trend (1-2 sentences)
        - regions: array of regions where it's popular (e.g., ["USA", "Europe", "Asia"])
        - engagement_score: estimated engagement potential 1-100 (integer)
        
        Focus on current, specific trends that are actively viral right now."""
        
        trends_response = apis['perplexity'].ask_structured_question(trends_query, TrendsAnalysis, model="sonar-pro")
        
        # Process all responses with better extraction
        import re
        
        # Extract country scores with multiple regex patterns
        country_scores = {}
        if engagement_response and 'choices' in engagement_response:
            engagement_content = engagement_response['choices'][0]['message']['content']
            
            # Try multiple patterns to extract scores
            patterns = [
                r'([A-Za-z\s]+)[:=]\s*(0\.\d+)',  # "Country: 0.85"
                r'([A-Za-z\s]+)\s*-\s*(0\.\d+)',   # "Country - 0.85" 
                r'([A-Za-z\s]+)\s+(0\.\d+)',       # "Country 0.85"
                r'(\w+).*?(0\.[0-9]+)'             # Flexible pattern
            ]
            
            country_mapping = {
                'usa': 'USA', 'united states': 'USA', 'america': 'USA',
                'canada': 'CAN', 'uk': 'GBR', 'britain': 'GBR', 'united kingdom': 'GBR',
                'germany': 'DEU', 'france': 'FRA', 'japan': 'JPN',
                'australia': 'AUS', 'brazil': 'BRA', 'india': 'IND',
                'south africa': 'ZAF'
            }
            
            for pattern in patterns:
                matches = re.findall(pattern, engagement_content, re.IGNORECASE)
                for country, score in matches:
                    country_clean = country.strip().lower()
                    if country_clean in country_mapping:
                        try:
                            country_scores[country_mapping[country_clean]] = float(score)
                        except:
                            pass
                if country_scores:  # If we found matches, stop trying other patterns
                    break
        
        # Extract trends with better cleaning
        trends = []
        if trends_response and 'choices' in trends_response:
            content = trends_response['choices'][0]['message']['content']
            
            # Split by various delimiters
            sections = re.split(r'[\n•\-]', content)
            
            for section in sections:
                section = section.strip()
                # Look for numbered items or trend indicators
                if re.match(r'^\d+\.', section) or any(word in section.lower() for word in ['trending', 'popular', 'viral']):
                    # Clean the section
                    clean_section = re.sub(r'^\d+\.\s*', '', section)  # Remove numbering
                    clean_section = re.sub(r'^[\*\-•]\s*', '', clean_section)  # Remove bullets
                    clean_section = clean_section.strip()
                    
                    if len(clean_section) > 10 and len(clean_section) < 80:
                        trends.append(clean_section[:50])
        
        # Extract regional trends with better parsing
        regional_trends = {}
        if regional_response and 'choices' in regional_response:
            regional_content = regional_response['choices'][0]['message']['content']
            
            # Split content into paragraphs
            paragraphs = regional_content.split('\n\n')
            regions = ['USA', 'Europe', 'India', 'Asia', 'Middle East', 'Latin America']
            
            for region in regions:
                best_match = ""
                for paragraph in paragraphs:
                    if region.lower() in paragraph.lower() and len(paragraph) > 30:
                        # Clean up the paragraph
                        clean_para = paragraph.replace('*', '').replace('---', '').strip()
                        clean_para = re.sub(r'^\d+\.\s*', '', clean_para)
                        
                        if len(clean_para) > len(best_match):
                            best_match = clean_para[:150]
                
                if best_match:
                    regional_trends[region] = best_match
        
        # Extract competitors from structured response
        competitors = []
        if competition_response and competition_response.competitors:
            for comp in competition_response.competitors[:5]:
                competitor_info = f"{comp.name} ({comp.platform}) - {comp.followers} followers | {comp.content_style} | Success: {comp.success_factor}"
                competitors.append(competitor_info[:120])  # Limit length
        
        # Extract trends from structured response and update global trends
        if trends_response and trends_response.trends:
            trends = []
            for trend in trends_response.trends[:5]:
                trends.append(trend.trend)
        
        # Get market insights from trends
        insights = ""
        if trends_response and trends_response.trends:
            # Create insights from structured trend data
            top_trend = trends_response.trends[0] if trends_response.trends else None
            if top_trend:
                insights = f"Leading trend: {top_trend.trend}. {top_trend.description} Popular in {', '.join(top_trend.regions[:3])} with {top_trend.engagement_score}/100 engagement potential."
            else:
                insights = f"Current {user_niche} trends show dynamic engagement patterns across global markets."
        else:
            insights = f"Current {user_niche} trends show dynamic engagement patterns across global markets."
        
        return {
            'global_trends': trends[:5] if trends else [],
            'insights': insights or f"Current {user_niche} trends show dynamic engagement patterns across global markets.",
            'country_data': country_scores if country_scores else {},
            'regional_trends': regional_trends,
            'competitors': competitors[:5]
        }
        
    except Exception as e:
        st.error(f"Error generating AI insights: {str(e)}")
        return {
            'global_trends': [],
            'insights': f"Unable to generate insights for {user_niche} content. Please check API connection.",
            'country_data': {},
            'regional_trends': {},
            'competitors': []
        }

def create_world_map(country_data):
    """Create world map visualization"""
    if not country_data:
        # Return empty figure if no data
        fig = go.Figure()
        fig.add_annotation(
            text="No country data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=40, b=0),
            font=dict(family="Inter, sans-serif"),
            title="Global Content Engagement Map"
        )
        return fig
    
    df = pd.DataFrame([
        {'country': country, 'engagement_score': score}
        for country, score in country_data.items()
    ])
    
    if df.empty:
        # Return empty figure if dataframe is empty
        fig = go.Figure()
        fig.add_annotation(
            text="No country data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=40, b=0),
            font=dict(family="Inter, sans-serif"),
            title="Global Content Engagement Map"
        )
        return fig
    
    fig = px.choropleth(
        df,
        locations='country',
        color='engagement_score',
        hover_name='country',
        hover_data={'engagement_score': ':.2f'},
        color_continuous_scale='Viridis',
        locationmode='ISO-3',
        title='Global Content Engagement Potential'
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(family="Inter, sans-serif")
    )
    
    return fig

def main():
    init_session_state()
    apis = initialize_apis()
    
    # API Status
    st.markdown(f"""
    <div class="api-status">
        <strong>API Status</strong><br>
        🟢 Qloo: {'Connected' if 'qloo' in apis else 'Offline'}<br>
        🟢 Perplexity: {'Connected' if 'perplexity' in apis else 'Offline'}<br>
        🟢 OpenAI: {'Connected' if 'openai' in apis else 'Offline'}
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>🚀 AI Influencer Research Studio</h1>
        <p>Powered by Qloo | Discover trends, analyze markets, predict viral content</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show different layouts based on onboarding status
    if not st.session_state.onboarding_complete:
        # Chat Interface - Two Columns
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 💬 AI Strategy Consultant")
            
            # Display conversation
            for i, msg in enumerate(st.session_state.messages):
                if msg.startswith("AI:"):
                    st.markdown(f'<div class="chat-msg msg-ai">🤖 <strong>AI:</strong> {msg[3:].strip()}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-msg msg-user">👤 <strong>You:</strong> {msg[4:].strip()}</div>', unsafe_allow_html=True)
            
            # Initial message
            if not st.session_state.messages:
                st.markdown("""
                <div class="chat-msg msg-ai">
                    🤖 <strong>AI:</strong> Hi! I'm your AI research assistant. What content niche do you primarily focus on? (e.g., tech, lifestyle, business, fitness, etc.)
                </div>
                """, unsafe_allow_html=True)
            
            # Input with dynamic key to clear after completion
            input_key = f"user_input_{len(st.session_state.messages)}"
            user_input = st.text_input("Your response:", key=input_key, placeholder="Tell me about your content...")
            
            # Send button
            if st.button("Send", type="primary", key="send_button") and user_input:
                # Add user message
                st.session_state.messages.append(f"You: {user_input}")
                
                # Count user messages to determine next step
                user_msg_count = len([msg for msg in st.session_state.messages if msg.startswith("You:")])
                
                if user_msg_count <= 4:  # Continue conversation
                    ai_response = generate_ai_question(apis, st.session_state.messages)
                    st.session_state.messages.append(f"AI: {ai_response}")
                    
                    # If we've completed 4 questions, mark onboarding complete
                    if user_msg_count == 4:
                        st.session_state.onboarding_complete = True
                        # Extract user niche and audience from responses
                        user_niche = st.session_state.messages[0].replace("You: ", "") if len(st.session_state.messages) > 0 else "general content"
                        user_audience = st.session_state.messages[2].replace("You: ", "") if len(st.session_state.messages) > 2 else "general audience"
                        with st.spinner("🤖 Generating your personalized insights..."):
                            st.session_state.world_data = get_comprehensive_insights(apis, user_niche, user_audience)
                
                st.rerun()
        
        with col2:
            # Getting started message during onboarding
            st.markdown("### 📊 Your Insights Dashboard")
            st.markdown("""
            <div class="insight-box">
                <h4>💬 Getting Started</h4>
                <p>Chat with the AI on the left to unlock personalized insights!</p>
                <ul>
                    <li>🌍 Global market analysis</li>
                    <li>🚀 Viral content prediction</li>
                    <li>📊 Growth strategies</li>
                    <li>📈 Trending topics</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Dashboard - Full Width
        st.markdown("## 📊 Your AI-Powered Insights Dashboard")
        
        # Metrics Row
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.markdown('<div class="metric"><h3>✅</h3><p>Profile Complete</p></div>', unsafe_allow_html=True)
        with col_b:
            st.markdown(f'<div class="metric"><h3>{len(apis)}/3</h3><p>APIs Active</p></div>', unsafe_allow_html=True)
        with col_c:
            st.markdown('<div class="metric"><h3>🌍</h3><p>Global Ready</p></div>', unsafe_allow_html=True)
        with col_d:
            if st.button("🔄 New Analysis", type="secondary"):
                # Reset for new analysis
                st.session_state.onboarding_complete = False
                st.session_state.messages = []
                st.session_state.world_data = None
                st.rerun()
        
        # Main Dashboard Content
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            # World Map
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("#### 🌍 Global Content Engagement Map")
            
            if st.session_state.world_data and 'country_data' in st.session_state.world_data:
                fig = create_world_map(st.session_state.world_data['country_data'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Loading global engagement data...")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Trending Topics
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("#### 🔥 Viral Trends by Region")
            
            if st.session_state.world_data and 'global_trends' in st.session_state.world_data:
                trends_html = ""
                for trend in st.session_state.world_data['global_trends']:
                    trends_html += f'<span class="trend-tag">{trend}</span>'
                st.markdown(trends_html, unsafe_allow_html=True)
                
                # Show regional trends
                if 'regional_trends' in st.session_state.world_data and st.session_state.world_data['regional_trends']:
                    st.markdown("**📍 Regional Trends:**")
                    for region, trend in st.session_state.world_data['regional_trends'].items():
                        st.markdown(f"**{region}:** {trend}")
                
                # Show insights text
                if 'insights' in st.session_state.world_data:
                    st.markdown("**🎯 Key Insights:**")
                    st.markdown(st.session_state.world_data['insights'])
            else:
                st.info("Loading trending topics...")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Competition Analysis
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("#### 🏆 Competition Analysis")
            
            if st.session_state.world_data and 'competitors' in st.session_state.world_data and st.session_state.world_data['competitors']:
                st.markdown("**Top Competitors in Your Niche:**")
                for i, competitor in enumerate(st.session_state.world_data['competitors'][:3], 1):
                    st.markdown(f"**{i}.** {competitor}")
            else:
                st.info("Loading competition data...")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            # Viral Content Predictor
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("#### 🚀 Viral Content Predictor")
            
            content_idea = st.text_area("Describe your content idea:", placeholder="E.g., A political satire video about current events in Gujarati with English subtitles...", height=100)
            
            if st.button("🔮 Predict Viral Score", key="viral_btn"):
                if 'openai' in apis and content_idea:
                    with st.spinner("Analyzing viral potential..."):
                        try:
                            # Simple viral prediction
                            profile_data = {}
                            for i, msg in enumerate(st.session_state.messages):
                                if msg.startswith("You:"):
                                    profile_data[f'response_{i}'] = msg[4:].strip()
                            
                            prediction = apis['openai'].predict_viral_potential(content_idea, profile_data, [])
                            score = prediction.get('viral_score', 65)
                            color = "#10b981" if score >= 70 else "#f59e0b" if score >= 50 else "#ef4444"
                            
                            st.markdown(f'<div style="text-align: center;"><h1 style="color: {color}; font-size: 3rem; margin: 1rem 0;">{score}/100</h1></div>', unsafe_allow_html=True)
                            
                            col_x, col_y = st.columns(2)
                            with col_x:
                                st.markdown("**Strengths:**")
                                for reason in prediction.get('reasons', ['Engaging topic'])[:3]:
                                    st.markdown(f"✅ {reason}")
                            
                            with col_y:
                                st.markdown("**Improvements:**")
                                for improvement in prediction.get('improvements', ['Add trending hashtags'])[:3]:
                                    st.markdown(f"💡 {improvement}")
                        except Exception as e:
                            st.error(f"Prediction error: {str(e)}")
                elif not content_idea:
                    st.warning("Please describe your content idea first!")
                else:
                    st.warning("OpenAI API required for predictions")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Growth Strategy
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("#### 📈 AI Growth Strategy")
            
            if st.button("🚀 Generate Strategy", key="strategy_btn"):
                if 'openai' in apis:
                    with st.spinner("Generating strategy..."):
                        try:
                            profile_data = {}
                            for i, msg in enumerate(st.session_state.messages):
                                if msg.startswith("You:"):
                                    profile_data[f'response_{i}'] = msg[4:].strip()
                            
                            strategy = apis['openai'].analyze_audience_growth_strategy(profile_data)
                            st.markdown(strategy)
                        except Exception as e:
                            st.markdown("""
                            **Growth Strategy Recommendations:**
                            
                            1. **Content Consistency** - Maintain regular posting schedule
                            2. **Trend Integration** - Incorporate current trending topics
                            3. **Community Engagement** - Actively respond to comments and messages
                            4. **Cross-Platform Presence** - Expand to multiple social platforms
                            5. **Performance Analytics** - Track and optimize based on metrics
                            """)
                else:
                    st.markdown("""
                    **Growth Strategy Recommendations:**
                    
                    1. **Content Consistency** - Maintain regular posting schedule
                    2. **Trend Integration** - Incorporate current trending topics
                    3. **Community Engagement** - Actively respond to comments and messages
                    4. **Cross-Platform Presence** - Expand to multiple social platforms
                    5. **Performance Analytics** - Track and optimize based on metrics
                    """)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Trending Audio/Music Integration
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("#### 🎵 Trending Audio Discovery")
            
            # Initialize Music Trends API
            music_api = MusicTrendsAPI()
            
            # Set default platform (no dropdown)
            selected_platform = "tiktok"
            
            
            # Search functionality
            st.markdown("---")
            search_keyword = st.text_input("🔎 Search for specific sounds:", placeholder="Enter keyword (e.g., 'dance', 'motivation')", key="sound_search")
            
            if search_keyword:
                if 'perplexity' in apis:
                    search_results = music_api.get_trending_sounds(
                        apis['perplexity'],
                        platform=selected_platform,
                        content_category=search_keyword,
                        limit=3
                    )
                else:
                    search_results = music_api._get_fallback_sounds(selected_platform)[:3]
                    
                if search_results:
                    st.markdown(f"**Search Results for '{search_keyword}':**")
                    for sound in search_results:
                        st.markdown(f"🎵 **{sound.get('title', 'Unknown')}** - {sound.get('mood', 'Unknown')} mood")
                else:
                    st.info(f"No sounds found for '{search_keyword}'")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Brand Collaboration Opportunities
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("#### 🤝 Brand Collaboration Finder")
            
            if st.button("🔍 Find Brand Partners", key="brand_btn"):
                if 'perplexity' in apis:
                    with st.spinner("Discovering brand collaboration opportunities..."):
                        try:
                            # Get user profile from messages
                            user_profile = {}
                            content_category = "general"
                            audience_type = "general audience"
                            
                            if st.session_state.messages:
                                content_category = st.session_state.messages[0].replace("You: ", "") if len(st.session_state.messages) > 0 else "general"
                                audience_type = st.session_state.messages[2].replace("You: ", "") if len(st.session_state.messages) > 2 else "general audience"
                            
                            # Get brand collaboration opportunities
                            brands = music_api.get_brand_collaboration_opportunities(
                                apis['perplexity'], 
                                content_category, 
                                audience_type, 
                                platform=selected_platform, 
                                limit=5
                            )
                            
                            if brands:
                                st.markdown(f"**🎯 Brand Collaboration Opportunities for {content_category.title()} Content:**")
                                
                                for i, brand in enumerate(brands, 1):
                                    # Clean all brand data to remove any HTML/formatting
                                    import html
                                    import re
                                    
                                    def clean_brand_data(text):
                                        """Clean any HTML or formatting from brand data"""
                                        if not text or not isinstance(text, str):
                                            return str(text) if text else ""
                                        
                                        # Remove HTML tags
                                        clean_text = re.sub(r'<[^>]*>', '', text)
                                        # Decode HTML entities
                                        clean_text = html.unescape(clean_text)
                                        # Remove markdown formatting
                                        clean_text = re.sub(r'\*+([^*]+)\*+', r'\1', clean_text)
                                        clean_text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', clean_text)
                                        # Clean up whitespace
                                        clean_text = ' '.join(clean_text.split())
                                        return clean_text
                                    
                                    # Clean all brand fields
                                    brand_name = clean_brand_data(brand.get('name', 'Unknown Brand'))
                                    fit_reason = clean_brand_data(brand.get('fit_reason', 'Great alignment with your content niche and audience'))
                                    value_range = clean_brand_data(brand.get('value_range', 'Varies'))
                                    approach = clean_brand_data(brand.get('approach', 'Direct outreach'))
                                    
                                    # Clean collaboration types
                                    collab_types = brand.get('collaboration_types', ['Sponsored Content'])
                                    clean_collab_types = [clean_brand_data(ct) for ct in collab_types[:3]]
                                    
                                    # Create brand card using clean data
                                    st.markdown(f"""
                                    <div style="
                                        background: linear-gradient(135deg, #f0f9ff, #ffffff);
                                        padding: 1.5rem;
                                        border-radius: 15px;
                                        margin: 1rem 0;
                                        border-left: 4px solid #3b82f6;
                                        border: 1px solid #e0f2fe;
                                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                                    ">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                            <strong style="color: #1e40af; font-size: 1.2rem;">🏢 {brand_name}</strong>
                                            <span style="background: #3b82f6; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">
                                                Partnership Ready
                                            </span>
                                        </div>
                                        
                                        <div style="margin: 0.8rem 0;">
                                            <strong style="color: #374151;">Why They're a Good Fit:</strong>
                                            <p style="color: #6b7280; margin: 0.3rem 0; font-size: 0.9rem; line-height: 1.4;">
                                                {fit_reason}
                                            </p>
                                        </div>
                                        
                                        <div style="margin: 0.8rem 0;">
                                            <strong style="color: #374151;">Collaboration Types:</strong>
                                            <div style="margin-top: 0.5rem;">
                                                {' '.join([f'<span style="background: #dbeafe; color: #1e40af; padding: 0.2rem 0.6rem; margin: 0.1rem; border-radius: 12px; font-size: 0.8rem; display: inline-block;">{collab_type}</span>' for collab_type in clean_collab_types])}
                                            </div>
                                        </div>
                                        
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
                                            <div>
                                                <strong style="color: #374151; font-size: 0.9rem;">💰 Value Range:</strong>
                                                <span style="color: #16a34a; font-weight: 600; margin-left: 0.5rem;">{value_range}</span>
                                            </div>
                                            <div style="text-align: right;">
                                                <strong style="color: #374151; font-size: 0.9rem;">📧 Approach:</strong>
                                                <br>
                                                <span style="color: #6b7280; font-size: 0.8rem;">{approach}</span>
                                            </div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # Show music-specific brand partnerships if we have trending sounds
                                try:
                                    # Get a sample sound ID for music brand partnerships
                                    sample_sound_id = f"{selected_platform[0:2]}_sample_001"
                                    music_brands = music_api.get_music_brand_partnerships(
                                        apis['perplexity'], 
                                        sample_sound_id, 
                                        platform=selected_platform
                                    )
                                    
                                    if music_brands:
                                        st.markdown("**🎵 Music-Related Brand Opportunities:**")
                                        for brand in music_brands[:2]:
                                            st.markdown(f"🎼 **{brand.get('name', 'Music Brand')}** - {brand.get('fit_reason', 'Music industry partnership opportunity')[:50]}...")
                                except:
                                    pass
                            else:
                                st.info("No brand collaborations found for the current criteria.")
                                
                        except Exception as e:
                            st.error(f"Error finding brand collaborations: {str(e)}")
                            
                            # Show sample brands as fallback
                            st.markdown("**🤝 Sample Brand Collaboration Opportunities:**")
                            sample_brands = [
                                {"name": "Fashion Forward Co.", "value_range": "$500-$2,000", "fit": "Trendy fashion brand seeking content creators"},
                                {"name": "TechGear Pro", "value_range": "$1,000-$5,000", "fit": "Technology brand looking for product reviewers"},
                                {"name": "Lifestyle Essentials", "value_range": "$200-$1,500", "fit": "Lifestyle brand targeting young demographics"}
                            ]
                            
                            for brand in sample_brands:
                                st.markdown(f"� **{brand['name']}** - {brand['fit']} (*{brand['value_range']}*)")
                else:
                    st.warning("Perplexity API required for brand collaboration discovery")
                    
                    # Show basic guidance without API
                    st.markdown("""
                    **💡 Brand Collaboration Tips:**
                    
                    1. **Research your niche** - Look for brands that align with your content
                    2. **Check engagement rates** - Brands prefer creators with engaged audiences
                    3. **Create a media kit** - Include your stats, demographics, and past work
                    4. **Start small** - Build relationships with smaller brands first
                    5. **Be authentic** - Only partner with brands you genuinely support
                    """)
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
