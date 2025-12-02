"""Discord integration using Agno's official Discord toolkit.

This provides full Discord bot integration for Effectiva,
enabling the agent system to interact with Discord servers and channels.
"""
from agno.tools.discord import DiscordTools
from config.settings import get_discord_config

# Initialize Discord tools with configuration
discord_tools = DiscordTools(
    bot_token=get_discord_config()["bot_token"],
    default_channel_id=get_discord_config()["default_channel_id"],
)

# Export the tools for use in agents
send_message = discord_tools.send_message
get_channel_messages = discord_tools.get_channel_messages
create_thread = discord_tools.create_thread
add_reaction = discord_tools.add_reaction
get_user_info = discord_tools.get_user_info