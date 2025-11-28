import os
from typing import Type
from datetime import datetime, timedelta
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from exa_py import Exa
# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")

class SearchAndContents(BaseTool):

    name: str = "Search and Contents tool"
    description: str = (
        "Searches the web based on a search query for the latest results. "
        "Results are only from the last week. Uses the Exa API. "
        "This also returns the contents of the search results."
    )
    # args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, search_query: str) -> str:
        exa = Exa(api_key=os.environ.get("EXA_API_KEY"))
        one_week_ago = datetime.now() - timedelta(weeks=1)
        date_cutoff=one_week_ago.strftime("%Y-%m-%d")   
        search_results = exa.search_and_contents(
            query=search_query,
            #use_autoprompt=True, # Enable autoprompt for better search results is deprecated in new version
            start_published_date=date_cutoff,
        
            text={"include_contents": False, "max_characters": 8000 }
            )
        #contents = "\n".join([result.content for result in search_results]
                             
        return str(search_results)

class FindSimilar(BaseTool):

    name: str = "Find Similar tool"
    description: str = (
         "Searches for similar articles to a given article using the Exa API. "
         "Takes in a URL of the article"
    )

    def _run(self, article_url: str) -> str:

        one_wk_ago = datetime.now() - timedelta(weeks=1)
        date_cutoff=one_wk_ago.strftime("%Y-%m-%d")

        exa = Exa(api_key=os.environ.get("EXA_API_KEY"))

        search_results = exa.find_similar(
            url=article_url,
            start_published_date=date_cutoff,
        )
        return str(search_results)

class GetContents(BaseTool):

    name: str = "Get Contents tool"
    description: str = (
         "Gets the contents of a specific article using the Exa API. Takes in a single article URL as a string, like this: 'https://www.cnbc.com/2024/04/18/my-news-story'"
    )

    def _run(self, article_ids: str) -> str:

        exa = Exa(api_key=os.environ.get("EXA_API_KEY"))

        # Convert single URL string to list for the API
        urls_list = [article_ids] if isinstance(article_ids, str) else article_ids
        contents = exa.get_contents(urls=urls_list)
        return str(contents)  

# if __name__ == "__main__":
    # search_and_contents = SearchAndContents()
    # search_results = search_and_contents._run(search_query = "Latest advancements in AI language models")
    # print(search_results)
    #https://paperswithcode.com/papers/2508.03680
    # find_similar = FindSimilar()
    # similar_results = find_similar._run(article_url = "https://paperswithcode.com/paper/2508.03680")
    # print(similar_results)
    # get_contents = GetContents()
    # contents_results = get_contents._run(article_ids = "https://paperswithcode.com/paper/2508.03680")
    # print(contents_results)