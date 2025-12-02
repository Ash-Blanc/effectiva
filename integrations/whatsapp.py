"""WhatsApp integration using Agno's official WhatsApp toolkit.

This provides full WhatsApp Business API integration for Effectiva,
enabling the agent system to send and receive messages via WhatsApp.
"""
import os
from config.settings import get_whatsapp_config

# Initialize WhatsApp tools only if API keys are available
whatsapp_tools = None
send_message = None
send_template_message = None
mark_message_as_read = None
get_message_status = None
log_whatsapp_message = None

# Check if WhatsApp API keys are configured
access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')

if access_token and phone_number_id:
    try:
        from agno.tools.whatsapp import WhatsAppTools
        # Initialize WhatsApp tools with configuration
        whatsapp_tools = WhatsAppTools(
            access_token=access_token,
            phone_number_id=phone_number_id,
        )

        # Export the tools for use in agents
        # Agno WhatsAppTools uses sync/async variants
        send_message = whatsapp_tools.send_text_message_sync
        send_template_message = whatsapp_tools.send_template_message_sync

        # Additional utility functions for agent use
        def log_whatsapp_message(message: str, recipient: str = None) -> str:
            """Log a WhatsApp message for agent coordination."""
            try:
                if recipient:
                    result = send_message(text=message, recipient=recipient)
                else:
                    # If no recipient specified, just log the message
                    result = f"WhatsApp message logged: {message}"
                return f"WhatsApp message sent: {result}"
            except Exception as e:
                return f"Failed to send WhatsApp message: {e}"

        # Export the log function
        globals()['log_whatsapp_message'] = log_whatsapp_message
    except Exception as e:
        print(f"⚠️ Failed to initialize WhatsApp tools: {e}")
        # Tools remain None, will be handled gracefully
else:
    print("⚠️ WhatsApp API keys not configured, WhatsApp integration disabled")
