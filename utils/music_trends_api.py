import requests
import json
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class MusicTrendsAPI:
    def __init__(self):
        """
        Initialize Music Trends API for discovering trending audio/music using Perplexity Sonar AI
        """
        self.base_urls = {
            'tiktok': 'https://www.tiktok.com',
            'instagram': 'https://www.instagram.com',
            'youtube': 'https://www.youtube.com'
        }
    
    def get_trending_sounds(self, perplexity_api, platform: str = 'tiktok', region: str = 'global', 
                           content_category: str = None, limit: int = 10) -> List[Dict]:
        """
        Get trending sounds for a specific platform and region using Perplexity AI with structured response
        
        Args:
            perplexity_api: PerplexityAPI instance
            platform (str): Platform ('tiktok', 'instagram', 'youtube')
            region (str): Geographic region
            content_category (str): Content category filter
            limit (int): Number of results to return
            
        Returns:
            List[Dict]: List of trending sounds with metadata
        """
        try:
            from utils.perplexity_api import TrendingSounds
            
            # Build query for structured response
            category_filter = f" for {content_category} content" if content_category else ""
            region_filter = f" in {region}" if region != 'global' else " globally"
            
            query = f"""Find the top {limit} trending audio tracks and sounds on {platform.title()}{category_filter}{region_filter} in 2024. 

            For each sound, provide exact details:
            - title: exact track/sound name
            - artist: creator or artist name  
            - duration: approximate duration in seconds (integer)
            - genre: music genre/style
            - mood: one of (Chill, Energetic, Upbeat, Emotional, Funny, Relaxing, Intense)
            - viral_potential: one of (High, Medium, Low, Extremely High)
            - usage_count: estimated number of uses (integer)
            - trend_score: trending score 1-100 (integer)
            - hashtags: array of popular hashtags (with #)
            - best_content_types: array of content categories this works for
            - peak_usage_time: best posting hours (e.g., "18:00-22:00")
            
            Focus on currently viral sounds with accurate, realistic data."""
            
            # Use structured response
            structured_response = perplexity_api.ask_structured_question(query, TrendingSounds, model="sonar-pro")
            
            if structured_response and structured_response.sounds:
                # Convert to dict format for compatibility
                sounds_list = []
                for i, sound in enumerate(structured_response.sounds[:limit]):
                    sounds_list.append({
                        'id': f'{platform[0:2]}_{i+1:03d}',
                        'title': sound.title,
                        'artist': sound.artist,
                        'duration': sound.duration,
                        'genre': sound.genre,
                        'mood': sound.mood,
                        'viral_potential': sound.viral_potential,
                        'usage_count': sound.usage_count,
                        'trend_score': sound.trend_score,
                        'hashtags': sound.hashtags,
                        'best_content_types': sound.best_content_types,
                        'trending_regions': [region] if region != 'global' else ['Global'],
                        'peak_usage_time': sound.peak_usage_time,
                        'audio_preview_url': f'https://example.com/preview/{platform[0:2]}_{i+1:03d}.mp3'
                    })
                return sounds_list
            
            return self._get_fallback_sounds(platform, content_category)[:limit]
            
        except Exception as e:
            print(f"Error fetching trending sounds from Perplexity: {e}")
            return self._get_fallback_sounds(platform, content_category)[:limit]
    
    def get_sound_details(self, perplexity_api, sound_id: str, platform: str = 'tiktok') -> Optional[Dict]:
        """
        Get detailed information about a specific sound using Perplexity AI
        
        Args:
            perplexity_api: PerplexityAPI instance
            sound_id (str): Sound identifier
            platform (str): Platform name
            
        Returns:
            Dict: Detailed sound information
        """
        try:
            # Extract sound name from ID if possible
            sound_name = sound_id.replace(f"{platform[0:2]}_", "").replace("_", " ")
            
            query = f"""Get detailed information about the trending sound or audio track "{sound_name}" on {platform.title()}. 

            Provide:
            - Full title and artist name
            - Genre and mood
            - Current usage statistics and popularity
            - Why it's trending
            - Best content types that use this sound
            - Popular hashtags
            - Peak usage times
            - Duration if known"""
            
            response = perplexity_api.ask_question(query, model="sonar-pro")
            
            if response and 'choices' in response:
                content = response['choices'][0]['message']['content']
                
                # Parse the detailed response
                sound_details = {
                    'id': sound_id,
                    'title': sound_name,
                    'artist': 'Unknown Artist',
                    'duration': 20,
                    'usage_count': 500000,
                    'trend_score': 80,
                    'genre': 'Unknown',
                    'mood': 'Upbeat',
                    'viral_potential': 'High',
                    'hashtags': [],
                    'best_content_types': ['General'],
                    'trending_regions': ['Global'],
                    'peak_usage_time': '18:00-22:00',
                    'detailed_description': content
                }
                
                return sound_details
            
            return None
        except Exception as e:
            print(f"Error fetching sound details: {e}")
            return None
    
    def get_sounds_by_mood(self, perplexity_api, mood: str, platform: str = 'tiktok', limit: int = 5) -> List[Dict]:
        """
        Get trending sounds filtered by mood
        
        Args:
            perplexity_api: PerplexityAPI instance
            mood (str): Mood filter (Chill, Energetic, Upbeat, Emotional, Funny)
            platform (str): Platform name
            limit (int): Number of results
            
        Returns:
            List[Dict]: Filtered sounds by mood
        """
        try:
            sounds = self.get_trending_sounds(perplexity_api, platform=platform, limit=50)
            filtered_sounds = [s for s in sounds if s.get('mood', '').lower() == mood.lower()]
            return filtered_sounds[:limit]
        except Exception as e:
            print(f"Error filtering sounds by mood: {e}")
            return []
    
    def get_sounds_by_genre(self, perplexity_api, genre: str, platform: str = 'tiktok', limit: int = 5) -> List[Dict]:
        """
        Get trending sounds filtered by genre
        
        Args:
            perplexity_api: PerplexityAPI instance
            genre (str): Genre filter
            platform (str): Platform name
            limit (int): Number of results
            
        Returns:
            List[Dict]: Filtered sounds by genre
        """
        try:
            sounds = self.get_trending_sounds(perplexity_api, platform=platform, limit=50)
            filtered_sounds = [s for s in sounds if s.get('genre', '').lower() == genre.lower()]
            return filtered_sounds[:limit]
        except Exception as e:
            print(f"Error filtering sounds by genre: {e}")
            return []
    
    def analyze_sound_performance(self, perplexity_api, sound_id: str, platform: str = 'tiktok') -> Dict:
        """
        Analyze performance metrics for a specific sound using Perplexity AI
        
        Args:
            perplexity_api: PerplexityAPI instance
            sound_id (str): Sound identifier
            platform (str): Platform name
            
        Returns:
            Dict: Performance analysis
        """
        try:
            sound = self.get_sound_details(perplexity_api, sound_id, platform)
            if not sound:
                return {}
            
            # Calculate performance metrics
            usage_count = sound.get('usage_count', 0)
            trend_score = sound.get('trend_score', 0)
            
            # Determine performance tier
            if usage_count > 2000000:
                performance_tier = 'Viral'
            elif usage_count > 500000:
                performance_tier = 'Trending'
            else:
                performance_tier = 'Emerging'
            
            # Growth prediction
            if trend_score > 90:
                growth_prediction = 'Rapidly Growing'
            elif trend_score > 75:
                growth_prediction = 'Steady Growth'
            else:
                growth_prediction = 'Stable'
            
            return {
                'sound_id': sound_id,
                'performance_tier': performance_tier,
                'usage_count': usage_count,
                'trend_score': trend_score,
                'growth_prediction': growth_prediction,
                'viral_potential': sound.get('viral_potential', 'Unknown'),
                'best_use_time': sound.get('peak_usage_time', ''),
                'top_regions': sound.get('trending_regions', []),
                'recommended_hashtags': sound.get('hashtags', []),
                'content_categories': sound.get('best_content_types', [])
            }
        except Exception as e:
            print(f"Error analyzing sound performance: {e}")
            return {}
    
    def get_personalized_sound_recommendations(self, perplexity_api, user_profile: Dict, platform: str = 'tiktok', 
                                             limit: int = 5) -> List[Dict]:
        """
        Get personalized sound recommendations based on user profile
        
        Args:
            perplexity_api: PerplexityAPI instance
            user_profile (dict): User profile with content category and audience info
            platform (str): Platform name
            limit (int): Number of recommendations
            
        Returns:
            List[Dict]: Personalized sound recommendations
        """
        try:
            content_category = user_profile.get('content_category', '')
            audience_type = user_profile.get('audience_type', '')
            
            # Get trending sounds
            sounds = self.get_trending_sounds(perplexity_api, platform=platform, content_category=content_category, limit=20)
            
            # Score sounds based on user profile
            scored_sounds = []
            for sound in sounds:
                score = sound.get('trend_score', 0)
                
                # Bonus for matching content types
                if content_category.title() in sound.get('best_content_types', []):
                    score += 15
                
                # Bonus for high viral potential
                if sound.get('viral_potential') == 'Extremely High':
                    score += 10
                elif sound.get('viral_potential') == 'High':
                    score += 5
                
                sound['recommendation_score'] = score
                scored_sounds.append(sound)
            
            # Sort by recommendation score
            scored_sounds = sorted(scored_sounds, key=lambda x: x.get('recommendation_score', 0), reverse=True)
            
            return scored_sounds[:limit]
        except Exception as e:
            print(f"Error generating personalized recommendations: {e}")
            return []
    
    def get_emerging_sounds(self, perplexity_api=None, platform: str = 'tiktok', region: str = 'global', limit: int = 5) -> List[Dict]:
        """
        Get emerging sounds before they go viral
        
        Args:
            perplexity_api: PerplexityAPI instance (optional)
            platform (str): Platform name
            region (str): Geographic region
            limit (int): Number of results
            
        Returns:
            List[Dict]: Emerging sounds with growth potential
        """
        sounds = []  # Initialize sounds variable with empty list
        emerging_sounds = []  # Initialize emerging_sounds variable
        
        try:
            if perplexity_api:
                sounds = self.get_trending_sounds(perplexity_api, platform=platform, region=region, limit=50)
            else:
                sounds = self._get_fallback_sounds(platform, None)
            
            # Ensure sounds is a list and not None
            if not sounds or not isinstance(sounds, list):
                sounds = []
            
            # Filter for emerging sounds (low usage but high trend score)
            for sound in sounds:
                if not sound or not isinstance(sound, dict):
                    continue
                    
                usage = sound.get('usage_count', 0)
                trend_score = sound.get('trend_score', 0)
                
                # Emerging criteria: usage < 1M but trend score > 75
                if usage < 1000000 and trend_score > 75:
                    emerging_sounds.append(sound)
            
            return emerging_sounds[:limit]
            
        except Exception as e:
            print(f"Error fetching emerging sounds: {e}")
            # Return fallback sounds if there was an error
            try:
                fallback_sounds = self._get_fallback_sounds(platform, None)
                return fallback_sounds[:limit] if fallback_sounds else []
            except:
                return []
    
    def search_sounds_by_keyword(self, perplexity_api, keyword: str, platform: str = 'tiktok', limit: int = 10) -> List[Dict]:
        """
        Search for sounds by keyword in title, artist, or hashtags
        
        Args:
            perplexity_api: PerplexityAPI instance
            keyword (str): Search keyword
            platform (str): Platform name
            limit (int): Number of results
            
        Returns:
            List[Dict]: Matching sounds
        """
        try:
            sounds = self.get_trending_sounds(perplexity_api, platform=platform, limit=100)
            keyword_lower = keyword.lower()
            
            matching_sounds = []
            for sound in sounds:
                # Search in title, artist, hashtags
                if (keyword_lower in sound.get('title', '').lower() or 
                    keyword_lower in sound.get('artist', '').lower() or
                    any(keyword_lower in tag.lower() for tag in sound.get('hashtags', []))):
                    matching_sounds.append(sound)
            
            return matching_sounds[:limit]
        except Exception as e:
            print(f"Error searching sounds: {e}")
            return []
    
    def get_sound_usage_analytics(self, perplexity_api=None, platform: str = 'tiktok', days: int = 7) -> Dict:
        """
        Get analytics on sound usage trends over time
        
        Args:
            perplexity_api: PerplexityAPI instance (optional)
            platform (str): Platform name
            days (int): Number of days for analysis
            
        Returns:
            Dict: Usage analytics and trends
        """
        sounds = []  # Initialize sounds variable with empty list
        
        try:
            if perplexity_api:
                sounds = self.get_trending_sounds(perplexity_api, platform=platform, limit=50)
            else:
                sounds = self._get_fallback_sounds(platform, None)
            
            # Ensure sounds is a list and not None
            if not sounds or not isinstance(sounds, list):
                sounds = []
            
            # Calculate analytics
            total_usage = sum(s.get('usage_count', 0) for s in sounds if isinstance(s, dict))
            avg_trend_score = sum(s.get('trend_score', 0) for s in sounds if isinstance(s, dict)) / len(sounds) if sounds else 0
            
            # Genre distribution
            genres = {}
            moods = {}
            for sound in sounds:
                if not isinstance(sound, dict):
                    continue
                    
                genre = sound.get('genre', 'Unknown')
                mood = sound.get('mood', 'Unknown')
                genres[genre] = genres.get(genre, 0) + 1
                moods[mood] = moods.get(mood, 0) + 1
            
            return {
                'platform': platform,
                'analysis_period_days': days,
                'total_sounds_analyzed': len(sounds),
                'total_usage_count': total_usage,
                'average_trend_score': round(avg_trend_score, 2),
                'top_genres': dict(sorted(genres.items(), key=lambda x: x[1], reverse=True)[:5]),
                'top_moods': dict(sorted(moods.items(), key=lambda x: x[1], reverse=True)[:5]),
                'viral_sounds_count': len([s for s in sounds if isinstance(s, dict) and s.get('viral_potential') == 'Extremely High']),
                'emerging_sounds_count': len([s for s in sounds if isinstance(s, dict) and s.get('usage_count', 0) < 1000000 and s.get('trend_score', 0) > 75])
            }
        except Exception as e:
            print(f"Error generating usage analytics: {e}")
            return {
                'platform': platform,
                'analysis_period_days': days,
                'total_sounds_analyzed': 0,
                'total_usage_count': 0,
                'average_trend_score': 0,
                'top_genres': {},
                'top_moods': {},
                'viral_sounds_count': 0,
                'emerging_sounds_count': 0
            }
    
    def get_brand_collaboration_opportunities(self, perplexity_api, content_category: str, audience_type: str, 
                                            platform: str = 'tiktok', limit: int = 5) -> List[Dict]:
        """
        Get potential brand collaboration opportunities using Perplexity AI with structured response
        
        Args:
            perplexity_api: PerplexityAPI instance
            content_category (str): Content category (e.g., 'fitness', 'fashion', 'tech')
            audience_type (str): Target audience description
            platform (str): Platform name
            limit (int): Number of brand suggestions
            
        Returns:
            List[Dict]: List of potential brand collaborators
        """
        try:
            from utils.perplexity_api import BrandOpportunities
            
            # Query for structured brand collaboration opportunities
            query = f"""Find {limit} brands currently active in influencer marketing that would partner with {content_category} content creators targeting {audience_type} on {platform.title()}. 

            For each brand, provide exact details:
            - name: exact brand name
            - fit_reason: why they're good for this niche (1-2 sentences)
            - collaboration_types: array of collaboration types (e.g., ["Sponsored Posts", "Product Reviews", "Affiliate Marketing"])
            - value_range: estimated partnership value (e.g., "$100-$1,000" or "Product gifting + commission")
            - approach: how to contact them (e.g., "Direct email contact", "Apply through influencer portal")

            Focus on brands working with micro and mid-tier influencers, providing diverse, realistic opportunities."""
            
            # Use structured response
            structured_response = perplexity_api.ask_structured_question(query, BrandOpportunities, model="sonar-pro")
            
            if structured_response and structured_response.brands:
                # Convert to dict format for compatibility with HTML cleaning
                brands_list = []
                for brand in structured_response.brands[:limit]:
                    brands_list.append({
                        'name': self._clean_text(brand.name),
                        'fit_reason': self._clean_text(brand.fit_reason),
                        'collaboration_types': [self._clean_text(ct) for ct in brand.collaboration_types],
                        'value_range': self._clean_text(brand.value_range),
                        'approach': self._clean_text(brand.approach)
                    })
                return brands_list
            
            return self._get_fallback_brands(content_category)
            
        except Exception as e:
            print(f"Error fetching brand collaboration opportunities: {e}")
            return self._get_fallback_brands(content_category)
    
    def get_music_brand_partnerships(self, perplexity_api, sound_id: str, platform: str = 'tiktok') -> List[Dict]:
        """
        Get brands that might be interested in partnering based on trending sounds
        
        Args:
            perplexity_api: PerplexityAPI instance
            sound_id (str): Sound identifier
            platform (str): Platform name
            
        Returns:
            List[Dict]: List of music-related brand opportunities
        """
        try:
            sound = self.get_sound_details(perplexity_api, sound_id, platform)
            if not sound:
                return []
            
            genre = sound.get('genre', 'Unknown')
            mood = sound.get('mood', 'Unknown')
            content_types = ', '.join(sound.get('best_content_types', []))
            
            query = f"""Find brands that would be interested in partnering with influencers using {genre} music with a {mood} mood for {content_types} content on {platform.title()}. 

            Include:
            - Music streaming services
            - Audio equipment brands
            - Lifestyle brands that match the sound's vibe
            - Entertainment companies
            - Tech brands related to content creation

            For each brand, explain why this sound trend would appeal to them."""
            
            response = perplexity_api.ask_question(query, model="sonar-pro")
            
            if response and 'choices' in response:
                content = response['choices'][0]['message']['content']
                brands = self._parse_brand_response(content)
                return brands[:5]
            
            return []
            
        except Exception as e:
            print(f"Error fetching music brand partnerships: {e}")
            return []
    
    def _parse_brand_response(self, content: str) -> List[Dict]:
        """
        Parse Perplexity response to extract brand information
        
        Args:
            content (str): Response content from Perplexity
            
        Returns:
            List[Dict]: Parsed brand information - CLEAN TEXT ONLY, NO HTML/FORMATTING
        """
        brands = []
        
        # ULTRA-AGGRESSIVE cleaning - remove ALL possible HTML/formatting
        clean_content = content
        
        # Remove ALL HTML tags (including div, span, p, strong, etc.)
        clean_content = re.sub(r'</?(?:div|span|p|strong|b|i|em|br|hr)[^>]*>', ' ', clean_content)
        clean_content = re.sub(r'<[^>]*>', '', clean_content)  # Remove any remaining HTML tags
        clean_content = re.sub(r'&[a-zA-Z0-9#]+;', '', clean_content)  # Remove HTML entities
        
        # Remove all markdown formatting aggressively
        clean_content = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', clean_content)  # Remove all asterisks
        clean_content = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', clean_content)    # Remove all underscores
        clean_content = re.sub(r'#{1,6}\s*([^\n]+)', r'\1', clean_content)      # Remove headers
        
        # Remove reference numbers, citations, and brackets
        clean_content = re.sub(r'\[\d+\]', '', clean_content)
        clean_content = re.sub(r'\[.*?\]', '', clean_content)
        clean_content = re.sub(r'\([^)]*\)', '', clean_content)
        
        # Remove ALL style and formatting attributes
        clean_content = re.sub(r'style\s*=\s*["\'][^"\']*["\']', '', clean_content)
        clean_content = re.sub(r'class\s*=\s*["\'][^"\']*["\']', '', clean_content)
        clean_content = re.sub(r'id\s*=\s*["\'][^"\']*["\']', '', clean_content)
        
        # Remove any remaining HTML attribute patterns
        clean_content = re.sub(r'\w+\s*=\s*["\'][^"\']*["\']', '', clean_content)
        
        # Clean up excessive whitespace and line breaks
        clean_content = re.sub(r'\n\s*\n+', '\n', clean_content)
        clean_content = re.sub(r'\s+', ' ', clean_content)
        clean_content = clean_content.strip()
        
        # Split by numbered sections (1., 2., etc.)
        sections = re.split(r'\n?\s*\d+\.\s*', clean_content)
        
        for i, section in enumerate(sections[1:], 1):  # Skip first empty section
            if not section or len(section.strip()) < 15:
                continue
            
            section = section.strip()
            
            # Extract brand name from the beginning of the section
            brand_name = 'Brand Partner'
            lines = section.split('\n')
            
            # Look for brand name in the first few words
            first_words = section.split()[:5]
            for j, word in enumerate(first_words):
                if word and len(word) > 2 and word[0].isupper():
                    # Found potential brand name
                    brand_name_parts = [word]
                    
                    # Add next words if they're also part of brand name
                    for k in range(j+1, min(j+4, len(first_words))):
                        next_word = first_words[k]
                        if (next_word and (next_word[0].isupper() or 
                                         next_word.lower() in ['&', 'and', 'co', 'inc', 'ltd'])):
                            brand_name_parts.append(next_word)
                        else:
                            break
                    
                    potential_name = ' '.join(brand_name_parts)
                    if len(potential_name) >= 3 and len(potential_name) <= 40:
                        brand_name = potential_name
                        break
            
            # Clean brand name
            brand_name = re.sub(r'^[^a-zA-Z]*', '', brand_name)  # Remove leading non-letters
            brand_name = re.sub(r'[^a-zA-Z0-9\s&.]+.*$', '', brand_name)  # Remove trailing junk
            brand_name = brand_name.strip()
            
            # Extract key information
            section_lower = section.lower()
            
            # Extract fit reason
            fit_reason = 'Good partnership opportunity for content creators'
            
            # Look for explanatory sentences
            sentences = section.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if (len(sentence) > 30 and len(sentence) < 150 and 
                    any(word in sentence.lower() for word in ['brand', 'fit', 'good', 'target', 'audience', 'partner', 'collab', 'work'])):
                    # Clean the sentence
                    sentence = re.sub(r'^[^a-zA-Z]*', '', sentence)
                    sentence = sentence.strip()
                    if sentence and not sentence.lower().startswith(brand_name.lower()):
                        fit_reason = sentence
                        if not fit_reason.endswith('.'):
                            fit_reason += '.'
                        break
            
            # Extract collaboration types
            collab_types = ['Sponsored Content']
            collab_keywords = {
                'sponsored': 'Sponsored Posts',
                'affiliate': 'Affiliate Marketing',
                'review': 'Product Reviews', 
                'placement': 'Product Placement',
                'partnership': 'Brand Partnership',
                'ambassador': 'Brand Ambassador',
                'content': 'Content Creation'
            }
            
            found_collabs = []
            for keyword, display in collab_keywords.items():
                if keyword in section_lower:
                    found_collabs.append(display)
            
            if found_collabs:
                collab_types = list(set(found_collabs))[:3]
            
            # Extract value range
            value_range = 'Contact for details'
            value_patterns = [
                r'\$(\d{1,3}(?:,\d{3})*)[-–]\$?(\d{1,3}(?:,\d{3})*)',  # $1,000-$5,000
                r'\$(\d{1,3}(?:,\d{3})*)\+',                           # $1,000+
                r'₹(\d{1,3}(?:,\d{3})*)[-–]₹?(\d{1,3}(?:,\d{3})*)',   # ₹10,000-₹50,000
                r'₹(\d{1,3}(?:,\d{3})*)\+',                            # ₹10,000+
            ]
            
            for pattern in value_patterns:
                match = re.search(pattern, section)
                if match:
                    value_range = match.group(0)
                    break
            
            # Extract approach
            approach = 'Direct outreach recommended'
            if 'website' in section_lower or 'portal' in section_lower:
                approach = 'Apply through official website'
            elif 'email' in section_lower:
                approach = 'Direct email contact'
            elif 'social media' in section_lower or 'instagram' in section_lower:
                approach = 'Social media outreach'
            
            # Create clean brand object
            brand = {
                'name': brand_name,
                'fit_reason': fit_reason,
                'collaboration_types': collab_types,
                'value_range': value_range,
                'approach': approach
            }
            
            # Final validation
            if (len(brand['name']) >= 3 and 
                len(brand['name']) <= 40 and
                not any(bad_word in brand['name'].lower() for bad_word in ['why', 'typical', 'estimated', 'contact', 'div', 'span', 'style'])):
                brands.append(brand)
        
        # If no brands found, create fallback
        if not brands:
            brands = [
                {
                    'name': 'Fitness Brand Opportunities',
                    'fit_reason': 'Multiple fitness brands actively seek influencer partnerships with engaged audiences.',
                    'collaboration_types': ['Sponsored Content', 'Product Reviews', 'Affiliate Marketing'],
                    'value_range': '$100-$1,000+',
                    'approach': 'Research brands in your niche and reach out directly'
                }
            ]
        
        return brands[:5]
    
    def _clean_text(self, text: str) -> str:
        """
        Clean HTML tags and formatting from any text string
        
        Args:
            text (str): Text that may contain HTML/formatting
            
        Returns:
            str: Clean text without HTML/formatting
        """
        if not text or not isinstance(text, str):
            return text
        
        clean_text = text
        
        # Remove ALL HTML tags (including div, span, p, strong, etc.)
        clean_text = re.sub(r'</?(?:div|span|p|strong|b|i|em|br|hr)[^>]*>', ' ', clean_text)
        clean_text = re.sub(r'<[^>]*>', '', clean_text)  # Remove any remaining HTML tags
        clean_text = re.sub(r'&[a-zA-Z0-9#]+;', '', clean_text)  # Remove HTML entities
        
        # Remove all markdown formatting aggressively
        clean_text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', clean_text)  # Remove all asterisks
        clean_text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', clean_text)    # Remove all underscores
        clean_text = re.sub(r'#{1,6}\s*([^\n]+)', r'\1', clean_text)      # Remove headers
        
        # Remove reference numbers, citations, and brackets
        clean_text = re.sub(r'\[\d+\]', '', clean_text)
        clean_text = re.sub(r'\[.*?\]', '', clean_text)
        clean_text = re.sub(r'\([^)]*\)', '', clean_text)
        
        # Remove ALL style and formatting attributes
        clean_text = re.sub(r'style\s*=\s*["\'][^"\']*["\']', '', clean_text)
        clean_text = re.sub(r'class\s*=\s*["\'][^"\']*["\']', '', clean_text)
        clean_text = re.sub(r'id\s*=\s*["\'][^"\']*["\']', '', clean_text)
        
        # Remove any remaining HTML attribute patterns
        clean_text = re.sub(r'\w+\s*=\s*["\'][^"\']*["\']', '', clean_text)
        
        # Clean up excessive whitespace and line breaks
        clean_text = re.sub(r'\n\s*\n+', '\n', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        clean_text = clean_text.strip()
        
        return clean_text
    
    def _get_fallback_brands(self, content_category: str) -> List[Dict]:
        """
        Get fallback brand suggestions when API fails
        
        Args:
            content_category (str): Content category
            
        Returns:
            List[Dict]: Fallback brand suggestions
        """
        fallback_brands = {
            'fitness': [
                {
                    'name': 'Gymshark',
                    'fit_reason': 'Leading fitness apparel brand with strong influencer program',
                    'collaboration_types': ['Sponsored posts', 'Affiliate marketing', 'Product gifting'],
                    'value_range': '$100-$5,000',
                    'approach': 'Apply through their influencer portal'
                },
                {
                    'name': 'MyProtein',
                    'fit_reason': 'Sports nutrition brand actively seeking fitness influencers',
                    'collaboration_types': ['Discount codes', 'Product reviews', 'Workout videos'],
                    'value_range': '$50-$2,000',
                    'approach': 'Contact their marketing team directly'
                }
            ],
            'fashion': [
                {
                    'name': 'Shein',
                    'fit_reason': 'Fast fashion brand with extensive influencer partnerships',
                    'collaboration_types': ['Try-on hauls', 'Styling videos', 'Discount codes'],
                    'value_range': '$100-$3,000',
                    'approach': 'Apply through Shein influencer program'
                },
                {
                    'name': 'PrettyLittleThing',
                    'fit_reason': 'Trendy fashion brand targeting young demographics',
                    'collaboration_types': ['OOTD posts', 'Event collaborations', 'Product gifting'],
                    'value_range': '$200-$5,000',
                    'approach': 'Reach out via social media or influencer platform'
                }
            ],
            'tech': [
                {
                    'name': 'Razer',
                    'fit_reason': 'Gaming and tech brand with active creator partnerships',
                    'collaboration_types': ['Product reviews', 'Gaming content', 'Tech tutorials'],
                    'value_range': '$500-$10,000',
                    'approach': 'Apply through Razer Creator Program'
                },
                {
                    'name': 'Anker',
                    'fit_reason': 'Consumer electronics brand seeking tech reviewers',
                    'collaboration_types': ['Product testing', 'Unboxing videos', 'Tech tips'],
                    'value_range': '$100-$2,000',
                    'approach': 'Contact through PR agency or direct email'
                }
            ]
        }
        
        return fallback_brands.get(content_category.lower(), [
            {
                'name': 'Generic Brand Opportunity',
                'fit_reason': f'Brands in the {content_category} space often seek influencer partnerships',
                'collaboration_types': ['Sponsored content', 'Product placement', 'Brand mentions'],
                'value_range': 'Varies by brand and audience size',
                'approach': 'Research brands in your niche and reach out directly'
            }
        ])
    
    def _parse_sound_response(self, content: str, platform: str) -> List[Dict]:
        """
        Parse Perplexity response to extract sound information
        
        Args:
            content (str): Response content from Perplexity
            platform (str): Platform name
            
        Returns:
            List[Dict]: Parsed sound information
        """
        sounds = []
        lines = content.split('\n')
        current_sound = {}
        sound_id_counter = 1
        
        for line in lines:
            line = line.strip()
            
            # Look for sound titles (typically bold or numbered)
            if re.match(r'^\d+\.\s*\*?\*?(.+?)\*?\*?', line) or re.match(r'^\*\*(.+?)\*\*', line):
                # Save previous sound if exists
                if current_sound:
                    sounds.append(current_sound)
                
                # Extract sound title
                title_match = re.match(r'^\d+\.\s*\*?\*?(.+?)\*?\*?', line) or re.match(r'^\*\*(.+?)\*\*', line)
                if title_match:
                    current_sound = {
                        'id': f'{platform[0:2]}_{sound_id_counter:03d}',
                        'title': title_match.group(1).strip(),
                        'artist': 'Unknown Artist',
                        'duration': 20,
                        'usage_count': 1000000,
                        'trend_score': 85,
                        'genre': 'Unknown',
                        'mood': 'Unknown',
                        'viral_potential': 'High',
                        'hashtags': [],
                        'best_content_types': [],
                        'trending_regions': ['Global'],
                        'peak_usage_time': '18:00-22:00',
                        'audio_preview_url': f'https://example.com/preview/{platform[0:2]}_{sound_id_counter:03d}.mp3'
                    }
                    sound_id_counter += 1
            
            # Extract artist information
            elif ('artist' in line.lower() or 'by ' in line.lower() or 'creator' in line.lower()) and current_sound:
                # Clean artist name from various formats
                artist_patterns = [
                    r'artist[:\-\s]*(.+?)(?:\s*\||$)',
                    r'by\s+(.+?)(?:\s*\||$)',
                    r'creator[:\-\s]*(.+?)(?:\s*\||$)'
                ]
                for pattern in artist_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        current_sound['artist'] = match.group(1).strip()
                        break
            
            # Extract genre
            elif ('genre' in line.lower() or 'style' in line.lower()) and current_sound:
                genre_match = re.search(r'genre[:\-\s]*(.+?)(?:\s*\||$)', line, re.IGNORECASE)
                if not genre_match:
                    genre_match = re.search(r'style[:\-\s]*(.+?)(?:\s*\||$)', line, re.IGNORECASE)
                if genre_match:
                    current_sound['genre'] = genre_match.group(1).strip()
            
            # Extract mood/vibe
            elif ('mood' in line.lower() or 'vibe' in line.lower()) and current_sound:
                mood_keywords = ['Chill', 'Energetic', 'Upbeat', 'Emotional', 'Funny', 'Relaxing', 'Intense', 'Happy', 'Sad']
                for mood in mood_keywords:
                    if mood.lower() in line.lower():
                        current_sound['mood'] = mood
                        break
            
            # Extract viral potential
            elif ('viral' in line.lower() or 'trending' in line.lower()) and current_sound:
                if 'high' in line.lower() or 'extremely' in line.lower():
                    current_sound['viral_potential'] = 'Extremely High' if 'extremely' in line.lower() else 'High'
                elif 'medium' in line.lower():
                    current_sound['viral_potential'] = 'Medium'
                elif 'low' in line.lower():
                    current_sound['viral_potential'] = 'Low'
            
            # Extract hashtags
            elif '#' in line and current_sound:
                hashtags = re.findall(r'#\w+', line)
                current_sound['hashtags'].extend(hashtags[:5])  # Limit to 5 hashtags
            
            # Extract content types
            elif ('content' in line.lower() or 'works for' in line.lower()) and current_sound:
                content_types = ['Fashion', 'Fitness', 'Dance', 'Comedy', 'Lifestyle', 'Tech', 'Food', 'Travel', 'Beauty', 'Gaming']
                for content_type in content_types:
                    if content_type.lower() in line.lower():
                        if content_type not in current_sound['best_content_types']:
                            current_sound['best_content_types'].append(content_type)
            
            # Extract duration
            elif ('duration' in line.lower() or 'seconds' in line.lower()) and current_sound:
                duration_match = re.search(r'(\d+)\s*seconds?', line, re.IGNORECASE)
                if duration_match:
                    current_sound['duration'] = int(duration_match.group(1))
        
        # Don't forget the last sound
        if current_sound:
            sounds.append(current_sound)
        
        # If parsing didn't work well, create some basic sounds from the content
        if not sounds and content:
            sentences = content.split('. ')
            for i, sentence in enumerate(sentences[:5]):
                if len(sentence) > 20:
                    sounds.append({
                        'id': f'{platform[0:2]}_{i+1:03d}',
                        'title': sentence.split()[0:4] if sentence.split() else ['Trending Sound'],
                        'title': ' '.join(sentence.split()[0:4]) if sentence.split() else 'Trending Sound',
                        'artist': 'AI Generated',
                        'duration': 20,
                        'usage_count': 500000,
                        'trend_score': 80,
                        'genre': 'Mixed',
                        'mood': 'Upbeat',
                        'viral_potential': 'High',
                        'hashtags': ['#trending', '#viral'],
                        'best_content_types': ['General'],
                        'trending_regions': ['Global'],
                        'peak_usage_time': '18:00-22:00',
                        'audio_preview_url': f'https://example.com/preview/{platform[0:2]}_{i+1:03d}.mp3'
                    })
        
        return sounds
    
    def _get_fallback_sounds(self, platform: str, content_category: str = None) -> List[Dict]:
        """
        Get minimal fallback sounds when Perplexity API fails
        
        Args:
            platform (str): Platform name
            content_category (str): Content category filter
            
        Returns:
            List[Dict]: Minimal fallback sound suggestions
        """
        # Create minimal fallback sounds - this should only be used when Perplexity API is unavailable
        category_filter = content_category.title() if content_category else "General"
        
        fallback_sounds = [
            {
                'id': f'{platform[0:2]}_fallback_001',
                'title': f'Trending {category_filter} Sound',
                'artist': 'Popular Artist',
                'duration': 20,
                'usage_count': 500000,
                'trend_score': 75,
                'genre': 'Mixed',
                'mood': 'Upbeat',
                'viral_potential': 'Medium',
                'hashtags': ['#trending', '#viral', f'#{category_filter.lower()}'],
                'best_content_types': [category_filter] if content_category else ['General'],
                'trending_regions': ['Global'],
                'peak_usage_time': '18:00-22:00',
                'audio_preview_url': f'https://example.com/preview/{platform[0:2]}_fallback_001.mp3'
            },
            {
                'id': f'{platform[0:2]}_fallback_002',
                'title': f'Popular {category_filter} Beat',
                'artist': 'Trending Creator',
                'duration': 15,
                'usage_count': 300000,
                'trend_score': 70,
                'genre': 'Electronic',
                'mood': 'Energetic',
                'viral_potential': 'Medium',
                'hashtags': ['#music', '#beat', f'#{category_filter.lower()}'],
                'best_content_types': [category_filter] if content_category else ['General'],
                'trending_regions': ['Global'],
                'peak_usage_time': '16:00-20:00',
                'audio_preview_url': f'https://example.com/preview/{platform[0:2]}_fallback_002.mp3'
            }
        ]
        
        return fallback_sounds
