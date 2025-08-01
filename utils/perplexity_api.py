import requests
import json
from typing import List, Optional
from pydantic import BaseModel

# Pydantic models for structured responses
class TrendingSound(BaseModel):
    title: str
    artist: str
    duration: int
    genre: str
    mood: str
    viral_potential: str
    usage_count: int
    trend_score: int
    hashtags: List[str]
    best_content_types: List[str]
    peak_usage_time: str

class TrendingSounds(BaseModel):
    sounds: List[TrendingSound]

class BrandOpportunity(BaseModel):
    name: str
    fit_reason: str
    collaboration_types: List[str]
    value_range: str
    approach: str

class BrandOpportunities(BaseModel):
    brands: List[BrandOpportunity]

class Competitor(BaseModel):
    name: str
    platform: str
    followers: str
    content_style: str
    success_factor: str

class CompetitorAnalysis(BaseModel):
    competitors: List[Competitor]

class GlobalTrend(BaseModel):
    trend: str
    description: str
    regions: List[str]
    engagement_score: int

class TrendsAnalysis(BaseModel):
    trends: List[GlobalTrend]

class CountryEngagement(BaseModel):
    country_code: str
    country_name: str
    engagement_score: float
    market_size: str
    key_insights: str

class GlobalEngagement(BaseModel):
    countries: List[CountryEngagement]

class PerplexityAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def ask_question(self, question, model="sonar-medium-online", max_tokens=1024):
        """
        Ask a question using the Perplexity API (Sonar Pro) - Legacy method
        
        Args:
            question (str): The question to ask
            model (str): The model to use (default: sonar-medium-online)
            max_tokens (int): Maximum tokens in the response
            
        Returns:
            dict: The API response with the answer
        """
        try:
            endpoint = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are an expert research assistant helping influencers discover trending content ideas based on geography and audience demographics."},
                    {"role": "user", "content": question}
                ],
                "max_tokens": max_tokens
            }
            
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error querying Perplexity API: {e}")
            return None
    
    def ask_structured_question(self, question, response_model, model="sonar-pro", max_tokens=2048):
        """
        Ask a question using Perplexity API with structured JSON response
        
        Args:
            question (str): The question to ask
            response_model: Pydantic model for structured response
            model (str): The model to use
            max_tokens (int): Maximum tokens in the response
            
        Returns:
            Pydantic model instance or None
        """
        try:
            endpoint = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are an expert research assistant. Always respond with valid JSON that matches the requested schema exactly."
                    },
                    {"role": "user", "content": question}
                ],
                "max_tokens": max_tokens,
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "schema": response_model.model_json_schema()
                    }
                }
            }
            
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            structured_data = response_model.model_validate_json(data["choices"][0]["message"]["content"])
            return structured_data
            
        except Exception as e:
            print(f"Error querying Perplexity API with structured response: {e}")
            return None
    
    def generate_content_ideas(self, country, trending_topics, content_category, audience_type):
        """
        Generate content ideas based on trending topics for a specific country
        
        Args:
            country (str): Country name
            trending_topics (list): List of trending topics
            content_category (str): Category of content
            audience_type (str): Type of audience
            
        Returns:
            str: Generated content ideas
        """
        topics_str = ", ".join(trending_topics[:5]) if trending_topics else "No specific topics available"
        
        prompt = f"""
        Generate 5 specific and detailed content ideas for an influencer in the {content_category} niche 
        targeting {audience_type} in {country}. 
        
        These are the current trending topics in this region: {topics_str}
        
        For each idea, provide:
        1. A catchy title
        2. Brief description of the content (2-3 sentences)
        3. Why this would resonate with the audience
        4. Potential hashtags
        
        Format your response as a structured list with clear headings for each idea.
        """
        
        response = self.ask_question(prompt)
        if response and 'choices' in response:
            return response['choices'][0]['message']['content']
        return "Sorry, I couldn't generate content ideas at this time."
    
    def generate_follow_up_questions(self, content_category=None, audience_type=None):
        """
        Generate follow-up questions to ask the user based on their initial responses
        
        Args:
            content_category (str, optional): Category of content if known
            audience_type (str, optional): Type of audience if known
            
        Returns:
            list: List of follow-up questions
        """
        if content_category and audience_type:
            prompt = f"""
            Generate 3 specific follow-up questions to help an influencer in the {content_category} niche 
            targeting {audience_type} refine their content strategy. 
            
            Questions should help the influencer understand their audience better or explore specific 
            sub-niches within their category. Return ONLY the questions in a list format, nothing else.
            """
        elif content_category:
            prompt = f"""
            Generate 3 specific questions to ask an influencer in the {content_category} niche to understand 
            their target audience better. 
            
            Questions should help determine audience demographics, interests, and preferences.
            Return ONLY the questions in a list format, nothing else.
            """
        elif audience_type:
            prompt = f"""
            Generate 3 specific questions to ask an influencer who targets {audience_type} to determine 
            what content categories would work best for them.
            
            Questions should help explore potential content niches and formats.
            Return ONLY the questions in a list format, nothing else.
            """
        else:
            prompt = """
            Generate 3 general questions to ask an influencer who is looking for content ideas.
            
            Questions should help determine their content niche, target audience, and content format preferences.
            Return ONLY the questions in a list format, nothing else.
            """
        
        response = self.ask_question(prompt)
        if response and 'choices' in response:
            content = response['choices'][0]['message']['content']
            # Extract questions from the response
            questions = [q.strip() for q in content.split("\n") if q.strip()]
            return questions[:3]  # Ensure we return at most 3 questions
        
        # Default questions if API fails
        return [
            "What content category are you primarily focusing on?",
            "Who is your target audience?",
            "What formats of content perform best with your audience?"
        ]
