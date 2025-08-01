import requests
import json
import pandas as pd
import numpy as np
import plotly.express as px

class QlooAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://hackathon.api.qloo.com"
        self.headers = {
            "accept": "application/json",
            "X-Api-Key": api_key
        }
        
        # Entity type mappings for easier use
        self.entity_types = {
            'movie': 'urn:entity:movie',
            'artist': 'urn:entity:artist',
            'book': 'urn:entity:book',
            'brand': 'urn:entity:brand',
            'destination': 'urn:entity:destination',
            'person': 'urn:entity:person',
            'place': 'urn:entity:place',
            'podcast': 'urn:entity:podcast',
            'tv_show': 'urn:entity:tv_show',
            'video_game': 'urn:entity:video_game'
        }
    
    def get_insights(self, entity_type, filters=None, signals=None, take=10, offset=0):
        """
        Get insights using v2 API with proper filters and signals
        
        Args:
            entity_type (str): Entity type (use key from entity_types or full URN)
            filters (dict, optional): Filter parameters (without 'filter.' prefix)
            signals (dict, optional): Signal parameters (without 'signal.' prefix)
            take (int, optional): Number of results to return
            offset (int, optional): Offset for pagination
            
        Returns:
            dict: API response containing insights
        """
        try:
            endpoint = f"{self.base_url}/v2/insights/"
            
            # Convert entity type if it's a short form
            if entity_type in self.entity_types:
                entity_type = self.entity_types[entity_type]
            
            params = {
                "filter.type": entity_type,
                "take": take,
                "offset": offset
            }
            
            # Add filters with proper prefix
            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        # Handle list values (for multiple values)
                        for i, v in enumerate(value):
                            params[f"filter.{key}"] = v if i == 0 else f"{params[f'filter.{key}']},{v}"
                    else:
                        params[f"filter.{key}"] = value
                        
            # Add signals with proper prefix
            if signals:
                for key, value in signals.items():
                    if isinstance(value, list):
                        # Handle list values
                        for i, v in enumerate(value):
                            params[f"signal.{key}"] = v if i == 0 else f"{params[f'signal.{key}']},{v}"
                    else:
                        params[f"signal.{key}"] = value
            
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error fetching insights: {e}")
            return {"results": []}
    
    def get_movies_by_genre(self, genre_tag, release_year_min=None, release_year_max=None, 
                           rating_min=None, rating_max=None, take=20):
        """
        Get movies filtered by genre and other criteria
        
        Args:
            genre_tag (str): Genre tag URN (e.g., 'urn:tag:genre:media:comedy')
            release_year_min (int, optional): Minimum release year
            release_year_max (int, optional): Maximum release year
            rating_min (float, optional): Minimum rating
            rating_max (float, optional): Maximum rating
            take (int, optional): Number of results
            
        Returns:
            dict: Movies matching criteria
        """
        filters = {
            "tags": genre_tag
        }
        
        if release_year_min:
            filters["release_year.min"] = release_year_min
        if release_year_max:
            filters["release_year.max"] = release_year_max
        if rating_min:
            filters["rating.min"] = rating_min
        if rating_max:
            filters["rating.max"] = rating_max
            
        return self.get_insights("movie", filters=filters, take=take)
    
    def get_places_by_location(self, location, radius=None, price_level_min=None, 
                              price_level_max=None, tags=None, take=20):
        """
        Get places filtered by location and other criteria
        
        Args:
            location (str): Location coordinates or address
            radius (float, optional): Search radius
            price_level_min (int, optional): Minimum price level
            price_level_max (int, optional): Maximum price level
            tags (str or list, optional): Tag filters
            take (int, optional): Number of results
            
        Returns:
            dict: Places matching criteria
        """
        filters = {
            "location": location
        }
        
        if radius:
            filters["location.radius"] = radius
        if price_level_min:
            filters["price_level.min"] = price_level_min
        if price_level_max:
            filters["price_level.max"] = price_level_max
        if tags:
            filters["tags"] = tags
            
        return self.get_insights("place", filters=filters, take=take)
    
    def get_books_by_publication_year(self, year_min=None, year_max=None, tags=None, 
                                     popularity_min=None, take=20):
        """
        Get books filtered by publication year and other criteria
        
        Args:
            year_min (int, optional): Minimum publication year
            year_max (int, optional): Maximum publication year
            tags (str or list, optional): Tag filters
            popularity_min (float, optional): Minimum popularity score
            take (int, optional): Number of results
            
        Returns:
            dict: Books matching criteria
        """
        filters = {}
        
        if year_min:
            filters["publication_year.min"] = year_min
        if year_max:
            filters["publication_year.max"] = year_max
        if tags:
            filters["tags"] = tags
        if popularity_min:
            filters["popularity.min"] = popularity_min
            
        return self.get_insights("book", filters=filters, take=take)
    
    def get_tv_shows_by_criteria(self, content_rating=None, release_year_min=None, 
                                release_year_max=None, tags=None, release_country=None, take=20):
        """
        Get TV shows filtered by various criteria
        
        Args:
            content_rating (str, optional): Content rating filter
            release_year_min (int, optional): Minimum release year
            release_year_max (int, optional): Maximum release year
            tags (str or list, optional): Tag filters
            release_country (str, optional): Release country filter
            take (int, optional): Number of results
            
        Returns:
            dict: TV shows matching criteria
        """
        filters = {}
        
        if content_rating:
            filters["content_rating"] = content_rating
        if release_year_min:
            filters["release_year.min"] = release_year_min
        if release_year_max:
            filters["release_year.max"] = release_year_max
        if tags:
            filters["tags"] = tags
        if release_country:
            filters["release_country"] = release_country
            
        return self.get_insights("tv_show", filters=filters, take=take)
    
    def get_people_by_demographics(self, gender=None, birth_year_min=None, birth_year_max=None, 
                                  tags=None, popularity_min=None, take=20):
        """
        Get people filtered by demographic criteria
        
        Args:
            gender (str, optional): Gender filter
            birth_year_min (int, optional): Minimum birth year
            birth_year_max (int, optional): Maximum birth year
            tags (str or list, optional): Tag filters
            popularity_min (float, optional): Minimum popularity score
            take (int, optional): Number of results
            
        Returns:
            dict: People matching criteria
        """
        filters = {}
        
        if gender:
            filters["gender"] = gender
        if birth_year_min:
            filters["date_of_birth.min"] = f"{birth_year_min}-01-01"
        if birth_year_max:
            filters["date_of_birth.max"] = f"{birth_year_max}-12-31"
        if tags:
            filters["tags"] = tags
        if popularity_min:
            filters["popularity.min"] = popularity_min
            
        return self.get_insights("person", filters=filters, take=take)
    
    def get_insights_with_demographics(self, entity_type, demographic_signals=None, 
                                     interest_entities=None, interest_tags=None, 
                                     filters=None, take=20):
        """
        Get insights with demographic and interest signals
        
        Args:
            entity_type (str): Entity type
            demographic_signals (dict, optional): Demographic signals (age, gender, audiences)
            interest_entities (list, optional): Interest entity signals
            interest_tags (list, optional): Interest tag signals
            filters (dict, optional): Additional filters
            take (int, optional): Number of results
            
        Returns:
            dict: Insights with demographic targeting
        """
        signals = {}
        
        if demographic_signals:
            if 'age' in demographic_signals:
                signals['demographics.age'] = demographic_signals['age']
            if 'gender' in demographic_signals:
                signals['demographics.gender'] = demographic_signals['gender']
            if 'audiences' in demographic_signals:
                signals['demographics.audiences'] = demographic_signals['audiences']
            if 'audiences.weight' in demographic_signals:
                signals['demographics.audiences.weight'] = demographic_signals['audiences.weight']
        
        if interest_entities:
            signals['interests.entities'] = interest_entities if isinstance(interest_entities, str) else ','.join(interest_entities)
        if interest_tags:
            signals['interests.tags'] = interest_tags if isinstance(interest_tags, str) else ','.join(interest_tags)
        
        return self.get_insights(entity_type, filters=filters, signals=signals, take=take)
    
    def get_trending_insights(self, entity_type, filters=None, take=20):
        """
        Get trending insights with bias towards trends
        
        Args:
            entity_type (str): Entity type
            filters (dict, optional): Additional filters
            take (int, optional): Number of results
            
        Returns:
            dict: Trending insights
        """
        signals = {
            'bias.trends': True  # Changed from string to boolean
        }
        
        return self.get_insights(entity_type, filters=filters, signals=signals, take=take)
    
    def search_entities_by_filters(self, entity_type, search_query, take=20):
        """
        Search entities by name using basic insights API (v2 doesn't support query search)
        
        Args:
            entity_type (str): Entity type
            search_query (str): Search query string (not supported in v2)
            take (int, optional): Number of results
            
        Returns:
            dict: Search results (fallback to basic insights)
        """
        # v2 API doesn't support search by query, so return basic insights
        return self.get_insights(entity_type, filters=None, take=take)
    
    def search_entities(self, query, entity_type=None, limit=10):
        """
        Legacy search method for backwards compatibility with existing apps
        Note: v2 API doesn't support text search, so this returns basic insights
        
        Args:
            query (str): Search query (not supported in v2)
            entity_type (str, optional): Limit search to a specific entity type
            limit (int, optional): Maximum number of results to return
            
        Returns:
            dict: Search results containing entity IDs and information
        """
        try:
            # If no entity type specified, default to movie for now
            if not entity_type:
                entity_type = "movie"
            
            # v2 API doesn't support text search, so return basic insights
            result = self.get_insights(entity_type, filters=None, take=limit)
            
            # Transform the result to match the expected legacy format
            if result and "results" in result and "entities" in result["results"]:
                # Convert the new format to legacy format
                legacy_results = []
                for entity in result["results"]["entities"]:
                    legacy_entity = {
                        "id": entity.get("entity_id", ""),
                        "name": entity.get("name", ""),
                        "type": entity.get("subtype", entity.get("type", "")),
                        "tags": entity.get("tags", [])
                    }
                    legacy_results.append(legacy_entity)
                
                return {"results": legacy_results}
            else:
                return {"results": []}
                
        except Exception as e:
            print(f"Error searching entities: {e}")
            return {"results": []}
    
    def get_tags(self, search_query=None):
        """
        Get tags from the v2 API
        Note: v2 API doesn't support tag search, returns all available tags
        
        Args:
            search_query (str, optional): Search query for tags (not supported in v2)
            
        Returns:
            dict: Available tags
        """
        try:
            endpoint = f"{self.base_url}/v2/tags"
            # v2 API doesn't support search parameters for tags
            params = {}
            
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error fetching tags: {e}")
            return {"results": []}
    
    def get_audiences(self):
        """
        Get available audience demographic segments
        
        Returns:
            dict: Available audience segments
        """
        try:
            endpoint = f"{self.base_url}/v2/audiences"
            
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error fetching audiences: {e}")
            return {"results": []}
    
    def get_country_insights(self, content_category, audience_type):
        """
        Get insights based on content category and audience type per country
        
        Args:
            content_category (str): Category of content (e.g., 'fashion', 'tech', 'fitness')
            audience_type (str): Type of audience (e.g., 'teens', 'young adults', 'professionals')
            
        Returns:
            dict: Dictionary containing insights by country
        """
        try:
            # Using the insights/geography endpoint from the hackathon API
            endpoint = f"{self.base_url}/insights/geography"
            
            payload = {
                "content_category": content_category,
                "audience_type": audience_type
            }
            
            # Use POST request with JSON payload as specified in examples
            response = requests.post(
                endpoint, 
                headers=self.headers, 
                json=payload
            )
            
            # Debug information
            print(f"Geography insights request to {endpoint}")
            print(f"Status code: {response.status_code}")
            
            response.raise_for_status()
            result = response.json()
            
            # If the result is already in the expected format, return it directly
            if "countries" in result:
                return result
                
            # Otherwise, transform it into our expected format for compatibility
            country_insights = {"countries": {}}
            
            # Process the response based on the hackathon API structure
            if "results" in result:
                for country_data in result.get("results", []):
                    country_code = country_data.get("country_code", "")
                    if country_code:
                        country_insights["countries"][country_code] = {
                            "relevance_score": country_data.get("relevance_score", 0),
                            "name": country_data.get("country_name", "Unknown")
                        }
            
            return country_insights
        except Exception as e:
            print(f"Error fetching country insights: {e}")
            # Return mock data for demonstration if API fails
            return {
                "countries": {
                    "USA": {"relevance_score": 0.85},
                    "GBR": {"relevance_score": 0.75},
                    "CAN": {"relevance_score": 0.70},
                    "AUS": {"relevance_score": 0.65},
                    "DEU": {"relevance_score": 0.60}
                }
            }
    
    def get_trending_topics(self, country_code, content_category, audience_type):
        """
        Get trending topics for a specific country using Qloo insights API
        
        Args:
            country_code (str): ISO country code (e.g., 'US', 'GB', 'JP')
            content_category (str): Category of content
            audience_type (str): Type of audience
            
        Returns:
            dict: Dictionary containing trending topics for the country
        """
        try:
            # Using the trends/region endpoint from the hackathon API
            endpoint = f"{self.base_url}/trends/region"
            
            payload = {
                "country_code": country_code,
                "content_category": content_category,
                "audience_type": audience_type
            }
            
            # Use POST request with JSON payload as specified in examples
            response = requests.post(
                endpoint, 
                headers=self.headers, 
                json=payload
            )
            
            # Debug information
            print(f"Region trends request to {endpoint}")
            print(f"Status code: {response.status_code}")
            
            response.raise_for_status()
            result = response.json()
            
            # If we get a direct trending_topics array, wrap it in our response format
            if "trending_topics" in result:
                return {
                    "country_code": country_code,
                    "country_name": result.get("country_name", country_code),
                    "trending_topics": result.get("trending_topics", [])
                }
                
            # If we don't have trending topics from the API, generate fallback topics
            country_map = {
                "USA": "United States", 
                "GBR": "United Kingdom",
                "CAN": "Canada",
                "AUS": "Australia",
                "DEU": "Germany",
                "FRA": "France",
                "JPN": "Japan"
            }
            country_name = country_map.get(country_code, country_code)
            
            # Generate fallback topics based on content category
            fallback_topics = []
            if content_category.lower() == "fashion":
                fallback_topics = ["Sustainable Fashion", "Vintage Styles", "Streetwear", "Minimalism", "Bold Colors"]
            elif content_category.lower() == "tech":
                fallback_topics = ["AI Tools", "Smart Home", "Productivity Apps", "Digital Wellness", "Virtual Reality"]
            elif content_category.lower() == "fitness":
                fallback_topics = ["HIIT Workouts", "Mind-Body Balance", "Nutrition Planning", "Home Fitness", "Outdoor Training"]
            else:
                fallback_topics = ["Visual Storytelling", "Short-form Content", "Behind-the-Scenes", "User Engagement", "Collaborations"]
            
            return {
                "country_code": country_code,
                "country_name": country_name,
                "trending_topics": fallback_topics
            }
        except Exception as e:
            print(f"Error fetching trending topics: {e}")
            # Return mock data if API call fails
            return {
                "country_code": country_code,
                "country_name": country_code,
                "trending_topics": [
                    "Visual Storytelling",
                    "Authentic Content",
                    "Interactive Polls",
                    "Behind-the-Scenes",
                    "Sustainability",
                    "Local Culture",
                    "Niche Communities",
                    "User-Generated Content",
                    "Short-form Videos",
                    "Social Commerce"
                ]
            }

    def create_heatmap(self, insights_data):
        """
        Create a heatmap visualization from country insights data
        
        Args:
            insights_data (dict): Country insights data from get_country_insights
            
        Returns:
            plotly.graph_objects.Figure: Plotly figure object with heatmap
        """
        try:
            # Transform the data into a format suitable for visualization
            countries = []
            relevance_scores = []
            
            for country, data in insights_data.get('countries', {}).items():
                countries.append(country)
                relevance_scores.append(data.get('relevance_score', 0))
            
            # Create dataframe for visualization
            df = pd.DataFrame({
                'country': countries,
                'relevance_score': relevance_scores
            })
            
            # Create choropleth map
            fig = px.choropleth(
                df,
                locations='country',
                color='relevance_score',
                hover_name='country',
                color_continuous_scale=px.colors.sequential.Plasma,
                locationmode='ISO-3',
                title='Content Relevance by Country'
            )
            
            fig.update_layout(
                margin=dict(l=0, r=0, t=50, b=0),
                coloraxis_colorbar=dict(
                    title='Relevance Score',
                )
            )
            
            return fig
        except Exception as e:
            print(f"Error creating heatmap: {e}")
            return None
