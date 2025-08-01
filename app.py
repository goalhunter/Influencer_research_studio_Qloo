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

# Enhanced CSS with Perfect Light/Dark Mode Support
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --bg-tertiary: #f1f5f9;
    --text-primary: #1a202c;
    --text-secondary: #718096;
    --text-muted: #a0aec0;
    --border-color: #e2e8f0;
    --border-light: #f7fafc;
    
    --shadow-light: 0 4px 12px rgba(0,0,0,0.08);
    --shadow-medium: 0 10px 25px rgba(0,0,0,0.15);
    --shadow-heavy: 0 20px 40px rgba(0,0,0,0.2);
    
    --radius: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
}

[data-theme="dark"] {
    --bg-primary: #1a202c;
    --bg-secondary: #2d3748;
    --bg-tertiary: #4a5568;
    --text-primary: #f7fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #94a3b8;
    --border-color: #4a5568;
    --border-light: #2d3748;
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

/* Hero Section - Works in both modes */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: var(--radius-xl);
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-heavy);
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateX(100%); opacity: 0; }
}

.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
}

.hero p {
    font-size: 1.3rem;
    opacity: 0.9;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

/* API Status - Adapts to theme */
.api-status {
    position: fixed;
    top: 1.5rem;
    right: 1.5rem;
    background: var(--bg-primary);
    padding: 1rem 1.5rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-medium);
    z-index: 1000;
    border: 1px solid var(--border-color);
    min-width: 180px;
    transition: all 0.3s ease;
}

.api-status:hover {
    transform: scale(1.02);
    box-shadow: var(--shadow-heavy);
}

.api-status h4 {
    margin: 0 0 0.75rem 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
}

.status-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0.5rem 0;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-right: 0.5rem;
    animation: blink 2s infinite;
}

.status-connected { background: var(--accent-color); }
.status-disconnected { background: var(--danger-color); }

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.4; }
}

/* Chat Messages - Theme aware */
.chat-msg {
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: var(--radius-lg);
    background: var(--bg-primary);
    box-shadow: var(--shadow-light);
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
}

.chat-msg:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
}

.msg-ai {
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-tertiary) 100%);
    border-left: 4px solid var(--primary-color);
}

.msg-user {
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    border-left: 4px solid var(--accent-color);
}

/* Insight Boxes - Beautiful in both modes */
.insight-box {
    background: var(--bg-primary);
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-light);
    margin: 1.5rem 0;
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
}

.insight-box:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-medium);
    border-color: var(--primary-color);
}

.insight-box h4 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    font-weight: 600;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

/* Metrics - Responsive to theme */
.metric {
    text-align: center;
    padding: 2rem 1rem;
    background: var(--bg-primary);
    border-radius: var(--radius-lg);
    margin: 0.5rem 0;
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
    box-shadow: var(--shadow-light);
}

.metric:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-medium);
    border-color: var(--primary-color);
}

.metric h3 {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.5rem 0;
    font-family: 'Space Grotesk', sans-serif;
}

.metric p {
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0;
}

/* Trend Tags - Multi-colored and theme aware */
.trend-tag {
    display: inline-block;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    margin: 0.25rem;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-light);
    cursor: pointer;
}

.trend-tag:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
}

.trend-tag:nth-child(2n) {
    background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}

.trend-tag:nth-child(3n) {
    background: linear-gradient(135deg, var(--accent-color), var(--primary-color));
}

/* Brand Cards - Professional in both themes */
.collab-card {
    background: var(--bg-primary);
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    margin: 1rem 0;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-light);
    transition: all 0.3s ease;
}

.collab-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-medium);
}

.collab-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.collab-badge {
    background: var(--accent-color);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.75rem;
    font-weight: 600;
}

.collab-types {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 1rem 0;
}

.collab-type {
    background: var(--bg-secondary);
    color: var(--text-secondary);
    padding: 0.4rem 0.8rem;
    border-radius: var(--radius);
    font-size: 0.8rem;
    border: 1px solid var(--border-color);
}

/* Enhanced Buttons - Theme responsive */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow-light) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-medium) !important;
}

/* Input Fields - Beautiful in both modes */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: var(--radius) !important;
    border: 2px solid var(--border-color) !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--text-muted) !important;
}

/* Loading States - Theme aware */
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem;
    text-align: center;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border-color);
    border-top: 3px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Theme Toggle Button */
