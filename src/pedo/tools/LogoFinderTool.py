from crewai import Agent
from crewai.tools import BaseTool
import requests
import os
import json

class LogoFinderTool(BaseTool):
    name: str = "logo_finder_tool"
    description: str = "Find a logo for a company or organization using a free API."
    
    def _run(self, company_name: str) -> str:
        """
        Find a logo URL for the given company using Clearbit Logo API
        """
        print(f"🔍 Searching for logo for: {company_name}")
        
        try:
            # Using Clearbit's Logo API (free for basic usage)
            url = f"https://logo.clearbit.com/{company_name.lower().replace(' ', '')}.com"
            
            # Check if the logo exists
            response = requests.head(url)
            if response.status_code == 200:
                print(f"✅ Found logo for {company_name} at {url}")
                return url
                
            # Fallback to a domain with hyphen
            url = f"https://logo.clearbit.com/{company_name.lower().replace(' ', '-')}.com"
            response = requests.head(url)
            if response.status_code == 200:
                print(f"✅ Found logo for {company_name} at {url}")
                return url
                
            # Second fallback - use a healthcare-related logo placeholder
            print(f"⚠️ Couldn't find specific logo for {company_name}, using fallback")
            return "https://upload.wikimedia.org/wikipedia/commons/5/58/Instagram-Icon.png"
            
        except Exception as e:
            print(f"❌ Error finding logo: {e}")
            # Return a default placeholder image
            return "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg"

class LogoFinderAgent:
    def create(self):
        return Agent( 
            role="Logo Retrieval Specialist",
            goal="Identify the subject of the case study and find an appropriate logo",
            backstory="A web search expert that retrieves high-quality logos related to the case study topic.",
            tools=[LogoFinderTool()],
            verbose=True,
            allow_delegation=False
        )