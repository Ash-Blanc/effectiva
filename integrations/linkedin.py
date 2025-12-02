"""LinkedIn integration using Agno's official LinkedIn toolkit.

This provides full LinkedIn API integration for Effectiva,
enabling the agent system to interact with LinkedIn for professional networking.
"""
from agno.tools.linkedin import LinkedInTools
from config.settings import get_linkedin_config

# Initialize LinkedIn tools with configuration
linkedin_tools = LinkedInTools(
    access_token=get_linkedin_config()["access_token"],
    person_urn=get_linkedin_config()["person_urn"],
)

# Export the tools for use in agents
send_message = linkedin_tools.send_message
get_profile = linkedin_tools.get_profile
search_people = linkedin_tools.search_people
get_connections = linkedin_tools.get_connections
create_post = linkedin_tools.create_post
get_feed = linkedin_tools.get_feed