.theme-toggle {
    position: fixed;
    top: 1.5rem;
    left: 1.5rem;
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
    color: var(--text-primary);
}

.theme-toggle:hover {
    transform: scale(1.1);
    box-shadow: var(--shadow-medium);
}

/* Ensure proper color inheritance */
.stMarkdown, .stMarkdown p, .stMarkdown div {
    color: var(--text-primary);
}

.stMarkdown strong {
    color: var(--text-primary);
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary);
    border-radius: var(--radius);
    padding: 0.25rem;
    border: 1px solid var(--border-color);
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: var(--radius) !important;
    color: var(--text-secondary) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    box-shadow: var(--shadow-light) !important;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Auto dark mode detection */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #1a202c;
        --bg-secondary: #2d3748;
        --bg-tertiary: #4a5568;
        --text-primary: #f7fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: #4a5568;
        --border-light: #2d3748;
        --shadow-light: 0 4px 12px rgba(0,0,0,0.3);
        --shadow-medium: 0 10px 25px rgba(0,0,0,0.4);
        --shadow-heavy: 0 20px 40px rgba(0,0,0,0.6);
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero h1 { font-size: 2.5rem; }
    .hero p { font-size: 1.1rem; }
    .api-status { 
        position: relative; 
        top: auto; 
        right: auto; 
        margin: 1rem 0; 
        width: 100%;
    }
    .theme-toggle {
        position: relative;
        top: auto;
        left: auto;
        margin: 1rem 0;
    }
    .insight-box { padding: 1.5rem; }
    .metric { padding: 1.5rem 1rem; }
}
</style>

<script>
// Enhanced Theme Management
function initializeTheme() {
    // Check for saved theme preference or default to system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    
    document.body.setAttribute('data-theme', theme);
    updateThemeToggle(theme);
}

function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeToggle(newTheme);
}

