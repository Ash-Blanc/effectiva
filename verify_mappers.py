from sqlalchemy.orm import configure_mappers
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from models import Agent, Optimizer, ToonConfig
    print("Models imported successfully.")
    configure_mappers()
    print("Mappers configured successfully.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
