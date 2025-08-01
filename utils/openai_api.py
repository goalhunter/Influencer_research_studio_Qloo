import openai
import json
from typing import List, Dict, Optional

class OpenAIAPI:
    def __init__(self, api_key: str):
        """
        Initialize OpenAI API client
        
        Args:
            api_key (str): OpenAI API key
        """
        self.api_key = api_key
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_influencer_questions(self, context: Dict = None) -> List[str]:
        """
        Generate personalized questions for influencers based on their context
        
        Args:
            context (dict, optional): Context about the influencer
            
        Returns:
            List[str]: List of questions to ask
        """
        try:
            prompt = """
            You are an expert influencer marketing consultant. Generate 5 strategic questions to ask an influencer 
            to understand their goals, audience, and content strategy needs.
            
            The questions should help determine:
            1. Their content niche/category
            2. Target audience demographics
            3. Current performance metrics they track
            4. Geographic markets they want to focus on
            5. Content formats they prefer
            
            Return ONLY a JSON array of question strings, nothing else.
            Example: ["What content category do you focus on?", "Who is your primary target audience?"]
            """
            
            if context:
                prompt += f"\n\nContext about the influencer: {json.dumps(context)}"
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert influencer marketing consultant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            # Parse JSON response
            questions = json.loads(content)
            return questions if isinstance(questions, list) else []
        except Exception as e:
            print(f"Error generating questions: {e}")
            # Return default questions if API fails
            return [
                "What content category or niche do you primarily focus on?",
                "Who is your target audience (age, interests, demographics)?",
                "Which geographic markets are you most interested in?",
                "What content formats perform best for you?",
                "What are your main goals for audience growth?"
            ]
    
    def analyze_audience_growth_strategy(self, profile_data: Dict) -> str:
        """
        Analyze influencer profile and suggest audience growth strategies
        
        Args:
            profile_data (dict): Influencer profile information
            
        Returns:
            str: Detailed audience growth analysis and recommendations
        """
        try:
            prompt = f"""
            As an expert social media growth strategist, analyze this influencer profile and provide detailed 
            recommendations for audience growth:
            
            Profile Data:
            {json.dumps(profile_data, indent=2)}
            
            Provide a comprehensive analysis including:
            1. Current strengths and opportunities
            2. Target audience expansion strategies
            3. Content optimization recommendations
            4. Geographic expansion opportunities
            5. Collaboration and partnership suggestions
            6. Specific tactics for the next 90 days
            
            Format your response with clear headings and actionable bullet points.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert social media growth strategist with deep knowledge of audience development."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing audience growth: {e}")
            return "Sorry, I couldn't generate the audience growth analysis at this time."
    
    def generate_content_calendar(self, trends: List[str], audience_data: Dict, timeframe: str = "monthly") -> str:
        """
        Generate a content calendar based on trending topics and audience data
        
        Args:
            trends (list): List of trending topics
            audience_data (dict): Target audience information
            timeframe (str): Calendar timeframe (daily, weekly, monthly)
            
        Returns:
            str: Formatted content calendar with post ideas
        """
        try:
            trends_text = ", ".join(trends[:10])
            
            prompt = f"""
            Create a {timeframe} content calendar for an influencer with this audience data:
            {json.dumps(audience_data, indent=2)}
            
            Incorporate these trending topics: {trends_text}
            
            For each content piece, include:
            - Content type (post, story, reel, etc.)
            - Topic/theme
            - Key message
            - Best posting time
            - Relevant hashtags
            - Engagement strategy
            
            Format as a clear, actionable calendar that the influencer can implement immediately.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert content strategist specializing in social media calendar planning."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.8
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating content calendar: {e}")
            return "Sorry, I couldn't generate the content calendar at this time."
    
    def analyze_competitor_landscape(self, niche: str, region: str = "global") -> str:
        """
        Analyze the competitive landscape for a given niche and region
        
        Args:
            niche (str): Content niche/category
            region (str): Geographic region for analysis
            
        Returns:
            str: Competitor analysis with insights and opportunities
        """
        try:
            prompt = f"""
            Conduct a competitive landscape analysis for the {niche} niche in the {region} market.
            
            Include:
            1. Key player categories and archetypes
            2. Content gaps and opportunities
            3. Emerging trends in this space
            4. Differentiation strategies
            5. Audience behavior patterns
            6. Monetization approaches being used
            7. Recommended positioning strategies
            
            Focus on actionable insights an influencer can use to stand out in this market.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert market research analyst specializing in influencer marketing and competitive analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing competitor landscape: {e}")
            return "Sorry, I couldn't generate the competitive analysis at this time."
    
    def predict_viral_potential(self, content_idea: str, audience_data: Dict, trends: List[str]) -> Dict:
        """
        Predict the viral potential of a content idea
        
        Args:
            content_idea (str): The content idea to analyze
            audience_data (dict): Target audience information
            trends (list): Current trending topics
            
        Returns:
            dict: Viral potential score and analysis
        """
        try:
            prompt = f"""
            Analyze this content idea for viral potential:
            Content Idea: "{content_idea}"
            
            Target Audience: {json.dumps(audience_data)}
            Current Trends: {", ".join(trends[:10])}
            
            Provide analysis in JSON format with these fields:
            {{
                "viral_score": (number 1-100),
                "reasons": [list of reasons for the score],
                "improvements": [list of suggested improvements],
                "timing": "best time to post this content",
                "hashtag_strategy": [recommended hashtags],
                "engagement_prediction": "predicted engagement level"
            }}
            
            Return ONLY the JSON object, no other text.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert viral content analyst with deep understanding of social media algorithms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.6
            )
            
            content = response.choices[0].message.content.strip()
            return json.loads(content)
        except Exception as e:
            print(f"Error predicting viral potential: {e}")
            return {
                "viral_score": 50,
                "reasons": ["Analysis unavailable"],
                "improvements": ["Try again later"],
                "timing": "Peak engagement hours",
                "hashtag_strategy": ["#trending", "#content"],
                "engagement_prediction": "Moderate"
            }
    
    def generate_hashtag_strategy(self, content_topic: str, target_audience: str, region: str = "global") -> List[str]:
        """
        Generate an optimized hashtag strategy for content
        
        Args:
            content_topic (str): The content topic
            target_audience (str): Description of target audience
            region (str): Geographic region
            
        Returns:
            List[str]: List of recommended hashtags
        """
        try:
            prompt = f"""
            Generate an optimized hashtag strategy for:
            Topic: {content_topic}
            Audience: {target_audience}
            Region: {region}
            
            Include a mix of:
            - High-volume popular hashtags
            - Medium-volume niche hashtags
            - Low-competition branded hashtags
            - Location-based hashtags (if relevant)
            
            Return ONLY a JSON array of hashtag strings (without #), nothing else.
            Example: ["contentcreator", "trending", "lifestyle"]
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert hashtag strategist with deep knowledge of social media algorithms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            hashtags = json.loads(content)
            return hashtags if isinstance(hashtags, list) else []
        except Exception as e:
            print(f"Error generating hashtags: {e}")
            return ["content", "creator", "trending", "social", "engagement"]
    
    def analyze_optimal_posting_times(self, audience_demographics: Dict, content_type: str) -> Dict:
        """
        Analyze optimal posting times based on audience demographics
        
        Args:
            audience_demographics (dict): Audience demographic data
            content_type (str): Type of content (post, story, reel, etc.)
            
        Returns:
            dict: Optimal posting schedule recommendations
        """
        try:
            prompt = f"""
            Analyze optimal posting times for this audience and content type:
            
            Audience Demographics: {json.dumps(audience_demographics)}
            Content Type: {content_type}
            
            Consider factors like:
            - Time zones and geographic distribution
            - Age group behavior patterns
            - Content type engagement patterns
            - Day of week preferences
            
            Return analysis in JSON format:
            {{
                "best_days": [list of best days],
                "optimal_hours": [list of optimal hours in 24h format],
                "timezone_considerations": "timezone strategy",
                "content_frequency": "recommended posting frequency",
                "seasonal_adjustments": "seasonal considerations"
            }}
            
            Return ONLY the JSON object.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert social media timing strategist with deep knowledge of audience behavior patterns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.6
            )
            
            content = response.choices[0].message.content.strip()
            return json.loads(content)
        except Exception as e:
            print(f"Error analyzing posting times: {e}")
            return {
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "optimal_hours": ["9:00", "14:00", "19:00"],
                "timezone_considerations": "Focus on primary audience timezone",
                "content_frequency": "1-2 posts per day",
                "seasonal_adjustments": "Adjust for holidays and events"
            }
