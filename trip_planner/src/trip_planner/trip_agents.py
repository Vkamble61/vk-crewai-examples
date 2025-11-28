from crewai import Agent

from trip_planner.tools.browser_tools import ScrapeWebsiteTool
from trip_planner.tools.calculator_tools import CalculatorTool
from trip_planner.tools.search_tools import SearchInternetTool

class TripAgents():

  def city_selection_agent(self):
    return Agent(
        role='City Selection Expert',
        goal='Select the best city based on weather, season, and prices',
        backstory=
        'An expert in analyzing travel data to pick ideal destinations',
        tools=[
            SearchInternetTool(),
            ScrapeWebsiteTool(),
        ],
        verbose=True)

  def local_expert(self):
    return Agent(
        role='Local Expert at this city',
        goal='Provide the BEST insights about the selected city',
        backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
        tools=[
            SearchInternetTool(),
            ScrapeWebsiteTool(),
        ],
        verbose=True)

  def travel_concierge(self):
    return Agent(
        role='Amazing Travel Concierge',
        goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city""",
        backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
        tools=[
            SearchInternetTool(),
            ScrapeWebsiteTool(),
            CalculatorTool(),
        ],
        verbose=True)
