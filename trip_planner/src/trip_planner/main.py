from crewai import Crew
from textwrap import dedent
from trip_planner.trip_agents import TripAgents
from trip_planner.trip_tasks import TripTasks

from dotenv import load_dotenv
load_dotenv()

class TripCrew:
    """Crew to plan an amazing trip based on user preferences and interests."""
    def __init__(self, origin, cities, date_range, interests):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        identify_task = tasks.identify_task(
            city_selector_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )
        gather_task = tasks.gather_task(
            local_expert_agent,
            self.origin,
            self.interests,
            self.date_range
        )
        plan_task = tasks.plan_task(
            travel_concierge_agent, 
            self.origin,
            self.interests,
            self.date_range
        )

        crew = Crew(
            agents=[
                city_selector_agent, local_expert_agent, travel_concierge_agent
            ],
            tasks=[identify_task, gather_task, plan_task],
            verbose=True
        )

        result = crew.kickoff()
        return result

def run():
    """Main entry point for running the trip planner crew."""
    print("## Welcome to Trip Planner Crew")
    print('-------------------------------')
    location = input(
        dedent("""
      From where will you be traveling from?
    """))
    cities = input(
        dedent("""
      What are the cities options you are interested in visiting?
    """))
    date_range = input(
        dedent("""
      What is the date range you are interested in traveling?
    """))
    interests = input(
        dedent("""
      What are some of your high level interests and hobbies?
    """))
    
    trip_crew = TripCrew(location, cities, date_range, interests)
    result = trip_crew.run()
    print("\n\n########################")
    print("## Here is you Trip Plan")
    print("########################\n")
    print(result)

def train():
    """Train the crew."""
    print("Training functionality not yet implemented")

def replay():
    """Replay the crew."""
    print("Replay functionality not yet implemented")

def test():
    """Test the crew."""
    print("Test functionality not yet implemented")

def run_with_trigger():
    """Run the crew with trigger."""
    print("Trigger functionality not yet implemented")

if __name__ == "__main__":
    run()