function updateThemeToggle(theme) {
    const toggles = document.querySelectorAll('.theme-toggle');
    toggles.forEach(toggle => {
        toggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
        toggle.title = `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`;
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            const theme = e.matches ? 'dark' : 'light';
            document.body.setAttribute('data-theme', theme);
            updateThemeToggle(theme);
        }
    });
    
    // Update toggle icon after a short delay to ensure elements are loaded
    setTimeout(() => {
        const currentTheme = document.body.getAttribute('data-theme') || 'light';
        updateThemeToggle(currentTheme);
    }, 100);
});
</script>
</style>
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
    
    # Clean API Status with Theme Toggle
    st.markdown(f"""
    <div class="api-status">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <h4 style="margin: 0;">🔗 API Status</h4>
            <div class="theme-toggle" onclick="toggleTheme()" title="Toggle theme" style="position: relative; width: 30px; height: 30px; font-size: 14px;">
                🌙
            </div>
        </div>
        <div class="status-item">
            <span>Qloo</span>
            <span style="display: flex; align-items: center; gap: 0.5rem;">
                <div class="status-dot {'status-connected' if 'qloo' in apis else 'status-disconnected'}"></div>
                {'Connected' if 'qloo' in apis else 'Offline'}
            </span>
        </div>
        <div class="status-item">
            <span>Perplexity</span>
            <span style="display: flex; align-items: center; gap: 0.5rem;">
                <div class="status-dot {'status-connected' if 'perplexity' in apis else 'status-disconnected'}"></div>
                {'Connected' if 'perplexity' in apis else 'Offline'}
            </span>
        </div>
        <div class="status-item">
            <span>OpenAI</span>
            <span style="display: flex; align-items: center; gap: 0.5rem;">
                <div class="status-dot {'status-connected' if 'openai' in apis else 'status-disconnected'}"></div>
                {'Connected' if 'openai' in apis else 'Offline'}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>🚀 Influencer Research Studio</h1>
        <p>Powered by Qloo • Now you never run out of content</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show different layouts based on onboarding status
    if not st.session_state.onboarding_complete:
        # Chat Interface - Two Columns
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="insight-box">
                <h4>💬 AI Strategy Consultant</h4>
            </div>
            """, unsafe_allow_html=True)
            
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
            # Enhanced getting started section using Streamlit components
            st.markdown("""
            <div class="insight-box">
                <h4>📊 Your Insights Dashboard</h4>
                <p style="color: var(--text-secondary); margin-bottom: 2rem; text-align: center; font-style: italic;">Chat with the AI to unlock personalized insights!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Feature preview cards using Streamlit columns
            col1_preview, col2_preview = st.columns(2)
            
            with col1_preview:
                with st.container():
                    st.markdown("""
                    <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: var(--radius-lg); text-align: center; border: 1px solid var(--border-color); margin-bottom: 1rem;">
                        <div style="font-size: 2.5rem; margin-bottom: 1rem;">🌍</div>
                        <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem; font-size: 1.1rem;">Global Analysis</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Worldwide market insights</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.container():
                    st.markdown("""
                    <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: var(--radius-lg); text-align: center; border: 1px solid var(--border-color);">
                        <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
                        <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem; font-size: 1.1rem;">Growth Strategy</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Smart recommendations</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2_preview:
                with st.container():
                    st.markdown("""
                    <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: var(--radius-lg); text-align: center; border: 1px solid var(--border-color); margin-bottom: 1rem;">
                        <div style="font-size: 2.5rem; margin-bottom: 1rem;">🚀</div>
                        <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem; font-size: 1.1rem;">Viral Prediction</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">AI content scoring</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.container():
                    st.markdown("""
                    <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: var(--radius-lg); text-align: center; border: 1px solid var(--border-color);">
                        <div style="font-size: 2.5rem; margin-bottom: 1rem;">📈</div>
                        <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem; font-size: 1.1rem;">Trending Topics</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Real-time trends</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Call to action section
            st.markdown("""
            <div style="text-align: center; margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); border-radius: var(--radius-lg); border: 1px solid var(--border-color);">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">✨</div>
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Ready to get started?</div>
                <div style="color: var(--text-secondary); font-size: 0.9rem;">Answer the AI's questions to unlock these powerful insights</div>
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
            st.markdown("""
            <div class="insight-box">
                <h4>🌍 Global Content Engagement Map</h4>
            """, unsafe_allow_html=True)
            
            if st.session_state.world_data and 'country_data' in st.session_state.world_data:
                fig = create_world_map(st.session_state.world_data['country_data'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <p>Loading global engagement data...</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Content Ideas Generator - NEW SECTION
            st.markdown("""
            <div class="insight-box">
                <h4>💡 Content Ideas Generator</h4>
            """, unsafe_allow_html=True)
            
            if st.button("✨ Generate Content Ideas", key="content_ideas_btn"):
                if 'openai' in apis:
                    with st.spinner("🎯 Generating content ideas..."):
                        try:
                            # Get user profile from messages
                            user_niche = "general content"
                            user_audience = "general audience"
                            user_platform = "social media"
                            
                            if st.session_state.messages:
                                user_niche = st.session_state.messages[0].replace("You: ", "") if len(st.session_state.messages) > 0 else "general content"
                                user_audience = st.session_state.messages[2].replace("You: ", "") if len(st.session_state.messages) > 2 else "general audience"
                                user_platform = st.session_state.messages[4].replace("You: ", "") if len(st.session_state.messages) > 4 else "social media"
                            
                            # Generate content ideas using OpenAI
                            profile_data = {
                                'niche': user_niche,
                                'audience': user_audience,
                                'platform': user_platform
                            }
                            
                            content_ideas = apis['openai'].generate_content_ideas(profile_data)
                            
                            # Display the ideas in a nice format
                            st.markdown("**🎯 Trending Content Ideas for Your Niche:**")
                            
                            if isinstance(content_ideas, list):
                                for i, idea in enumerate(content_ideas[:5], 1):
                                    st.markdown(f"""
                                    <div style="background: var(--bg-secondary); padding: 1rem; border-radius: var(--radius); margin: 0.75rem 0; border-left: 3px solid var(--primary-color); transition: all 0.3s ease;" onmouseover="this.style.transform='translateX(5px)'" onmouseout="this.style.transform='translateX(0)'">
                                        <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">💡 Idea #{i}</div>
                                        <div style="color: var(--text-secondary); font-size: 0.95rem;">{idea}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.markdown(content_ideas)
                                
                        except Exception as e:
                            # Fallback content ideas based on user niche
                            user_niche = st.session_state.messages[0].replace("You: ", "").lower() if st.session_state.messages else "general"
                            
                            # Generate niche-specific ideas
                            if "fitness" in user_niche or "health" in user_niche:
                                ideas = [
                                    "5 Morning Exercises You Can Do in 10 Minutes",
                                    "Healthy Meal Prep Ideas for Busy Professionals", 
                                    "Common Workout Mistakes and How to Fix Them",
                                    "30-Day Fitness Challenge for Beginners",
                                    "Quick Stretches to Do at Your Desk"
                                ]
                            elif "tech" in user_niche or "programming" in user_niche:
                                ideas = [
                                    "5 Programming Languages to Learn in 2025",
                                    "AI Tools That Will Boost Your Productivity",
                                    "Beginner's Guide to Web Development",
                                    "Tech Career Tips for New Graduates",
                                    "Coding Challenges to Improve Your Skills"
                                ]
                            elif "business" in user_niche or "entrepreneur" in user_niche:
                                ideas = [
                                    "5 Side Business Ideas You Can Start Today",
                                    "Essential Tools for Remote Team Management",
                                    "How to Create a Winning Business Plan",
                                    "Social Media Marketing on a Budget",
                                    "Productivity Hacks for Entrepreneurs"
                                ]
                            elif "lifestyle" in user_niche or "fashion" in user_niche:
                                ideas = [
                                    "5 Wardrobe Essentials for Every Season",
                                    "Home Decor Ideas on a Budget",
                                    "Self-Care Routine for Busy People",
                                    "Sustainable Living Tips for Beginners",
                                    "Travel Hacks for Budget-Conscious Explorers"
                                ]
                            elif "food" in user_niche or "cooking" in user_niche:
                                ideas = [
                                    "5 Quick Dinner Recipes Under 30 Minutes",
                                    "Healthy Snacks for Weight Loss",
                                    "Beginner's Guide to Meal Planning",
                                    "International Dishes You Can Make at Home",
                                    "Kitchen Gadgets That Actually Save Time"
                                ]
                            else:
                                ideas = [
                                    "5 Trending Topics in Your Industry",
                                    "Behind-the-Scenes of Your Daily Routine",
                                    "Common Myths in Your Field (Debunked)",
                                    "Quick Tips for Beginners in Your Niche",
                                    "Tools and Resources You Actually Use"
                                ]
                            
                            st.markdown("**🎯 Trending Content Ideas for Your Niche:**")
                            for i, idea in enumerate(ideas, 1):
                                st.markdown(f"""
                                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: var(--radius); margin: 0.75rem 0; border-left: 3px solid var(--primary-color); transition: all 0.3s ease;" onmouseover="this.style.transform='translateX(5px)'" onmouseout="this.style.transform='translateX(0)'">
                                    <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">💡 Idea #{i}</div>
                                    <div style="color: var(--text-secondary); font-size: 0.95rem;">{idea}</div>
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    # Show sample ideas when no API is available
                    st.markdown("**💡 Sample Content Ideas:**")
                    
                    sample_ideas = [
                        "5 Morning Habits That Changed My Life",
                        "Behind the Scenes: My Content Creation Process",
                        "Common Mistakes in [Your Niche] and How to Avoid Them",
                        "Quick Tips for Beginners in [Your Field]",
                        "Tools I Actually Use Daily (Honest Review)"
                    ]
                    
                    for i, idea in enumerate(sample_ideas, 1):
                        st.markdown(f"""
                        <div style="background: var(--bg-secondary); padding: 1rem; border-radius: var(--radius); margin: 0.75rem 0; border-left: 3px solid var(--primary-color); transition: all 0.3s ease;" onmouseover="this.style.transform='translateX(5px)'" onmouseout="this.style.transform='translateX(0)'">
                            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">💡 Idea #{i}</div>
                            <div style="color: var(--text-secondary); font-size: 0.95rem;">{idea}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.info("💡 Connect OpenAI API for personalized content ideas based on your specific niche!")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Trending Topics
            st.markdown("""
            <div class="insight-box">
                <h4>🔥 Viral Trends by Region</h4>
            """, unsafe_allow_html=True)
            
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
                st.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <p>Loading trending topics...</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Competition Analysis
            st.markdown("""
            <div class="insight-box">
                <h4>🏆 Competition Analysis</h4>
            """, unsafe_allow_html=True)
            
            if st.session_state.world_data and 'competitors' in st.session_state.world_data and st.session_state.world_data['competitors']:
                st.markdown("**Top Competitors in Your Niche:**")
                for i, competitor in enumerate(st.session_state.world_data['competitors'][:3], 1):
                    st.markdown(f"**{i}.** {competitor}")
            else:
                st.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <p>Loading competition data...</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            # Viral Content Predictor
            st.markdown("""
            <div class="insight-box">
                <h4>🚀 Viral Content Predictor</h4>
            """, unsafe_allow_html=True)
            
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
                            color = "#06d6a0" if score >= 70 else "#f59e0b" if score >= 50 else "#ef4444"
                            
                            st.markdown(f"""
                            <div style="text-align: center; background: var(--bg-primary); padding: 2rem; border-radius: var(--radius-lg); box-shadow: var(--shadow-light); margin: 1rem 0; border: 1px solid var(--border-color);">
                                <h1 style="color: {color}; font-size: 3rem; margin: 1rem 0; font-family: 'Space Grotesk', sans-serif;">{score}/100</h1>
                                <p style="color: var(--text-secondary);">Viral Potential Score</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col_x, col_y = st.columns(2)
                            with col_x:
                                st.markdown("**✅ Strengths:**")
                                for reason in prediction.get('reasons', ['Engaging topic'])[:3]:
                                    st.markdown(f"• {reason}")
                            
                            with col_y:
                                st.markdown("**💡 Improvements:**")
                                for improvement in prediction.get('improvements', ['Add trending hashtags'])[:3]:
                                    st.markdown(f"• {improvement}")
                        except Exception as e:
                            st.error(f"Prediction error: {str(e)}")
                elif not content_idea:
                    st.warning("Please describe your content idea first!")
                else:
                    st.warning("OpenAI API required for predictions")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Growth Strategy
            st.markdown("""
            <div class="insight-box">
                <h4>📈 AI Growth Strategy</h4>
            """, unsafe_allow_html=True)
            
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
            st.markdown("""
            <div class="insight-box">
                <h4>🎵 Trending Audio Discovery</h4>
            """, unsafe_allow_html=True)
            
            # Initialize Music Trends API
            music_api = MusicTrendsAPI()
            
            # Set default platform (no dropdown)
            selected_platform = "tiktok"
            
            # Search functionality
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
            # Brand Collaboration Opportunities - FIXED VERSION
            st.markdown("""
            <div class="insight-box">
                <h4>🤝 Brand Collaboration Finder</h4>
            """, unsafe_allow_html=True)

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
                                    # Enhanced text cleaning function
                                    def clean_brand_text(text):
                                        """Thoroughly clean brand text data"""
                                        if not text or not isinstance(text, str):
                                            return "Not specified"
                                        
                                        import re
                                        import html
                                        
                                        # Remove all HTML tags completely
                                        text = re.sub(r'<[^>]*?>', '', text)
                                        
                                        # Remove markdown formatting
                                        text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
                                        text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
                                        text = re.sub(r'`([^`]+)`', r'\1', text)
                                        
                                        # Remove extra whitespace and newlines
                                        text = re.sub(r'\s+', ' ', text)
                                        text = text.strip()
                                        
                                        # Decode HTML entities
                                        text = html.unescape(text)
                                        
                                        # Limit length to prevent overflow
                                        if len(text) > 150:
                                            text = text[:147] + "..."
                                        
                                        return text if text else "Not specified"
                                    
                                    # Clean all brand data
                                    brand_name = clean_brand_text(brand.get('name', 'Unknown Brand'))
                                    fit_reason = clean_brand_text(brand.get('fit_reason', 'Great alignment with your content niche'))
                                    value_range = clean_brand_text(brand.get('value_range', 'Varies'))
                                    approach = clean_brand_text(brand.get('approach', 'Direct outreach'))
                                    
                                    # Handle collaboration types safely
                                    collab_types = brand.get('collaboration_types', ['Sponsored Content'])
                                    if isinstance(collab_types, str):
                                        collab_types = [collab_types]
                                    elif not isinstance(collab_types, list):
                                        collab_types = ['Sponsored Content']
                                    
                                    # Clean and limit collaboration types
                                    clean_types = []
                                    for ct in collab_types[:3]:  # Limit to 3 types
                                        cleaned = clean_brand_text(str(ct))
                                        if cleaned and cleaned != "Not specified":
                                            clean_types.append(cleaned)
                                    
                                    if not clean_types:
                                        clean_types = ['Sponsored Content']
                                    
                                    # Create brand card using Streamlit components instead of raw HTML
                                    with st.container():
                                        # Brand header
                                        col_brand, col_badge = st.columns([3, 1])
                                        with col_brand:
                                            st.markdown(f"**🏢 {brand_name}**")
                                        with col_badge:
                                            st.markdown('<span style="background: var(--accent-color); color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.75rem;">Partnership Ready</span>', unsafe_allow_html=True)
                                        
                                        # Fit reason
                                        st.markdown(f"*{fit_reason}*")
                                        
                                        # Collaboration types
                                        types_html = " ".join([f'<span style="background: var(--bg-secondary); color: var(--text-secondary); padding: 0.4rem 0.8rem; border-radius: var(--radius); font-size: 0.8rem; margin-right: 0.5rem; display: inline-block;">{ct}</span>' for ct in clean_types])
                                        st.markdown(types_html, unsafe_allow_html=True)
                                        
                                        # Value and approach
                                        col_value, col_approach = st.columns(2)
                                        with col_value:
                                            st.markdown(f"**💰 {value_range}**")
                                        with col_approach:
                                            st.markdown(f"📧 {approach}")
                                        
                                        st.markdown("---")  # Separator
                            
                            else:
                                st.info("No brand collaborations found for the current criteria.")
                                
                        except Exception as e:
                            st.error(f"Error finding brand collaborations: {str(e)}")
                            
                            # Show sample brands as fallback
                            st.markdown("**🤝 Sample Brand Collaboration Opportunities:**")
                            
                            sample_brands = [
                                {"name": "Fashion Forward Co.", "value_range": "$500-$2,000", "fit": "Trendy fashion brand seeking content creators", "types": ["Sponsored Posts", "Product Reviews"]},
                                {"name": "TechGear Pro", "value_range": "$1,000-$5,000", "fit": "Technology brand looking for product reviewers", "types": ["Unboxing Videos", "Tech Reviews"]},
                                {"name": "Lifestyle Essentials", "value_range": "$200-$1,500", "fit": "Lifestyle brand targeting young demographics", "types": ["Product Placement", "Story Features"]}
                            ]
                            
                            for brand in sample_brands:
                                with st.container():
                                    # Brand header
                                    col_brand, col_badge = st.columns([3, 1])
                                    with col_brand:
                                        st.markdown(f"**🏢 {brand['name']}**")
                                    with col_badge:
                                        st.markdown('<span style="background: var(--accent-color); color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.75rem;">Available</span>', unsafe_allow_html=True)
                                    
                                    # Fit reason
                                    st.markdown(f"*{brand['fit']}*")
                                    
                                    # Types
                                    types_html = " ".join([f'<span style="background: var(--bg-secondary); color: var(--text-secondary); padding: 0.4rem 0.8rem; border-radius: var(--radius); font-size: 0.8rem; margin-right: 0.5rem; display: inline-block;">{ct}</span>' for ct in brand['types']])
                                    st.markdown(types_html, unsafe_allow_html=True)
                                    
                                    # Value
                                    st.markdown(f"**💰 {brand['value_range']}**")
                                    
                                    st.markdown("---")
                else:
                    st.warning("Perplexity API required for brand collaboration discovery")
                    
                    # Show enhanced guidance without API
                    st.markdown("**💡 Brand Collaboration Strategy Guide:**")
                    
                    # Create tabs for different aspects
                    tab1, tab2, tab3 = st.tabs(["🎯 Finding Brands", "📧 Outreach", "💰 Pricing"])
                    
                    with tab1:
                        st.markdown("""
                        **Research Your Niche:**
                        - Look for brands that align with your content style
                        - Check competitor partnerships for inspiration
                        - Use tools like Social Blade to find brand partnerships
                        - Follow brand hashtags to see their current campaigns
                        """)
                    
                    with tab2:
                        st.markdown("""
                        **Effective Outreach:**
                        - Create a professional media kit with your stats
                        - Personalize every email - mention specific products
                        - Include your best content examples
                        - Be clear about your rates and deliverables
                        """)
                    
                    with tab3:
                        st.markdown("""
                        **Pricing Guidelines:**
                        - **Micro (1K-10K):** $10-100 per 1K followers
                        - **Mid-tier (10K-100K):** $100-500 per post
                        - **Macro (100K+):** $1000+ per campaign
                        - Factor in engagement rate and content quality
                        """)

            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()