import os

from dotenv import load_dotenv
from google.genai import types
from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.tools import VertexAiSearchTool
from bs4 import BeautifulSoup
from markdown import markdown

# It's good practice to import instructions from a separate file
from .instructions import ROOT_INSTRUCTIONS


load_dotenv()

# --- Configuration ---
MODEL = "gemini-2.5-flash"
CONTENT_CONFIG = types.GenerateContentConfig(
    temperature=0.0, # More deterministic output
    max_output_tokens=None,
)

# Load environment variables
LOCATION = os.getenv('LOCATION')
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
COLLECTION_ID = os.getenv('COLLECTION_ID')

# Assuming you might have different app IDs for each engine
# If they are all the same, this still works perfectly.
POLICY_NAVIGATOR_APP = os.getenv('POLICY_NAVIGATOR_APP')
POLICY_NAVIGATOR_COMPLIANCE_APP = os.getenv('POLICY_NAVIGATOR_COMPLIANCE_APP')
POLICY_NAVIGATOR_CLINICAL_GUIDELINES_APP = os.getenv('POLICY_NAVIGATOR_CLINICAL_GUIDELINES_APP')
POLICY_NAVIGATOR_HR_APP = os.getenv('POLICY_NAVIGATOR_HR_APP')

# Debug: Print environment variables to verify they are loaded correctly
print("DEBUG: LOCATION:", LOCATION)
print("DEBUG: PROJECT_ID:", PROJECT_ID)
print("DEBUG: COLLECTION_ID:", COLLECTION_ID)
print("DEBUG: POLICY_NAVIGATOR_APP:", POLICY_NAVIGATOR_APP)
print("DEBUG: POLICY_NAVIGATOR_COMPLIANCE_APP:", POLICY_NAVIGATOR_COMPLIANCE_APP)
print("DEBUG: POLICY_NAVIGATOR_CLINICAL_GUIDELINES_APP:", POLICY_NAVIGATOR_CLINICAL_GUIDELINES_APP)
print("DEBUG: POLICY_NAVIGATOR_HR_APP:", POLICY_NAVIGATOR_HR_APP)

# --- Engine & Tool Definitions ---

# Construct full engine paths
def get_engine_path(app_id):
    return f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/{COLLECTION_ID}/engines/{app_id}"

policy_navigator_engine = get_engine_path(POLICY_NAVIGATOR_APP)
policy_navigator_compliance_engine = get_engine_path(POLICY_NAVIGATOR_COMPLIANCE_APP)
policy_navigator_clinical_engine = get_engine_path(POLICY_NAVIGATOR_CLINICAL_GUIDELINES_APP)
policy_navigator_hr_engine = get_engine_path(POLICY_NAVIGATOR_HR_APP)

# Create a dedicated tool for each search engine
policy_navigator_tool = VertexAiSearchTool(search_engine_id=policy_navigator_engine)
policy_navigator_compliance_tool = VertexAiSearchTool(search_engine_id=policy_navigator_compliance_engine)
policy_navigator_clinical_tool = VertexAiSearchTool(search_engine_id=policy_navigator_clinical_engine)
policy_navigator_hr_tool = VertexAiSearchTool(search_engine_id=policy_navigator_hr_engine)


# --- 1. Define Specialist "Expert" Agents ---

root_agent = LlmAgent(
    model=MODEL,
    name='policy_navigator_agent',
    description="An AI agent to answer questions based on clinical guidelines, HR policies, or compliance documents.",
    instruction=ROOT_INSTRUCTIONS.strip(),
    tools=[policy_navigator_tool],
    generate_content_config=CONTENT_CONFIG,
)