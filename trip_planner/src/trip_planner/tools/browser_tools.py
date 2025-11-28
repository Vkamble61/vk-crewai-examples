import json
import os

import requests
from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field


class ScrapeWebsiteInput(BaseModel):
    """Input schema for ScrapeWebsiteTool."""
    website: str = Field(..., description="The website URL to scrape and summarize")


class ScrapeWebsiteTool(BaseTool):
    name: str = "Scrape website content"
    description: str = "Useful to scrape and summarize a website content"
    args_schema: Type[BaseModel] = ScrapeWebsiteInput

    def _run(self, website: Any) -> str:
        try:
            # Handle if website is passed as a dict
            if isinstance(website, dict):
                if 'website' in website:
                    website = website['website']
                elif 'url' in website:
                    website = website['url']
                else:
                    website = str(website)
            
            # Convert to string if needed
            website = str(website)
            
            # Check if BROWSERLESS_API_KEY is set
            browserless_key = os.environ.get('BROWSERLESS_API_KEY')
            if not browserless_key:
                return "Error: BROWSERLESS_API_KEY not found in environment variables. Please add it to your .env file."
            
            url = f"https://chrome.browserless.io/content?token={browserless_key}"
            payload = json.dumps({"url": website})
            headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
            
            # Check if request was successful
            if response.status_code != 200:
                return f"Error: Failed to scrape website. Status code: {response.status_code}. Message: {response.text[:200]}"
            
            # Return the scraped content directly without complex summarization
            # The AI agent can process and summarize the content itself
            content = response.text
            
            # Limit content size to prevent token overflow
            max_length = 15000
            if len(content) > max_length:
                content = content[:max_length] + "\n\n[Content truncated due to length...]"
            
            return content
            
        except requests.exceptions.Timeout:
            return "Error: Request timed out while trying to scrape the website."
        except requests.exceptions.RequestException as e:
            return f"Error: Failed to scrape website. {str(e)}"
        except Exception as e:
            return f"Error: An unexpected error occurred: {str(e)}"
