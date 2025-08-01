# 🚀 AI-Powered Influencer Research Tool

A comprehensive research dashboard for influencers that combines **Qloo**, **Perplexity**, and **OpenAI** APIs to provide data-driven insights for content creation, audience growth, and market analysis.

## ✨ Features

### 🌍 Global Market Intelligence
- **Interactive World Map**: Visualize market relevance across different countries
- **Geographic Insights**: Understand which markets are most receptive to your content
- **Regional Trending Topics**: Discover what's trending in specific countries
- **Market Penetration Analysis**: Identify untapped geographic opportunities

### 📊 Audience Growth Strategy
- **AI-Powered Growth Analysis**: Get personalized recommendations based on your profile
- **Demographic Targeting**: Understand your audience composition and preferences
- **Expansion Opportunities**: Discover new audience segments to target
- **90-Day Action Plans**: Receive specific tactics for immediate implementation

### 🏁 Competitive Landscape Analysis
- **Market Positioning**: Understand how you fit in your niche
- **Content Gap Analysis**: Identify opportunities your competitors are missing
- **Differentiation Strategies**: Get recommendations on how to stand out
- **Monetization Insights**: Learn from successful competitor approaches

### 🚀 Viral Content Prediction
- **AI Scoring System**: Get a viral potential score (1-100) for your content ideas
- **Optimization Suggestions**: Receive specific improvements to increase viral potential
- **Hashtag Strategy**: Get optimized hashtag recommendations
- **Timing Analysis**: Learn when to post for maximum engagement

### 📅 AI Content Calendar
- **Personalized Scheduling**: Generate content calendars based on your audience and trends
- **Topic Suggestions**: Get daily/weekly content ideas aligned with trending topics
- **Multi-Platform Strategy**: Tailored recommendations for different content formats
- **Seasonal Adjustments**: Content adapted for holidays and events

### ⏰ Optimal Posting Schedule
- **Audience Behavior Analysis**: Understand when your audience is most active
- **Platform-Specific Timing**: Different schedules for posts, stories, reels, etc.
- **Geographic Considerations**: Timing recommendations based on audience location
- **Engagement Optimization**: Maximize reach and interaction rates

## 🔧 Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- API keys for Qloo, Perplexity, and OpenAI

### 2. Installation

```bash
# Clone or download the project
cd qloo_hack

# Install required packages
pip install -r requirements.txt
```

### 3. API Key Configuration

Edit the `secrets.toml` file with your actual API keys:

```toml
[default]
QLOO_API_KEY = "your_actual_qloo_api_key_here"
PERPLEXITY_API_KEY = "your_actual_perplexity_api_key_here" 
OPENAI_API_KEY = "your_actual_openai_api_key_here"

[secrets]
qloo = "your_actual_qloo_api_key_here"
perplexity = "your_actual_perplexity_api_key_here"
openai = "your_actual_openai_api_key_here"
```

### 4. Running the Application

```bash
# Run the main application
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🎯 How to Use

### Step 1: Onboarding
- Complete the AI-generated questionnaire about your content niche, target audience, and goals
- The system uses OpenAI to generate personalized questions based on your responses
- Your profile information is used to customize all subsequent analyses

### Step 2: Explore Features
Navigate through the different sections using the sidebar:

- **🏠 Dashboard**: Overview of your profile and quick actions
- **🌍 Global Market Map**: Interactive world map with market insights
- **📊 Audience Growth**: Personalized growth strategies and recommendations
- **🏁 Competitor Analysis**: Market positioning and competitive landscape
- **🚀 Viral Predictor**: Analyze content ideas for viral potential
- **📅 Content Calendar**: Generate AI-powered content schedules
- **⏰ Posting Schedule**: Optimize posting times for maximum engagement

### Step 3: Generate Insights
- Each section provides different AI-powered analyses
- Results are cached for performance and can be regenerated as needed
- All insights are personalized based on your onboarding responses

## 🔑 API Information

### Qloo API
- **Purpose**: Provides audience insights, geographic data, and trending topics
- **Endpoints Used**: 
  - `/v2/insights/` - Core recommendation engine
  - `/insights/geography` - Geographic market analysis
  - `/trends/region` - Regional trending topics
- **Data**: Entity relationships, audience demographics, cultural preferences

### Perplexity API
- **Purpose**: Real-time content research and trend analysis
- **Model Used**: `sonar-medium-online` for current information
- **Applications**: Content idea generation, market research, trend analysis

### OpenAI API
- **Purpose**: Advanced AI analysis and content generation
- **Models Used**: 
  - `gpt-3.5-turbo` - Fast analysis and structured responses
  - `gpt-4` - Complex strategic analysis and recommendations
- **Applications**: Growth strategy, competitor analysis, viral prediction

## 📁 Project Structure

```
qloo_hack/
├── app.py                       # Main Streamlit application
├── secrets.toml                 # API keys configuration (not in repo)
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup file
├── utils/
│   ├── qloo_api.py             # Qloo API wrapper
│   ├── perplexity_api.py       # Perplexity API wrapper
│   ├── openai_api.py           # OpenAI API wrapper
│   └── music_trends_api.py     # Music trends API wrapper
├── test.ipynb                  # Jupyter notebook for testing
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🚀 Key Features Breakdown

