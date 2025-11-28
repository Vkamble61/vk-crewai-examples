import json
import os

import requests
from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field


class SearchInternetInput(BaseModel):
    """Input schema for SearchInternetTool."""
    query: str = Field(..., description="The search query to look up on the internet")


class SearchInternetTool(BaseTool):
    name: str = "Search the internet"
    description: str = "Useful to search the internet about a given topic and return relevant results"
    args_schema: Type[BaseModel] = SearchInternetInput

    def _run(self, query: Any) -> str:
        try:
            # Handle if query is passed as a dict
            if isinstance(query, dict):
                if 'query' in query:
                    query = query['query']
                elif 'description' in query:
                    query = query['description']
                else:
                    query = str(query)
            
            # Convert to string if needed
            query = str(query)
            
            # Check if SERPER_API_KEY is set
            serper_key = os.environ.get('SERPER_API_KEY')
            if not serper_key:
                return "Error: SERPER_API_KEY not found in environment variables. Please add it to your .env file."
            
            top_result_to_return = 4
            url = "https://google.serper.dev/search"
            payload = json.dumps({"q": query})
            headers = {
                'X-API-KEY': serper_key,
                'content-type': 'application/json'
            }
            
            response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
            
            # Check if request was successful
            if response.status_code != 200:
                return f"Error: Search API returned status code {response.status_code}. Message: {response.text[:200]}"
            
            response_data = response.json()
            
            # check if there is an organic key
            if 'organic' not in response_data:
                if 'message' in response_data:
                    return f"Error: {response_data['message']}"
                return "Sorry, I couldn't find anything about that. There could be an error with your Serper API key."
            
            results = response_data['organic']
            
            if not results:
                return f"No search results found for query: {query}"
            
            string = []
            for result in results[:top_result_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}", 
                        f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", 
                        "\n-----------------"
                    ]))
                except KeyError:
                    continue

            return '\n'.join(string) if string else "No valid results found."
            
        except requests.exceptions.Timeout:
            return "Error: Search request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Error: Failed to perform search. {str(e)}"
        except json.JSONDecodeError:
            return "Error: Failed to parse search results. The API response was not valid JSON."
        except Exception as e:
            return f"Error: An unexpected error occurred: {str(e)}"
