import os
from dotenv import load_dotenv

load_dotenv() # take environment variables from .env.

# --- Configuration Variables ---
HR_USERNAME = os.getenv("HR_USERNAME")
HR_PASSWORD = os.getenv("HR_PASSWORD")

# --- TEMPORARY DIAGNOSTIC PRINT (ADD THESE TWO LINES) ---
print(f"DEBUG: HR_USERNAME from config.py: {HR_USERNAME}")
print(f"DEBUG: HR_PASSWORD from config.py: {HR_PASSWORD}")
# --- END TEMPORARY DIAGNOSTIC PRINT ---

OUTPUT_DIR = "Python" # Default directory for output solutions
LOG_FILE = "sync_log.log" # Default log file