"""
Web Search Agent - Searches university websites for real-time course information
Uses Google Custom Search JSON API (respectful of robots.txt, no scraping)
"""

import os
import json
import logging
from typing import List, Dict, Any
from .base import BaseAgent

class WebSearchAgent(BaseAgent):
    """
    Agent that performs web searches on Singapore university websites
    to fetch real-time course information, admission requirements, and updates.
    
    Uses Google Custom Search JSON API which respects robots.txt and site preferences.
    """
    
    def __init__(self, context):
        super().__init__(context)
        self.logger = logging.getLogger(__name__)
        self.api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
        self.search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")
        self.enabled = self.api_key and self.search_engine_id
        self.genai_client = getattr(context, 'genai_client', None)  # For LLM summaries
        
        # Singapore university domains for targeted search
        self.university_domains = [
            "nus.edu.sg",
            "ntu.edu.sg",
            "smu.edu.sg",
            "sit.singaporetech.edu.sg",
            "sp.edu.sg",  # Singapore Polytechnic
            "np.edu.sg",  # Ngee Ann Polytechnic
            "tp.edu.sg",  # Temasek Polytechnic
            "rp.edu.sg",  # Republic Polytechnic
            "nyp.edu.sg", # Nanyang Polytechnic
            "lasalle.edu.sg"
        ]
    
    def run(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search university websites for courses matching student interests
        
        Args:
            profile: Student profile with interests, target_level
        
        Returns:
            Dict with search_results containing latest course info from web
        """
        if not self.enabled:
            return {
                "agent": "web_search",
                "enabled": False,
                "message": "Web search disabled. Set GOOGLE_CUSTOM_SEARCH_API_KEY and GOOGLE_CUSTOM_SEARCH_ENGINE_ID to enable.",
                "search_results": []
            }
        
        interests = profile.get("interests", [])
        target_level = profile.get("target_level", "degree")
        
        if not interests:
            return {
                "agent": "web_search",
                "search_results": [],
                "message": "No interests provided for search"
            }
        
        # Construct search queries
        search_results = []
        
        for interest in interests[:3]:  # Limit to 3 interests to avoid quota
            query = self._build_search_query(interest, target_level)
            results = self._perform_search(query)
            search_results.extend(results)
        
        # Deduplicate and rank
        unique_results = self._deduplicate_results(search_results)
        
        # Generate LLM summary if available
        llm_summary = ""
        if self.genai_client and unique_results:
            llm_summary = self._generate_summary(unique_results, interests, target_level)
        
        return {
            "agent": "web_search",
            "search_results": unique_results[:10],  # Top 10 results
            "queries_used": len(interests[:3]),
            "total_results_found": len(unique_results),
            "llm_summary": llm_summary
        }
    
    def _build_search_query(self, interest: str, target_level: str) -> str:
        """Build targeted search query for Singapore universities"""
        level_keywords = {
            "diploma": "diploma programme",
            "degree": "bachelor degree programme",
            "postgrad": "master postgraduate programme"
        }
        
        level_term = level_keywords.get(target_level, "programme")
        
        # Add Singapore and year for freshness
        query = f"{interest} {level_term} Singapore university 2025"
        
        return query
    
    def _perform_search(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform Google Custom Search API call
        
        Args:
            query: Search query string
        
        Returns:
            List of search results with title, link, snippet
        """
        if not self.enabled:
            return []
        
        try:
            import requests
            
            url = "https://www.googleapis.com/customsearch/v1"
            
            params = {
                "key": self.api_key,
                "cx": self.search_engine_id,
                "q": query,
                "num": 5  # Results per query
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            for item in data.get("items", []):
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "display_link": item.get("displayLink", ""),
                    "query": query
                })
            
            return results
            
        except Exception as e:
            self.pass}")
            return []
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate URLs and rank by relevance"""
        seen_links = set()
        unique_results = []
        
        for result in results:
            link = result.get("link", "")
            if link and link not in seen_links:
                seen_links.add(link)
                unique_results.append(result)
        
        return unique_results
    
    def _generate_summary(self, results: List[Dict[str, Any]], interests: List[str], target_level: str) -> str:
        """
        Generate LLM summary of search results
        
        Args:
            results: List of search results
            interests: Student interests
            target_level: Target education level
        
        Returns:
            AI-generated summary of the search results
        """
        if not self.genai_client or not results:
            return ""
        
        try:
            # Format results for LLM
            results_text = ""
            for i, result in enumerate(results[:5], 1):
                results_text += f"\n{i}. {result.get('title', 'N/A')}\n"
                results_text += f"   URL: {result.get('link', 'N/A')}\n"
                results_text += f"   {result.get('snippet', 'No description')}\n"
            
            prompt = f"""Based on the following real-time search results from Singapore university websites, 
provide a brief, helpful summary for a student interested in {', '.join(interests)} at {target_level} level.

Search Results:
{results_text}

Generate a concise 3-4 sentence summary highlighting:
1. Key programs found that match their interests
2. Which universities offer relevant programs
3. Any notable features or opportunities mentioned

Keep it practical and actionable."""

            response = self.genai_client.summarize(prompt)
            return response.strip() if response else ""
            
        except Exception as e:
            self.pass}")
            return ""
    
    def handle(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        BaseAgent abstract method implementation - delegates to run()
        """
        return self.run(profile)