### AI-Powered Onboarding
- Dynamic question generation using OpenAI
- Personalized questionnaire based on user responses
- Profile building for customized insights

### Global Market Intelligence
- Real-time geographic analysis using Qloo's cultural AI
- Interactive visualizations with Plotly
- Country-specific trending topics and content opportunities

### Multi-API Integration
- **Qloo**: Cultural insights and audience intelligence
- **Perplexity**: Real-time content research and trends
- **OpenAI**: Strategic analysis and content optimization

### Advanced Analytics
- Viral potential scoring algorithm
- Competitive landscape analysis
- Optimal timing recommendations
- Content calendar generation

## 💡 Tips for Best Results

1. **Complete Onboarding Thoroughly**: Detailed responses lead to better personalized insights
2. **Explore Multiple Countries**: Different markets may offer unique opportunities
3. **Test Content Ideas**: Use the viral predictor to optimize before posting
4. **Follow Posting Schedules**: Timing can significantly impact engagement
5. **Update Profile Regularly**: Refresh your profile as your content evolves

## 🛠️ Troubleshooting

### API Connection Issues
- Verify API keys are correctly entered in `secrets.toml`
- Check that all APIs have sufficient credits/quota
- Ensure internet connection is stable

### Performance Issues
- Large market analyses may take time to process
- Use browser refresh if the interface becomes unresponsive
- Clear browser cache if visualizations don't load properly

### Feature-Specific Issues
- **World Map**: Requires Qloo API for geographic data
- **Growth Analysis**: Requires OpenAI API for strategic recommendations  
- **Content Ideas**: Requires Perplexity API for real-time research
- **Viral Prediction**: Requires OpenAI API for scoring algorithm

## 📈 Advanced Usage

### Custom Analysis
- Modify API parameters in the utility classes for specific use cases
- Adjust scoring algorithms for different content types
- Customize geographic regions for analysis

### Data Export
- Copy generated content calendars and strategies
- Save viral predictions for content planning
- Export growth strategies for team collaboration

## 🎨 Customization

The application UI can be customized by modifying the CSS styles in the main app file. Key styling classes:
- `.main-header`: Main page headers
- `.section-header`: Section titles
- `.insight-card`: Analysis result containers
- `.metric-card`: Statistics display cards
- `.trend-tag`: Trending topic tags

## 📞 Support

For issues related to:
- **Qloo API**: Check Qloo hackathon documentation
- **Perplexity API**: Refer to Perplexity API docs
- **OpenAI API**: Consult OpenAI API documentation
- **Application Bugs**: Check console logs and error messages

## 🔮 Future Enhancements

Potential additions to the tool:
- Social media platform integrations
- Historical trend analysis
- Collaboration features for teams
- Advanced visualization options
- Export capabilities for reports
- Automated content scheduling

---

**Built with ❤️ for the Qloo Hackathon**

*This tool demonstrates the power of combining multiple AI APIs to create comprehensive, data-driven insights for content creators and influencers.*
