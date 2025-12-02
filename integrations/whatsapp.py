"""WhatsApp integration using Agno's official WhatsApp toolkit.

This provides full WhatsApp Business API integration for Effectiva,
enabling the agent system to send and receive messages via WhatsApp.
"""
from agno.tools.whatsapp import WhatsAppTools
from config.settings import get_whatsapp_config

# Initialize WhatsApp tools with configuration
whatsapp_tools = WhatsAppTools(
    access_token=get_whatsapp_config()["access_token"],
    phone_number_id=get_whatsapp_config()["phone_number_id"],
)

# Export the tools for use in agents
send_message = whatsapp_tools.send_message
send_template_message = whatsapp_tools.send_template_message
mark_message_as_read = whatsapp_tools.mark_message_as_read
get_message_status = whatsapp_tools.get_message_status
